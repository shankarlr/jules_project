import React, { useEffect, useState } from 'react';
import { API_BASE } from '../config';

interface RevenueStats {
  total_revenue: number;
  hourly_revenue: number;
}

export const RevenueStream: React.FC = () => {
  const [stats, setStats] = useState<RevenueStats>({ total_revenue: 0, hourly_revenue: 0 });
  const [qrUrl, setQrUrl] = useState<string>('');

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/revenue/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching revenue stats:', error);
    }
  };

  const fetchSettings = async () => {
    try {
      const response = await fetch(`${API_BASE}/settings`);
      const data = await response.json();
      if (data.google_pay_qr) {
        setQrUrl(data.google_pay_qr);
      }
    } catch (error) {
      console.error('Error fetching settings:', error);
    }
  };

  useEffect(() => {
    fetchStats();
    fetchSettings();
    const interval = setInterval(fetchStats, 10000); // Update every 10s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white p-6 rounded-xl shadow-lg mb-8 border border-green-100 flex flex-col md:flex-row justify-between items-center gap-8">
      <div className="flex-1">
        <h2 className="text-sm font-semibold text-green-600 uppercase tracking-wider mb-1">Live Revenue Stream</h2>
        <div className="flex items-baseline gap-4">
          <span className="text-5xl font-black text-gray-900">${stats.total_revenue.toLocaleString()}</span>
          <span className="text-lg font-medium text-green-500 animate-pulse">
            +${stats.hourly_revenue.toLocaleString()}/hr
          </span>
        </div>
        <p className="text-gray-500 mt-2">Targeting $100 - $500 per hour across all autonomous agents.</p>
      </div>

      <div className="flex flex-col items-center gap-2">
        <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Payment Gateway</p>
        <div className="w-32 h-32 bg-gray-200 rounded-lg flex items-center justify-center overflow-hidden border-2 border-dashed border-gray-300">
          {qrUrl ? (
            <img src={qrUrl} alt="Google Pay QR" className="w-full h-full object-cover" />
          ) : (
            <div className="text-[10px] text-gray-400 text-center px-2">Google Pay QR Pending...</div>
          )}
        </div>
      </div>
    </div>
  );
};
