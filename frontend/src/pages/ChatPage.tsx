import { useCallback, useEffect, useRef, useState } from 'react'
import type { FormEvent, KeyboardEvent } from 'react'
import './ChatPage.css'
import { API_BASE_URL } from '../api'
import type { Copy } from '../i18n/copy'

type Conversation = { id: number; title: string | null; created_at: string; updated_at: string }
type Message = { id: number; role: 'USER' | 'ASSISTANT'; content: string; created_at: string }
type ChatPageProps = { text: Copy }

class ChatApiError extends Error {
  readonly status: number
  readonly savedMessageId: number | null

  constructor(message: string, status: number, savedMessageId: number | null) {
    super(message)
    this.status = status
    this.savedMessageId = savedMessageId
  }
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

export function ChatPage({ text: t }: ChatPageProps) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [retryMessageId, setRetryMessageId] = useState<number | null>(null)
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
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
      setError('')
      return items
    } catch {
      setError(t.chatLoadError)
      return []
    }
  }, [fetchConversations, t.chatLoadError])

  useEffect(() => {
    let active = true
    void fetchConversations()
      .then((items) => {
        if (active) {
          setConversations(items)
          setError('')
        }
      })
      .catch(() => {
        if (active) setError(t.chatLoadError)
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => { active = false }
  }, [fetchConversations, t.chatLoadError])

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
  }

  const openConversation = async (id: number) => {
    const requestId = ++conversationRequest.current
    activeConversationId.current = id
    setActiveId(id)
    setMessages([])
    setRetryMessageId(null)
    setError('')
    try {
      const items = await api<Message[]>(`/api/v1/conversations/${id}/messages`)
      if (activeConversationId.current !== id || conversationRequest.current !== requestId) return
      setMessages(items)
      const lastMessage = items.at(-1)
      setRetryMessageId(lastMessage?.role === 'USER' ? lastMessage.id : null)
    } catch {
      if (activeConversationId.current === id && conversationRequest.current === requestId) {
        setError(t.chatLoadError)
      }
    }
  }

  const startConversation = async () => {
    setError('')
    try {
      const item = await api<Conversation>('/api/v1/conversations', {
        method: 'POST', body: JSON.stringify({}),
      })
      ++conversationRequest.current
      activeConversationId.current = item.id
      setActiveId(item.id)
      setConversations((current) => [item, ...current])
      setMessages([])
      setRetryMessageId(null)
    } catch {
      setError(t.chatLoadError)
    }
  }

  const sendMessage = async (event: FormEvent) => {
    event.preventDefault()
    const content = draft.trim()
    if (!content || sending) return

    let conversationId = activeConversationId.current
    let requestId = conversationRequest.current
    setSending(true)
    setError('')
    try {
      if (conversationId === null) {
        const created = await api<Conversation>('/api/v1/conversations', {
          method: 'POST', body: JSON.stringify({}),
        })
        conversationId = created.id
        const stillCurrent = conversationRequest.current === requestId && activeConversationId.current === null
        if (stillCurrent) {
          requestId = ++conversationRequest.current
          activeConversationId.current = created.id
          setActiveId(created.id)
        }
        setConversations((current) => [created, ...current])
      }
      const result = await api<{
        conversation_id: number
        user_message: Message
        assistant_message: Message
      }>(`/api/v1/conversations/${conversationId}/messages`, {
        method: 'POST', body: JSON.stringify({ content }),
      })
      if (activeConversationId.current === conversationId && conversationRequest.current === requestId) {
        focusComposerAfterResponse.current = true
        setMessages((current) => [...current, result.user_message, result.assistant_message])
        setRetryMessageId(null)
      }
      setDraft('')
      await loadConversations()
    } catch (requestError) {
      if (activeConversationId.current !== conversationId || conversationRequest.current !== requestId) return
      if (requestError instanceof ChatApiError && requestError.savedMessageId !== null) {
        setDraft('')
        setRetryMessageId(requestError.savedMessageId)
        setError(t.chatAiUnavailable)
        if (conversationId !== null) {
          try { await refreshMessages(conversationId, requestId) } catch { /* Keep the retry ID from the response header. */ }
        }
      } else {
        setError(requestError instanceof ChatApiError && requestError.status === 409
          ? t.chatPreviousUnanswered
          : t.chatSendError)
        if (requestError instanceof ChatApiError && requestError.status === 409 && conversationId !== null) {
          try { await refreshMessages(conversationId, requestId) } catch { /* Preserve the original request error. */ }
        }
      }
    } finally {
      setSending(false)
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
            <button className="button button-primary" type="button" onClick={() => void startConversation()}>{t.chatNew}</button>
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
          {error === t.chatLoadError && (
            <button className="text-link" type="button" onClick={() => void loadConversations()}>{t.chatRetry}</button>
          )}
        </aside>
        <div className="chat-panel">
          <div className="chat-messages" aria-live="polite" aria-relevant="additions text" ref={messagesRef}>
            {messages.length === 0 && <p className="chat-empty">{t.chatEmpty}</p>}
            {messages.map((message) => (
              <article key={message.id} className={`chat-message ${message.role.toLowerCase()}`}>
                <span>{message.role === 'USER' ? t.chatUser : t.chatAssistant}</span>
                <p>{message.content}</p>
              </article>
            ))}
            {sending && <p className="chat-empty" role="status">{t.chatSending}</p>}
          </div>
          {error && error !== t.chatLoadError && <p className="chat-error" role="alert">{error}</p>}
          {retryMessageId !== null && (
            <button className="button button-secondary" type="button" onClick={() => void retryAnswer()} disabled={sending}>
              {t.chatRetry}
            </button>
          )}
          <form className="chat-composer" onSubmit={sendMessage}>
            <label className="sr-only" htmlFor="chat-composer-input">{t.chatComposerLabel}</label>
            <textarea id="chat-composer-input" ref={composerRef} value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={handleComposerKeyDown}
              placeholder={t.chatPlaceholder} maxLength={12000} rows={3} disabled={sending} />
            <button className="button button-primary" type="submit" disabled={sending || !draft.trim()}>
              {t.chatSend}
            </button>
          </form>
        </div>
      </div>
    </section>
  )
}
