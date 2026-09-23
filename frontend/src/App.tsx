import { useEffect, useState } from "react";
import { api, type Profile } from "./api/client";
import ChatPanel from "./components/ChatPanel";
import ProfileForm from "./components/ProfileForm";

export default function App() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [activeProfile, setActiveProfile] = useState<Profile | null>(null);
  const [provider, setProvider] = useState("demo");
  const [error, setError] = useState("");

  const refresh = async () => {
    const list = await api.listProfiles();
    setProfiles(list);
    if (!activeProfile && list.length) setActiveProfile(list[0]);
    if (activeProfile) {
      const updated = list.find((p) => p.id === activeProfile.id);
      if (updated) setActiveProfile(updated);
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const h = await api.health();
        setProvider(h.llm_provider);
        setError("");
        await refresh();
      } catch {
        setError("Backend unavailable. Start the API on port 8000.");
      }
    };
    init();
  }, []);

  const saveProfile = async (data: Omit<Profile, "id" | "created_at">) => {
    if (activeProfile) {
      await api.updateProfile(activeProfile.id, data);
    } else {
      const created = await api.createProfile(data);
      setActiveProfile(created);
    }
    await refresh();
  };

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Personalized Healthcare Assistant</h1>
            <p className="text-sm text-slate-400">Generative AI · Profile-aware RAG · Safety guardrails</p>
          </div>
          <span className="text-xs px-3 py-1 rounded-full border border-slate-700">
            LLM: {provider}
          </span>
        </div>
      </header>

      {error && (
        <div className="max-w-6xl mx-auto px-4 mt-4 text-amber-300 text-sm bg-amber-900/30 border border-amber-700 rounded-lg p-3">
          {error}
        </div>
      )}

      <main className="max-w-6xl mx-auto px-4 py-6 grid lg:grid-cols-[340px_1fr] gap-6">
        <aside className="space-y-4">
          <ProfileForm profile={activeProfile} onSave={saveProfile} />
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Saved patients</h3>
            <ul className="space-y-1">
              {profiles.map((p) => (
                <li key={p.id}>
                  <button
                    onClick={() => setActiveProfile(p)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm ${
                      activeProfile?.id === p.id ? "bg-brand-600/20 border border-brand-500/50" : "hover:bg-slate-800"
                    }`}
                  >
                    {p.name} · {p.age}y
                  </button>
                </li>
              ))}
            </ul>
            <button
              onClick={() => setActiveProfile(null)}
              className="mt-2 text-xs text-brand-400 hover:underline"
            >
              + New patient
            </button>
          </div>
        </aside>

        <section className="rounded-2xl border border-slate-800 bg-slate-900/40 p-4">
          {activeProfile ? (
            <ChatPanel profile={activeProfile} />
          ) : (
            <p className="text-slate-400">Create a patient profile to start a personalized chat.</p>
          )}
        </section>
      </main>
    </div>
  );
}
