import { useCallback, useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import './ChatPage.css'
import { API_BASE_URL } from '../api'
import type { Language } from '../types'

type Conversation = { id: number; title: string | null; created_at: string; updated_at: string }
type Message = { id: number; role: 'USER' | 'ASSISTANT'; content: string; created_at: string }
type ChatPageProps = { language: Language; onBackHome: () => void }

const labels = {
  fi: {
    title: 'AI-keskustelu', newChat: 'Uusi keskustelu', placeholder: 'Kirjoita tekninen ongelmasi…',
    send: 'Lähetä', sending: 'AI vastaa…', empty: 'Aloita kuvailemalla tekninen ongelmasi.',
    loadError: 'Keskusteluja ei voitu ladata.', sendError: 'Viestin lähettäminen epäonnistui. Yritä uudelleen.',
    back: 'Etusivulle', history: 'Keskusteluhistoria', retry: 'Yritä uudelleen',
  },
  en: {
    title: 'AI chat', newChat: 'New conversation', placeholder: 'Describe your technical issue…',
    send: 'Send', sending: 'AI is responding…', empty: 'Start by describing your technical issue.',
    loadError: 'Could not load conversations.', sendError: 'Could not send the message. Please try again.',
    back: 'Home', history: 'Conversation history', retry: 'Try again',
  },
}

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!response.ok) {
    let detail = ''
    try { const body = await response.json(); detail = typeof body.detail === 'string' ? body.detail : '' } catch { /* ignore */ }
    throw new Error(detail || `HTTP ${response.status}`)
  }
  return response.status === 204 ? undefined as T : response.json()
}

export function ChatPage({ language, onBackHome }: ChatPageProps) {
  const t = labels[language]
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')

  const loadConversations = useCallback(async () => {
    try {
      const items = await api<Conversation[]>('/api/v1/conversations')
      setConversations(items)
      setError('')
      return items
    } catch {
      setError(t.loadError)
      return []
    } finally {
      setLoading(false)
    }
  }, [t.loadError])

  useEffect(() => { void loadConversations() }, [loadConversations])

  const openConversation = async (id: number) => {
    setActiveId(id)
    setMessages([])
    setError('')
    try {
      const items = await api<Message[]>(`/api/v1/conversations/${id}/messages`)
      setMessages(items)
    } catch { setError(t.loadError) }
  }

  const startConversation = async () => {
    setError('')
    try {
      const item = await api<Conversation>('/api/v1/conversations', {
        method: 'POST', body: JSON.stringify({}),
      })
      setConversations((current) => [item, ...current])
      setActiveId(item.id)
      setMessages([])
    } catch { setError(t.loadError) }
  }

  const sendMessage = async (event: FormEvent) => {
    event.preventDefault()
    const content = draft.trim()
    if (!content || sending) return
    let conversationId = activeId
    setSending(true)
    setError('')
    try {
      if (conversationId === null) {
        const created = await api<Conversation>('/api/v1/conversations', {
          method: 'POST', body: JSON.stringify({}),
        })
        conversationId = created.id
        setActiveId(created.id)
        setConversations((current) => [created, ...current])
      }
      const result = await api<{
        conversation_id: number
        user_message: Message
        assistant_message: Message
      }>(`/api/v1/conversations/${conversationId}/messages`, {
        method: 'POST', body: JSON.stringify({ content }),
      })
      setMessages((current) => [...current, result.user_message, result.assistant_message])
      setDraft('')
      await loadConversations()
    } catch {
      setError(t.sendError)
    } finally { setSending(false) }
  }

  return (
    <section className="chat-page" aria-label={t.title}>
      <header className="chat-page-header">
        <div><h1>{t.title}</h1><p>{t.history}</p></div>
        <button className="button button-secondary" type="button" onClick={onBackHome}>{t.back}</button>
      </header>
      <div className="chat-layout">
        <aside className="chat-history">
          <button className="button button-primary" type="button" onClick={startConversation}>{t.newChat}</button>
          {loading ? <p>{t.sending}</p> : conversations.map((item) => (
            <button key={item.id} type="button"
              className={`chat-history-item ${activeId === item.id ? 'active' : ''}`}
              onClick={() => void openConversation(item.id)}>
              {item.title || t.newChat}
            </button>
          ))}
        </aside>
        <div className="chat-panel">
          <div className="chat-messages" aria-live="polite">
            {messages.length === 0 && <p className="chat-empty">{t.empty}</p>}
            {messages.map((message) => (
              <article key={message.id} className={`chat-message ${message.role.toLowerCase()}`}>
                <span>{message.role === 'USER' ? 'You' : 'AI HelpDesk'}</span>
                <p>{message.content}</p>
              </article>
            ))}
            {sending && <p className="chat-empty">{t.sending}</p>}
          </div>
          {error && <p className="chat-error" role="alert">{error}</p>}
          <form className="chat-composer" onSubmit={sendMessage}>
            <textarea value={draft} onChange={(event) => setDraft(event.target.value)}
              placeholder={t.placeholder} maxLength={12000} rows={3} disabled={sending} />
            <button className="button button-primary" type="submit" disabled={sending || !draft.trim()}>
              {t.send}
            </button>
          </form>
        </div>
      </div>
    </section>
  )
}
