import { useEffect, useState } from 'react'
import './App.css'
import { AuthPage } from './pages/AuthPage'
import { HomePage } from './pages/HomePage'
import { API_BASE_URL } from './api'
import { copy } from './i18n/copy'
import { ForcedPasswordChange } from './pages/ForcedPasswordChange'
import type { AuthMode, AuthenticatedUser, AuthStatus, Language } from './types'

function getAuthModeFromPath(): AuthMode | null {
  const path = window.location.pathname.replace(/\/+$/, '') || '/'
  if (path === '/login') return 'login'
  if (path === '/register') return 'register'
  return null
}

function getInitialLanguage(): Language {
  try {
    return localStorage.getItem('ai-helpdesk-language') === 'en' ? 'en' : 'fi'
  } catch {
    return 'fi'
  }
}

function App() {
  const [language, setLanguage] = useState<Language>(getInitialLanguage)
  const [notice, setNotice] = useState('')
  const [authMode, setAuthMode] = useState<AuthMode | null>(getAuthModeFromPath)
  const [user, setUser] = useState<AuthenticatedUser | null>(null)
  const [mustChangePassword, setMustChangePassword] = useState(false)
  const [authLoading, setAuthLoading] = useState(true)
  const [isSigningOut, setIsSigningOut] = useState(false)
  const text = copy[language]

  const navigateAuth = (mode: AuthMode | null, replace = false) => {
    const path = mode === 'login' ? '/login' : mode === 'register' ? '/register' : '/'
    if (window.location.pathname !== path || window.location.hash) {
      window.history[replace ? 'replaceState' : 'pushState'](null, '', path)
    }
    setAuthMode(mode)
  }

  useEffect(() => {
    const syncAuthMode = () => setAuthMode(getAuthModeFromPath())
    window.addEventListener('popstate', syncAuthMode)
    return () => window.removeEventListener('popstate', syncAuthMode)
  }, [])

  useEffect(() => {
    document.documentElement.lang = language
  }, [language])

  useEffect(() => {
    let active = true

    const loadCurrentUser = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
          credentials: 'include',
        })
        if (response.status === 401) {
          if (active) { setUser(null); setMustChangePassword(false) }
          return
        }
        if (!response.ok) throw new Error(`Session check failed: ${response.status}`)
        const authStatus: AuthStatus = await response.json()
        if (active) {
          setMustChangePassword(authStatus.must_change_password)
          if (!authStatus.must_change_password) {
            const profileResponse = await fetch(`${API_BASE_URL}/api/v1/users/me`, { credentials: 'include' })
            if (!profileResponse.ok) throw new Error(`Profile load failed: ${profileResponse.status}`)
            const currentUser: AuthenticatedUser = await profileResponse.json()
            setUser(currentUser)
          } else setUser(null)
        }
      } catch {
        if (active) {
          setUser(null)
          setNotice(copy[language].sessionCheckError)
        }
      } finally {
        if (active) setAuthLoading(false)
      }
    }

    void loadCurrentUser()
    return () => {
      active = false
    }
  }, [language])

  const showPreviewNotice = () => setNotice(text.actionNotice)
  const changeLanguage = (nextLanguage: Language): string => {
    setLanguage(nextLanguage)
    try {
      localStorage.setItem('ai-helpdesk-language', nextLanguage)
      setNotice('')
      return ''
    } catch {
      const storageError = copy[nextLanguage].storageError
      setNotice(storageError)
      return storageError
    }
  }

  const handleLoginSuccess = async (authStatus: AuthStatus) => {
    setMustChangePassword(authStatus.must_change_password)
    if (authStatus.must_change_password) {
      setUser(null)
    } else {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/users/me`, { credentials: 'include' })
        if (!response.ok) throw new Error(`Profile load failed: ${response.status}`)
        setUser(await response.json())
      } catch {
        setNotice(text.sessionCheckError)
        return
      }
    }
    navigateAuth(null, true)
    setNotice('')
  }

  const handlePasswordChanged = () => {
    setUser(null)
    setMustChangePassword(false)
    navigateAuth('login')
    setNotice(text.passwordChanged)
  }

  const handleSignOut = async (): Promise<boolean> => {
    setIsSigningOut(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      })
      if (!response.ok) throw new Error(`Sign out failed: ${response.status}`)
      setUser(null)
      setNotice(text.signedOut)
      return true
    } catch {
      setNotice(text.signOutError)
      return false
    } finally {
      setIsSigningOut(false)
    }
  }

  const handleForcedPasswordSignOut = async (): Promise<boolean> => {
    const signedOut = await handleSignOut()
    if (signedOut) {
      setMustChangePassword(false)
      navigateAuth(null, true)
    }
    return signedOut
  }

  if (mustChangePassword) {
    return (
      <ForcedPasswordChange
        language={language}
        text={text}
        onLanguageChange={changeLanguage}
        onCompleted={handlePasswordChanged}
        onSignOut={handleForcedPasswordSignOut}
        isSigningOut={isSigningOut}
      />
    )
  }

  if (authMode) {
    return (
      <AuthPage
        language={language}
        mode={authMode}
        onLoginSuccess={handleLoginSuccess}
        onBack={() => navigateAuth(null)}
        onLanguageChange={changeLanguage}
        onModeChange={navigateAuth}
        text={text}
      />
    )
  }

  return (
    <HomePage
      language={language}
      notice={notice}
      authLoading={authLoading}
      currentUser={user}
      onUserUpdated={setUser}
      isSigningOut={isSigningOut}
      onLanguageChange={changeLanguage}
      onOpenAuth={navigateAuth}
      onSignOut={handleSignOut}
      onPasswordChanged={handlePasswordChanged}
      onShowPreviewNotice={showPreviewNotice}
      text={text}
    />
  )
}

export default App
