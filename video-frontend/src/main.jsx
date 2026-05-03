import { StrictMode } from 'react'
import { ClerkProvider } from '@clerk/clerk-react'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import { createRoot } from 'react-dom/client'
import './index.css'

const PUBLISHABLE_KEY = "pk_test_YWRlcXVhdGUtZmluY2gtOC5jbGVyay5hY2NvdW50cy5kZXYk"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <App />
    </ClerkProvider>
  </StrictMode>,
)
