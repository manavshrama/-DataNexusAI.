import React from 'react';
import { Sidebar } from '@/components/Sidebar';
import { Bell, Search, User } from 'lucide-react';

export default function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-full w-full">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-16 border-b border-outline/10 bg-surface flex items-center px-8 gap-4 shadow-sm z-10">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-on-background/40" />
            <input 
              type="text" 
              placeholder="Search datasets, insights, or commands..." 
              className="w-full h-10 bg-surface-low border border-outline/20 rounded-lg pl-10 pr-4 text-sm focus:outline-none focus:border-primary transition-colors"
            />
          </div>
          <div className="flex items-center gap-4 ml-auto">
            <button className="p-2 text-on-background/60 hover:text-primary transition-colors relative">
              <Bell className="w-5 h-5" />
              <div className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-surface" />
            </button>
            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-xs border border-primary/20">
              <User className="w-5 h-5" />
            </div>
            <span className="text-sm font-semibold opacity-80">Admin Nexus</span>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-8 bg-background-base/50">
          {children}
        </main>
      </div>
    </div>
  );
}
