import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, Lock, User } from 'lucide-react';

export default function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            // In a real app we'd make a POST to /api/auth/login with OAuth2 form data
            // const formData = new URLSearchParams(); formData.append('username', username); ...
            // Hardcoded bypass for RedSim setup demo
            login('dummy_token_123', { username, role: 'admin' });
            navigate('/');
        } catch (err: any) {
            setError("Invalid credentials");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="glass-card w-full max-w-md p-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary/20 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2"></div>

                <div className="relative z-10 flex flex-col items-center mb-8">
                    <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mb-4 border border-primary/50 shadow-[0_0_30px_rgba(79,70,229,0.3)]">
                        <Shield className="text-primary" size={32} />
                    </div>
                    <h2 className="text-2xl font-bold">Access RedSim Console</h2>
                    <p className="text-gray-400 mt-2 text-sm">Enter your credentials to initiate operations</p>
                </div>

                {error && <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded-lg mb-6 text-sm text-center">{error}</div>}

                <form onSubmit={handleLogin} className="relative z-10 space-y-5">
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Username</label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-500">
                                <User size={18} />
                            </div>
                            <input
                                type="text"
                                value={username} onChange={e => setUsername(e.target.value)}
                                className="block w-full pl-10 pr-3 py-2.5 bg-black/20 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                                placeholder="admin"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-500">
                                <Lock size={18} />
                            </div>
                            <input
                                type="password"
                                value={password} onChange={e => setPassword(e.target.value)}
                                className="block w-full pl-10 pr-3 py-2.5 bg-black/20 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                                placeholder="••••••••"
                            />
                        </div>
                    </div>

                    <button type="submit" className="w-full bg-primary hover:bg-indigo-500 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 mt-4 shadow-[0_0_20px_rgba(79,70,229,0.4)]">
                        Authenticate Session
                    </button>
                </form>
            </div>
        </div>
    );
}
