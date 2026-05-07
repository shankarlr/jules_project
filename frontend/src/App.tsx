import { useState, useEffect } from 'react';
import { OpportunityCard } from './components/OpportunityCard';
import { ReportModal } from './components/ReportModal';

interface Opportunity {
  id: number;
  title: string;
  description: string;
  market_potential: string;
}

interface Report {
  id: number;
  plan: string;
  assets: string;
}

function App() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(false);
  const [triggering, setTriggering] = useState(false);

  const API_BASE = 'http://localhost:8000';

  const fetchOpportunities = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/opportunities`);
      const data = await response.json();
      setOpportunities(data);
    } catch (error) {
      console.error('Error fetching opportunities:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchReport = async (id: number) => {
    try {
      const response = await fetch(`${API_BASE}/reports/${id}`);
      const data = await response.json();
      setSelectedReport(data);
    } catch (error) {
      console.error('Error fetching report:', error);
    }
  };

  const triggerAutonomousCycle = async () => {
    setTriggering(true);
    try {
      await fetch(`${API_BASE}/trigger`, { method: 'POST' });
      alert('Autonomous cycle started! Refresh in a few seconds.');
    } catch (error) {
      console.error('Error triggering cycle:', error);
    } finally {
      setTriggering(false);
    }
  };

  useEffect(() => {
    fetchOpportunities();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
              Spark <span className="text-blue-600">Autonomous</span>
            </h1>
            <p className="mt-2 text-lg text-gray-600">Zero-cost intelligence for the future of work.</p>
          </div>
          <div className="flex gap-4">
            <button
              onClick={fetchOpportunities}
              className="bg-white text-gray-700 px-6 py-2 rounded-lg border border-gray-300 font-medium hover:bg-gray-50 transition"
              disabled={loading}
            >
              {loading ? 'Refreshing...' : 'Refresh Feed'}
            </button>
            <button
              onClick={triggerAutonomousCycle}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition shadow-sm"
              disabled={triggering}
            >
              {triggering ? 'Triggering...' : 'Run Autonomous Cycle'}
            </button>
          </div>
        </header>

        {opportunities.length === 0 && !loading ? (
          <div className="text-center py-20 bg-white rounded-xl shadow-sm">
            <p className="text-xl text-gray-500">No opportunities found. Click "Run Autonomous Cycle" to begin.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {opportunities.map((opp) => (
              <OpportunityCard
                key={opp.id}
                opportunity={opp}
                onSelect={fetchReport}
              />
            ))}
          </div>
        )}
      </div>

      <ReportModal
        report={selectedReport}
        onClose={() => setSelectedReport(null)}
      />
    </div>
  );
}

export default App;
