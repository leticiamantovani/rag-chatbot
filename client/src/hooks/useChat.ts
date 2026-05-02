import { useCallback, useRef, useState } from "react"
import { streamChat } from "../services/api"
import type { ChatState, Message } from "../types"

function randomId() {
  return Math.random().toString(36).slice(2)
}

export function useChat(collectionName: string) {
  const [state, setState] = useState<ChatState>({
    messages: [],
    conversationId: null,
    collectionName,
  })
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

      setState((s) => ({ ...s, messages: [...s.messages, userMsg, assistantMsg] }))
      setLoading(true)

      try {
        await streamChat(
          question,
          collectionName,
          state.conversationId,
          (chunk) => {
            setState((s) => ({
              ...s,
              messages: s.messages.map((m) =>
                m.id === assistantId ? { ...m, content: m.content + chunk } : m
              ),
            }))
          },
          (newConversationId) => {
            setState((s) => ({
              ...s,
              conversationId: newConversationId,
              messages: s.messages.map((m) =>
                m.id === assistantId ? { ...m, streaming: false } : m
              ),
            }))
          },
          controller.signal
        )
      } finally {
        setLoading(false)
      }
    },
    [collectionName, state.conversationId]
  )

  return { messages: state.messages, conversationId: state.conversationId, loading, sendMessage }
}
