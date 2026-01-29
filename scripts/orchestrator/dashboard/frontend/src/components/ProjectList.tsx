// Autopilot Dashboard Project List
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

import { formatDistanceToNow } from 'date-fns';
import { Folder, Play, Pause, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import clsx from 'clsx';

interface Project {
  id: string;
  name: string;
  path: string;
  task: string;
  status: string;
  created_at: string;
  updated_at: string;
  completed_tasks: number;
  cost?: {
    total_cost: number;
    remaining_budget: number;
    threshold_level: string;
  };
}

interface ProjectListProps {
  projects: Project[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onRefresh: () => void;
}

const statusConfig: Record<string, { icon: typeof Play; color: string; label: string }> = {
  idle: { icon: Pause, color: 'text-gray-400', label: 'Idle' },
  running: { icon: Play, color: 'text-green-500', label: 'Running' },
  paused: { icon: Pause, color: 'text-yellow-500', label: 'Paused' },
  completed: { icon: CheckCircle, color: 'text-blue-500', label: 'Completed' },
  error: { icon: AlertCircle, color: 'text-red-500', label: 'Error' },
};

export function ProjectList({ projects, selectedId, onSelect, onRefresh }: ProjectListProps) {
  return (
    <div className="border border-gray-800 rounded-lg bg-gray-900/30 h-full">
      <div className="p-4 border-b border-gray-800 flex items-center justify-between">
        <h2 className="font-semibold">Projects</h2>
        <button
          onClick={onRefresh}
          className="p-1.5 hover:bg-gray-800 rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4 text-gray-400" />
        </button>
      </div>

      <div className="divide-y divide-gray-800 max-h-[600px] overflow-y-auto custom-scrollbar">
        {projects.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <Folder className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No projects yet</p>
            <p className="text-sm">Create a new project to get started</p>
          </div>
        ) : (
          projects.map((project) => {
            const status = statusConfig[project.status] || statusConfig.idle;
            const StatusIcon = status.icon;

            return (
              <button
                key={project.id}
                onClick={() => onSelect(project.id)}
                className={clsx(
                  'w-full p-4 text-left hover:bg-gray-800/50 transition-colors',
                  selectedId === project.id && 'bg-gray-800/70'
                )}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium truncate">{project.name}</h3>
                      <span className={clsx('flex items-center gap-1 text-xs', status.color)}>
                        <StatusIcon className="w-3 h-3" />
                        {status.label}
                      </span>
                    </div>
                    <p className="text-sm text-gray-400 truncate mt-1">{project.task}</p>
                    <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                      <span>{project.completed_tasks} tasks</span>
                      {project.cost && (
                        <span>${project.cost.total_cost.toFixed(2)}</span>
                      )}
                      <span>
                        {formatDistanceToNow(new Date(project.updated_at), { addSuffix: true })}
                      </span>
                    </div>
                  </div>
                </div>
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}
