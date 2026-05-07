import React, { useEffect, useState, useRef } from 'react';
import { API_BASE } from '../config';

interface AgentStatus {
  id: number;
  name: string;
  role: string;
  current_task: string;
  status: string;
  updated_at: string;
}

interface ActionLog {
  agentName: string;
  task: string;
  time: string;
}

export const AgentMonitor: React.FC = () => {
  const [agents, setAgents] = useState<AgentStatus[]>([]);
  const [history, setHistory] = useState<ActionLog[]>([]);
  const lastTaskRef = useRef<Record<string, string>>({});

  const fetchAgents = async () => {
    try {
      const response = await fetch(`${API_BASE}/agents`);
      const data = await response.json();
      setAgents(data);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const fetchAuditLogs = async () => {
    try {
      const response = await fetch(`${API_BASE}/audit`);
      const data = await response.json();
      setHistory(data.map((log: any) => ({
        agentName: log.agent_name,
        task: log.action,
        time: new Date(log.created_at).toLocaleTimeString()
      })));
    } catch (error) {
      console.error('Error fetching audit logs:', error);
    }
  };

  useEffect(() => {
    fetchAgents();
    fetchAuditLogs();
    const interval = setInterval(() => {
      fetchAgents();
      fetchAuditLogs();
    }, 5000); // Update every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col lg:flex-row gap-8 mb-8">
      {/* Real-time Status Cards */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <div key={agent.id} className="bg-gray-900 p-4 rounded-xl border border-gray-700 hover:border-blue-500/50 transition-colors shadow-xl">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-blue-400 font-mono font-bold text-lg">{agent.name}</h3>
                <p className="text-[10px] text-gray-500 font-mono uppercase tracking-widest">{agent.role}</p>
              </div>
              <span className={`text-[10px] px-2 py-0.5 rounded font-mono font-bold ${
                agent.status === 'Acting' ? 'bg-green-900/30 text-green-400' :
                agent.status === 'Thinking' ? 'bg-yellow-900/30 text-yellow-400' : 'bg-blue-900/30 text-blue-400'
              }`}>
                {agent.status}
              </span>
            </div>
            <div className="bg-black/50 p-3 rounded font-mono text-xs text-gray-300 min-h-[80px] flex items-center border border-gray-800">
              <span className="text-green-500 mr-2">$</span>
              {agent.current_task}
            </div>
          </div>
        ))}
        {agents.length === 0 && (
          <div className="col-span-3 text-center py-12 bg-gray-900 rounded-xl border border-dashed border-gray-700 text-gray-600 font-mono">
            Awaiting Command Signal...
          </div>
        )}
      </div>

      {/* Historical Audit Log */}
      <div className="lg:w-80 bg-black rounded-xl border border-gray-800 p-4 shadow-2xl">
        <h3 className="text-gray-400 text-[10px] font-bold uppercase tracking-tighter mb-4 border-b border-gray-800 pb-2 flex items-center gap-2">
           <span className="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span>
           Intelligence Audit Log
        </h3>
        <div className="space-y-3 max-h-[300px] overflow-y-auto pr-2">
          {history.map((log, i) => (
            <div key={i} className="font-mono text-[10px] border-l-2 border-gray-800 pl-2 py-1">
              <span className="text-gray-600">[{log.time}]</span>{' '}
              <span className="text-blue-500 font-bold">{log.agentName}:</span>{' '}
              <span className="text-gray-400">{log.task.substring(0, 40)}...</span>
            </div>
          ))}
          {history.length === 0 && (
             <p className="text-gray-700 font-mono text-[10px] italic">No active logs...</p>
          )}
        </div>
      </div>
    </div>
  );
};
