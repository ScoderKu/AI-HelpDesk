import type { Language } from '../types'

export function LanguageSwitch({
  language,
  label,
  onChange,
}: {
  language: Language
  label: string
  onChange: (language: Language) => void
}) {
  return (
    <div className="language-switch" role="group" aria-label={label}>
      <button
        aria-pressed={language === 'fi'}
        className={language === 'fi' ? 'selected' : ''}
        onClick={() => onChange('fi')}
        type="button"
      >
        FI
      </button>
      <button
        aria-pressed={language === 'en'}
        className={language === 'en' ? 'selected' : ''}
        onClick={() => onChange('en')}
        type="button"
      >
        EN
      </button>
    </div>
  )
}
