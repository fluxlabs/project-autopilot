// Autopilot Dashboard New Project Modal
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

'use client';

import { useState } from 'react';
import { X, Folder, Zap, DollarSign } from 'lucide-react';

interface NewProjectModalProps {
  onClose: () => void;
  onCreated: (project: any) => void;
}

export function NewProjectModal({ onClose, onCreated }: NewProjectModalProps) {
  const [name, setName] = useState('');
  const [path, setPath] = useState('');
  const [task, setTask] = useState('');
  const [maxCost, setMaxCost] = useState(50);
  const [model, setModel] = useState('sonnet');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          path,
          task,
          max_cost: maxCost,
          model,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Failed to create project');
      }

      const project = await res.json();
      onCreated(project);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-gray-900 border border-gray-800 rounded-lg w-full max-w-lg shadow-xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-primary-500" />
            <h2 className="text-lg font-semibold">New Project</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 hover:bg-gray-800 rounded-lg transition-colors text-gray-400"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          {error && (
            <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
              {error}
            </div>
          )}

          {/* Name */}
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1.5">
              Project Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="my-awesome-project"
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-primary-500 text-white placeholder-gray-500"
              required
            />
          </div>

          {/* Path */}
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1.5">
              <div className="flex items-center gap-1.5">
                <Folder className="w-4 h-4" />
                Project Path
              </div>
            </label>
            <input
              type="text"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              placeholder="/path/to/your/project"
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-primary-500 text-white placeholder-gray-500 font-mono text-sm"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Absolute path to the project directory
            </p>
          </div>

          {/* Task */}
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1.5">
              Task Description
            </label>
            <textarea
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="Build a REST API with user authentication, database integration, and comprehensive tests"
              rows={3}
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-primary-500 text-white placeholder-gray-500 resize-none"
              required
            />
          </div>

          {/* Model & Budget */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1.5">
                Model
              </label>
              <select
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-primary-500 text-white"
              >
                <option value="haiku">Haiku ($1/1M)</option>
                <option value="sonnet">Sonnet ($3/1M)</option>
                <option value="opus">Opus ($5/1M)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1.5">
                <div className="flex items-center gap-1.5">
                  <DollarSign className="w-4 h-4" />
                  Max Budget
                </div>
              </label>
              <input
                type="number"
                value={maxCost}
                onChange={(e) => setMaxCost(Number(e.target.value))}
                min={1}
                max={1000}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-primary-500 text-white"
              />
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-500 disabled:bg-primary-600/50 rounded-lg transition-colors"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4" />
                  Create Project
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
