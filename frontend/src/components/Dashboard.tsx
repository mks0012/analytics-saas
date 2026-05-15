'use client';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Activity, Layout, Database, RefreshCw, Trash2, Calendar, Zap } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState({ total_events: 0, breakdown: [] });
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(1);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://127.0.0.1:8000/v1/analytics/summary?days=${days}`);
      setData(response.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  };

  useEffect(() => {
    fetchStats();
    const inv = setInterval(fetchStats, 10000);
    return () => clearInterval(inv);
  }, [days]);

  return (
    <div style={{ backgroundColor: '#020617', minHeight: '100vh', color: '#f8fafc', padding: '40px', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
        
        {/* HEADER */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ background: '#1e293b', padding: '10px', borderRadius: '12px' }}>
              <Zap size={24} color="#38bdf8" fill="#38bdf8" />
            </div>
            <h1 style={{ fontSize: '28px', fontWeight: '800', letterSpacing: '-1px', margin: 0 }}>System Metrics</h1>
          </div>
          
          <div style={{ display: 'flex', gap: '10px' }}>
            <div style={{ background: '#0f172a', border: '1px solid #1e2937', borderRadius: '12px', padding: '4px 12px', display: 'flex', alignItems: 'center' }}>
              <Calendar size={14} style={{ color: '#64748b', marginRight: '8px' }} />
              <select 
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                style={{ backgroundColor: 'transparent', color: 'white', border: 'none', fontSize: '14px', fontWeight: '600', outline: 'none', cursor: 'pointer' }}
              >
                <option value={1}>Last 24h</option>
                <option value={7}>Last 7 Days</option>
                <option value={30}>Last 30 Days</option>
              </select>
            </div>
            <button onClick={fetchStats} style={{ backgroundColor: '#1e293b', border: 'none', padding: '10px', borderRadius: '12px', cursor: 'pointer', color: 'white' }}>
              <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
            </button>
            <button onClick={() => {/* clear logic */}} style={{ backgroundColor: '#ef444415', color: '#ef4444', border: '1px solid #ef444430', padding: '0 15px', borderRadius: '12px', fontSize: '13px', fontWeight: 'bold' }}>
              Wipe
            </button>
          </div>
        </div>

        {/* TOP METRICS - RENAMED FOR CLARITY */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', marginBottom: '30px' }}>
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', padding: '24px', borderRadius: '20px' }}>
            <Activity color="#38bdf8" size={24} style={{ marginBottom: '15px' }} />
            <p style={{ color: '#64748b', fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', margin: '0 0 5px 0' }}>Total Raw Events</p>
            <p style={{ fontSize: '32px', fontWeight: '800', margin: 0 }}>{data.total_events}</p>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #1e293b', padding: '24px', borderRadius: '20px' }}>
            <Layout color="#8b5cf6" size={24} style={{ marginBottom: '15px' }} />
            <p style={{ color: '#64748b', fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', margin: '0 0 5px 0' }}>Unique Activity Types</p>
            <p style={{ fontSize: '32px', fontWeight: '800', margin: 0 }}>{data.breakdown.length}</p>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #1e293b', padding: '24px', borderRadius: '20px' }}>
            <Database color="#10b981" size={24} style={{ marginBottom: '15px' }} />
            <p style={{ color: '#64748b', fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', margin: '0 0 5px 0' }}>Pipeline Status</p>
            <p style={{ fontSize: '32px', fontWeight: '800', margin: 0, color: '#10b981' }}>LIVE</p>
          </div>
        </div>

        {/* CHART SECTION */}
        <div style={{ background: '#0f172a', border: '1px solid #1e293b', padding: '30px', borderRadius: '24px' }}>
          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ margin: 0, fontSize: '18px' }}>Event Breakdown</h3>
            <p style={{ margin: '5px 0 0 0', color: '#64748b', fontSize: '14px' }}>Frequency of specific actions in your system</p>
          </div>
          
          <div style={{ width: '100%', height: '350px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.breakdown} margin={{ top: 0, right: 0, left: -25, bottom: 40 }}>
                <defs>
                  <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#38bdf8" stopOpacity={1} />
                    <stop offset="100%" stopColor="#38bdf8" stopOpacity={0.2} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis 
                  dataKey="event_name" 
                  stroke="#475569" 
                  fontSize={11} 
                  tickLine={false} 
                  axisLine={false} 
                  dy={10}
                />
                <YAxis stroke="#475569" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{ fill: '#1e293b', opacity: 0.4 }}
                  contentStyle={{ backgroundColor: '#020617', borderRadius: '12px', border: '1px solid #1e293b', color: '#fff' }}
                />
                <Bar 
                  dataKey="count" 
                  fill="url(#barGradient)" 
                  radius={[6, 6, 0, 0]} 
                  barSize={40} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}