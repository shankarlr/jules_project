import React from 'react';

interface Opportunity {
  id: number;
  title: string;
  description: string;
  market_potential: string;
  version?: number;
  efficiency_score?: number;
  is_prime_path?: number;
}

interface OpportunityCardProps {
  opportunity: Opportunity;
  onSelect: (id: number) => void;
}

export const OpportunityCard: React.FC<OpportunityCardProps> = ({ opportunity, onSelect }) => {
  return (
    <div className={`bg-white p-6 rounded-lg shadow-md border-l-4 ${opportunity.is_prime_path ? 'border-green-500 ring-2 ring-green-100' : 'border-blue-500'} hover:shadow-lg transition-shadow cursor-pointer`} onClick={() => onSelect(opportunity.id)}>
      <div className="flex justify-between items-start">
        <h3 className="text-xl font-bold text-gray-800 mb-2">{opportunity.title}</h3>
        {opportunity.version && (
          <span className="bg-gray-100 text-gray-600 text-[10px] px-2 py-1 rounded font-mono">
            v{opportunity.version}
          </span>
        )}
      </div>
      <p className="text-gray-600 mb-4 line-clamp-2">{opportunity.description}</p>
      <div className="flex justify-between items-center">
        <div className="flex gap-2">
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
            opportunity.market_potential === 'High' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
          }`}>
            Potential: {opportunity.market_potential}
          </span>
          {opportunity.efficiency_score && (
            <span className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-semibold">
              {(opportunity.efficiency_score * 100).toFixed(0)}% Eff
            </span>
          )}
        </div>
        <button className="text-blue-600 hover:underline">View Report →</button>
      </div>
    </div>
  );
};
