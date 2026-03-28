import MainLayout from '@/components/MainLayout';
import { 
  BarChart3, 
  Database, 
  ArrowUpRight, 
  ArrowDownRight, 
  Clock,
  Zap,
  Layout
} from 'lucide-react';
import { cn } from '@/lib/utils';

const stats = [
  { label: 'Total Datasets', value: '24', change: '+2', trend: 'up', icon: Database },
  { label: 'AI Insights', value: '1,284', change: '+12%', trend: 'up', icon: Zap },
  { label: 'System Health', value: '98.2%', change: '-0.3%', trend: 'down', icon: Layout },
  { label: 'Latency', value: '142ms', change: '-12ms', trend: 'up', icon: Clock },
];

export default function Home() {
  return (
    <MainLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-display font-bold text-on-background tracking-tight">Command Center</h1>
            <p className="text-on-background/50 font-medium">Real-time overview of your AI Data Nexus.</p>
          </div>
          <button className="px-5 py-2.5 rounded-lg gradient-cta text-white font-bold text-sm shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Launch Nexus AI
          </button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-surface rounded-2xl p-6 border border-outline/10 tonal-lift hover:border-primary/20 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 rounded-xl bg-primary/5 text-primary group-hover:bg-primary/10 transition-colors">
                  <stat.icon className="w-6 h-6" />
                </div>
                <div className={cn(
                  "flex items-center gap-1 text-xs font-bold px-2 py-1 rounded-full",
                  stat.trend === 'up' ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                )}>
                  {stat.trend === 'up' ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                  {stat.change}
                </div>
              </div>
              <div className="space-y-1">
                <h3 className="text-sm font-medium text-on-background/40">{stat.label}</h3>
                <p className="text-2xl font-display font-bold text-on-background tracking-tight">{stat.value}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          <div className="xl:col-span-2 bg-surface rounded-2xl border border-outline/10 tonal-lift p-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-xl font-display font-bold flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-primary" />
                Data Nexus Stream
              </h2>
              <div className="flex items-center gap-2 bg-surface-low p-1 rounded-lg border border-outline/10">
                <button className="px-3 py-1 text-xs font-bold rounded-md bg-white shadow-sm">Daily</button>
                <button className="px-3 py-1 text-xs font-bold rounded-md opacity-40 hover:opacity-100">Weekly</button>
              </div>
            </div>
            
            <div className="h-[300px] flex items-end justify-between gap-2 px-4">
              {[40, 70, 45, 90, 65, 80, 55, 100, 85, 75, 60, 40].map((height, i) => (
                <div key={i} className="flex-1 space-y-2 group">
                  <div className="relative w-full bg-primary/5 rounded-t-md overflow-hidden" style={{ height: `${height}%` }}>
                    <div className="absolute inset-0 gradient-cta opacity-40 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <div className="text-[10px] font-bold text-center opacity-30 group-hover:opacity-100 transition-opacity">0{i+1}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-surface rounded-2xl border border-outline/10 tonal-lift p-8 glass overflow-hidden relative">
            <div className="absolute top-0 right-0 w-32 h-32 gradient-cta opacity-5 blur-3xl -mr-16 -mt-16" />
            <h2 className="text-xl font-display font-bold mb-6 flex items-center gap-2">
              <Zap className="w-5 h-5 text-primary" />
              Latest Insights
            </h2>
            <div className="space-y-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex gap-4 group">
                  <div className="w-10 h-10 rounded-full bg-primary/5 flex items-center justify-center border border-primary/10 group-hover:bg-primary group-hover:text-white transition-all">
                    <Zap className="w-5 h-5" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <h4 className="text-sm font-bold group-hover:text-primary transition-colors">Anomalies Detected in Sales_2024.csv</h4>
                    <p className="text-xs text-on-background/50 line-clamp-2 leading-relaxed">System identified unusual patterns in the Q3 revenue column suggesting potential data entry errors.</p>
                    <div className="flex items-center gap-2 pt-1">
                      <Clock className="w-3 h-3 opacity-30" />
                      <span className="text-[10px] font-bold opacity-30 uppercase">2 mins ago</span>
                    </div>
                  </div>
                </div>
              ))}
              <button className="w-full py-3 rounded-xl border border-outline/20 text-xs font-bold hover:bg-background-base transition-colors duration-200 mt-4">
                View All Insights
              </button>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
