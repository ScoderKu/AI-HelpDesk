import { useEffect, useRef, useState } from 'react'
import { Icon } from '../components/Icon'
import { LanguageSwitch } from '../components/LanguageSwitch'
import type { Copy } from '../i18n/copy'
import type { AuthMode, AuthenticatedUser, Language } from '../types'

type HomePageProps = {
  language: Language
  text: Copy
  notice: string
  currentUser: AuthenticatedUser | null
  authLoading: boolean
  isSigningOut: boolean
  onLanguageChange: (language: Language) => void
  onOpenAuth: (mode: AuthMode) => void
  onSignOut: () => void
  onShowPreviewNotice: () => void
}

export function HomePage({
  language,
  text,
  notice,
  currentUser,
  authLoading,
  isSigningOut,
  onLanguageChange,
  onOpenAuth,
  onSignOut,
  onShowPreviewNotice,
}: HomePageProps) {
  const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false)
  const accountMenuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!isAccountMenuOpen) return

    function handlePointerDown(event: PointerEvent) {
      if (
        event.target instanceof Node &&
        !accountMenuRef.current?.contains(event.target)
      ) {
        setIsAccountMenuOpen(false)
      }
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        setIsAccountMenuOpen(false)
      }
    }

    document.addEventListener('pointerdown', handlePointerDown)
    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('pointerdown', handlePointerDown)
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isAccountMenuOpen])

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#home" aria-label="AI HelpDesk home">
          <span className="brand-mark"><Icon name="sparkle" /></span>
          <span className="brand-name">AI <strong>HelpDesk</strong></span>
        </a>

        <div className="sidebar-language">
          <span className="language-label"><Icon name="globe" />{text.language}</span>
          <LanguageSwitch language={language} label={text.language} onChange={onLanguageChange} />
        </div>

        <div className="sidebar-section-label">{text.workspace}</div>
        <nav className="main-nav" aria-label={text.workspace}>
          <a className="nav-link active" href="#home" aria-current="page">
            <Icon name="home" />
            <span>{text.home}</span>
          </a>
          <button className="nav-link" onClick={onShowPreviewNotice} type="button">
            <Icon name="message" />
            <span>{text.chat}</span>
            <span className="nav-soon">›</span>
          </button>
          <button className="nav-link" onClick={onShowPreviewNotice} type="button">
            <Icon name="ticket" />
            <span>{text.tickets}</span>
            <span className="nav-soon">›</span>
          </button>
        </nav>

        {currentUser && (
          <div className="sidebar-bottom">
            <div className="account-menu" ref={accountMenuRef}>
              {isAccountMenuOpen && (
                <div className="account-menu-panel" id="account-menu-panel">
                  <button
                    className="account-menu-item"
                    onClick={() => {
                      setIsAccountMenuOpen(false)
                      onShowPreviewNotice()
                    }}
                    type="button"
                  >
                    <Icon name="user" />
                    <span>{text.profile}</span>
                  </button>
                  <button
                    className="account-menu-item"
                    disabled={isSigningOut}
                    onClick={() => {
                      setIsAccountMenuOpen(false)
                      onSignOut()
                    }}
                    type="button"
                  >
                    <Icon name="logout" />
                    <span>{isSigningOut ? text.signingOut : text.signOut}</span>
                  </button>
                </div>
              )}
              <button
                aria-controls="account-menu-panel"
                aria-expanded={isAccountMenuOpen}
                aria-haspopup="menu"
                className="account-trigger"
                onClick={() => setIsAccountMenuOpen((open) => !open)}
                type="button"
              >
                <span className="account-avatar" aria-hidden="true">
                  <Icon name="user" />
                </span>
                <span className="account-identity">
                  <span className="account-name">{currentUser.first_name} {currentUser.last_name}</span>
                  <span className="account-email">{currentUser.email}</span>
                </span>
                <span className="account-chevron" aria-hidden="true">⌃</span>
              </button>
            </div>
          </div>
        )}
      </aside>

      <main className="main-content" id="home">
        <header className="topbar">
          <div className="breadcrumb"><span>HelpDesk</span><span className="breadcrumb-divider">/</span>{text.home}</div>
          <div className="topbar-actions">
            <div className="topbar-status"><span className="status-dot" />{text.preview}</div>
            {currentUser ? (
              <span className="signed-in-user" title={currentUser.email}>
                {text.signedInAs} {currentUser.username}
              </span>
            ) : authLoading ? (
              <span className="topbar-auth-loading">{text.checkingSession}</span>
            ) : (
              <>
                <button className="topbar-auth-link" onClick={() => onOpenAuth('login')} type="button">{text.signIn}</button>
                <button className="topbar-auth-link topbar-auth-primary" onClick={() => onOpenAuth('register')} type="button">{text.createAccount}</button>
              </>
            )}
          </div>
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
            <button className="button button-primary" onClick={onShowPreviewNotice} type="button">
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
              <button className="text-link" onClick={onShowPreviewNotice} type="button">
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

          <div aria-live="polite" className="action-feedback" role="status">
            {notice && <span>{notice}</span>}
          </div>

          <footer className="page-footer">{text.footer}</footer>
          <div className="lab-signature">Developed by ScoderKu Lab</div>
        </div>
      </main>
    </div>
  )
}
