import { useEffect, useState } from 'react'
import './App.css'
import { AuthPage } from './pages/AuthPage'
import { HomePage } from './pages/HomePage'
import { copy } from './i18n/copy'
import type { AuthMode, Language } from './types'

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
  const text = copy[language]

  useEffect(() => {
    document.documentElement.lang = language
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

  if (authMode) {
    return (
      <AuthPage
        language={language}
        mode={authMode}
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
      onLanguageChange={changeLanguage}
      onOpenAuth={setAuthMode}
      onShowPreviewNotice={showPreviewNotice}
      text={text}
    />
  )
}

export default App
