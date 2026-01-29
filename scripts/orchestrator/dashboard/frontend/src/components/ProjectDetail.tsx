// Autopilot Dashboard Project Detail
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

'use client';

import { useEffect, useState, useRef } from 'react';
import { formatDistanceToNow } from 'date-fns';
import {
  Play,
  Square,
  Trash2,
  Folder,
  Clock,
  DollarSign,
  CheckCircle,
  Terminal,
  BarChart3,
} from 'lucide-react';
import clsx from 'clsx';
import { CostChart } from './CostChart';

interface ProjectDetailData {
  id: string;
  name: string;
  path: string;
  task: string;
  status: string;
  created_at: string;
  updated_at: string;
  completed_tasks: number;
  completed_task_list: string[];
  current_phase: string | null;
  checkpoint_available: boolean;
  last_checkpoint: string | null;
  cost?: {
    total_cost: number;
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
    api_calls: number;
    threshold_level: string;
    remaining_budget: number;
    cost_by_model: Record<string, number>;
  };
}

interface OutputLine {
  type: 'output' | 'tool_start' | 'tool_end' | 'error' | 'status';
  text?: string;
  tool_name?: string;
  is_error?: boolean;
  timestamp: string;
}

interface ProjectDetailProps {
  projectId: string;
  onUpdate: () => void;
}

