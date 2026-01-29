// Autopilot Dashboard Cost Chart
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { DollarSign, Cpu, Zap } from 'lucide-react';

interface CostData {
  total_cost: number;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  api_calls: number;
  threshold_level: string;
  remaining_budget: number;
  cost_by_model: Record<string, number>;
}

const COLORS = ['#0ea5e9', '#8b5cf6', '#f59e0b', '#10b981'];

const thresholdColors: Record<string, string> = {
  ok: 'text-green-500',
  warning: 'text-yellow-500',
  alert: 'text-orange-500',
  stop: 'text-red-500',
};

export function CostChart({ cost }: { cost: CostData }) {
  const modelData = Object.entries(cost.cost_by_model).map(([model, value]) => ({
    // Model names are now short (haiku, sonnet, opus) - capitalize for display
    name: model.charAt(0).toUpperCase() + model.slice(1),
    value: Number(value.toFixed(4)),
  }));

  const tokenData = [
    { name: 'Input', value: cost.input_tokens },
    { name: 'Output', value: cost.output_tokens },
  ];

  const budgetUsed = cost.total_cost;
  const budgetTotal = cost.total_cost + cost.remaining_budget;
  const budgetPercentage = (budgetUsed / budgetTotal) * 100;

  const formatTokens = (value: number) => {
    if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
    if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
    return value.toString();
  };

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-gray-800/50 rounded-lg">
          <div className="flex items-center gap-2 text-gray-400 mb-2">
            <DollarSign className="w-4 h-4" />
            <span className="text-sm">Total Cost</span>
          </div>
          <p className="text-2xl font-semibold">${cost.total_cost.toFixed(2)}</p>
          <p className={`text-sm ${thresholdColors[cost.threshold_level]}`}>
            {cost.threshold_level.toUpperCase()}
          </p>
        </div>

        <div className="p-4 bg-gray-800/50 rounded-lg">
          <div className="flex items-center gap-2 text-gray-400 mb-2">
            <Cpu className="w-4 h-4" />
            <span className="text-sm">Total Tokens</span>
          </div>
          <p className="text-2xl font-semibold">{formatTokens(cost.total_tokens)}</p>
          <p className="text-sm text-gray-400">{cost.api_calls} API calls</p>
        </div>

        <div className="p-4 bg-gray-800/50 rounded-lg">
          <div className="flex items-center gap-2 text-gray-400 mb-2">
            <Zap className="w-4 h-4" />
            <span className="text-sm">Budget</span>
          </div>
          <p className="text-2xl font-semibold">${cost.remaining_budget.toFixed(2)}</p>
          <p className="text-sm text-gray-400">remaining</p>
        </div>
      </div>

      {/* Budget Progress */}
      <div className="p-4 bg-gray-800/50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Budget Usage</span>
          <span className="text-sm">{budgetPercentage.toFixed(1)}%</span>
        </div>
        <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all ${
              budgetPercentage > 80
                ? 'bg-red-500'
                : budgetPercentage > 50
                ? 'bg-yellow-500'
                : 'bg-green-500'
            }`}
            style={{ width: `${Math.min(budgetPercentage, 100)}%` }}
          />
        </div>
        <div className="flex justify-between mt-1 text-xs text-gray-500">
          <span>$0</span>
          <span>${budgetTotal.toFixed(2)}</span>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-2 gap-4">
        {/* Cost by Model */}
        <div className="p-4 bg-gray-800/50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-400 mb-4">Cost by Model</h3>
          {modelData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={modelData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={70}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, value }) => `${name}: $${value}`}
                  labelLine={false}
                >
                  {modelData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value: number) => [`$${value.toFixed(4)}`, 'Cost']}
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[200px] flex items-center justify-center text-gray-500">
              No model data
            </div>
          )}
        </div>

        {/* Tokens Breakdown */}
        <div className="p-4 bg-gray-800/50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-400 mb-4">Token Usage</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={tokenData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis type="number" tickFormatter={formatTokens} stroke="#9ca3af" />
              <YAxis type="category" dataKey="name" width={60} stroke="#9ca3af" />
              <Tooltip
                formatter={(value: number) => [formatTokens(value), 'Tokens']}
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="value" fill="#0ea5e9" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Breakdown */}
      <div className="p-4 bg-gray-800/50 rounded-lg">
        <h3 className="text-sm font-medium text-gray-400 mb-4">Detailed Breakdown</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-400">Input tokens</span>
            <span>{formatTokens(cost.input_tokens)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Output tokens</span>
            <span>{formatTokens(cost.output_tokens)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">API calls</span>
            <span>{cost.api_calls}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Avg tokens/call</span>
            <span>{cost.api_calls > 0 ? formatTokens(Math.round(cost.total_tokens / cost.api_calls)) : '0'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Avg cost/call</span>
            <span>${cost.api_calls > 0 ? (cost.total_cost / cost.api_calls).toFixed(4) : '0'}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
