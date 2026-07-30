"use client";

import { useState, useEffect } from "react";

interface Lead {
  id: string;
  name: string;
  phone: string;
  email: string;
  location: string;
  niche: string;
  score: number;
  quality: string;
  status: string;
  tags: string;
  notes: string;
  date_added?: string;
}

const qualityColors: Record<string, string> = {
  HOT: "bg-red-500/20 text-red-400 border-red-500/30",
  WARM: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  COLD: "bg-blue-500/20 text-blue-400 border-blue-500/30",
};

const statusColors: Record<string, string> = {
  interested: "bg-green-500/20 text-green-400",
  not_interested: "bg-red-500/20 text-red-400",
  maybe: "bg-yellow-500/20 text-yellow-400",
  follow_up: "bg-indigo-500/20 text-indigo-400",
  customer: "bg-emerald-500/20 text-emerald-400",
};

export default function Dashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<Lead | null>(null);
  const [apiBase, setApiBase] = useState(
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
  );
  const [apiKey] = useState(
    process.env.NEXT_PUBLIC_API_KEY || "changeme"
  );

  async function fetchLeads() {
    try {
      const res = await fetch(`${apiBase}/api/leads?limit=100`, {
        headers: { "X-API-KEY": apiKey },
      });
      const data = await res.json();
      if (data.success) setLeads(data.data.leads);
    } catch {
      setLeads([]);
    } finally {
      setLoading(false);
    }
  }

  async function updateStatus(leadId: string, status: string) {
    const res = await fetch(
      `${apiBase}/api/leads/${leadId}/status`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "X-API-KEY": apiKey,
        },
        body: JSON.stringify({ status }),
      }
    );
    if (res.ok) fetchLeads();
  }

  useEffect(() => {
    fetchLeads();
  }, []);

  const filtered =
    filter === "all" ? leads : leads.filter((l) => l.quality === filter);

  return (
    <div className="min-h-screen bg-black text-zinc-100">
      <header className="w-full border-b border-white/10 bg-black/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
            PropertyVala Dashboard
          </div>
          <div className="flex gap-3">
            {["all", "HOT", "WARM", "COLD"].map((q) => (
              <button
                key={q}
                onClick={() => setFilter(q)}
                className={`px-3 py-1 rounded-full text-xs font-medium border transition ${
                  filter === q
                    ? "bg-white text-black border-white"
                    : "bg-white/5 border-white/10 text-zinc-400 hover:text-white"
                }`}
              >
                {q === "all" ? "All" : q}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {loading ? (
          <div className="text-zinc-500 text-sm">Loading leads...</div>
        ) : (
          <div className="grid gap-3">
            {filtered.map((lead) => (
              <div
                key={lead.id}
                onClick={() => setSelected(selected?.id === lead.id ? null : lead)}
                className="flex items-center gap-4 p-4 bg-white/[0.03] border border-white/10 rounded-xl hover:bg-white/[0.06] cursor-pointer transition"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3">
                    <span className="font-medium text-sm truncate">
                      {lead.name}
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-medium border ${qualityColors[lead.quality] || "bg-white/10 text-zinc-400"}`}
                    >
                      {lead.quality}
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${statusColors[lead.status] || "bg-white/10 text-zinc-400"}`}
                    >
                      {lead.status}
                    </span>
                  </div>
                  <div className="flex gap-4 mt-1 text-xs text-zinc-500">
                    <span>{lead.phone}</span>
                    <span>{lead.location}</span>
                    <span>{lead.niche}</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-mono font-bold">
                    {lead.score}
                  </div>
                  <div className="text-[10px] text-zinc-500">score</div>
                </div>
              </div>
            ))}
          </div>
        )}

        {selected && (
          <div className="mt-8 bg-white/[0.03] border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold">{selected.name}</h2>
              <button
                onClick={() => setSelected(null)}
                className="text-zinc-500 hover:text-white text-sm"
              >
                Close
              </button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-black/50 rounded-lg p-4">
                <div className="text-xs text-zinc-500 mb-1">Score</div>
                <div className="text-2xl font-bold font-mono">
                  {selected.score}
                </div>
              </div>
              <div className="bg-black/50 rounded-lg p-4">
                <div className="text-xs text-zinc-500 mb-1">Quality</div>
                <div className="text-lg font-semibold">{selected.quality}</div>
              </div>
              <div className="bg-black/50 rounded-lg p-4">
                <div className="text-xs text-zinc-500 mb-1">Status</div>
                <div className="text-lg font-semibold">{selected.status}</div>
              </div>
              <div className="bg-black/50 rounded-lg p-4">
                <div className="text-xs text-zinc-500 mb-1">Location</div>
                <div className="text-lg font-semibold">{selected.location}</div>
              </div>
            </div>
            <div className="flex gap-2 flex-wrap">
              <button
                onClick={() => updateStatus(selected.id, "interested")}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition"
              >
                Interested
              </button>
              <button
                onClick={() => updateStatus(selected.id, "not_interested")}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded-lg transition"
              >
                Not Interested
              </button>
              <button
                onClick={() => updateStatus(selected.id, "maybe")}
                className="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white text-sm rounded-lg transition"
              >
                Maybe
              </button>
              <button
                onClick={() => updateStatus(selected.id, "follow_up")}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm rounded-lg transition"
              >
                Follow Up
              </button>
              <button
                onClick={() => updateStatus(selected.id, "customer")}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm rounded-lg transition"
              >
                Mark Customer
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
