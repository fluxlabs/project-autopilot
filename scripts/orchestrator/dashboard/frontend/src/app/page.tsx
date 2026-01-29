// Autopilot Dashboard Main Page
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

'use client';

import { useEffect, useState } from 'react';
import { ProjectList } from '@/components/ProjectList';
import { ProjectDetail } from '@/components/ProjectDetail';
import { StatsBar } from '@/components/StatsBar';
import { NewProjectModal } from '@/components/NewProjectModal';
import { Plus, Zap } from 'lucide-react';

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

interface Stats {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_cost: number;
  total_tokens: number;
  avg_cost_per_project: number;
}

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [showNewProject, setShowNewProject] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchProjects = async () => {
    try {
      const res = await fetch('/api/projects');
      const data = await res.json();
      setProjects(data.projects);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  useEffect(() => {
    const init = async () => {
      await Promise.all([fetchProjects(), fetchStats()]);
      setLoading(false);
    };
    init();

    // Poll for updates
    const interval = setInterval(() => {
      fetchProjects();
      fetchStats();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleProjectCreated = (project: Project) => {
    setProjects([...projects, project]);
    setSelectedProject(project.id);
    setShowNewProject(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex items-center gap-3 text-gray-400">
          <Zap className="w-6 h-6 animate-pulse" />
          <span>Loading Autopilot...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Zap className="w-6 h-6 text-primary-500" />
            <h1 className="text-xl font-semibold">Autopilot Dashboard</h1>
          </div>
          <button
            onClick={() => setShowNewProject(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-500 rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Project
          </button>
        </div>
      </header>

      {/* Stats Bar */}
      {stats && <StatsBar stats={stats} />}

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-6">
        <div className="grid grid-cols-12 gap-6">
          {/* Project List */}
          <div className="col-span-4">
            <ProjectList
              projects={projects}
              selectedId={selectedProject}
              onSelect={setSelectedProject}
              onRefresh={fetchProjects}
            />
          </div>

          {/* Project Detail */}
          <div className="col-span-8">
            {selectedProject ? (
              <ProjectDetail
                projectId={selectedProject}
                onUpdate={fetchProjects}
              />
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500 border border-gray-800 rounded-lg bg-gray-900/30">
                <p>Select a project to view details</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* New Project Modal */}
      {showNewProject && (
        <NewProjectModal
          onClose={() => setShowNewProject(false)}
          onCreated={handleProjectCreated}
        />
      )}
    </div>
  );
}
