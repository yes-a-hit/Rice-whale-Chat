import { createRoot } from 'react-dom/client'
import { App } from './app/App.js'
import { setupAppearance } from './app/skins.js'
import { setupTheme } from './app/theme.js'
import { ensureKatex } from './services/markdown/katex.js'
import './app/theme.css'
import './app/themes/themes.css'
import './app/global.css'

ensureKatex()
setupTheme()
setupAppearance()

createRoot(document.getElementById('root') as HTMLElement).render(<App />)
