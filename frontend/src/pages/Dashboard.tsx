import { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import { ShieldAlert, Zap, Server, Activity } from 'lucide-react';

interface DashboardStats {
    active_alerts: number;
    total_events: number;
    monitored_hosts: number;
    global_risk: number;
    risk_graph: { time: string; risk: number }[];
    recent_detections: string[];
}

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        axios.get('http://localhost:8080/api/analytics/dashboard')
            .then(res => setStats(res.data))
            .catch(err => {
                console.error("Failed to fetch dashboard stats", err);
                setError("Could not connect to the backend API.");
            });
    }, []);

    if (error) {
        return <div className="text-red-400">Error loading dashboard: {error}</div>;
    }

    if (!stats) {
        return <div className="text-gray-400">Loading dashboard...</div>;
    }

    return (
        <div className="space-y-8">
            <h2 className="text-3xl font-bold">Executive Dashboard</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                    { label: 'Active Alerts', val: stats.active_alerts.toString(), icon: <ShieldAlert size={24} className="text-red-400" /> },
                    { label: 'Total Events', val: stats.total_events.toString(), icon: <Zap size={24} className="text-yellow-400" /> },
                    { label: 'Monitored Hosts', val: stats.monitored_hosts.toString(), icon: <Server size={24} className="text-blue-400" /> },
                    { label: 'Global Risk', val: `${stats.global_risk}/100`, icon: <Activity size={24} className="text-purple-400" /> },
                ].map((stat, i) => (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                        key={i}
                        className="glass-card flex items-center p-6 gap-4"
                    >
                        <div className="p-3 bg-white/5 rounded-full border border-white/10">{stat.icon}</div>
                        <div>
                            <div className="text-sm text-gray-400 font-medium">{stat.label}</div>
                            <div className="text-2xl font-bold">{stat.val}</div>
                        </div>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="lg:col-span-2 glass-card p-6">
                    <h3 className="text-lg font-semibold mb-4">Risk Extrapolation Graph</h3>
                    <div className="h-72">
                        {stats.risk_graph.length > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={stats.risk_graph}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                    <XAxis dataKey="time" stroke="#9ca3af" />
                                    <YAxis stroke="#9ca3af" />
                                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                                    <Line type="monotone" dataKey="risk" stroke="#8b5cf6" strokeWidth={3} dot={{ r: 4, fill: '#8b5cf6' }} />
                                </LineChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="flex h-full items-center justify-center text-gray-500">No chart data available.</div>
                        )}
                    </div>
                </motion.div>

                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="glass-card p-6">
                    <h3 className="text-lg font-semibold mb-4">Recent Detections</h3>
                    <div className="space-y-4">
                        {stats.recent_detections.length > 0 ? stats.recent_detections.map((d, i) => (
                            <div key={i} className="flex flex-col border-b border-white/10 pb-3 last:border-0 last:pb-0">
                                <span className="text-sm font-semibold">{d}</span>
                                <span className="text-xs text-red-400 bg-red-400/10 self-start px-2 py-0.5 rounded-full mt-1 border border-red-500/20">Critical</span>
                            </div>
                        )) : (
                            <div className="text-gray-500 text-sm">No recent detections reported.</div>
                        )}
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
