export interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  streaming?: boolean
}

export interface ChatState {
  messages: Message[]
  conversationId: string | null
  collectionName: string
}
