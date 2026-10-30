import { useEffect, useState } from 'react'
import './App.css'
import { AuthPage } from './pages/AuthPage'
import { HomePage } from './pages/HomePage'
import { API_BASE_URL } from './api'
import { copy } from './i18n/copy'
import type { AuthMode, AuthenticatedUser, Language } from './types'

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
  const [authMode, setAuthMode] = useState<AuthMode | null>(null)
  const [user, setUser] = useState<AuthenticatedUser | null>(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [isSigningOut, setIsSigningOut] = useState(false)
  const text = copy[language]

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
          if (active) setUser(null)
          return
        }
        if (!response.ok) throw new Error(`Session check failed: ${response.status}`)
        const currentUser: AuthenticatedUser = await response.json()
        if (active) setUser(currentUser)
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

  const handleLoginSuccess = (authenticatedUser: AuthenticatedUser) => {
    setUser(authenticatedUser)
    setAuthMode(null)
    setNotice('')
  }

  const handleSignOut = async () => {
    setIsSigningOut(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      })
      if (!response.ok) throw new Error(`Sign out failed: ${response.status}`)
      setUser(null)
      setNotice(text.signedOut)
    } catch {
      setNotice(text.signOutError)
    } finally {
      setIsSigningOut(false)
    }
  }

  if (authMode) {
    return (
      <AuthPage
        language={language}
        mode={authMode}
        onLoginSuccess={handleLoginSuccess}
        onBack={() => setAuthMode(null)}
        onLanguageChange={changeLanguage}
        onModeChange={setAuthMode}
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
      isSigningOut={isSigningOut}
      onLanguageChange={changeLanguage}
      onOpenAuth={setAuthMode}
      onSignOut={handleSignOut}
      onShowPreviewNotice={showPreviewNotice}
      text={text}
    />
  )
}

export default App
