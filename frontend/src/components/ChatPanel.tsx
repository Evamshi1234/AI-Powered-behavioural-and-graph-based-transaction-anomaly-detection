import { useEffect, useRef, useState } from "react";
import { api, type Conversation, type Message, type Profile } from "../api/client";

type Props = {
  profile: Profile;
};

const STARTERS = [
  "What lifestyle changes help my conditions?",
  "How can I improve medication adherence?",
  "Suggest a safe weekly exercise plan.",
  "What preventive screenings should I discuss with my doctor?",
];

export default function ChatPanel({ profile }: Props) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [meta, setMeta] = useState<{ provider?: string; rag?: string[]; flags?: string[] }>({});
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.listConversations(profile.id).then(setConversations).catch(console.error);
  }, [profile.id]);

  useEffect(() => {
    if (!activeConversationId) {
      setMessages([]);
      return;
    }
    api.listMessages(activeConversationId).then(setMessages).catch(console.error);
  }, [activeConversationId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = async (text: string) => {
    if (!text.trim() || loading) return;
    setLoading(true);
    setInput("");
    const optimistic: Message = {
      id: Date.now(),
      role: "user",
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimistic]);

    try {
      const result = await api.sendMessage({
        profile_id: profile.id,
        conversation_id: activeConversationId ?? undefined,
        message: text,
      });
      setActiveConversationId(result.conversation_id);
      setMeta({ provider: result.provider, rag: result.rag_sources, flags: result.safety_flags });
      const updated = await api.listMessages(result.conversation_id);
      setMessages(updated);
      const convs = await api.listConversations(profile.id);
      setConversations(convs);
    } catch (err) {
      console.error(err);
      setMessages((prev) => prev.filter((m) => m.id !== optimistic.id));
      setInput(text);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full min-h-[70vh]">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h2 className="text-xl font-semibold">AI Health Assistant</h2>
          <p className="text-sm text-slate-400">Personalized for {profile.name}</p>
        </div>
        <button
          onClick={() => {
            setActiveConversationId(null);
            setMessages([]);
            setMeta({});
          }}
          className="text-sm px-3 py-1 rounded-lg border border-slate-700 hover:border-brand-500"
        >
          New chat
        </button>
      </div>

      {conversations.length > 0 && (
        <div className="flex gap-2 overflow-x-auto pb-2 mb-2">
          {conversations.map((c) => (
            <button
              key={c.id}
              onClick={() => setActiveConversationId(c.id)}
              className={`text-xs whitespace-nowrap px-3 py-1 rounded-full border ${
                activeConversationId === c.id
                  ? "border-brand-500 bg-brand-600/20"
                  : "border-slate-700"
              }`}
            >
              {c.title}
            </button>
          ))}
        </div>
      )}

      <div className="flex-1 overflow-y-auto rounded-xl border border-slate-800 bg-slate-900/60 p-4 space-y-3">
        {messages.length === 0 && (
          <div className="text-slate-400 text-sm space-y-3">
            <p>Ask about nutrition, exercise, medications, or preventive care.</p>
            <div className="flex flex-wrap gap-2">
              {STARTERS.map((s) => (
                <button
                  key={s}
                  onClick={() => send(s)}
                  className="text-left text-xs px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m) => (
          <div
            key={m.id}
            className={`max-w-[90%] rounded-xl px-3 py-2 text-sm whitespace-pre-wrap ${
              m.role === "user"
                ? "ml-auto bg-brand-600/30 border border-brand-600/40"
                : "bg-slate-800 border border-slate-700"
            }`}
          >
            {m.content}
          </div>
        ))}
        {loading && <p className="text-xs text-slate-500 animate-pulse">Assistant is thinking...</p>}
        <div ref={bottomRef} />
      </div>

      {(meta.provider || meta.rag?.length || meta.flags?.length) && (
        <p className="text-xs text-slate-500 mt-2">
          Provider: {meta.provider}
          {meta.rag?.length ? ` · Sources: ${meta.rag.join(", ")}` : ""}
          {meta.flags?.length ? ` · Safety: ${meta.flags.join(", ")}` : ""}
        </p>
      )}

      <form
        className="mt-3 flex gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          send(input);
        }}
      >
        <input
          className="flex-1 rounded-lg bg-slate-900 border border-slate-700 px-3 py-2"
          placeholder="Type your health question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-brand-600 hover:bg-brand-500 px-4 py-2 font-medium disabled:opacity-50"
        >
          Send
        </button>
      </form>
      <p className="text-[11px] text-slate-500 mt-2">
        Not medical advice. For emergencies, call your local emergency number.
      </p>
    </div>
  );
}
