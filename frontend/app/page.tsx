import React from "react";
import Link from "next/link";
import { Server, ArrowRight, ShieldCheck, Database } from "lucide-react";
import { CloneMetrics } from "@/components/CloneMetrics";

export default function ForgeLabDashboard() {
  const environments = [
    {
      id: "env_eval_run_801",
      agent: "coder_agent_4",
      database_clone: "clone_prod_replica_801.db",
      services: 3,
      status: "active",
      ttl_remaining: "184s",
    },
    {
      id: "env_migration_test_902",
      agent: "patch_verifier_agent_2",
      database_clone: "clone_billing_db_902.db",
      services: 2,
      status: "active",
      ttl_remaining: "240s",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Ephemeral Test Environments</h1>
          <p className="text-sm text-slate-400 mt-1">
            Production-faithful database clones and HTTP replay stubs for autonomous agent evaluation.
          </p>
        </div>
      </div>

      <CloneMetrics coldStartMs={0.16} anonymizedRows={10000} integrityVerified={true} />

      <div className="space-y-4">
        <h2 className="text-sm font-semibold text-slate-200">Active Agent Replicas</h2>
        <div className="space-y-3">
          {environments.map((env) => (
            <div
              key={env.id}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 transition-all flex items-center justify-between group"
            >
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-sm font-bold text-slate-100">{env.id}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full font-mono bg-emerald-950 border border-emerald-800 text-emerald-400">
                    {env.status}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">
                    Watchdog TTL: <strong className="text-amber-400">{env.ttl_remaining}</strong>
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-slate-400 font-mono">
                  <span>Agent: {env.agent}</span>
                  <span>•</span>
                  <span>DB: {env.database_clone}</span>
                  <span>•</span>
                  <span>{env.services} network services provisioned</span>
                </div>
              </div>

              <div>
                <Link
                  href={`/env/${env.id}`}
                  className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
                >
                  <Server className="w-4 h-4" />
                  <span>Inspect Replica</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1 opacity-70 group-hover:translate-x-0.5 transition-transform" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
