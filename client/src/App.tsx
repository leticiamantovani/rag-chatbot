import { useCallback, useState } from "react"
import { ChatInput } from "./components/ChatInput"
import { MessageList } from "./components/MessageList"
import { PdfDropzone } from "./components/PdfDropzone"
import { useChat } from "./hooks/useChat"
import type { Message } from "./types"
import "./index.css"

const DEFAULT_COLLECTION = "default"

export default function App() {
  const [collectionName] = useState(DEFAULT_COLLECTION)
  const { messages, loading, sendMessage } = useChat(collectionName)
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
        <span className="app__collection">Collection: {collectionName}</span>
      </header>

      <PdfDropzone collectionName={collectionName} onUploadSuccess={handleUploadSuccess} />

      <main className="app__chat">
        <MessageList messages={allMessages} />
        <ChatInput onSend={sendMessage} disabled={loading} />
      </main>
    </div>
  )
}
