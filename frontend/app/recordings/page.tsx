import React from "react";
import Link from "next/link";
import { ArrowLeft, Globe, ShieldCheck } from "lucide-react";

export default function CassettesPage() {
  const cassettes = [
    {
      method: "GET",
      url: "https://api.stripe.com/v1/customers",
      status: 200,
      sanitized: true,
      lastReplayed: "3 mins ago",
    },
    {
      method: "POST",
      url: "https://api.github.com/repos/owner/repo/pulls",
      status: 201,
      sanitized: true,
      lastReplayed: "8 mins ago",
    },
    {
      method: "GET",
      url: "https://api.sendgrid.com/v3/mail/send",
      status: 202,
      sanitized: true,
      lastReplayed: "14 mins ago",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="p-2 bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-lg text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white">HTTP Recorded Cassettes</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Deterministic offline mock recordings with automatic credential sanitization.
            </p>
          </div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="space-y-3">
          {cassettes.map((c, i) => (
            <div
              key={i}
              className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <span className="px-2 py-0.5 rounded bg-slate-800 font-bold text-amber-400">
                  {c.method}
                </span>
                <span className="text-slate-200">{c.url}</span>
              </div>

              <div className="flex items-center gap-4 text-slate-500">
                <span className="text-emerald-400 font-bold">Status: {c.status}</span>
                <span className="flex items-center gap-1 text-slate-400">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Sanitized</span>
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
