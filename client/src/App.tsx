import { useCallback, useEffect, useRef, useState } from "react"
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import { ChatInput } from "./components/ChatInput"
import { ConversationSidebar } from "./components/ConversationSidebar"
import { MessageList } from "./components/MessageList"
import { PdfDropzone } from "./components/PdfDropzone"
import { useChat } from "./hooks/useChat"
import "./index.css"
import { LoginPage } from "./pages/LoginPage"
import { isAuthenticated, listConversations, logout } from "./services/api"
import type { Conversation, Message } from "./types"

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  if (!isAuthenticated()) return <Navigate to="/login" replace />
  return <>{children}</>
}

function ChatPage() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [sidebarLoading, setSidebarLoading] = useState(false)
  const [systemMessages, setSystemMessages] = useState<Message[]>([])

  // sessionKey changes only when the user deliberately switches conversation or clicks New.
  // It never changes when the backend assigns an ID to a brand-new conversation.
  const [sessionKey, setSessionKey] = useState(() => `new-${Date.now()}`)
  const [sessionConversationId, setSessionConversationId] = useState<string | null>(null)

  const { messages, conversationId, loading, historyLoading, sendMessage } = useChat({
    sessionKey,
    conversationId: sessionConversationId,
  })

  // Track the last known backend ID so we can refresh the sidebar once after creation
  const lastConvIdRef = useRef<string | null>(null)

  const refreshConversations = useCallback(async () => {
    setSidebarLoading(true)
    try {
      const list = await listConversations()
      setConversations(list)
    } finally {
      setSidebarLoading(false)
    }
  }, [])

  useEffect(() => {
    refreshConversations()
  }, [refreshConversations])

  // Refresh sidebar when a new conversation is confirmed by the backend
  useEffect(() => {
    if (conversationId && conversationId !== lastConvIdRef.current) {
      lastConvIdRef.current = conversationId
      refreshConversations()
    }
  }, [conversationId, refreshConversations])

  const handleSelectConversation = useCallback((id: string) => {
    lastConvIdRef.current = id
    setSessionConversationId(id)
    setSessionKey(id)          // new sessionKey → useChat resets + loads history
    setSystemMessages([])
  }, [])

  const handleNewConversation = useCallback(() => {
    lastConvIdRef.current = null
    setSessionConversationId(null)
    setSessionKey(`new-${Date.now()}`)   // new sessionKey → useChat resets to empty
    setSystemMessages([])
  }, [])

  const handleUploadSuccess = useCallback((content: string) => {
    setSystemMessages((prev) => [
      ...prev,
      { id: `sys-${Date.now()}`, role: "assistant", content },
    ])
  }, [])

  const allMessages = [...systemMessages, ...messages]
  const isEmpty = allMessages.length === 0 && !historyLoading

  return (
    <div className="layout">
      <ConversationSidebar
        conversations={conversations}
        activeId={conversationId}
        onSelect={handleSelectConversation}
        onNew={handleNewConversation}
        loading={sidebarLoading}
      />

      <div className="main">
        <header className="main__header">
          <PdfDropzone onUploadSuccess={handleUploadSuccess} />
          <button className="app__logout" onClick={logout}>Logout</button>
        </header>

        <main className="app__chat">
          {historyLoading && <div className="chat__empty"><p>Loading messages...</p></div>}
          {isEmpty && <div className="chat__empty"><p>Ask anything about your documents</p></div>}
          <MessageList messages={allMessages} />
          <ChatInput onSend={sendMessage} disabled={loading || historyLoading} />
        </main>
      </div>
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
