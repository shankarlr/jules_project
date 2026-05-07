import React from 'react';

interface Opportunity {
  id: number;
  title: string;
  description: string;
  market_potential: string;
}

interface OpportunityCardProps {
  opportunity: Opportunity;
  onSelect: (id: number) => void;
}

export const OpportunityCard: React.FC<OpportunityCardProps> = ({ opportunity, onSelect }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500 hover:shadow-lg transition-shadow cursor-pointer" onClick={() => onSelect(opportunity.id)}>
      <h3 className="text-xl font-bold text-gray-800 mb-2">{opportunity.title}</h3>
      <p className="text-gray-600 mb-4 line-clamp-2">{opportunity.description}</p>
      <div className="flex justify-between items-center">
        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
          opportunity.market_potential === 'High' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
        }`}>
          Potential: {opportunity.market_potential}
        </span>
        <button className="text-blue-600 hover:underline">View Report →</button>
      </div>
    </div>
  );
};
