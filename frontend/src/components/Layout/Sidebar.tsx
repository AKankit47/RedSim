import { NavLink } from 'react-router-dom';
import { Shield, Activity, Share2, Layers, Search, BarChart2, CheckSquare, Bell, User } from 'lucide-react';

export default function Sidebar() {
    const routes = [
        { path: "/", name: "Dashboard", icon: <Activity size={20} /> },
        { path: "/builder", name: "Scenario Builder", icon: <CheckSquare size={20} /> },
        { path: "/graph", name: "Attack Graph", icon: <Share2 size={20} /> },
        { path: "/timeline", name: "Attack Timeline", icon: <Layers size={20} /> },
        { path: "/mitre", name: "MITRE Mapping", icon: <Shield size={20} /> },
        { path: "/detections", name: "Detections", icon: <Bell size={20} /> },
        { path: "/analytics", name: "Analytics", icon: <BarChart2 size={20} /> },
        { path: "/search", name: "Global Search", icon: <Search size={20} /> },
        { path: "/labs", name: "Lab Management", icon: <User size={20} /> }
    ];

    return (
        <aside className="w-64 bg-cyber-card backdrop-blur-xl border-r border-white/10 flex flex-col pt-6">
            <div className="px-6 mb-8 flex items-center gap-3">
                <Shield className="text-primary" size={32} />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent">RedSim</h1>
            </div>

            <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
                {routes.map((route) => (
                    <NavLink
                        key={route.path}
                        to={route.path}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive
                                ? 'bg-primary/10 text-primary border border-primary/20 shadow-[0_0_15px_rgba(79,70,229,0.15)]'
                                : 'text-gray-400 hover:text-gray-100 hover:bg-white/5'
                            }`
                        }
                    >
                        {route.icon}
                        <span className="font-medium">{route.name}</span>
                    </NavLink>
                ))}
            </nav>
        </aside>
    );
}
