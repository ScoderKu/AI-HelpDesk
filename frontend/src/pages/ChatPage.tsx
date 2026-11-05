import { useCallback, useEffect, useRef, useState } from 'react'
import type { FormEvent, KeyboardEvent } from 'react'
import './ChatPage.css'
import { API_BASE_URL } from '../api'
import type { Copy } from '../i18n/copy'

type Conversation = { id: number; title: string | null; created_at: string; updated_at: string }
type Message = { id: number; role: 'USER' | 'ASSISTANT'; content: string; created_at: string }
type TicketDraft = { title: string; description: string; priority: 'LOW' | 'MEDIUM' | 'HIGH' }
type ChatPageProps = { text: Copy; initialConversationId: number | null; onConversationChange: (id: number | null) => void }

type MarkdownBlock =
  | { type: 'paragraph' | 'heading' ; text: string; level?: number }
  | { type: 'list'; items: string[]; ordered: boolean }
  | { type: 'code'; code: string; language: string }

function parseMarkdownBlocks(content: string): MarkdownBlock[] {
  const lines = content.replace(/\r\n?/g, '\n').split('\n')
  const blocks: MarkdownBlock[] = []
  let index = 0
  while (index < lines.length) {
    const line = lines[index]
    if (!line.trim()) { index += 1; continue }
    if (line.trimStart().startsWith('```')) {
      const language = line.trim().slice(3).trim()
      const codeLines: string[] = []
      index += 1
      while (index < lines.length && !lines[index].trimStart().startsWith('```')) {
        codeLines.push(lines[index])
        index += 1
      }
      if (index < lines.length) index += 1
      blocks.push({ type: 'code', code: codeLines.join('\n'), language })
      continue
    }
    const heading = line.match(/^(#{1,6})\s+(.+)$/)
    if (heading) {
      blocks.push({ type: 'heading', level: heading[1].length, text: heading[2] })
      index += 1
      continue
    }
    const unordered = line.match(/^\s*[-*+]\s+(.+)$/)
    const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/)
    if (unordered || ordered) {
      const items: string[] = []
      const isOrdered = Boolean(ordered)
      while (index < lines.length) {
        const match = lines[index].match(isOrdered ? /^\s*\d+[.)]\s+(.+)$/ : /^\s*[-*+]\s+(.+)$/)
        if (!match) break
        items.push(match[1])
        index += 1
      }
      blocks.push({ type: 'list', items, ordered: isOrdered })
      continue
    }
    const paragraph = [line]
    index += 1
    while (index < lines.length && lines[index].trim()
      && !lines[index].trimStart().startsWith('```')
      && !/^#{1,6}\s+/.test(lines[index])
      && !/^\s*[-*+]\s+/.test(lines[index])
      && !/^\s*\d+[.)]\s+/.test(lines[index])) {
      paragraph.push(lines[index])
      index += 1
    }
    blocks.push({ type: 'paragraph', text: paragraph.join('\n') })
  }
  return blocks
}

function renderInlineMarkdown(text: string, keyPrefix: string) {
  const tokens = text.split(/(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|~~[^~]+~~)/g)
  return tokens.map((token, index) => {
    if (token.startsWith('`') && token.endsWith('`')) return <code key={`${keyPrefix}-${index}`}>{token.slice(1, -1)}</code>
    if (token.startsWith('**') && token.endsWith('**')) return <strong key={`${keyPrefix}-${index}`}>{token.slice(2, -2)}</strong>
    if (token.startsWith('*') && token.endsWith('*')) return <em key={`${keyPrefix}-${index}`}>{token.slice(1, -1)}</em>
    if (token.startsWith('~~') && token.endsWith('~~')) return <del key={`${keyPrefix}-${index}`}>{token.slice(2, -2)}</del>
    return token
  })
}

