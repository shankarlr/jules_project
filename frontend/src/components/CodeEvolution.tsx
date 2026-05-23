import React, { useState, useEffect } from 'react';
import { API_BASE } from '../config';

interface EvolvedFile {
  filename: string;
  content: string;
}

export const CodeEvolution: React.FC = () => {
  const [files, setFiles] = useState<EvolvedFile[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchEvolution = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/evolution/code`);
      const data = await response.json();
      setFiles(data);
    } catch (error) {
      console.error('Error fetching evolution:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvolution();
    const interval = setInterval(fetchEvolution, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-slate-900 rounded-xl shadow-xl overflow-hidden border border-slate-700 mb-12">
      <div className="px-6 py-4 bg-slate-800 border-b border-slate-700 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
          <h2 className="text-xl font-bold text-white">Self-Evolution: Agent Source Code</h2>
        </div>
        <button
          onClick={fetchEvolution}
          className="text-xs text-slate-400 hover:text-white transition uppercase tracking-widest"
        >
          {loading ? 'Reading Disk...' : 'Refresh Source'}
        </button>
      </div>

      <div className="p-6">
        {files.length === 0 ? (
          <div className="text-center py-10 text-slate-500 italic">
            Waiting for agents to generate first evolution modules...
          </div>
        ) : (
          <div className="space-y-6">
            {files.map((file, idx) => (
              <div key={file.filename} className="relative">
                <div className="absolute top-0 right-0 bg-slate-700 text-slate-300 text-[10px] px-2 py-1 rounded-bl-lg font-mono">
                  {file.filename} {idx === 0 ? '(ACTIVE)' : '(LEGACY)'}
                </div>
                <pre className="bg-slate-950 p-4 rounded-lg text-emerald-400 font-mono text-sm overflow-x-auto border border-slate-800">
                  <code>{file.content}</code>
                </pre>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="px-6 py-3 bg-slate-800 text-[10px] text-slate-400 font-mono flex justify-between">
        <span>STATUS: SYSTEM RECURSIVELY OPTIMIZING CORE LOGIC</span>
        <span>GOAL: REVENUE MAXIMIZATION ($500/HR)</span>
      </div>
    </div>
  );
};
