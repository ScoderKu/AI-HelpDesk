import { useEffect, useState, type FormEvent } from 'react'
import { ticketsApi } from '../ticketsApi'
import type { Ticket, TicketPriority, Language } from '../types'
import type { Copy } from '../i18n/copy'

type TicketsPageProps = {
  language: Language
  text: Copy
  onBackHome: () => void
  onChanged: () => void
}

type TicketFormValues = {
  title: string
  description: string
  priority: TicketPriority
}

const emptyForm: TicketFormValues = { title: '', description: '', priority: 'MEDIUM' }

function getErrorStatus(error: unknown): number | undefined {
  return error instanceof Error && 'status' in error
    ? Number((error as Error & { status: number }).status)
    : undefined
}

function statusLabel(status: Ticket['status'], text: Copy): string {
  return status === 'OPEN' ? text.ticketOpen : text.ticketClosed
}

function priorityLabel(priority: TicketPriority, text: Copy): string {
  if (priority === 'LOW') return text.priorityLow
  if (priority === 'HIGH') return text.priorityHigh
  return text.priorityMedium
}

function formatDate(value: string, language: Language): string {
  return new Intl.DateTimeFormat(language === 'fi' ? 'fi-FI' : 'en-GB', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export function TicketsPage({ language, text, onBackHome, onChanged }: TicketsPageProps) {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)
  const [mode, setMode] = useState<'list' | 'create' | 'detail'>('list')
  const [form, setForm] = useState<TicketFormValues>(emptyForm)
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [feedback, setFeedback] = useState('')

  const loadTickets = async () => {
    setIsLoading(true)
    setError('')
    try {
      setTickets(await ticketsApi.list())
    } catch {
      setError(text.ticketLoadError)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let active = true
    ticketsApi.list()
      .then((items) => { if (active) setTickets(items) })
      .catch(() => { if (active) setError(text.ticketLoadError) })
      .finally(() => { if (active) setIsLoading(false) })
    return () => { active = false }
  }, [text.ticketLoadError])

  const openCreate = () => {
    setForm(emptyForm)
    setFeedback('')
    setError('')
    setMode('create')
  }

  const openTicket = async (id: number) => {
    setIsLoading(true)
    setError('')
    setFeedback('')
    try {
      const ticket = await ticketsApi.get(id)
      setSelectedTicket(ticket)
      setForm({ title: ticket.title, description: ticket.description, priority: ticket.priority })
      setIsEditing(false)
      setMode('detail')
    } catch (requestError) {
      setError(getErrorStatus(requestError) === 404 ? text.ticketNotFound : text.ticketLoadError)
    } finally {
      setIsLoading(false)
    }
  }

  const returnToList = async () => {
    setMode('list')
    setSelectedTicket(null)
    setIsEditing(false)
    await loadTickets()
  }

  const handleCreate = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')
    setIsSaving(true)
    try {
      const ticket = await ticketsApi.create(form)
      setSelectedTicket(ticket)
      setForm({ title: ticket.title, description: ticket.description, priority: ticket.priority })
      setMode('detail')
      setFeedback(text.ticketCreated)
      onChanged()
    } catch {
      setError(text.ticketActionError)
    } finally {
      setIsSaving(false)
    }
  }

  const handleUpdate = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!selectedTicket) return
    setError('')
    setIsSaving(true)
    try {
      const ticket = await ticketsApi.update(selectedTicket.id, form)
      setSelectedTicket(ticket)
      setForm({ title: ticket.title, description: ticket.description, priority: ticket.priority })
      setIsEditing(false)
      setFeedback(text.ticketUpdated)
    } catch {
      setError(text.ticketActionError)
    } finally {
      setIsSaving(false)
    }
  }

  const handleClose = async () => {
    if (!selectedTicket) return
    setError('')
    setIsSaving(true)
    try {
      const ticket = await ticketsApi.close(selectedTicket.id)
      setSelectedTicket(ticket)
      setFeedback(text.ticketCloseSuccess)
      onChanged()
    } catch {
      setError(text.ticketActionError)
    } finally {
      setIsSaving(false)
    }
  }

  const formFields = (
    <>
      <label className="ticket-field">
        <span>{text.ticketTitleLabel}</span>
        <input
          maxLength={200}
          required
          value={form.title}
          onChange={(event) => setForm({ ...form, title: event.target.value })}
        />
      </label>
      <label className="ticket-field">
        <span>{text.ticketDescriptionLabel}</span>
        <textarea
          maxLength={65535}
          required
          rows={6}
          value={form.description}
          onChange={(event) => setForm({ ...form, description: event.target.value })}
        />
      </label>
      <label className="ticket-field ticket-priority-field">
        <span>{text.ticketPriorityLabel}</span>
        <select
          value={form.priority}
          onChange={(event) => setForm({ ...form, priority: event.target.value as TicketPriority })}
        >
          <option value="LOW">{text.priorityLow}</option>
          <option value="MEDIUM">{text.priorityMedium}</option>
          <option value="HIGH">{text.priorityHigh}</option>
        </select>
      </label>
    </>
  )

  return (
    <section className="tickets-page" aria-labelledby="tickets-title">
      <div className="tickets-page-heading">
        <div>
          <button className="text-link ticket-home-link" onClick={onBackHome} type="button">
            {text.ticketBackHome}
          </button>
          <h1 id="tickets-title">{mode === 'create' ? text.ticketCreateTitle : text.ticketTitle}</h1>
          <p>{text.ticketDescription}</p>
        </div>
        {mode === 'list' && (
          <button className="button button-primary" onClick={openCreate} type="button">
            {text.newTicket}
          </button>
        )}
      </div>

      {error && <p className="ticket-message ticket-error" role="alert">{error}</p>}
      {feedback && <p className="ticket-message ticket-success" role="status">{feedback}</p>}

      {mode === 'list' && (
        <div className="ticket-list-panel">
          {isLoading ? <p className="ticket-empty-state" role="status">{text.ticketLoading}</p> :
            tickets.length === 0 ? (
              <div className="ticket-empty-state">
                <p>{text.ticketEmpty}</p>
                <button className="text-link" onClick={openCreate} type="button">{text.newTicket}</button>
              </div>
            ) : (
              <div className="ticket-list" aria-label={text.ticketTitle}>
                {tickets.map((ticket) => (
                  <button className="ticket-list-row" key={ticket.id} onClick={() => void openTicket(ticket.id)} type="button">
                    <span className="ticket-list-main">
                      <strong>{ticket.title}</strong>
                      <span>{formatDate(ticket.created_at, language)}</span>
                    </span>
                    <span className={`ticket-badge ticket-status-${ticket.status.toLowerCase()}`}>
                      {statusLabel(ticket.status, text)}
                    </span>
                    <span className={`ticket-badge ticket-priority-${ticket.priority.toLowerCase()}`}>
                      {priorityLabel(ticket.priority, text)}
                    </span>
                  </button>
                ))}
              </div>
            )}
        </div>
      )}

      {mode === 'create' && (
        <form className="ticket-form-panel" onSubmit={(event) => void handleCreate(event)}>
          {formFields}
          <div className="ticket-form-actions">
            <button className="button button-secondary" disabled={isSaving} onClick={() => setMode('list')} type="button">
              {text.ticketCancel}
            </button>
            <button className="button button-primary" disabled={isSaving} type="submit">
              {isSaving ? text.ticketLoading : text.ticketCreate}
            </button>
          </div>
        </form>
      )}

      {mode === 'detail' && selectedTicket && (
        <div className="ticket-detail-panel">
          <button className="text-link ticket-home-link" onClick={() => void returnToList()} type="button">
            {text.ticketBack}
          </button>
          <div className="ticket-detail-heading">
            <h2>{selectedTicket.title}</h2>
            <span className={`ticket-badge ticket-status-${selectedTicket.status.toLowerCase()}`}>
              {statusLabel(selectedTicket.status, text)}
            </span>
          </div>
          {isEditing ? (
            <form className="ticket-form" onSubmit={(event) => void handleUpdate(event)}>
              {formFields}
              <div className="ticket-form-actions">
                <button className="button button-secondary" disabled={isSaving} onClick={() => {
                  setForm({ title: selectedTicket.title, description: selectedTicket.description, priority: selectedTicket.priority })
                  setIsEditing(false)
                }} type="button">{text.ticketCancel}</button>
                <button className="button button-primary" disabled={isSaving} type="submit">
                  {isSaving ? text.ticketLoading : text.ticketSave}
                </button>
              </div>
            </form>
          ) : (
            <>
              <dl className="ticket-detail-meta">
                <div><dt>{text.ticketPriorityLabel}</dt><dd>{priorityLabel(selectedTicket.priority, text)}</dd></div>
                <div><dt>{text.ticketCreatedAt}</dt><dd>{formatDate(selectedTicket.created_at, language)}</dd></div>
              </dl>
              <div className="ticket-detail-description">
                <h3>{text.ticketDescriptionLabel}</h3>
                <p>{selectedTicket.description}</p>
              </div>
              <div className="ticket-form-actions">
                {selectedTicket.status === 'OPEN' && (
                  <>
                    <button className="button button-secondary" disabled={isSaving} onClick={() => setIsEditing(true)} type="button">
                      {text.ticketEdit}
                    </button>
                    <button className="button button-danger" disabled={isSaving} onClick={() => void handleClose()} type="button">
                      {isSaving ? text.ticketLoading : text.ticketClose}
                    </button>
                  </>
                )}
              </div>
            </>
          )}
        </div>
      )}
    </section>
  )
}