function MarkdownMessage({ content, copyLabel, copiedLabel }: { content: string; copyLabel: string; copiedLabel: string }) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)
  const blocks = parseMarkdownBlocks(content)
  const copyCode = async (code: string, index: number) => {
    try {
      await navigator.clipboard.writeText(code)
      setCopiedIndex(index)
    } catch {
      setCopiedIndex(null)
    }
  }
  return (
    <div className="markdown-content">
      {blocks.map((block, index) => {
        if (block.type === 'code') return (
          <div className="markdown-code-block" key={index}>
            <div className="markdown-code-toolbar">
              <span>{block.language || 'code'}</span>
              <button type="button" onClick={() => void copyCode(block.code, index)}>
                {copiedIndex === index ? copiedLabel : copyLabel}
              </button>
            </div>
            <pre><code>{block.code}</code></pre>
          </div>
        )
        if (block.type === 'heading') {
          const Heading = (`h${block.level ?? 3}`) as 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6'
          return <Heading key={index}>{renderInlineMarkdown(block.text, `heading-${index}`)}</Heading>
        }
        if (block.type === 'list') {
          const List = block.ordered ? 'ol' : 'ul'
          return <List key={index}>{block.items.map((item, itemIndex) => <li key={itemIndex}>{renderInlineMarkdown(item, `list-${index}-${itemIndex}`)}</li>)}</List>
        }
        return <p key={index}>{renderInlineMarkdown(block.text, `paragraph-${index}`)}</p>
      })}
    </div>
  )
}

class ChatApiError extends Error {
  readonly status: number
  readonly savedMessageId: number | null

  constructor(message: string, status: number, savedMessageId: number | null) {
    super(message)
    this.status = status
    this.savedMessageId = savedMessageId
  }
}

function truncateUtf8(value: string, maxBytes: number): string {
  const encoder = new TextEncoder()
  let result = ''
  let byteLength = 0
  for (const character of value) {
    const size = encoder.encode(character).length
    if (byteLength + size > maxBytes) break
    result += character
    byteLength += size
  }
  return result
}

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!response.ok) {
    let detail = ''
    try {
      const body = await response.json()
      detail = typeof body.detail === 'string' ? body.detail : ''
    } catch { /* The response may not contain JSON. */ }
    const savedMessageIdHeader = response.headers.get('X-Chat-Message-Id')
    const savedMessageId = savedMessageIdHeader === null ? Number.NaN : Number(savedMessageIdHeader)
    throw new ChatApiError(
      detail || `HTTP ${response.status}`,
      response.status,
      response.headers.get('X-Chat-Message-Saved') === 'true' && Number.isInteger(savedMessageId)
        ? savedMessageId
        : null,
    )
  }
  return response.status === 204 ? undefined as T : response.json()
}

