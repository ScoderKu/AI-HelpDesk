import { useEffect, useState, type ReactNode } from 'react'
import './App.css'

type Language = 'fi' | 'en'
type IconName = 'home' | 'message' | 'ticket' | 'user' | 'sparkle' | 'arrow' | 'layers' | 'circle' | 'check' | 'globe'

const iconPaths: Record<IconName, ReactNode> = {
  home: <><path d="m3 10 9-7 9 7" /><path d="M5 9v11h14V9M9 20v-6h6v6" /></>,
  message: <><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8A8.5 8.5 0 0 1 8.7 3.9a8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8z" /></>,
  ticket: <><path d="M4 5h16v5a2 2 0 0 0 0 4v5H4v-5a2 2 0 0 0 0-4z" /><path d="M13 5v2m0 4v2m0 4v2" /></>,
  user: <><circle cx="12" cy="8" r="4" /><path d="M5 21a7 7 0 0 1 14 0" /></>,
  sparkle: <><path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z" /><path d="m19 14 1.2 2.8L23 18l-2.8 1.2L19 22l-1.2-2.8L15 18l2.8-1.2z" /></>,
  arrow: <><path d="M7 17 17 7M7 7h10v10" /></>,
  layers: <><path d="m12 3 9 5-9 5-9-5z" /><path d="m3 12 9 5 9-5M3 16l9 5 9-5" /></>,
  circle: <><circle cx="12" cy="12" r="8" /></>,
  check: <><path d="m5 12 4 4L19 6" /></>,
  globe: <><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18" /></>,
}

function Icon({ name, className = '' }: { name: IconName; className?: string }) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="1.7"
      viewBox="0 0 24 24"
    >
      {iconPaths[name]}
    </svg>
  )
}

const copy = {
  fi: {
    home: 'Etusivu',
    chat: 'AI-keskustelu',
    tickets: 'Tukipyynnöt',
    profile: 'Profiili',
    workspace: 'TYÖTILA',
    account: 'OMA TILI',
    language: 'Kieli',
    preview: 'Frontend-esikatselu',
    previewDetails: 'Nämä ovat esimerkkilukuja. Tukipyyntöjä ei vielä haeta palvelimelta.',
    eyebrow: 'AI HELP DESK',
    title: 'Miten voimme auttaa tänään?',
    subtitle: 'Kuvaile tekninen ongelmasi ja aloita ratkaiseminen AI-avustajan kanssa.',
    startChat: 'Aloita AI-keskustelu',
    viewTickets: 'Tarkastele tukipyyntöjä',
    summary: 'Tukipyyntöjen yhteenveto',
    summaryDetails: 'Näet tästä omien tukipyyntöjesi tilanteen yhdellä silmäyksellä.',
    total: 'Yhteensä',
    open: 'Avoimet',
    closed: 'Suljetut',
    totalHint: 'kaikki tukipyynnöt',
    openHint: 'odottavat käsittelyä',
    closedHint: 'merkitty ratkaistuiksi',
    quickTitle: 'NOPEASTI ALKUUN',
    actionTitle: 'Ratkaise ongelma AI-avustajan kanssa',
    actionDescription: 'Kuvaile ongelmasi omin sanoin, niin saat ehdotuksia seuraavista askelista.',
    footer: 'AI:n ehdotukset voivat olla virheellisiä. Älä lisää keskusteluun salasanoja tai muita salaisia tietoja.',
    actionNotice: 'Tämä näkymä ei ole vielä yhdistetty palveluun. Mitään tietoja ei lähetetty.',
    storageError: 'Kieliasetusta ei voitu tallentaa tähän selaimeen.',
  },
  en: {
    home: 'Home',
    chat: 'AI chat',
    tickets: 'Support tickets',
    profile: 'Profile',
    workspace: 'WORKSPACE',
    account: 'ACCOUNT',
    language: 'Language',
    preview: 'Frontend preview',
    previewDetails: 'These are sample counts. Tickets are not loaded from a server yet.',
    eyebrow: 'AI HELP DESK',
    title: 'How can we help today?',
    subtitle: 'Describe your technical issue and start solving it with the AI assistant.',
    startChat: 'Start an AI chat',
    viewTickets: 'View support tickets',
    summary: 'Support ticket summary',
    summaryDetails: 'Get a quick overview of your own support tickets.',
    total: 'Total',
    open: 'Open',
    closed: 'Closed',
    totalHint: 'all support tickets',
    openHint: 'waiting for resolution',
    closedHint: 'marked as resolved',
    quickTitle: 'A QUICK START',
    actionTitle: 'Solve the issue with an AI assistant',
    actionDescription: 'Describe the issue in your own words to get suggestions for what to try next.',
    footer: "AI suggestions may be inaccurate. Don't include passwords or other sensitive information in a chat.",
    actionNotice: 'This view is not connected to a service yet. No data was sent.',
    storageError: 'This browser could not save your language preference.',
  },
} satisfies Record<Language, Record<string, string>>

