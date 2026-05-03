import { useCallback, useRef, useState } from "react"
import { streamChat } from "../services/api"
import type { Message } from "../types"

function randomId() {
  return Math.random().toString(36).slice(2)
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const abortRef = useRef<AbortController | null>(null)

  const sendMessage = useCallback(
    async (question: string) => {
      abortRef.current?.abort()
      const controller = new AbortController()
      abortRef.current = controller

      const userMsg: Message = { id: randomId(), role: "user", content: question }
      const assistantId = randomId()
      const assistantMsg: Message = { id: assistantId, role: "assistant", content: "", streaming: true }

      setMessages((prev) => [...prev, userMsg, assistantMsg])
      setLoading(true)

      try {
        await streamChat(
          question,
          conversationId,
          (chunk) => {
            setMessages((prev) =>
              prev.map((m) => (m.id === assistantId ? { ...m, content: m.content + chunk } : m))
            )
          },
          (newConversationId) => {
            setConversationId(newConversationId)
            setMessages((prev) =>
              prev.map((m) => (m.id === assistantId ? { ...m, streaming: false } : m))
            )
          },
          controller.signal
        )
      } finally {
        setLoading(false)
      }
    },
    [conversationId]
  )

  return { messages, conversationId, loading, sendMessage }
}
