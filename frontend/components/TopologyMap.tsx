import React from "react";
import { Server, Database, Globe, ArrowRight } from "lucide-react";

interface ServiceNode {
  name: string;
  type: "app" | "db" | "proxy";
  port: number;
  status: "running" | "provisioning";
}

interface TopologyMapProps {
  services: ServiceNode[];
}

export function TopologyMap({ services }: TopologyMapProps) {
  const getIcon = (type: string) => {
    switch (type) {
      case "db":
        return <Database className="w-4 h-4 text-sky-400" />;
      case "proxy":
        return <Globe className="w-4 h-4 text-purple-400" />;
      default:
        return <Server className="w-4 h-4 text-emerald-400" />;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <span className="font-semibold text-slate-200 text-sm">Isolated Ephemeral Network Topology</span>
        <span className="text-xs text-slate-500 font-mono">Watchdog Protected</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {services.map((svc) => (
          <div
            key={svc.name}
            className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono space-y-2"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {getIcon(svc.type)}
                <span className="text-slate-200 font-bold">{svc.name}</span>
              </div>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            </div>

            <div className="text-slate-500 text-[11px] flex items-center justify-between">
              <span>Port: {svc.port}</span>
              <span className="text-emerald-400 uppercase">{svc.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
