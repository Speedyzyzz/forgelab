import React from "react";
import { Terminal } from "lucide-react";

interface LiveLogTerminalProps {
  logs: string[];
}

export function LiveLogTerminal({ logs }: LiveLogTerminalProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 font-mono">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <span className="font-semibold text-slate-200 text-xs">Ephemeral Sandbox Stream</span>
        </div>
        <span className="text-[10px] text-slate-500">Live SSE</span>
      </div>

      <div className="bg-slate-950 p-4 rounded-lg text-xs space-y-1.5 max-h-64 overflow-y-auto text-slate-300">
        {logs.map((line, i) => (
          <div key={i} className="flex gap-2">
            <span className="text-slate-600 select-none">›</span>
            <span>{line}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
