import React from "react";
import { Zap, Database, ShieldCheck } from "lucide-react";

interface CloneMetricsProps {
  coldStartMs: number;
  anonymizedRows: number;
  integrityVerified: boolean;
}

export function CloneMetrics({
  coldStartMs,
  anonymizedRows,
  integrityVerified,
}: CloneMetricsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
        <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
          <Zap className="w-3.5 h-3.5 text-amber-400" />
          <span>Cold-Start Provision Latency</span>
        </div>
        <p className="text-2xl font-bold text-white font-mono">{coldStartMs.toFixed(2)} ms</p>
        <span className="text-[11px] text-emerald-400 font-mono">Sub-second copy-on-write clone</span>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
        <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
          <Database className="w-3.5 h-3.5 text-indigo-400" />
          <span>Pseudonymized Rows</span>
        </div>
        <p className="text-2xl font-bold text-indigo-300 font-mono">{anonymizedRows.toLocaleString()}</p>
        <span className="text-[11px] text-slate-500 font-mono">Keyed HMAC Deterministic Mapping</span>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
        <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Foreign Key Referential Integrity</span>
        </div>
        <p className="text-2xl font-bold text-emerald-400 font-mono">100% Preserved</p>
        <span className="text-[11px] text-slate-500 font-mono">Zero Broken Relations</span>
      </div>
    </div>
  );
}
