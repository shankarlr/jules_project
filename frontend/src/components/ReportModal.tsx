import React from 'react';

interface Report {
  id: number;
  plan: string;
  assets: string;
}

interface ReportModalProps {
  report: Report | null;
  onClose: () => void;
}

export const ReportModal: React.FC<ReportModalProps> = ({ report, onClose }) => {
  if (!report) return null;

  const assets = JSON.parse(report.assets);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-8 relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
        <h2 className="text-3xl font-bold mb-6 text-gray-900 border-b pb-4">Autonomous Business Report</h2>

        <div className="prose max-w-none mb-8">
          <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
            {report.plan}
          </pre>
        </div>

        <div className="bg-gray-50 p-6 rounded-lg">
          <h4 className="font-bold text-lg mb-4">Generated Assets</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider">Logo Prompt</p>
              <p className="text-gray-800">{assets.logo_prompt}</p>
            </div>
            <div>
              <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider">Target Audience</p>
              <p className="text-gray-800">{assets.target_audience}</p>
            </div>
            <div className="col-span-full">
              <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider">Headline</p>
              <p className="text-gray-800 italic">"{assets.landing_page_headline}"</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
