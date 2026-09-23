export type Profile = {
  id: number;
  name: string;
  age: number;
  gender: string;
  conditions: string;
  medications: string;
  allergies: string;
  health_goals: string;
  created_at: string;
};

export type Conversation = {
  id: number;
  profile_id: number;
  title: string;
  created_at: string;
};

export type Message = {
  id: number;
  role: string;
  content: string;
  created_at: string;
};

export type ChatResult = {
  conversation_id: number;
  reply: string;
  safety_flags: string[];
  rag_sources: string[];
  provider: string;
};

const API = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || res.statusText);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  health: () => request<{ status: string; llm_provider: string }>("/health"),
  listProfiles: () => request<Profile[]>("/profiles"),
  createProfile: (body: Omit<Profile, "id" | "created_at">) =>
    request<Profile>("/profiles", { method: "POST", body: JSON.stringify(body) }),
  updateProfile: (id: number, body: Omit<Profile, "id" | "created_at">) =>
    request<Profile>(`/profiles/${id}`, { method: "PUT", body: JSON.stringify(body) }),
  listConversations: (profileId: number) =>
    request<Conversation[]>(`/chat/conversations/${profileId}`),
  listMessages: (conversationId: number) =>
    request<Message[]>(`/chat/messages/${conversationId}`),
  sendMessage: (body: { profile_id: number; conversation_id?: number; message: string }) =>
    request<ChatResult>("/chat", { method: "POST", body: JSON.stringify(body) }),
};
