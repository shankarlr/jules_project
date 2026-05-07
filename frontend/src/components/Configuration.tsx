import React, { useState, useEffect } from 'react';
import { API_BASE } from '../config';

export const Configuration: React.FC = () => {
  const [adminSecret, setAdminSecret] = useState('');
  const [llmKey, setLlmKey] = useState('');
  const [isSaved, setIsSaved] = useState(false);

  const saveSetting = async (key: string, value: string) => {
    try {
      await fetch(`${API_BASE}/settings`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Secret': adminSecret || 'dev_secret'
        },
        body: JSON.stringify({ key, value })
      });
      setIsSaved(true);
      setTimeout(() => setIsSaved(false), 3000);
    } catch (e) {
      alert('Failed to save. Check Admin Secret.');
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-12">
      <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Intelligence Configuration
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Admin Secret</label>
          <input
            type="password"
            value={adminSecret}
            onChange={(e) => setAdminSecret(e.target.value)}
            placeholder="Required for updates"
            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none"
          />
        </div>
        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-2">LLM API Key (Optional)</label>
          <input
            type="text"
            value={llmKey}
            onChange={(e) => setLlmKey(e.target.value)}
            placeholder="sk-..."
            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none"
          />
        </div>
        <div className="flex items-end">
          <button
            onClick={() => saveSetting('LLM_API_KEY', llmKey)}
            className="w-full bg-gray-800 text-white p-2 rounded hover:bg-gray-900 transition flex items-center justify-center gap-2"
          >
            {isSaved ? 'Settings Saved' : 'Update Configuration'}
          </button>
        </div>
      </div>
      <p className="mt-4 text-[10px] text-gray-400 font-mono">
        System uses heuristic processing by default. Add an API key to switch to LLM-driven autonomous execution.
      </p>
    </div>
  );
};
