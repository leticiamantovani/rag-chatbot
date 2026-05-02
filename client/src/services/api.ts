const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export async function streamChat(
  question: string,
  collectionName: string,
  conversationId: string | null,
  onChunk: (chunk: string) => void,
  onDone: (conversationId: string) => void,
  signal?: AbortSignal
): Promise<void> {
  const url = new URL(`${BASE_URL}/chat`)
  if (conversationId) url.searchParams.set("conversation_id", conversationId)

  const response = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, collection_name: collectionName }),
    signal,
  })

  if (!response.ok) throw new Error(`HTTP ${response.status}`)

  const newConversationId = response.headers.get("X-Conversation-ID") ?? conversationId ?? ""

  const reader = response.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    onChunk(decoder.decode(value, { stream: true }))
  }

  onDone(newConversationId)
}

export async function uploadPdf(file: File, collectionName: string): Promise<{ collection_name: string }> {
  const form = new FormData()
  form.append("file", file)
  form.append("collection_name", collectionName)

  const response = await fetch(`${BASE_URL}/upload`, { method: "POST", body: form })
  if (!response.ok) throw new Error(`Upload failed: HTTP ${response.status}`)
  return response.json()
}
