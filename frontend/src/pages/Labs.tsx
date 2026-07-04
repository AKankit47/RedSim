import { useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import axios from 'axios';
import { Play, Square, RotateCcw, ExternalLink, Cpu, MemoryStick, Shield, Globe, Network, Code2, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';

const API_BASE = 'http://localhost:8080/api/labs';

const CATEGORIES = ['All', 'OWASP', 'Web', 'API', 'Network'] as const;
type Category = typeof CATEGORIES[number];

const DIFFICULTY_COLOR: Record<string, string> = {
    'Beginner': 'text-green-400 bg-green-400/10 border-green-500/30',
    'Beginner–Intermediate': 'text-yellow-400 bg-yellow-400/10 border-yellow-500/30',
    'Intermediate': 'text-orange-400 bg-orange-400/10 border-orange-500/30',
    'Beginner–Advanced': 'text-orange-400 bg-orange-400/10 border-orange-500/30',
    'Advanced': 'text-red-400 bg-red-400/10 border-red-500/30',
};

const CATEGORY_ICON: Record<string, ReactNode> = {
    OWASP: <Shield size={14} />,
    Web: <Globe size={14} />,
    API: <Code2 size={14} />,
    Network: <Network size={14} />,
};

interface Lab {
    id: string;
    name: string;
    image: string;
    port: number;
    category: string;
    description: string;
    difficulty: string;
    status: string;
    url: string | null;
    cpu: number | null;
    ram_mb: number | null;
}

type ActionKey = `${string}-${'start' | 'stop' | 'restart'}`;

export default function Labs() {
    const [labs, setLabs] = useState<Lab[]>([]);
    const [loading, setLoading] = useState(true);
    const [actionLoading, setAction] = useState<ActionKey | null>(null);
    const [filter, setFilter] = useState<Category>('All');
    const [dockerOk, setDockerOk] = useState<boolean | null>(null);
    const [demoMode, setDemoMode] = useState(false);

    const fetchLabs = useCallback(async () => {
        try {
            const [labsRes, statusRes] = await Promise.all([
                axios.get<Lab[]>(API_BASE),
                axios.get(`${API_BASE}/status`),
            ]);
            setLabs(labsRes.data);
            setDockerOk(statusRes.data.docker === 'Running');
            setDemoMode(statusRes.data.mode === 'demo');
        } catch {
            setDockerOk(false);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchLabs();
        const iv = setInterval(fetchLabs, 5000);
        return () => clearInterval(iv);
    }, [fetchLabs]);

    const handleAction = async (labId: string, action: 'start' | 'stop' | 'restart') => {
        const key: ActionKey = `${labId}-${action}`;
        setAction(key);
        try {
            await axios.post(`${API_BASE}/${action}/${labId}`);
            await fetchLabs();
        } catch (err: any) {
            console.error(`${action} failed:`, err?.response?.data?.detail ?? err.message);
        } finally {
            setAction(null);
        }
    };

    const visible = filter === 'All' ? labs : labs.filter(l => l.category === filter);
    const running = labs.filter(l => l.status === 'Running').length;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h2 className="text-3xl font-bold">Lab Management</h2>
                    <p className="text-gray-400 mt-1 text-sm">
                        Spin up real vulnerable machines. All containers run in isolated Docker networks.
                    </p>
                </div>
                <DockerBadge ok={dockerOk} demo={demoMode} running={running} total={labs.length} />
            </div>

            {/* Category Tabs */}
            <div className="flex gap-2 flex-wrap">
                {CATEGORIES.map(cat => (
                    <button
                        key={cat}
                        onClick={() => setFilter(cat)}
                        className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${filter === cat
                            ? 'bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-900/40'
                            : 'bg-white/5 border-white/10 text-gray-400 hover:text-white hover:border-white/20'
                            }`}
                    >
                        {cat !== 'All' && CATEGORY_ICON[cat]}
                        {cat}
                    </button>
                ))}
            </div>

            {/* Grid */}
            {loading ? (
                <div className="flex items-center justify-center h-64 gap-3 text-gray-400">
                    <Loader2 size={24} className="animate-spin" />
                    <span>Connecting to Docker...</span>
                </div>
            ) : visible.length === 0 ? (
                <p className="text-gray-500 py-12 text-center">No labs in this category.</p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
                    {visible.map(lab => (
                        <LabCard
                            key={lab.id}
                            lab={lab}
                            actionLoading={actionLoading}
                            onAction={handleAction}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}

/* ─── Sub-components ────────────────────────────────────────────────────── */

function DockerBadge({ ok, demo, running, total }: { ok: boolean | null; demo: boolean; running: number; total: number }) {
    if (ok === null) return null;
    if (!ok) return (
        <div className="flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium bg-red-500/10 border-red-500/30 text-red-400">
            <AlertCircle size={16} /> Docker Unavailable
        </div>
    );
    if (demo) return (
        <div className="flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium bg-purple-500/10 border-purple-500/30 text-purple-400">
            <CheckCircle size={16} /> Demo Mode · {running}/{total} simulated
        </div>
    );
    return (
        <div className="flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium bg-green-500/10 border-green-500/30 text-green-400">
            <CheckCircle size={16} /> Docker OK · {running}/{total} running
        </div>
    );
}

function StatusBadge({ status }: { status: string }) {
    const styles: Record<string, string> = {
        Running: 'text-green-400 bg-green-400/10 border-green-500/30',
        Stopped: 'text-gray-400 bg-white/5 border-white/10',
        'Docker Unavailable': 'text-red-400 bg-red-400/10 border-red-500/30',
    };
    const dot: Record<string, string> = {
        Running: 'bg-green-400 animate-pulse',
        Stopped: 'bg-gray-500',
    };
    const cls = styles[status] ?? 'text-orange-400 bg-orange-400/10 border-orange-500/30';
    return (
        <span className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-xs font-semibold ${cls}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${dot[status] ?? 'bg-orange-400'}`} />
            {status}
        </span>
    );
}

function StatBox({ icon, label, value }: { icon: ReactNode; label: string; value: string }) {
    return (
        <div className="flex-1 bg-white/5 rounded-xl p-3 border border-white/5 flex flex-col gap-1">
            <div className="flex items-center gap-1.5 text-gray-400 text-xs">{icon}{label}</div>
            <div className="text-base font-bold">{value}</div>
        </div>
    );
}

function LabCard({
    lab, actionLoading, onAction,
}: {
    lab: Lab;
    actionLoading: ActionKey | null;
    onAction: (id: string, action: 'start' | 'stop' | 'restart') => void;
}) {
    const isRunning = lab.status === 'Running';
    const isBusy = (a: 'start' | 'stop' | 'restart') => actionLoading === `${lab.id}-${a}`;

    return (
        <div className="glass-card p-5 flex flex-col gap-4 hover:border-indigo-500/30 transition-all duration-200">
            {/* Top row */}
            <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                        <span className={`flex items-center gap-1 px-2 py-0.5 rounded-full border text-xs ${'bg-indigo-500/10 border-indigo-500/30 text-indigo-400'
                            }`}>
                            {CATEGORY_ICON[lab.category]}
                            {lab.category}
                        </span>
                    </div>
                    <h3 className="font-semibold text-lg leading-tight truncate">{lab.name}</h3>
                </div>
                <StatusBadge status={lab.status} />
            </div>

            {/* Description */}
            <p className="text-gray-400 text-sm leading-relaxed">{lab.description}</p>

            {/* Meta row */}
            <div className="flex items-center justify-between text-xs gap-2">
                <code className="bg-black/30 px-2 py-1 rounded text-gray-400 truncate max-w-[60%]">{lab.image}</code>
                <span className={`px-2 py-1 rounded-full border text-xs font-medium ${DIFFICULTY_COLOR[lab.difficulty] ?? 'text-gray-400 bg-white/5 border-white/10'
                    }`}>{lab.difficulty}</span>
            </div>

            {/* Stats */}
            <div className="flex gap-2">
                <StatBox
                    icon={<Cpu size={12} />}
                    label="CPU"
                    value={isRunning && lab.cpu !== null ? `${lab.cpu}%` : '—'}
                />
                <StatBox
                    icon={<MemoryStick size={12} />}
                    label="RAM"
                    value={isRunning && lab.ram_mb !== null ? `${lab.ram_mb} MB` : '—'}
                />
                <StatBox
                    icon={<Globe size={12} />}
                    label="Port"
                    value={String(lab.port)}
                />
            </div>

            {/* Actions */}
            <div className="flex gap-2 pt-1">
                <button
                    onClick={() => onAction(lab.id, 'start')}
                    disabled={isRunning || isBusy('start')}
                    className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-sm font-medium transition-colors"
                >
                    {isBusy('start') ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
                    Start
                </button>
                <button
                    onClick={() => onAction(lab.id, 'stop')}
                    disabled={!isRunning || isBusy('stop')}
                    className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg bg-red-600/80 hover:bg-red-500 disabled:opacity-40 disabled:cursor-not-allowed text-sm font-medium transition-colors"
                >
                    {isBusy('stop') ? <Loader2 size={14} className="animate-spin" /> : <Square size={14} />}
                    Stop
                </button>
                <button
                    onClick={() => onAction(lab.id, 'restart')}
                    disabled={!isRunning || isBusy('restart')}
                    className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 disabled:opacity-40 disabled:cursor-not-allowed text-sm font-medium transition-colors"
                >
                    {isBusy('restart') ? <Loader2 size={14} className="animate-spin" /> : <RotateCcw size={14} />}
                </button>
                {isRunning && lab.url && (
                    <a
                        href={lab.url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-green-600/80 hover:bg-green-500 text-sm font-medium transition-colors"
                    >
                        <ExternalLink size={14} />
                    </a>
                )}
            </div>
        </div>
    );
}
