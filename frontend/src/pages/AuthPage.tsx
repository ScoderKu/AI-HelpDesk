import { useState, type FormEvent } from 'react'
import { Icon } from '../components/Icon'
import { LanguageSwitch } from '../components/LanguageSwitch'
import type { Copy } from '../i18n/copy'
import type { AuthMode, Language } from '../types'

type AuthPageProps = {
  mode: AuthMode
  language: Language
  text: Copy
  onLanguageChange: (language: Language) => string
  onModeChange: (mode: AuthMode) => void
  onBack: () => void
}

export function AuthPage({
  mode,
  language,
  text,
  onLanguageChange,
  onModeChange,
  onBack,
}: AuthPageProps) {
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [notice, setNotice] = useState('')
  const isRegister = mode === 'register'

  const updateField = (field: string) => {
    setErrors((current) => {
      if (!current[field]) return current
      const next = { ...current }
      delete next[field]
      return next
    })
    setNotice('')
  }

  const submitForm = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    const values = Object.fromEntries(
      Array.from(formData.entries(), ([key, value]) => [
        key,
        key === 'password' ? String(value) : String(value).trim(),
      ]),
    )
    const nextErrors: Record<string, string> = {}
    const requiredFields = isRegister
      ? ['firstName', 'lastName', 'username', 'email', 'password']
      : ['email', 'password']

    requiredFields.forEach((field) => {
      if (!values[field]) nextErrors[field] = text.requiredError
    })
    if (values.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
      nextErrors.email = text.emailError
    }
    if (values.password && values.password.length < 8) {
      nextErrors.password = text.passwordError
    }
    if (isRegister && values.username && values.username.length < 3) {
      nextErrors.username = text.usernameError
    }

    setErrors(nextErrors)
    setNotice(Object.keys(nextErrors).length === 0 ? text.authUnavailable : '')
  }

  const fieldError = (name: string) => errors[name]
  const changeAuthLanguage = (nextLanguage: Language) => {
    setErrors({})
    setNotice(onLanguageChange(nextLanguage))
  }

  return (
    <div className="auth-shell">
      <header className="auth-topbar">
        <a
          className="brand"
          href="#home"
          onClick={(event) => {
            event.preventDefault()
            onBack()
          }}
        >
          <span className="brand-mark"><Icon name="sparkle" /></span>
          <span className="brand-name">AI <strong>HelpDesk</strong></span>
        </a>
        <div className="auth-toolbar">
          <button className="auth-back" onClick={onBack} type="button">{text.backToHome}</button>
          <LanguageSwitch language={language} label={text.language} onChange={changeAuthLanguage} />
        </div>
      </header>

      <main className="auth-content">
        <section className="auth-card" aria-labelledby="auth-title">
          <div className="auth-heading">
            <span className="auth-icon"><Icon name={isRegister ? 'user' : 'sparkle'} /></span>
            <div className="eyebrow"><span className="eyebrow-line" />AI HELP DESK</div>
            <h1 id="auth-title">{isRegister ? text.registerTitle : text.loginTitle}</h1>
            <p>{isRegister ? text.registerDescription : text.loginDescription}</p>
          </div>

          <form className="auth-form" noValidate onSubmit={submitForm}>
            {isRegister && (
              <div className="auth-name-grid">
                <label className="auth-field">
                  <span>{text.firstName}</span>
                  <input
                    autoComplete="given-name"
                    aria-describedby={fieldError('firstName') ? 'firstName-error' : undefined}
                    aria-invalid={Boolean(fieldError('firstName'))}
                    name="firstName"
                    onChange={() => updateField('firstName')}
                    required
                  />
                  {fieldError('firstName') && <span className="field-error" id="firstName-error">{fieldError('firstName')}</span>}
                </label>
                <label className="auth-field">
                  <span>{text.lastName}</span>
                  <input
                    autoComplete="family-name"
                    aria-describedby={fieldError('lastName') ? 'lastName-error' : undefined}
                    aria-invalid={Boolean(fieldError('lastName'))}
                    name="lastName"
                    onChange={() => updateField('lastName')}
                    required
                  />
                  {fieldError('lastName') && <span className="field-error" id="lastName-error">{fieldError('lastName')}</span>}
                </label>
              </div>
            )}

            {isRegister && (
              <label className="auth-field">
                <span>{text.username}</span>
                <input
                  autoComplete="username"
                  aria-describedby={fieldError('username') ? 'username-error' : undefined}
                  aria-invalid={Boolean(fieldError('username'))}
                  name="username"
                  onChange={() => updateField('username')}
                  required
                />
                {fieldError('username') && <span className="field-error" id="username-error">{fieldError('username')}</span>}
              </label>
            )}

            <label className="auth-field">
              <span>{text.email}</span>
              <input
                autoComplete="email"
                aria-describedby={fieldError('email') ? 'email-error' : undefined}
                aria-invalid={Boolean(fieldError('email'))}
                name="email"
                onChange={() => updateField('email')}
                required
                type="email"
              />
              {fieldError('email') && <span className="field-error" id="email-error">{fieldError('email')}</span>}
            </label>

            <label className="auth-field">
              <span>{text.password}</span>
              <input
                autoComplete={isRegister ? 'new-password' : 'current-password'}
                aria-describedby={[
                  isRegister ? 'password-hint' : '',
                  fieldError('password') ? 'password-error' : '',
                ].filter(Boolean).join(' ') || undefined}
                aria-invalid={Boolean(fieldError('password'))}
                minLength={8}
                name="password"
                onChange={() => updateField('password')}
                required
                type="password"
              />
              {isRegister && <span className="field-hint" id="password-hint">{text.passwordHint}</span>}
              {fieldError('password') && <span className="field-error" id="password-error">{fieldError('password')}</span>}
            </label>

            <button className="button button-primary auth-submit" type="submit">
              {isRegister ? text.registerSubmit : text.loginSubmit}
              <Icon name="arrow" />
            </button>
            <p className="auth-switch">
              {isRegister ? text.hasAccount : text.noAccount}{' '}
              <button onClick={() => onModeChange(isRegister ? 'login' : 'register')} type="button">
                {isRegister ? text.signIn : text.createAccount}
              </button>
            </p>
            {notice && <p className="auth-notice" role="alert">{notice}</p>}
          </form>
        </section>
        <div className="lab-signature">Developed by ScoderKu Lab</div>
      </main>
    </div>
  )
}
