import { useState, type FormEvent } from 'react'
import { API_BASE_URL } from '../api'
import { Icon } from '../components/Icon'
import { LanguageSwitch } from '../components/LanguageSwitch'
import type { Language } from '../types'
import type { Copy } from '../i18n/copy'

type Props = {
  language: Language
  text: Copy
  onLanguageChange: (language: Language) => string
  onCompleted: () => void
  onSignOut: () => Promise<void>
  isSigningOut: boolean
}

export function ForcedPasswordChange({
  language,
  text,
  onLanguageChange,
  onCompleted,
  onSignOut,
  isSigningOut,
}: Props) {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')
    if (newPassword.length < 8) { setError(text.passwordMinLength); return }
    if (newPassword !== confirmPassword) { setError(text.passwordMismatch); return }
    setBusy(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/users/me/password`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
          confirm_new_password: confirmPassword,
        }),
      })
      if (!response.ok) {
        setError(response.status === 400 ? text.currentPasswordError : text.passwordChangeError)
        return
      }
      onCompleted()
    } catch {
      setError(text.passwordChangeError)
    } finally { setBusy(false) }
  }

  return (
    <main className="auth-shell forced-password-shell">
      <header className="auth-topbar">
        <div className="brand" aria-label="AI HelpDesk">
          <span className="brand-mark"><Icon name="sparkle" /></span>
          <span className="brand-name">AI <strong>HelpDesk</strong></span>
        </div>
        <div className="auth-toolbar">
          <span className="forced-password-badge"><span />{text.forcedPasswordBadge}</span>
          <LanguageSwitch language={language} label={text.language} onChange={onLanguageChange} />
        </div>
      </header>

      <section className="forced-password-content">
        <div className="forced-password-card">
          <aside className="forced-password-aside">
            <div className="forced-password-art" aria-hidden="true">
              <span className="forced-password-orbit forced-password-orbit-one" />
              <span className="forced-password-orbit forced-password-orbit-two" />
              <span className="forced-password-lock">
                <svg viewBox="0 0 48 48" fill="none">
                  <path d="M15 21v-6a9 9 0 0 1 18 0v6" />
                  <rect x="10" y="21" width="28" height="21" rx="5" />
                  <circle cx="24" cy="31" r="2" />
                  <path d="M24 33v4" />
                </svg>
              </span>
              <span className="forced-password-spark forced-password-spark-one">✦</span>
              <span className="forced-password-spark forced-password-spark-two">✧</span>
            </div>

            <div className="forced-password-aside-copy">
              <span className="forced-password-kicker">{text.forcedPasswordBadge}</span>
              <h2>{text.forcedPasswordSecurityTitle}</h2>
              <p>{text.forcedPasswordSecurityDescription}</p>
            </div>

            <ol className="forced-password-steps">
              <li className="complete">
                <span className="forced-password-step-icon"><Icon name="check" /></span>
                <span>{text.forcedPasswordStepComplete}</span>
              </li>
              <li className="current" aria-current="step">
                <span className="forced-password-step-icon">2</span>
                <span>{text.forcedPasswordStepCurrent}</span>
              </li>
            </ol>

            <div className="forced-password-tip">
              <span className="forced-password-tip-icon"><Icon name="check" /></span>
              <div>
                <strong>{text.forcedPasswordTipTitle}</strong>
                <p>{text.forcedPasswordTipDescription}</p>
              </div>
            </div>
          </aside>

          <div className="forced-password-main">
            <div className="auth-heading forced-password-heading">
              <span className="auth-icon forced-password-form-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                  <rect x="4" y="10" width="16" height="11" rx="2.5" />
                  <path d="M8 10V7a4 4 0 1 1 8 0v3M12 14v3" />
                </svg>
              </span>
              <div className="eyebrow"><span className="eyebrow-line" />{text.forcedPasswordEyebrow}</div>
              <h1 id="forced-password-title">{text.forcedPasswordTitle}</h1>
              <p>{text.forcedPasswordFormDescription}</p>
            </div>

            <form
              aria-busy={busy || isSigningOut}
              aria-labelledby="forced-password-title"
              className="auth-form forced-password-form"
              onSubmit={(event) => void submit(event)}
            >
              <label className="auth-field" htmlFor="temporary-password">
                <span>{text.currentPassword}</span>
                <input
                  autoComplete="current-password"
                  id="temporary-password"
                  maxLength={128}
                  onChange={(event) => setCurrentPassword(event.target.value)}
                  required
                  type="password"
                  value={currentPassword}
                />
              </label>

              <label className="auth-field" htmlFor="new-password">
                <span>{text.newPassword}</span>
                <input
                  autoComplete="new-password"
                  id="new-password"
                  maxLength={128}
                  minLength={8}
                  onChange={(event) => setNewPassword(event.target.value)}
                  required
                  type="password"
                  value={newPassword}
                />
                <span className="field-hint">{text.forcedPasswordLengthHint}</span>
              </label>

              <label className="auth-field" htmlFor="confirm-password">
                <span>{text.confirmNewPassword}</span>
                <input
                  autoComplete="new-password"
                  id="confirm-password"
                  maxLength={128}
                  minLength={8}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  required
                  type="password"
                  value={confirmPassword}
                />
              </label>

              {error && <p className="forced-password-error" role="alert">{error}</p>}

              <button
                className="button button-primary auth-submit forced-password-submit"
                type="submit"
                disabled={busy || isSigningOut}
              >
                {busy ? text.forcedPasswordSubmitting : text.passwordChangeSubmit}
                {!busy && <span aria-hidden="true">→</span>}
              </button>
              <button
                className="button button-secondary forced-password-signout"
                type="button"
                disabled={busy || isSigningOut}
                onClick={() => void onSignOut()}
              >
                {isSigningOut ? text.signingOut : text.signOut}
              </button>
            </form>

            <p className="forced-password-footer">
              <Icon name="check" />
              <span>{text.forcedPasswordFooter}</span>
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}
