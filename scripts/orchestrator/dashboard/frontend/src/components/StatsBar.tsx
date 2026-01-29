// Autopilot Dashboard Stats Bar
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

import { DollarSign, Zap, CheckCircle, Activity } from 'lucide-react';

interface Stats {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_cost: number;
  total_tokens: number;
  avg_cost_per_project: number;
}

export function StatsBar({ stats }: { stats: Stats }) {
  const formatTokens = (tokens: number) => {
    if (tokens >= 1_000_000) return `${(tokens / 1_000_000).toFixed(1)}M`;
    if (tokens >= 1_000) return `${(tokens / 1_000).toFixed(1)}K`;
    return tokens.toString();
  };

  return (
    <div className="border-b border-gray-800 bg-gray-900/30">
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="grid grid-cols-4 gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-500/10 rounded-lg">
              <Zap className="w-5 h-5 text-primary-500" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Projects</p>
              <p className="text-lg font-semibold">{stats.total_projects}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-500/10 rounded-lg">
              <Activity className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Active</p>
              <p className="text-lg font-semibold">{stats.active_projects}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <CheckCircle className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Completed</p>
              <p className="text-lg font-semibold">{stats.completed_projects}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2 bg-yellow-500/10 rounded-lg">
              <DollarSign className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Cost</p>
              <p className="text-lg font-semibold">${stats.total_cost.toFixed(2)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
