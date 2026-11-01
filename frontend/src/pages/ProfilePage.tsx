import { useState, type FormEvent } from 'react'
import { API_BASE_URL } from '../api'
import type { AuthenticatedUser, Language } from '../types'
import type { Copy } from '../i18n/copy'

type Props = {
  currentUser: AuthenticatedUser
  language: Language
  text: Copy
  onBackHome: () => void
  onProfileUpdated: (user: AuthenticatedUser) => void
  onPasswordChanged: () => Promise<void>
}

async function send<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: path.endsWith('/password') ? 'POST' : 'PATCH',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    const error = new Error(`Request failed: ${response.status}`)
    Object.assign(error, { status: response.status })
    throw error
  }
  return (response.status === 204 ? undefined : response.json()) as T
}

export function ProfilePage({ currentUser, text, onBackHome, onProfileUpdated, onPasswordChanged }: Props) {
  const [firstName, setFirstName] = useState(currentUser.first_name)
  const [lastName, setLastName] = useState(currentUser.last_name)
  const [username, setUsername] = useState(currentUser.username)
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmNewPassword, setConfirmNewPassword] = useState('')
  const [profileError, setProfileError] = useState('')
  const [profileNotice, setProfileNotice] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [passwordNotice, setPasswordNotice] = useState('')
  const [savingProfile, setSavingProfile] = useState(false)
  const [savingPassword, setSavingPassword] = useState(false)

  const saveProfile = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setProfileError('')
    setProfileNotice('')
    setSavingProfile(true)
    try {
      const updated = await send<AuthenticatedUser>('/api/v1/users/me', {
        first_name: firstName.trim(), last_name: lastName.trim(), username: username.trim(),
      })
      onProfileUpdated(updated)
      setProfileNotice(text.profileSaved)
    } catch (error) {
      const status = error instanceof Error && 'status' in error ? Number((error as Error & { status: number }).status) : 0
      setProfileError(status === 409 ? text.profileUsernameTaken : text.profileSaveError)
    } finally { setSavingProfile(false) }
  }

  const changePassword = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setPasswordError('')
    setPasswordNotice('')
    if (newPassword.length < 8) { setPasswordError(text.passwordMinLength); return }
    if (newPassword !== confirmNewPassword) { setPasswordError(text.passwordMismatch); return }
    setSavingPassword(true)
    try {
      await send<void>('/api/v1/users/me/password', {
        current_password: currentPassword, new_password: newPassword, confirm_new_password: confirmNewPassword,
      })
      setCurrentPassword('')
      setNewPassword('')
      setConfirmNewPassword('')
      setPasswordNotice(text.passwordChanged)
      await onPasswordChanged()
    } catch (error) {
      const status = error instanceof Error && 'status' in error ? Number((error as Error & { status: number }).status) : 0
      setPasswordError(status === 400 ? text.currentPasswordError : text.passwordChangeError)
    } finally { setSavingPassword(false) }
  }

  return <section className="tickets-page profile-page" aria-labelledby="profile-title">
    <div className="tickets-page-heading">
      <div>
        <button className="text-link ticket-home-link" onClick={onBackHome} type="button">{text.ticketBackHome}</button>
        <h1 id="profile-title">{text.profileTitle}</h1>
        <p>{text.profileDescription}</p>
      </div>
    </div>
    <form className="profile-panel" onSubmit={(event) => void saveProfile(event)}>
      <h2>{text.profileTitle}</h2>
      <div className="profile-grid">
        <label className="profile-field">{text.firstName}<input required maxLength={100} value={firstName} onChange={e => setFirstName(e.target.value)} /></label>
        <label className="profile-field">{text.lastName}<input required maxLength={100} value={lastName} onChange={e => setLastName(e.target.value)} /></label>
        <label className="profile-field">{text.username}<input required minLength={3} maxLength={100} value={username} onChange={e => setUsername(e.target.value)} /></label>
        <label className="profile-field">{text.email}<input value={currentUser.email} disabled readOnly aria-describedby="profile-email-help" /></label>
      </div>
      <p className="profile-message">{text.emailReadOnly}</p>
      {profileError && <p className="profile-message" role="alert">{profileError}</p>}
      {profileNotice && <p className="profile-message" role="status">{profileNotice}</p>}
      <div className="profile-actions"><button className="button button-primary" disabled={savingProfile} type="submit">{text.profileSave}</button></div>
    </form>
    <form className="profile-panel" onSubmit={(event) => void changePassword(event)}>
      <h2>{text.changePasswordTitle}</h2>
      <div className="profile-grid">
        <label className="profile-field">{text.currentPassword}<input type="password" autoComplete="current-password" required maxLength={128} value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} /></label>
        <label className="profile-field">{text.newPassword}<input type="password" autoComplete="new-password" required minLength={8} maxLength={128} value={newPassword} onChange={e => setNewPassword(e.target.value)} /></label>
        <label className="profile-field">{text.confirmNewPassword}<input type="password" autoComplete="new-password" required minLength={8} maxLength={128} value={confirmNewPassword} onChange={e => setConfirmNewPassword(e.target.value)} /></label>
      </div>
      {passwordError && <p className="profile-message" role="alert">{passwordError}</p>}
      {passwordNotice && <p className="profile-message" role="status">{passwordNotice}</p>}
      <div className="profile-actions"><button className="button button-primary" disabled={savingPassword} type="submit">{text.passwordChangeSubmit}</button></div>
    </form>
  </section>
}
