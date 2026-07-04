
import { useAuth } from '../../context/AuthContext';
import { Bell, User, LogOut, Sun } from 'lucide-react';

export default function TopNav() {
    const { user, logout } = useAuth();

    return (
        <header className="h-16 border-b border-white/10 bg-cyber-card/50 backdrop-blur-md flex items-center justify-between px-6 z-10">
            <div className="flex-1 flex items-center">
                {/* Placeholder for Breadcrumbs or title */}
            </div>

            <div className="flex items-center gap-4">
                <button className="text-gray-400 hover:text-white transition-colors">
                    <Sun size={20} />
                </button>
                <button className="text-gray-400 hover:text-white transition-colors relative">
                    <Bell size={20} />
                    <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>

                <div className="h-8 w-px bg-white/10 mx-2"></div>

                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary/20 border border-primary/50 flex items-center justify-center text-primary">
                        <User size={16} />
                    </div>
                    <span className="font-medium text-sm hidden sm:block">
                        {user ? user.username : 'Guest Mode'}
                    </span>
                    {user && (
                        <button onClick={logout} className="text-red-400 hover:text-red-300 ml-2">
                            <LogOut size={18} />
                        </button>
                    )}
                </div>
            </div>
        </header>
    );
}
