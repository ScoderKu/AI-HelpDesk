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

type TicketRoute = { mode: 'list' | 'create' | 'detail' | 'edit'; ticketId: number | null }

function readTicketRoute(): TicketRoute {
  const parts = window.location.hash.slice(1).replace(/^\//, '').split('/')
  if (parts[0] !== 'tickets') return { mode: 'list', ticketId: null }
  if (parts[1] === 'new') return { mode: 'create', ticketId: null }
  const ticketId = parts[1] ? Number(parts[1]) : null
  if (ticketId !== null && Number.isInteger(ticketId) && ticketId > 0) return { mode: parts[2] === 'edit' ? 'edit' : 'detail', ticketId }
  return { mode: 'list', ticketId: null }
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

export function TicketsPage({ language, text, onChanged }: TicketsPageProps) {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)
  const [ticketRoute, setTicketRoute] = useState<TicketRoute>(readTicketRoute)
  const mode = ticketRoute.mode === 'edit' ? 'detail' : ticketRoute.mode
  const isEditing = ticketRoute.mode === 'edit'
  const [form, setForm] = useState<TicketFormValues>(emptyForm)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [feedback, setFeedback] = useState('')
  const [showValidation, setShowValidation] = useState(false)
  const [sortBy, setSortBy] = useState('newest')
  const [statusFilter, setStatusFilter] = useState('ALL')
  const [priorityFilter, setPriorityFilter] = useState('ALL')
  const loadRequestKey = ticketRoute.mode === 'list'
    ? `list:${text.ticketLoadError}:${text.ticketNotFound}`
    : (ticketRoute.mode === 'detail' || ticketRoute.mode === 'edit') && ticketRoute.ticketId !== null
      ? `${ticketRoute.mode}:${ticketRoute.ticketId}:${text.ticketLoadError}:${text.ticketNotFound}`
      : null
  const [completedLoadRequestKey, setCompletedLoadRequestKey] = useState<string | null>(null)
  const isLoading = loadRequestKey !== null && loadRequestKey !== completedLoadRequestKey
  const visibleSelectedTicket =
    loadRequestKey === completedLoadRequestKey && ticketRoute.ticketId === selectedTicket?.id
      ? selectedTicket
      : null
  const sortedTickets = tickets.filter((ticket) =>
    (statusFilter === 'ALL' || ticket.status === statusFilter) &&
    (priorityFilter === 'ALL' || ticket.priority === priorityFilter)
  ).sort((a, b) => {
    const date = new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    const priorityRank = { HIGH: 0, MEDIUM: 1, LOW: 2 }
    const priority = priorityRank[a.priority] - priorityRank[b.priority]
    const status = (a.status === b.status ? 0 : a.status === 'OPEN' ? -1 : 1)
    const orders: Record<string, number[]> = { newest: [date], oldest: [-date], priorityHigh: [priority, date], priorityLow: [-priority, date], openFirst: [status, date], closedFirst: [-status, date] }
    return (orders[sortBy] ?? orders.newest).find((value) => value !== 0) ?? 0
  })

  const navigateTicket = (next: TicketRoute) => {
    const hash = next.mode === 'list' ? '#tickets' : next.mode === 'create' ? '#tickets/new' : next.mode === 'edit' ? `#tickets/${next.ticketId}/edit` : `#tickets/${next.ticketId}`
    if (window.location.hash !== hash) window.history.pushState(null, '', hash)
    setError('')
    setTicketRoute(next)
  }

  useEffect(() => {
    const syncRoute = () => {
      setError('')
      setTicketRoute(readTicketRoute())
    }
    window.addEventListener('hashchange', syncRoute)
    window.addEventListener('popstate', syncRoute)
    return () => { window.removeEventListener('hashchange', syncRoute); window.removeEventListener('popstate', syncRoute) }
  }, [])

  useEffect(() => {
    let active = true
    if (ticketRoute.mode === 'list') {
      ticketsApi.list().then((items) => { if (active) setTickets(items) })
        .catch(() => { if (active) setError(text.ticketLoadError) })
        .finally(() => { if (active && loadRequestKey !== null) setCompletedLoadRequestKey(loadRequestKey) })
    } else if (ticketRoute.mode === 'detail' || ticketRoute.mode === 'edit') {
      const id = ticketRoute.ticketId
      if (id === null) return () => { active = false }
      ticketsApi.get(id).then((ticket) => {
        if (!active) return
        setSelectedTicket(ticket)
        setForm({ title: ticket.title, description: ticket.description, priority: ticket.priority })
        setShowValidation(false)
      }).catch((requestError) => {
        if (active) setError(getErrorStatus(requestError) === 404 ? text.ticketNotFound : text.ticketLoadError)
      }).finally(() => { if (active && loadRequestKey !== null) setCompletedLoadRequestKey(loadRequestKey) })
    } else {
      return () => { active = false }
    }
    return () => { active = false }
  }, [ticketRoute, loadRequestKey, text.ticketLoadError, text.ticketNotFound])

  const openCreate = () => {
    setForm(emptyForm)
    setFeedback('')
    setError('')
    setShowValidation(false)
    navigateTicket({ mode: 'create', ticketId: null })
  }

  const openTicket = (id: number) => {
    setFeedback('')
    navigateTicket({ mode: 'detail', ticketId: id })
  }

  const returnToList = () => {
    setFeedback('')
    setSelectedTicket(null)
    navigateTicket({ mode: 'list', ticketId: null })
  }

  const changeSortBy = (nextSortBy: string) => {
    setSortBy(nextSortBy)
    if ((nextSortBy === 'openFirst' && statusFilter === 'CLOSED') ||
        (nextSortBy === 'closedFirst' && statusFilter === 'OPEN')) {
      setStatusFilter('ALL')
    }
    if ((nextSortBy === 'priorityHigh' && priorityFilter === 'LOW') ||
        (nextSortBy === 'priorityLow' && priorityFilter === 'HIGH')) {
      setPriorityFilter('ALL')
    }
  }

  const resetTicketControls = () => {
    setSortBy('newest')
    setStatusFilter('ALL')
    setPriorityFilter('ALL')
  }

  const handleCreate = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setShowValidation(true)
    setError('')
    if (!form.title.trim()) { setError(text.ticketTitleRequired); return }
    if (!form.description.trim()) { setError(text.ticketDescriptionRequired); return }
    setIsSaving(true)
    try {
      const ticket = await ticketsApi.create({ ...form, title: form.title.trim(), description: form.description.trim() })
      setSelectedTicket(ticket)
      setForm({ title: ticket.title, description: ticket.description, priority: ticket.priority })
      navigateTicket({ mode: 'detail', ticketId: ticket.id })
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
    if (!visibleSelectedTicket) return
    setShowValidation(true)
    setError('')
    if (!form.title.trim()) { setError(text.ticketTitleRequired); return }
    if (!form.description.trim()) { setError(text.ticketDescriptionRequired); return }
    setIsSaving(true)
    try {
      const ticket = await ticketsApi.update(visibleSelectedTicket.id, { ...form, title: form.title.trim(), description: form.description.trim() })
      setSelectedTicket(ticket)
      setForm({ title: ticket.title, description: ticket.description, priority: ticket.priority })
      navigateTicket({ mode: 'detail', ticketId: ticket.id })
      setFeedback(text.ticketUpdated)
    } catch {
      setError(text.ticketActionError)
    } finally {
      setIsSaving(false)
    }
  }

  const handleClose = async () => {
    if (!visibleSelectedTicket) return
    setError('')
    setIsSaving(true)
    try {
      const ticket = await ticketsApi.close(visibleSelectedTicket.id)
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
          id="ticket-title-input"
          required
          value={form.title}
          aria-invalid={showValidation && !form.title.trim()}
          aria-describedby={showValidation && !form.title.trim() ? 'ticket-title-error' : undefined}
          onChange={(event) => setForm({ ...form, title: event.target.value })}
        />
        {showValidation && !form.title.trim() && <span className="ticket-field-error" id="ticket-title-error">{text.ticketTitleRequired}</span>}
      </label>
      <label className="ticket-field">
        <span>{text.ticketDescriptionLabel}</span>
        <textarea
          maxLength={65535}
          id="ticket-description-input"
          required
          rows={6}
          value={form.description}
          aria-invalid={showValidation && !form.description.trim()}
          aria-describedby={showValidation && !form.description.trim() ? 'ticket-description-error' : undefined}
          onChange={(event) => setForm({ ...form, description: event.target.value })}
        />
        {showValidation && !form.description.trim() && <span className="ticket-field-error" id="ticket-description-error">{text.ticketDescriptionRequired}</span>}
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

      {mode === 'list' && (
        <div className="ticket-list-panel">
          {feedback && <p className="ticket-message ticket-success ticket-list-feedback" role="status">{feedback}</p>}
          <div className="ticket-list-toolbar">
            <div className="ticket-list-controls">
              <label><span>{text.ticketSortLabel}</span><select value={sortBy} onChange={(event) => changeSortBy(event.target.value)}>
                <option value="newest">{text.ticketSortNewest}</option><option value="oldest">{text.ticketSortOldest}</option>
                <option value="priorityHigh">{text.ticketSortPriorityHigh}</option><option value="priorityLow">{text.ticketSortPriorityLow}</option>
                <option value="openFirst">{text.ticketSortOpen}</option><option value="closedFirst">{text.ticketSortClosed}</option>
              </select></label>
              <label><span>{text.ticketFilterStatus}</span><select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
                <option value="ALL">{text.ticketFilterAll}</option>
                <option value="OPEN" disabled={sortBy === 'closedFirst'}>{text.ticketOpen}</option>
                <option value="CLOSED" disabled={sortBy === 'openFirst'}>{text.ticketClosed}</option>
              </select></label>
              <label><span>{text.ticketFilterPriority}</span><select value={priorityFilter} onChange={(event) => setPriorityFilter(event.target.value)}>
                <option value="ALL">{text.ticketFilterAll}</option>
                <option value="HIGH" disabled={sortBy === 'priorityLow'}>{text.priorityHigh}</option>
                <option value="MEDIUM">{text.priorityMedium}</option>
                <option value="LOW" disabled={sortBy === 'priorityHigh'}>{text.priorityLow}</option>
              </select></label>
              <button className="ticket-reset-button" onClick={resetTicketControls} type="button" disabled={sortBy === 'newest' && statusFilter === 'ALL' && priorityFilter === 'ALL'}>{text.ticketResetFilters}</button>
              <span className="ticket-results-count">{sortedTickets.length} {text.ticketResults}</span>
            </div>
          </div>
          {isLoading ? <p className="ticket-empty-state" role="status">{text.ticketLoading}</p> :
            tickets.length === 0 ? (
              <div className="ticket-empty-state">
                <p>{text.ticketEmpty}</p>
                <button className="text-link" onClick={openCreate} type="button">{text.newTicket}</button>
              </div>
            ) : sortedTickets.length === 0 ? <p className="ticket-empty-state">{text.ticketNoMatches}</p> : (
              <div className="ticket-list" aria-label={text.ticketTitle}>
                {sortedTickets.map((ticket) => (
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
        <form className="ticket-form-panel" noValidate onSubmit={(event) => void handleCreate(event)}>
          {feedback && <p className="ticket-message ticket-success" role="status">{feedback}</p>}
          {formFields}
          <div className="ticket-form-actions">
            <button className="button button-secondary" disabled={isSaving} onClick={() => navigateTicket({ mode: 'list', ticketId: null })} type="button">
              {text.ticketCancel}
            </button>
            <button className="button button-primary" disabled={isSaving} type="submit">
              {isSaving ? text.ticketLoading : text.ticketCreate}
            </button>
          </div>
        </form>
      )}

      {(ticketRoute.mode === 'detail' || ticketRoute.mode === 'edit') && isLoading && <p className="ticket-empty-state" role="status">{text.ticketLoading}</p>}

      {mode === 'detail' && visibleSelectedTicket && (
        <div className="ticket-detail-panel">
          {feedback && <p className="ticket-message ticket-success ticket-list-feedback" role="status">{feedback}</p>}
          <div className="ticket-detail-heading">
            <h2>{visibleSelectedTicket.title}</h2>
            <span className={`ticket-badge ticket-status-${visibleSelectedTicket.status.toLowerCase()}`}>
              {statusLabel(visibleSelectedTicket.status, text)}
            </span>
          </div>
          {isEditing ? (
            <form className="ticket-form" noValidate onSubmit={(event) => void handleUpdate(event)}>
              {formFields}
              <div className="ticket-form-actions">
                <button className="button button-secondary" disabled={isSaving} onClick={() => {
                  setForm({ title: visibleSelectedTicket.title, description: visibleSelectedTicket.description, priority: visibleSelectedTicket.priority })
                  navigateTicket({ mode: 'detail', ticketId: visibleSelectedTicket.id })
                }} type="button">{text.ticketCancel}</button>
                <button className="button button-primary" disabled={isSaving} type="submit">
                  {isSaving ? text.ticketLoading : text.ticketSave}
                </button>
              </div>
            </form>
          ) : (
            <>
              <dl className="ticket-detail-meta">
                <div><dt>{text.ticketPriorityLabel}</dt><dd>{priorityLabel(visibleSelectedTicket.priority, text)}</dd></div>
                <div><dt>{text.ticketCreatedAt}</dt><dd>{formatDate(visibleSelectedTicket.created_at, language)}</dd></div>
              </dl>
              <div className="ticket-detail-description">
                <h3>{text.ticketDescriptionLabel}</h3>
                <p>{visibleSelectedTicket.description}</p>
              </div>
              <div className="ticket-form-actions">
                <button className="button button-secondary" onClick={() => void returnToList()} type="button">{text.ticketBack}</button>
                {visibleSelectedTicket.status === 'OPEN' && (
                  <>
                    <button className="button button-secondary" disabled={isSaving} onClick={() => { setShowValidation(false); navigateTicket({ mode: 'edit', ticketId: visibleSelectedTicket.id }) }} type="button">
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