function App() {
  const [language, setLanguage] = useState<Language>(() => {
    try {
      return localStorage.getItem('ai-helpdesk-language') === 'en' ? 'en' : 'fi'
    } catch {
      return 'fi'
    }
  })
  const [notice, setNotice] = useState('')
  const text = copy[language]

  useEffect(() => {
    document.documentElement.lang = language
  }, [language])

  const showPreviewNotice = () => setNotice(text.actionNotice)
  const changeLanguage = (nextLanguage: Language) => {
    setLanguage(nextLanguage)
    try {
      localStorage.setItem('ai-helpdesk-language', nextLanguage)
    } catch {
      setNotice(copy[nextLanguage].storageError)
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#home" aria-label="AI HelpDesk home">
          <span className="brand-mark"><Icon name="sparkle" /></span>
          <span className="brand-name">AI <strong>HelpDesk</strong></span>
        </a>

        <div className="sidebar-language">
            <span className="language-label"><Icon name="globe" />{text.language}</span>
            <div className="language-switch" role="group" aria-label={text.language}>
              <button
                aria-pressed={language === 'fi'}
                className={language === 'fi' ? 'selected' : ''}
                onClick={() => changeLanguage('fi')}
                type="button"
              >
                FI
              </button>
              <button
                aria-pressed={language === 'en'}
                className={language === 'en' ? 'selected' : ''}
                onClick={() => changeLanguage('en')}
                type="button"
              >
                EN
              </button>
            </div>
          </div>
          
        <div className="sidebar-section-label">{text.workspace}</div>
        <nav className="main-nav" aria-label={text.workspace}>
          <a className="nav-link active" href="#home" aria-current="page">
            <Icon name="home" />
            <span>{text.home}</span>
          </a>
          <button className="nav-link" onClick={showPreviewNotice} type="button">
            <Icon name="message" />
            <span>{text.chat}</span>
            <span className="nav-soon">›</span>
          </button>
          <button className="nav-link" onClick={showPreviewNotice} type="button">
            <Icon name="ticket" />
            <span>{text.tickets}</span>
            <span className="nav-soon">›</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-section-label">{text.account}</div>
          <button className="nav-link" onClick={showPreviewNotice} type="button">
            <Icon name="user" />
            <span>{text.profile}</span>
          </button>
        </div>
        <div className="sidebar-brand-note">Teknistä apua, selkeästi.</div>
      </aside>

      <main className="main-content" id="home">
        <header className="topbar">
          <div className="breadcrumb"><span>HelpDesk</span><span className="breadcrumb-divider">/</span>{text.home}</div>
          <div className="topbar-status"><span className="status-dot" />{text.preview}</div>
        </header>

        <div className="page-content">
          <div className="preview-notice" role="note">
            <span className="notice-indicator"><Icon name="layers" /></span>
            <div>
              <strong>{text.preview}</strong>
              <p>{text.previewDetails}</p>
            </div>
          </div>

          <section className="welcome-section" aria-labelledby="page-title">
            <div className="welcome-copy">
              <div className="eyebrow"><span className="eyebrow-line" />{text.eyebrow}</div>
              <h1 id="page-title">{text.title}</h1>
              <p>{text.subtitle}</p>
            </div>
            <div className="welcome-decoration" aria-hidden="true">
              <span className="decoration-orbit orbit-one" />
              <span className="decoration-orbit orbit-two" />
              <span className="decoration-sparkle"><Icon name="sparkle" /></span>
            </div>
          </section>

          <section className="action-card" aria-label={text.quickTitle}>
            <div className="action-icon"><Icon name="sparkle" /></div>
            <div className="action-copy">
              <span className="action-kicker">{text.quickTitle}</span>
              <h2>{text.actionTitle}</h2>
              <p>{text.actionDescription}</p>
            </div>
            <button className="button button-primary" onClick={showPreviewNotice} type="button">
              {text.startChat}
              <Icon name="arrow" />
            </button>
          </section>

          <section className="summary-section" aria-labelledby="summary-title">
            <div className="section-heading">
              <div>
                <h2 id="summary-title">{text.summary}</h2>
                <p>{text.summaryDetails}</p>
              </div>
              <button className="text-link" onClick={showPreviewNotice} type="button">
                {text.viewTickets}<Icon name="arrow" />
              </button>
            </div>

            <div className="stats-grid">
              <article className="stat-card stat-total">
                <div className="stat-topline">
                  <span className="stat-icon"><Icon name="layers" /></span>
                  <span className="stat-label">{text.total}</span>
                </div>
                <div className="stat-value">0</div>
                <p>{text.totalHint}</p>
              </article>
              <article className="stat-card stat-open">
                <div className="stat-topline">
                  <span className="stat-icon"><Icon name="circle" /></span>
                  <span className="stat-label">{text.open}</span>
                </div>
                <div className="stat-value">0</div>
                <p>{text.openHint}</p>
              </article>
              <article className="stat-card stat-closed">
                <div className="stat-topline">
                  <span className="stat-icon"><Icon name="check" /></span>
                  <span className="stat-label">{text.closed}</span>
                </div>
                <div className="stat-value">0</div>
                <p>{text.closedHint}</p>
              </article>
            </div>
          </section>

          <div aria-live="polite" className="action-feedback">
            {notice && <span>{notice}</span>}
          </div>

          <footer className="page-footer">{text.footer}</footer>
        </div>
      </main>
    </div>
  )
}

export default App
