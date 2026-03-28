import MainLayout from '@/components/MainLayout';
import { 
  Settings as SettingsIcon, 
  Key, 
  Shield, 
  User, 
  Paintbrush, 
  Database,
  Check,
  ChevronRight
} from 'lucide-react';
import { cn } from '@/lib/utils';

const settingsSections = [
  { 
    id: 'account', 
    title: 'Profile & Account', 
    icon: User, 
    description: 'Manage your connected accounts and personal details.' 
  },
  { 
    id: 'security', 
    title: 'API Keys & Secrets', 
    icon: Key, 
    description: 'Configure Groq, Gemini, and other AI provider keys.' 
  },
  { 
    id: 'appearance', 
    title: 'System Interface', 
    icon: Paintbrush, 
    description: 'Personalize the theme, density, and animations of Nexus Noir.' 
  },
  { 
    id: 'storage', 
    title: 'Data Nexus Storage', 
    icon: Database, 
    description: 'Manage your local and cloud datasets connections.' 
  },
  { 
    id: 'privacy', 
    title: 'Security & Privacy', 
    icon: Shield, 
    description: 'Control data encryption and access permissions.' 
  }
];

export default function SettingsPage() {
  return (
    <MainLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <header>
          <h1 className="text-3xl font-display font-bold text-on-background tracking-tight">System Configuration</h1>
          <p className="text-on-background/50 font-medium">Manage your DataNexus AI environment and security.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <aside className="space-y-1">
            {settingsSections.map((section) => (
              <button 
                key={section.id} 
                className={cn(
                  "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group text-sm font-semibold",
                  section.id === 'security' ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'hover:bg-surface text-on-background/60 hover:text-primary'
                )}
              >
                <section.icon className="w-5 h-5" />
                <span>{section.title}</span>
              </button>
            ))}
          </aside>

          <main className="lg:col-span-3 space-y-6">
            <div className="bg-surface rounded-2xl border border-outline/10 tonal-lift p-8">
              <h2 className="text-xl font-display font-bold mb-6 flex items-center gap-2">
                <Key className="w-5 h-5 text-primary" />
                API Integration
              </h2>
              <div className="space-y-6 max-w-2xl">
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-on-background/40 uppercase tracking-wider">Groq API Key</label>
                    <div className="relative group">
                      <input 
                        type="password" 
                        defaultValue="••••••••••••••••••••••••"
                        className="w-full h-11 bg-surface-low border border-outline/20 rounded-xl px-4 text-sm font-mono focus:outline-none focus:border-primary transition-all group-focus-within:border-primary/50"
                      />
                      <div className="absolute right-3 top-1/2 -translate-y-1/2 px-2 py-1 bg-green-50 text-green-600 rounded-md text-[10px] font-bold border border-green-200">
                        ACTIVE
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-on-background/40 uppercase tracking-wider">Gemini API Key</label>
                    <input 
                      type="password" 
                      placeholder="Enter your Gemini Key"
                      className="w-full h-11 bg-surface-low border border-outline/20 rounded-xl px-4 text-sm font-mono focus:outline-none focus:border-primary transition-all"
                    />
                  </div>
                </div>

                <div className="pt-4 flex items-center gap-3">
                  <button className="px-6 py-2.5 rounded-xl gradient-cta text-white font-bold text-sm shadow-md shadow-primary/10 hover:scale-[1.02] transition-all">
                    Save Changes
                  </button>
                  <button className="px-6 py-2.5 rounded-xl border border-outline/20 text-xs font-bold hover:bg-background-base transition-colors">
                    Reset to Default
                  </button>
                </div>
              </div>
            </div>

            <div className="bg-surface rounded-2xl border border-outline/10 tonal-lift p-8 glass">
              <h2 className="text-xl font-display font-bold mb-6 flex items-center gap-2">
                <Paintbrush className="w-5 h-5 text-primary" />
                Appearance
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border-2 border-primary rounded-xl bg-primary/5 flex items-center justify-between group cursor-pointer transition-all">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-surface flex items-center justify-center border border-primary/20">
                      <div className="w-6 h-6 rounded-full bg-on-background" />
                    </div>
                    <div>
                      <p className="text-sm font-bold">Nexus Noir (Dark)</p>
                      <p className="text-[10px] font-bold opacity-40">System Default</p>
                    </div>
                  </div>
                  <div className="w-5 h-5 rounded-full bg-primary flex items-center justify-center">
                    <Check className="w-3 h-3 text-white" />
                  </div>
                </div>

                <div className="p-4 border border-outline/20 rounded-xl hover:border-primary/50 transition-all cursor-pointer flex items-center justify-between group">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-surface flex items-center justify-center border border-outline/10">
                      <div className="w-6 h-6 rounded-full bg-background-base" />
                    </div>
                    <div>
                      <p className="text-sm font-bold opacity-60 group-hover:opacity-100 transition-opacity">Arctic Light</p>
                      <p className="text-[10px] font-bold opacity-40 uppercase">Coming Soon</p>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 opacity-20" />
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </MainLayout>
  );
}
