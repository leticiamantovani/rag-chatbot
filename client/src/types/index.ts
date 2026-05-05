export interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  streaming?: boolean
}

export interface Conversation {
  id: string
  title: string | null
  created_at: string
}
