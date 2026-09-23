import { useEffect, useState } from "react";
import type { Profile } from "../api/client";

type Props = {
  profile: Profile | null;
  onSave: (data: Omit<Profile, "id" | "created_at">) => Promise<void>;
};

const empty = {
  name: "",
  age: 30,
  gender: "prefer_not_to_say",
  conditions: "",
  medications: "",
  allergies: "",
  health_goals: "",
};

export default function ProfileForm({ profile, onSave }: Props) {
  const [form, setForm] = useState(profile ? { ...profile } : empty);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (profile) {
      setForm({ ...profile });
    } else {
      setForm(empty);
    }
  }, [profile?.id]);

  const update = (key: keyof typeof form, value: string | number) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const { id: _id, created_at: _ca, ...payload } = form as Profile & typeof empty;
      await onSave(payload);
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={submit} className="space-y-3">
      <h2 className="text-lg font-semibold text-brand-400">Patient profile</h2>
      <input
        className="w-full rounded-lg bg-slate-900 border border-slate-700 px-3 py-2"
        placeholder="Full name"
        value={form.name}
        onChange={(e) => update("name", e.target.value)}
        required
      />
      <div className="grid grid-cols-2 gap-2">
        <input
          type="number"
          min={1}
          max={120}
          className="rounded-lg bg-slate-900 border border-slate-700 px-3 py-2"
          value={form.age}
          onChange={(e) => update("age", Number(e.target.value))}
        />
        <select
          className="rounded-lg bg-slate-900 border border-slate-700 px-3 py-2"
          value={form.gender}
          onChange={(e) => update("gender", e.target.value)}
        >
          <option value="female">Female</option>
          <option value="male">Male</option>
          <option value="non_binary">Non-binary</option>
          <option value="prefer_not_to_say">Prefer not to say</option>
        </select>
      </div>
      <textarea
        className="w-full rounded-lg bg-slate-900 border border-slate-700 px-3 py-2 h-20"
        placeholder="Conditions (e.g., Type 2 diabetes, hypertension)"
        value={form.conditions}
        onChange={(e) => update("conditions", e.target.value)}
      />
      <textarea
        className="w-full rounded-lg bg-slate-900 border border-slate-700 px-3 py-2 h-20"
        placeholder="Medications"
        value={form.medications}
        onChange={(e) => update("medications", e.target.value)}
      />
      <textarea
        className="w-full rounded-lg bg-slate-900 border border-slate-700 px-3 py-2 h-16"
        placeholder="Allergies"
        value={form.allergies}
        onChange={(e) => update("allergies", e.target.value)}
      />
      <textarea
        className="w-full rounded-lg bg-slate-900 border border-slate-700 px-3 py-2 h-16"
        placeholder="Health goals"
        value={form.health_goals}
        onChange={(e) => update("health_goals", e.target.value)}
      />
      <button
        type="submit"
        disabled={saving}
        className="w-full rounded-lg bg-brand-600 hover:bg-brand-500 transition px-4 py-2 font-medium"
      >
        {saving ? "Saving..." : profile ? "Update profile" : "Create profile"}
      </button>
    </form>
  );
}
