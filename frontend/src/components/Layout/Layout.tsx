import React from 'react';
import Sidebar from './Sidebar';
import TopNav from './TopNav';

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex h-screen bg-cyber-950 text-white overflow-hidden">
            <Sidebar />
            <div className="flex-1 flex flex-col min-w-0">
                <TopNav />
                <main className="flex-1 overflow-y-auto p-6 lg:p-8">
                    <div className="max-w-7xl mx-auto space-y-6">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
