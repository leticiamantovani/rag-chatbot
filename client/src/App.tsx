import { useCallback, useState } from "react"
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import { ChatInput } from "./components/ChatInput"
import { MessageList } from "./components/MessageList"
import { PdfDropzone } from "./components/PdfDropzone"
import { useChat } from "./hooks/useChat"
import "./index.css"
import { LoginPage } from "./pages/LoginPage"
import { isAuthenticated, logout } from "./services/api"
import type { Message } from "./types"

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  if (!isAuthenticated()) return <Navigate to="/login" replace />
  return <>{children}</>
}

function ChatPage() {
  const { messages, loading, sendMessage } = useChat()
  const [systemMessages, setSystemMessages] = useState<Message[]>([])

  const handleUploadSuccess = useCallback((content: string) => {
    setSystemMessages((prev) => [
      ...prev,
      { id: `sys-${Date.now()}`, role: "assistant", content },
    ])
  }, [])

  const allMessages = [...systemMessages, ...messages]

  return (
    <div className="app">
      <header className="app__header">
        <h1>RAG Chatbot</h1>
        <button className="app__logout" onClick={logout}>Logout</button>
      </header>

      <PdfDropzone onUploadSuccess={handleUploadSuccess} />

      <main className="app__chat">
        <MessageList messages={allMessages} />
        <ChatInput onSend={sendMessage} disabled={loading} />
      </main>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}