export function ChatPage({ text: t, initialConversationId, onConversationChange }: ChatPageProps) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [retryMessageId, setRetryMessageId] = useState<number | null>(null)
  const [draft, setDraft] = useState('')
  const draftRef = useRef('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [streaming, setStreaming] = useState(false)
  const [error, setError] = useState('')
  const [conversationListError, setConversationListError] = useState(false)
  const [messageLoadError, setMessageLoadError] = useState(false)
  const [ticketDraft, setTicketDraft] = useState<TicketDraft | null>(null)
  const [ticketDraftLoading, setTicketDraftLoading] = useState(false)
  const [ticketRecommendation, setTicketRecommendation] = useState(false)
  const [creatingTicket, setCreatingTicket] = useState(false)
  const [ticketFeedback, setTicketFeedback] = useState('')
  const messagesRef = useRef<HTMLDivElement>(null)
  const composerRef = useRef<HTMLTextAreaElement>(null)
  const focusComposerAfterResponse = useRef(false)
  const activeConversationId = useRef<number | null>(null)
  const conversationRequest = useRef(0)

  const fetchConversations = useCallback(
    () => api<Conversation[]>('/api/v1/conversations'),
    [],
  )

  const loadConversations = useCallback(async () => {
    try {
      const items = await fetchConversations()
      setConversations(items)
      setConversationListError(false)
      return items
    } catch {
      setConversationListError(true)
      return []
    }
  }, [fetchConversations])

  useEffect(() => {
    let active = true
    void fetchConversations()
      .then((items) => {
        if (active) {
          setConversations(items)
          setConversationListError(false)
        }
      })
      .catch(() => {
        if (active) setConversationListError(true)
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => { active = false }
  }, [fetchConversations])

  useEffect(() => {
    if (loading) return
    if (initialConversationId !== null && activeConversationId.current !== initialConversationId) {
      void openConversation(initialConversationId)
    } else if (initialConversationId === null && activeConversationId.current !== null) {
      ++conversationRequest.current
      activeConversationId.current = null
      setActiveId(null)
      setMessages([])
      setRetryMessageId(null)
      setTicketDraft(null)
      setTicketRecommendation(false)
      setTicketFeedback('')
      setMessageLoadError(false)
      setError('')
    }
  // Restore the URL-selected conversation after history is ready or browser navigation changes it.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading, initialConversationId])

  useEffect(() => {
    const messagesElement = messagesRef.current
    if (messagesElement) messagesElement.scrollTop = messagesElement.scrollHeight
  }, [messages, sending])

  useEffect(() => {
    if (!sending && focusComposerAfterResponse.current) {
      focusComposerAfterResponse.current = false
      composerRef.current?.focus()
    }
  }, [sending])

  const refreshMessages = async (id: number, requestId: number) => {
    const items = await api<Message[]>(`/api/v1/conversations/${id}/messages`)
    if (activeConversationId.current !== id || conversationRequest.current !== requestId) return
    setMessages(items)
    const lastMessage = items.at(-1)
    setRetryMessageId(lastMessage?.role === 'USER' ? lastMessage.id : null)
    setMessageLoadError(false)
  }

  const openConversation = async (id: number) => {
    const requestId = ++conversationRequest.current
    activeConversationId.current = id
    setActiveId(id)
    onConversationChange(id)
    setMessages([])
    setRetryMessageId(null)
    setTicketDraft(null)
    setTicketRecommendation(false)
    setTicketFeedback('')
    setMessageLoadError(false)
    try {
      const items = await api<Message[]>(`/api/v1/conversations/${id}/messages`)
      if (activeConversationId.current !== id || conversationRequest.current !== requestId) return
      setMessages(items)
      const lastMessage = items.at(-1)
      setRetryMessageId(lastMessage?.role === 'USER' ? lastMessage.id : null)
      setMessageLoadError(false)
    } catch {
      if (activeConversationId.current === id && conversationRequest.current === requestId) {
        setMessageLoadError(true)
      }
    }
  }

  const startConversation = () => {
    ++conversationRequest.current
    activeConversationId.current = null
    setActiveId(null)
    onConversationChange(null)
    setMessages([])
    setDraft('')
    draftRef.current = ''
    setRetryMessageId(null)
    setTicketDraft(null)
    setTicketRecommendation(false)
    setTicketFeedback('')
    setMessageLoadError(false)
    setError('')
  }

  const sendMessage = async (event: FormEvent) => {
    event.preventDefault()
    const content = draft.trim()
    if (!content || sending) return

    const optimisticId = -Date.now()
    const optimisticMessage: Message = {
      id: optimisticId,
      role: 'USER',
      content,
      created_at: new Date().toISOString(),
    }
    let conversationId = activeConversationId.current
    let requestId = conversationRequest.current
    let persistedUserMessageId: number | null = null
    let streamedAssistantMessageId: number | null = null
    let rejectionDetail = ''
    const previousRetryMessageId = retryMessageId
    setSending(true)
    setTicketRecommendation(false)
    setError('')
    setDraft('')
    draftRef.current = ''
    setMessages((current) => [...current, optimisticMessage])

    try {
      if (conversationId === null) {
        const created = await api<Conversation>('/api/v1/conversations', {
          method: 'POST', body: JSON.stringify({}),
        })
        conversationId = created.id
        const stillCurrent = conversationRequest.current === requestId && activeConversationId.current === null
        if (!stillCurrent) {
          setMessages((current) => current.filter((message) => message.id !== optimisticId))
          return
        }
        requestId = ++conversationRequest.current
        activeConversationId.current = created.id
        setActiveId(created.id)
        onConversationChange(created.id)
        setConversations((current) => [created, ...current])
      }

      const response = await fetch(
        `${API_BASE_URL}/api/v1/conversations/${conversationId}/messages/stream`,
        {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content }),
        },
      )
      if (!response.ok || !response.body) {
        let detail = ''
        try {
          const body = await response.json()
          detail = typeof body.detail === 'string' ? body.detail : ''
        } catch { /* The response may not contain JSON. */ }
        rejectionDetail = detail
        throw new Error(detail || `HTTP ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let assistantMessageId = -optimisticId
      streamedAssistantMessageId = assistantMessageId
      let streamFailed = false
      let completed = false

      const processEvent = (line: string) => {
        if (!line.trim()) return
        const item = JSON.parse(line) as {
          event: 'user_message' | 'token' | 'done' | 'error'
          message?: Message
          assistant_message?: Message
          content?: string
          detail?: string
          saved_message_id?: number
          ticket_recommended?: boolean
        }
        if (activeConversationId.current !== conversationId || conversationRequest.current !== requestId) return
        if (item.event === 'user_message' && item.message) {
          persistedUserMessageId = item.message.id
          setRetryMessageId(null)
          setMessages((current) => current.map((message) =>
            message.id === optimisticId ? item.message! : message,
          ))
        } else if (item.event === 'token' && typeof item.content === 'string') {
          setStreaming(true)
          setMessages((current) => {
            const existing = current.some((message) => message.id === assistantMessageId)
            if (!existing) {
              return [...current, {
                id: assistantMessageId,
                role: 'ASSISTANT',
                content: item.content!,
                created_at: new Date().toISOString(),
              }]
            }
            return current.map((message) => message.id === assistantMessageId
              ? { ...message, content: message.content + item.content! }
              : message)
          })
        } else if (item.event === 'done' && item.assistant_message) {
          completed = true
          setStreaming(false)
          setMessages((current) => current.map((message) =>
            message.id === assistantMessageId ? item.assistant_message! : message,
          ))
          setTicketRecommendation(item.ticket_recommended === true)
          streamFailed = false
        } else if (item.event === 'error') {
          streamFailed = true
          setStreaming(false)
          if (item.saved_message_id) {
            setMessages((current) => current.filter((message) => message.id !== assistantMessageId))
            setRetryMessageId(item.saved_message_id)
            setError(t.chatAiUnavailable)
          } else {
            setMessages((current) => current.filter((message) =>
              message.id !== optimisticId && message.id !== assistantMessageId,
            ))
            if (draftRef.current === '') {
              draftRef.current = content
              setDraft(content)
            }
            setRetryMessageId(previousRetryMessageId)
            if (item.detail?.includes('previous message') && conversationId !== null) {
              void refreshMessages(conversationId, requestId).catch(() => undefined)
            }
            setError(item.detail?.includes('previous message') ? t.chatPreviousUnanswered : t.chatSendError)
          }
        }
      }

      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''
        for (const line of lines) processEvent(line)
      }
      buffer += decoder.decode()
      if (buffer.trim()) processEvent(buffer)
      if (!completed && !streamFailed) {
        throw new Error('The AI response stream ended before completion.')
      }
      if (!streamFailed) {
        focusComposerAfterResponse.current = true
        setRetryMessageId(null)
        await loadConversations()
      }
    } catch {
      if (activeConversationId.current === conversationId && conversationRequest.current === requestId) {
        setMessages((current) => current.filter((message) =>
          message.id !== optimisticId && message.id !== streamedAssistantMessageId,
        ))
        if (persistedUserMessageId !== null) {
          setRetryMessageId(persistedUserMessageId)
          setError(t.chatAiUnavailable)
        } else {
          if (draftRef.current === '') {
            draftRef.current = content
            setDraft(content)
          }
          setRetryMessageId(previousRetryMessageId)
          if (rejectionDetail.includes('previous message') && conversationId !== null) {
            try { await refreshMessages(conversationId, requestId) } catch { /* Keep the existing retry state. */ }
          }
          setError(rejectionDetail.includes('previous message') ? t.chatPreviousUnanswered : t.chatSendError)
        }
      }
    } finally {
      setStreaming(false)
      setSending(false)
    }
  }

  const openTicketDraft = async () => {
    const conversationId = activeConversationId.current
    const requestId = conversationRequest.current
    if (conversationId === null || messages.length === 0 || sending || ticketDraftLoading) return
    setTicketDraftLoading(true)
    setTicketFeedback('')
    setError('')
    try {
      const generated = await api<{ title: string; description: string }>(`/api/v1/conversations/${conversationId}/ticket-draft`, { method: 'POST' })
      if (activeConversationId.current !== conversationId || conversationRequest.current !== requestId) return
      setTicketDraft({ ...generated, priority: 'MEDIUM' })
      setTicketRecommendation(false)
    } catch {
      if (activeConversationId.current === conversationId && conversationRequest.current === requestId) setError(t.chatTicketDraftError)
    } finally {
      setTicketDraftLoading(false)
    }
  }

  const createTicketFromConversation = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const conversationId = activeConversationId.current
    const requestId = conversationRequest.current
    if (conversationId === null || ticketDraft === null || creatingTicket) return
    if (!ticketDraft.title.trim() || !ticketDraft.description.trim()) { setError(t.chatTicketFieldsRequired); return }
    setCreatingTicket(true)
    setError('')
    setTicketFeedback('')
    try {
      await api(`/api/v1/conversations/${conversationId}/tickets`, {
        method: 'POST',
        body: JSON.stringify({ title: ticketDraft.title.trim(), description: ticketDraft.description.trim(), priority: ticketDraft.priority }),
      })
      if (activeConversationId.current === conversationId && conversationRequest.current === requestId) {
        setTicketDraft(null)
        setTicketFeedback(t.chatTicketCreated)
      }
    } catch {
      if (activeConversationId.current === conversationId && conversationRequest.current === requestId) {
        setError(t.chatTicketCreateError)
      }
    } finally {
      setCreatingTicket(false)
    }
  }

  const handleComposerKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey && !event.repeat && !event.nativeEvent.isComposing) {
      event.preventDefault()
      event.currentTarget.form?.requestSubmit()
    }
  }

  const retryAnswer = async () => {
    const conversationId = activeConversationId.current
    const requestId = conversationRequest.current
    if (conversationId === null || retryMessageId === null || sending) return
    setSending(true)
    setError('')
    try {
      const result = await api<{
        conversation_id: number
        user_message: Message
        assistant_message: Message
      }>(`/api/v1/conversations/${conversationId}/messages/${retryMessageId}/retry`, {
        method: 'POST',
      })
      if (activeConversationId.current === conversationId && conversationRequest.current === requestId) {
        focusComposerAfterResponse.current = true
        setMessages((current) => [
          ...current.filter((message) => message.id !== result.user_message.id),
          result.user_message,
          result.assistant_message,
        ])
        setRetryMessageId(null)
      }
      await loadConversations()
    } catch {
      if (activeConversationId.current === conversationId && conversationRequest.current === requestId) {
        setError(t.chatSendError)
        try { await refreshMessages(conversationId, requestId) } catch { /* Keep the retry action available. */ }
      }
    } finally {
      setSending(false)
    }
  }

  return (
    <section className="chat-page" aria-label={t.chatTitle}>
      <div className="chat-layout">
        <aside className="chat-history" aria-label={t.chatHistory}>
          <div className="chat-history-heading">
            <h2>{t.chatHistory}</h2>
            <button className="button button-primary" type="button" onClick={startConversation}>{t.chatNew}</button>
          </div>
          <div className="chat-history-list" aria-busy={loading}>
            {loading ? <p role="status">{t.chatLoadingHistory}</p> : conversations.length === 0 ? (
              <p className="chat-history-empty">{t.chatHistoryEmpty}</p>
            ) : conversations.map((item) => (
              <button key={item.id} type="button"
                className={`chat-history-item ${activeId === item.id ? 'active' : ''}`}
                aria-current={activeId === item.id ? 'true' : undefined}
                onClick={() => void openConversation(item.id)}>
                {item.title || t.chatNew}
              </button>
            ))}
          </div>
          {conversationListError && (
            <button className="text-link" type="button" onClick={() => void loadConversations()}>{t.chatRetry}</button>
          )}
        </aside>
        <div className="chat-panel">
          <div className="chat-messages" aria-live="polite" aria-relevant="additions" aria-busy={sending} ref={messagesRef}>
            {messages.length === 0 && !messageLoadError && <p className="chat-empty">{t.chatEmpty}</p>}
            {messages.map((message) => (
              <article key={message.id} className={`chat-message ${message.role.toLowerCase()}`}>
                {message.role === 'ASSISTANT'
                  ? <MarkdownMessage content={message.content} copyLabel={t.chatCopyCode} copiedLabel={t.chatCodeCopied} />
                  : <p>{message.content}</p>}
              </article>
            ))}
            {sending && !streaming && <p className="chat-empty" role="status">{t.chatSending}</p>}
          </div>
          {messageLoadError && (
            <div className="chat-error" role="alert">
              <span>{t.chatLoadError}</span>
              <button className="text-link" type="button" onClick={() => {
                const id = activeConversationId.current
                if (id !== null) void openConversation(id)
              }}>{t.chatRetry}</button>
            </div>
          )}
          {error && <p className="chat-error" role="alert">{error}</p>}
          {ticketFeedback && <p className="chat-ticket-feedback" role="status">{ticketFeedback} <a href="#tickets">{t.viewTickets}</a></p>}
          {ticketRecommendation && !sending && activeId !== null && ticketDraft === null && <p className="chat-ticket-feedback" role="status">{t.chatTicketRecommended}</p>}
          {activeId !== null && messages.length > 0 && !sending && ticketDraft === null && (
            <div className="chat-ticket-actions">
              <button className="button button-secondary" type="button" disabled={ticketDraftLoading} onClick={() => void openTicketDraft()}>
                {ticketDraftLoading ? t.chatTicketDraftLoading : ticketRecommendation ? t.chatCreateRecommendedTicket : t.chatCreateTicket}
              </button>
            </div>
          )}
          {ticketDraft !== null && (
            <form className="chat-ticket-editor" noValidate onSubmit={(event) => void createTicketFromConversation(event)}>
              <h3>{t.chatTicketReviewTitle}</h3>
              <p>{t.chatTicketReviewDescription}</p>
              <label className="chat-ticket-field">
                <span>{t.ticketTitleLabel}</span>
                <input maxLength={200} required value={ticketDraft.title} onChange={(event) => setTicketDraft({ ...ticketDraft, title: event.target.value })} />
              </label>
              <label className="chat-ticket-field">
                <span>{t.ticketDescriptionLabel}</span>
                <textarea maxLength={60000} required rows={6} value={ticketDraft.description} onChange={(event) => setTicketDraft({ ...ticketDraft, description: truncateUtf8(event.target.value, 60000) })} />
              </label>
              <label className="chat-ticket-field">
                <span>{t.ticketPriorityLabel}</span>
                <select value={ticketDraft.priority} onChange={(event) => setTicketDraft({ ...ticketDraft, priority: event.target.value as TicketDraft['priority'] })}>
                  <option value="LOW">{t.priorityLow}</option><option value="MEDIUM">{t.priorityMedium}</option><option value="HIGH">{t.priorityHigh}</option>
                </select>
              </label>
              <div className="chat-ticket-editor-actions">
                <button className="button button-secondary" type="button" disabled={creatingTicket} onClick={() => setTicketDraft(null)}>{t.ticketCancel}</button>
                <button className="button button-primary" type="submit" disabled={creatingTicket || !ticketDraft.title.trim() || !ticketDraft.description.trim()}>{creatingTicket ? t.chatTicketCreating : t.chatTicketConfirm}</button>
              </div>
            </form>
          )}
          {retryMessageId !== null && (
            <button className="button button-secondary" type="button" onClick={() => void retryAnswer()} disabled={sending}>
              {t.chatRetry}
            </button>
          )}
          <form className="chat-composer" onSubmit={sendMessage}>
            <label className="sr-only" htmlFor="chat-composer-input">{t.chatComposerLabel}</label>
            <textarea id="chat-composer-input" ref={composerRef} value={draft}
              onChange={(event) => {
                draftRef.current = event.target.value
                setDraft(event.target.value)
              }}
              onKeyDown={handleComposerKeyDown}
              placeholder={t.chatPlaceholder} maxLength={12000} rows={3} disabled={sending || ticketDraft !== null} />
            <button className="button button-primary" type="submit" disabled={sending || ticketDraft !== null || !draft.trim()}>
              {t.chatSend}
            </button>
          </form>
        </div>
      </div>
    </section>
  )
}
