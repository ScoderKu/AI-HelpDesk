import { useState, type FormEvent } from 'react'
import { API_BASE_URL } from '../api'
import { LanguageSwitch } from '../components/LanguageSwitch'
import type { Language } from '../types'
import type { Copy } from '../i18n/copy'

type Props = {
  language: Language
  text: Copy
  onLanguageChange: (language: Language) => string
  onCompleted: () => void
}

export function ForcedPasswordChange({ language, text, onLanguageChange, onCompleted }: Props) {
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

  return <main className="auth-shell">
    <header className="auth-topbar"><span className="brand-name">AI <strong>HelpDesk</strong></span><LanguageSwitch language={language} label={text.language} onChange={onLanguageChange} /></header>
    <section className="auth-content">
      <div className="auth-card">
        <h1>{text.forcedPasswordTitle}</h1>
        <p>{text.forcedPasswordDescription}</p>
        <form className="profile-panel" onSubmit={(event) => void submit(event)}>
          <label className="profile-field">{text.currentPassword}<input type="password" autoComplete="current-password" required maxLength={128} value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} /></label>
          <label className="profile-field">{text.newPassword}<input type="password" autoComplete="new-password" required minLength={8} maxLength={128} value={newPassword} onChange={e => setNewPassword(e.target.value)} /></label>
          <label className="profile-field">{text.confirmNewPassword}<input type="password" autoComplete="new-password" required minLength={8} maxLength={128} value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} /></label>
          {error && <p role="alert" className="profile-message">{error}</p>}
          <button className="button button-primary" type="submit" disabled={busy}>{busy ? text.registerSubmitting : text.passwordChangeSubmit}</button>
        </form>
      </div>
    </section>
  </main>
}
