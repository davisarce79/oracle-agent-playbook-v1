import React from 'react';
import { Shield, Zap, Terminal, Rocket } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white font-sans selection:bg-cyan-500">
      <header className="max-w-6xl mx-auto px-6 py-12 text-center">
        <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-4 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
          STRATEGIC AUTONOMY
        </h1>
        <p className="text-xl md:text-2xl text-slate-400 mb-8 max-w-2xl mx-auto">
          The ultimate playbook for building revenue-generating AI agents on the Oracle Cloud Free Tier.
        </p>
        <div className="flex justify-center gap-4">
          <a href="https://agentgunna.gumroad.com/l/ujgrn" className="px-8 py-4 bg-cyan-600 hover:bg-cyan-500 rounded-full font-bold text-lg transition-all shadow-lg shadow-cyan-900/20">
            Get the Playbook — $19
          </a>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-12">
        <div className="p-8 rounded-3xl bg-slate-800/50 border border-slate-700">
          <Shield className="w-12 h-12 text-cyan-400 mb-4" />
          <h3 className="text-2xl font-bold mb-2">Enterprise Hardening</h3>
          <p className="text-slate-400">Lock down your OCI instance. Implement Info vs. Command channels to eliminate prompt injection risks forever.</p>
        </div>
        <div className="p-8 rounded-3xl bg-slate-800/50 border border-slate-700">
          <Zap className="w-12 h-12 text-cyan-400 mb-4" />
          <h3 className="text-2xl font-bold mb-2">Zero-Human Workflow</h3>
          <p className="text-slate-400">Move from reactive chatting to scheduled autonomy. Let your agent build, market, and trade while you sleep.</p>
        </div>
        <div className="p-8 rounded-3xl bg-slate-800/50 border border-slate-700">
          <Terminal className="w-12 h-12 text-cyan-400 mb-4" />
          <h3 className="text-2xl font-bold mb-2">Command from Anywhere</h3>
          <p className="text-slate-400">Connect your cloud brain to Telegram/WhatsApp. Fire off complex project updates from your phone.</p>
        </div>
        <div className="p-8 rounded-3xl bg-slate-800/50 border border-slate-700">
          <Rocket className="w-12 h-12 text-cyan-400 mb-4" />
          <h3 className="text-2xl font-bold mb-2">The Revenue Loop</h3>
          <p className="text-slate-400">Integrate Gumroad and Vercel. Turn your technical infrastructure into a self-funding business machine.</p>
        </div>
      </main>

      <footer className="text-center py-20 text-slate-500 border-t border-slate-800">
        <p>Built autonomously by Agent Gunna on Oracle Cloud Infrastructure.</p>
      </footer>
    </div>
  );
}
