import { useCallback, useEffect, useRef, useState } from "react"
import { getConversationMessages, streamChat } from "../services/api"
import type { Message } from "../types"

function randomId() {
  return Math.random().toString(36).slice(2)
}

interface UseChatOptions {
  // Stable key that identifies which "slot" we're in.
  // When the user picks an existing conversation or clicks "New", this changes.
  // It does NOT change when the backend assigns an ID to a brand-new conversation.
  sessionKey: string
  // The conversation ID to pre-load (null = brand-new conversation).
  conversationId: string | null
}

export function useChat({ sessionKey, conversationId }: UseChatOptions) {
  const [messages, setMessages] = useState<Message[]>([])
  const [activeConversationId, setActiveConversationId] = useState<string | null>(conversationId)
  const [loading, setLoading] = useState(false)
  const [historyLoading, setHistoryLoading] = useState(false)
  const abortRef = useRef<AbortController | null>(null)

  // Reset + optionally load history whenever the user switches session.
  useEffect(() => {
    abortRef.current?.abort()
    setMessages([])
    setActiveConversationId(conversationId)
    setLoading(false)

    if (!conversationId) return

    let cancelled = false
    setHistoryLoading(true)

    getConversationMessages(conversationId)
      .then((apiMessages) => {
        if (cancelled) return
        setMessages(
          apiMessages.map((m) => ({ id: m.id, role: m.role, content: m.content }))
        )
      })
      .catch(() => {/* silently ignore — worst case the user just sees empty */})
      .finally(() => { if (!cancelled) setHistoryLoading(false) })

    return () => { cancelled = true }
  // sessionKey is the only trigger — not conversationId directly,
  // so promoting a new-conversation ID doesn't cause a reset.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionKey])

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
          activeConversationId,
          (chunk) => {
            setMessages((prev) =>
              prev.map((m) => (m.id === assistantId ? { ...m, content: m.content + chunk } : m))
            )
          },
          (newConversationId) => {
            // Promote the backend-assigned ID without triggering a session reset
            setActiveConversationId(newConversationId)
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
    [activeConversationId]
  )

  return { messages, conversationId: activeConversationId, loading, historyLoading, sendMessage }
}
