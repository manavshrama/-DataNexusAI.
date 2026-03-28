"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  BarChart3, 
  Settings, 
  Database, 
  Sparkles,
  ChevronRight
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', href: '/' },
  { icon: BarChart3, label: 'AI Insights', href: '/insights' },
  { icon: Database, label: 'Datasets', href: '/datasets' },
  { icon: Sparkles, label: 'Nexus AI', href: '/nexus' },
  { icon: Settings, label: 'Settings', href: '/settings' },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 h-full bg-surface-low border-r border-outline/10 flex flex-col p-4 gap-8">
      <div className="flex items-center gap-3 px-2">
        <div className="w-8 h-8 rounded-lg gradient-cta flex items-center justify-center">
          <Sparkles className="text-white w-5 h-5" />
        </div>
        <span className="font-display font-bold text-lg tracking-tight">DataNexus AI</span>
      </div>

      <nav className="flex-1 flex flex-col gap-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-md transition-all duration-200 group text-sm font-medium",
                isActive 
                  ? "bg-primary/10 text-primary border-l-4 border-primary" 
                  : "text-on-background/60 hover:bg-primary/5 hover:text-primary"
              )}
            >
              <item.icon className={cn("w-5 h-5", isActive ? "text-primary" : "text-on-background/40 group-hover:text-primary")} />
              <span>{item.label}</span>
              {isActive && <ChevronRight className="ml-auto w-4 h-4" />}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto p-4 glass rounded-xl border border-primary/10">
        <div className="text-[10px] font-bold text-primary uppercase tracking-widest mb-1">Status</div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-xs font-semibold">Nexus Core Active</span>
        </div>
      </div>
    </div>
  );
}