export function ProjectDetail({ projectId, onUpdate }: ProjectDetailProps) {
  const [project, setProject] = useState<ProjectDetailData | null>(null);
  const [output, setOutput] = useState<OutputLine[]>([]);
  const [activeTab, setActiveTab] = useState<'output' | 'tasks' | 'costs'>('output');
  const [loading, setLoading] = useState(true);
  const outputRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    fetchProject();
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [projectId]);

  useEffect(() => {
    // Auto-scroll output
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  const fetchProject = async () => {
    try {
      const res = await fetch(`/api/projects/${projectId}`);
      const data = await res.json();
      setProject(data);
    } catch (error) {
      console.error('Failed to fetch project:', error);
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${projectId}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleWSMessage(data);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
      // Reconnect after delay
      setTimeout(connectWebSocket, 3000);
    };

    wsRef.current = ws;
  };

  const handleWSMessage = (data: any) => {
    switch (data.type) {
      case 'output':
        setOutput((prev) => [...prev, { type: 'output', text: data.text, timestamp: data.timestamp }]);
        break;
      case 'tool_start':
        setOutput((prev) => [
          ...prev,
          { type: 'tool_start', tool_name: data.tool_name, timestamp: data.timestamp },
        ]);
        break;
      case 'tool_end':
        setOutput((prev) => [
          ...prev,
          {
            type: 'tool_end',
            tool_name: data.tool_name,
            text: data.result,
            is_error: data.is_error,
            timestamp: data.timestamp,
          },
        ]);
        break;
      case 'status':
        fetchProject();
        break;
      case 'complete':
        fetchProject();
        onUpdate();
        break;
      case 'error':
        setOutput((prev) => [...prev, { type: 'error', text: data.error, timestamp: data.timestamp }]);
        break;
    }
  };

  const handleStart = async () => {
    try {
      await fetch(`/api/projects/${projectId}/start`, { method: 'POST' });
      fetchProject();
    } catch (error) {
      console.error('Failed to start project:', error);
    }
  };

  const handleStop = async () => {
    try {
      await fetch(`/api/projects/${projectId}/stop`, { method: 'POST' });
      fetchProject();
    } catch (error) {
      console.error('Failed to stop project:', error);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this project?')) return;

    try {
      await fetch(`/api/projects/${projectId}`, { method: 'DELETE' });
      onUpdate();
    } catch (error) {
      console.error('Failed to delete project:', error);
    }
  };

  if (loading || !project) {
    return (
      <div className="h-full flex items-center justify-center border border-gray-800 rounded-lg bg-gray-900/30">
        <p className="text-gray-400">Loading...</p>
      </div>
    );
  }

  const isRunning = project.status === 'running';

  return (
    <div className="border border-gray-800 rounded-lg bg-gray-900/30 h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-800">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-lg font-semibold">{project.name}</h2>
            <p className="text-sm text-gray-400 mt-1">{project.task}</p>
          </div>
          <div className="flex items-center gap-2">
            {isRunning ? (
              <button
                onClick={handleStop}
                className="flex items-center gap-2 px-3 py-1.5 bg-red-600 hover:bg-red-500 rounded-lg transition-colors text-sm"
              >
                <Square className="w-4 h-4" />
                Stop
              </button>
            ) : (
              <button
                onClick={handleStart}
                className="flex items-center gap-2 px-3 py-1.5 bg-green-600 hover:bg-green-500 rounded-lg transition-colors text-sm"
              >
                <Play className="w-4 h-4" />
                {project.checkpoint_available ? 'Resume' : 'Start'}
              </button>
            )}
            <button
              onClick={handleDelete}
              className="p-1.5 hover:bg-gray-800 rounded-lg transition-colors text-gray-400 hover:text-red-500"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Meta info */}
        <div className="flex items-center gap-6 mt-4 text-sm text-gray-400">
          <div className="flex items-center gap-1.5">
            <Folder className="w-4 h-4" />
            <span className="truncate max-w-[200px]">{project.path}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Clock className="w-4 h-4" />
            <span>{formatDistanceToNow(new Date(project.updated_at), { addSuffix: true })}</span>
          </div>
          {project.cost && (
            <div className="flex items-center gap-1.5">
              <DollarSign className="w-4 h-4" />
              <span>${project.cost.total_cost.toFixed(2)} / ${project.cost.remaining_budget.toFixed(2)}</span>
            </div>
          )}
          <div className="flex items-center gap-1.5">
            <CheckCircle className="w-4 h-4" />
            <span>{project.completed_tasks} tasks</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-800">
        <button
          onClick={() => setActiveTab('output')}
          className={clsx(
            'flex items-center gap-2 px-4 py-2 text-sm border-b-2 transition-colors',
            activeTab === 'output'
              ? 'border-primary-500 text-primary-500'
              : 'border-transparent text-gray-400 hover:text-gray-200'
          )}
        >
          <Terminal className="w-4 h-4" />
          Output
        </button>
        <button
          onClick={() => setActiveTab('tasks')}
          className={clsx(
            'flex items-center gap-2 px-4 py-2 text-sm border-b-2 transition-colors',
            activeTab === 'tasks'
              ? 'border-primary-500 text-primary-500'
              : 'border-transparent text-gray-400 hover:text-gray-200'
          )}
        >
          <CheckCircle className="w-4 h-4" />
          Tasks
        </button>
        <button
          onClick={() => setActiveTab('costs')}
          className={clsx(
            'flex items-center gap-2 px-4 py-2 text-sm border-b-2 transition-colors',
            activeTab === 'costs'
              ? 'border-primary-500 text-primary-500'
              : 'border-transparent text-gray-400 hover:text-gray-200'
          )}
        >
          <BarChart3 className="w-4 h-4" />
          Costs
        </button>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'output' && (
          <div
            ref={outputRef}
            className="h-full overflow-y-auto p-4 terminal custom-scrollbar bg-gray-950"
          >
            {output.length === 0 ? (
              <p className="text-gray-500">No output yet. Start the project to see output.</p>
            ) : (
              output.map((line, i) => (
                <div key={i} className="terminal-line mb-1">
                  {line.type === 'output' && <span className="text-gray-200">{line.text}</span>}
                  {line.type === 'tool_start' && (
                    <span className="text-blue-400">→ {line.tool_name}</span>
                  )}
                  {line.type === 'tool_end' && (
                    <span className={line.is_error ? 'text-red-400' : 'text-green-400'}>
                      {line.is_error ? '✗' : '✓'} {line.tool_name}
                    </span>
                  )}
                  {line.type === 'error' && <span className="text-red-400">Error: {line.text}</span>}
                </div>
              ))
            )}
            {isRunning && (
              <div className="flex items-center gap-2 text-gray-400 mt-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span>Running...</span>
              </div>
            )}
          </div>
        )}

        {activeTab === 'tasks' && (
          <div className="h-full overflow-y-auto p-4 custom-scrollbar">
            {project.completed_task_list.length === 0 ? (
              <p className="text-gray-500">No completed tasks yet.</p>
            ) : (
              <ul className="space-y-2">
                {project.completed_task_list.map((task, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm">{task}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {activeTab === 'costs' && (
          <div className="h-full overflow-y-auto p-4 custom-scrollbar">
            {project.cost ? (
              <CostChart cost={project.cost} />
            ) : (
              <p className="text-gray-500">No cost data yet.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
