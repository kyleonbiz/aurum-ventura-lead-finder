import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [industries, setIndustries] = useState([]);
  const [locations, setLocations] = useState([]);
  const [selectedIndustry, setSelectedIndustry] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState('');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadIndustries();
    loadStats();
  }, []);

  useEffect(() => {
    if (selectedIndustry) {
      loadLocations(selectedIndustry);
    }
  }, [selectedIndustry]);

  const loadIndustries = async () => {
    try {
      const res = await fetch(`${API_URL}/search/industries`);
      const data = await res.json();
      if (data.success) {
        setIndustries(data.industries);
      }
    } catch (e) {
      console.error('Error loading industries:', e);
    }
  };

  const loadLocations = async (industry) => {
    try {
      const res = await fetch(`${API_URL}/search/locations?industry=${industry}`);
      const data = await res.json();
      if (data.success) {
        setLocations(data.locations);
      }
    } catch (e) {
      console.error('Error loading locations:', e);
    }
  };

  const loadStats = async () => {
    try {
      const res = await fetch(`${API_URL}/search/stats`);
      const data = await res.json();
      if (data.success) {
        setStats(data);
      }
    } catch (e) {
      console.error('Error loading stats:', e);
    }
  };

  const handleSearch = async () => {
    if (!selectedIndustry || !selectedCity) {
      setError('Please select an industry and city');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const params = new URLSearchParams({
        industry: selectedIndustry,
        city: selectedCity,
        ...(selectedState && { state: selectedState })
      });

      const res = await fetch(`${API_URL}/search/businesses?${params}`);
      const data = await res.json();

      if (!res.ok) {
        setError(data.error || 'Search failed');
        return;
      }

      if (data.results.length === 0) {
        setError('No businesses found for this search');
        return;
      }

      setResults(data.results);
    } catch (e) {
      setError('Search failed: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format) => {
    if (!selectedIndustry || !selectedCity) {
      setError('Please search first');
      return;
    }

    setExporting(true);

    try {
      const endpoint = format === 'csv' ? 'csv' : format === 'excel' ? 'excel' : 'json';

      const res = await fetch(`${API_URL}/export/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          industry: selectedIndustry,
          city: selectedCity,
          ...(selectedState && { state: selectedState })
        })
      });

      if (!res.ok) {
        setError('Export failed');
        return;
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;

      const contentDisposition = res.headers.get('content-disposition');
      a.download = contentDisposition
        ? contentDisposition.split('filename=')[1].replace(/"/g, '')
        : `businesses.${format}`;

      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (e) {
      setError('Export failed: ' + e.message);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 bg-gradient-to-br from-purple-600 via-purple-500 to-pink-600">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 text-white">
          <h1 className="text-5xl font-bold mb-4">🔍 Aurum Ventura Lead Finder</h1>
          <p className="text-xl opacity-90">Find local businesses by industry and location</p>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
            <StatCard icon="📊" label="Businesses" value={stats.total_businesses} />
            <StatCard icon="🏢" label="Industries" value={stats.total_industries} />
            <StatCard icon="🔎" label="Searches" value={stats.total_searches} />
          </div>
        )}

        {/* Search Panel */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Search Criteria</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {/* Industry Select */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Industry</label>
              <select
                value={selectedIndustry}
                onChange={(e) => {
                  setSelectedIndustry(e.target.value);
                  setSelectedCity('');
                  setSelectedState('');
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">Select an industry...</option>
                {industries.map(ind => (
                  <option key={ind} value={ind}>
                    {ind.charAt(0).toUpperCase() + ind.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            {/* City Select */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">City</label>
              <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={!selectedIndustry}
              >
                <option value="">Select a city...</option>
                {locations.map(loc => (
                  <option key={`${loc.city}-${loc.state}`} value={loc.city}>
                    {loc.city}, {loc.state}
                  </option>
                ))}
              </select>
            </div>

            {/* State Select */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">State (Optional)</label>
              <select
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={!selectedIndustry}
              >
                <option value="">All states</option>
                {[...new Set(locations.map(loc => loc.state))].sort().map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {/* Search Button */}
          <button
            onClick={handleSearch}
            disabled={loading || !selectedIndustry || !selectedCity}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
          >
            {loading ? 'Searching...' : 'Search Businesses'}
          </button>
        </div>

        {/* Results Panel */}
        {results.length > 0 && (
          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
              <h2 className="text-2xl font-bold text-gray-800">
                Results ({results.length} found)
              </h2>

              {/* Export Buttons */}
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => handleExport('csv')}
                  disabled={exporting}
                  className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition"
                >
                  📥 CSV
                </button>
                <button
                  onClick={() => handleExport('excel')}
                  disabled={exporting}
                  className="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition"
                >
                  📊 Excel
                </button>
                <button
                  onClick={() => handleExport('json')}
                  disabled={exporting}
                  className="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition"
                >
                  {} JSON
                </button>
              </div>
            </div>

            {/* Results Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-3 text-left font-semibold text-gray-700">Business Name</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-700">Contact</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-700">Phone</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-700">Website</th>
                    <th className="px-4 py-3 text-center font-semibold text-gray-700">Quality</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((biz, idx) => (
                    <tr key={idx} className="border-t hover:bg-gray-50">
                      <td className="px-4 py-3 font-semibold text-gray-800">{biz.name}</td>
                      <td className="px-4 py-3 text-gray-600">
                        {biz.email ? (
                          <a href={`mailto:${biz.email}`} className="text-blue-500 hover:underline">
                            {biz.email}
                          </a>
                        ) : (
                          '-'
                        )}
                      </td>
                      <td className="px-4 py-3 text-gray-600">{biz.phone || '-'}</td>
                      <td className="px-4 py-3 text-gray-600">
                        {biz.website ? (
                          <a href={`https://${biz.website}`} target="_blank" rel="noopener noreferrer"
                            className="text-blue-500 hover:underline">
                            {biz.website}
                          </a>
                        ) : (
                          '-'
                        )}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold">
                          {(biz.quality_score * 100).toFixed(0)}%
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && results.length === 0 && !error && (
          <div className="bg-white rounded-2xl shadow-2xl p-12 text-center text-gray-400">
            <p className="text-lg">👇 Use the search form above to find businesses</p>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon, label, value }) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 text-center">
      <div className="text-4xl mb-2">{icon}</div>
      <div className="text-3xl font-bold text-purple-600">{value.toLocaleString()}</div>
      <div className="text-gray-600 text-sm mt-1">{label}</div>
    </div>
  );
}

export default App;
