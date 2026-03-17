#!/usr/bin/env python3
"""
Build Me This: Claude Clone (Gunna-Powered Private Chat)

Generates a Next.js app that chats with this Agent Gunna instance via OpenClaw sub-agent.
Includes: chat UI, artifacts pane, code terminal readout.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

import requests

# Use CRFT detection (or fallback) to get base stack, then override to Claude Clone template
BASE_BUILDER = Path('/home/opc/.openclaw/workspace/build_me_this.py')

def run_base_builder(target_url: str, output_dir: Path) -> dict:
    """Run the standard build_me_this to get a base scaffold and plan, then customize."""
    cmd = [sys.executable, str(BASE_BUILDER), target_url, '--output-dir', str(output_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(f"Base builder failed: {result.stderr}")
    # Load build plan from the output dir parent (where build_plan_*.json was saved)
    plan_files = list(output_dir.parent.glob("build_plan_*.json"))
    if plan_files:
        with open(plan_files[-1]) as f:
            plan = json.load(f)
    else:
        plan = {"stack": {"frontend": "Next.js (App Router)", "styling": "Tailwind CSS", "language": "TypeScript"}}
    return plan

def customize_for_claude_clone(output_dir: Path, plan: dict):
    """
    Overlay the Claude Clone specific files and modifications:
    - app/api/chat/route.ts: proxied chat endpoint using OpenClaw sub-agent session
    - app/components/Chat.tsx: main chat UI with streaming
    - app/components/Artifact.tsx: artifact renderer (iframe sandbox)
    - app/components/TerminalPanel.tsx: read-only terminal display
    - app/layout.tsx tweaks: include sidebars
    """
    # Create API route
    api_dir = output_dir / 'app' / 'api' / 'chat'
    api_dir.mkdir(parents=True, exist_ok=True)
    api_route = api_dir / 'route.ts'
    api_route.write_text(API_ROUTE_TS)

    # Create Chat component
    components_dir = output_dir / 'app' / 'components'
    components_dir.mkdir(parents=True, exist_ok=True)
    (components_dir / 'Chat.tsx').write_text(CHAT_TSX)
    (components_dir / 'Artifact.tsx').write_text(ARTIFACT_TSX)
    (components_dir / 'TerminalPanel.tsx').write_text(TERMINAL_TSX)

    # Update main page to use Chat and side panels
    page_tsx = output_dir / 'app' / 'page.tsx'
    page_tsx.write_text(PAGE_TSX)

    # Update layout to include fonts and global styles
    layout_tsx = output_dir / 'app' / 'layout.tsx'
    layout_tsx.write_text(LAYOUT_TSX)

    # Update tailwind to include dark theme colors
    tailwind_config = output_dir / 'tailwind.config.js'
    tailwind_config.write_text(TAILWIND_CONFIG_JS)

    # Add environment variable example
    env_local = output_dir / '.env.local.example'
    env_local.write_text(ENV_LOCAL_EXAMPLE)

    # Update README with Claude Clone instructions
    readme = output_dir / 'README.md'
    readme.write_text(README_TEMPLATE.format(created=datetime.utcnow().isoformat()))

def main():
    parser = argparse.ArgumentParser(description="Generate a Claude Clone scaffold powered by Agent Gunna (OpenClaw).")
    parser.add_argument('url', help='Reference website URL (ignored except for plan metadata)')
    parser.add_argument('--output-dir', default='./claude-clone', help='Output directory')
    args = parser.parse_args()

    target_url = args.url
    output_dir = Path(args.output_dir).resolve()

    print(f"Generating Claude Clone scaffold at: {output_dir}")

    # Step 1: Get base Next.js/Tailwind scaffold
    print("Creating base Next.js scaffold...")
    plan = run_base_builder(target_url, output_dir)

    # Step 2: Apply Claude Clone customizations
    print("Applying Claude Clone customizations...")
    customize_for_claude_clone(output_dir, plan)

    print("\n=== Claude Clone Generated ===")
    print(f"Location: {output_dir}")
    print("Next steps:")
    print("1. cd", output_dir)
    print("2.npm install (or pnpm/yarn)")
    print("3. Copy .env.local.example to .env.local and add OPENCLAW_GATEWAY_URL if needed")
    print("4. npm run dev")
    print("5. Open http://localhost:3000")
    print("\nNote: This uses OpenClaw sub-agent sessions. Ensure the gateway is running and accessible from this app.")

if __name__ == "__main__":
    main()

# === TEMPLATES ===

API_ROUTE_TS = """import { NextRequest, NextResponse } from 'next/server';
import { sessions_spawn, sessions_send, sessions_list } from 'openclaw';

// Maintain a single sub-agent session for the chat
let sessionKey: string | null = null;
const LABEL = 'claude-clone-chat';

async function getOrCreateSession(): Promise<string> {
  if (sessionKey) return sessionKey;
  // Spawn a sub-agent using the main agent runtime
  const resp = await sessions_spawn({
    task: 'You are a helpful AI assistant in a private chat. Respond conversationally.',
    runtime: 'subagent',
    mode: 'session',
    thread: true,
    label: LABEL
  });
  sessionKey = resp.sessionKey;
  return sessionKey;
}

export async function POST(req: NextRequest) {
  try {
    const { message } = await req.json();
    if (!message) return NextResponse.json({ error: 'Missing message' }, { status: 400 });

    const sessKey = await getOrCreateSession();
    // Send user message to the sub-agent
    await sessions_send({ sessionKey: sessKey, message });

    // Wait briefly and read the latest assistant message from that session
    // In production, use streaming via sessions_history or an event stream
    const history = await sessions_history({ sessionKey: sessKey, limit: 10 });
    const latest = history.messages?.[history.messages.length - 1];
    if (!latest || latest.role !== 'assistant') {
      return NextResponse.json({ reply: '(No response yet)' });
    }

    // Check for artifact directives in the message content (e.g., ```artifacts or special markers)
    const content = latest.content as string;
    const artifactMatch = content.match(/```artifacts?\\n([\\s\\S]*?)```/);
    let artifact = null;
    let reply = content;
    if (artifactMatch) {
      artifact = artifactMatch[1].trim();
      reply = content.replace(artifactMatch[0], '').trim();
    }

    return NextResponse.json({ reply, artifact });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
"""

CHAT_TSX = """'use client';
import { useState, useRef, useEffect } from 'react';
import Artifact from './Artifact';
import TerminalPanel from './TerminalPanel';

export default function Chat() {
  const [messages, setMessages] = useState<Array<{role: string, content: string, artifact?: string}>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showArtifacts, setShowArtifacts] = useState(true);
  const [showTerminal, setShowTerminal] = useState(true);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function sendMessage(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput('');
    setMessages(m => [...m, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg })
      });
      const data = await res.json();
      if (data.reply) {
        setMessages(m => [...m, { role: 'assistant', content: data.reply, artifact: data.artifact }]);
      } else {
        setMessages(m => [...m, { role: 'assistant', content: `Error: ${data.error}` }]);
      }
    } catch (err: any) {
      setMessages(m => [...m, { role: 'assistant', content: `Fetch error: ${err.message}` }]);
    }
    setLoading(false);
  }

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      {/* Main Chat Area */}
      <main className={`flex-1 flex flex-col ${showArtifacts ? 'mr-96' : ''} ${showTerminal ? 'pb-64' : ''}`}>
        <header className="p-4 border-b border-gray-700">
          <h1 className="text-xl font-semibold">Private Claude — Gunna Powered</h1>
        </header>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`rounded-lg px-4 py-2 max-w-[80%] ${msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
                <pre className="whitespace-pre-wrap font-sans">{msg.content}</pre>
                {msg.artifact && showArtifacts && (
                  <div className="mt-2 border-t border-gray-600 pt-2">
                    <Artifact code={msg.artifact} />
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <form onSubmit={sendMessage} className="p-4 border-t border-gray-700 flex gap-2">
          <input
            className="flex-1 bg-gray-800 border border-gray-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Send a message…"
            disabled={loading}
          />
          <button type="submit" disabled={loading} className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-medium">
            {loading ? 'Sending…' : 'Send'}
          </button>
        </form>
      </main>

      {/* Artifacts Sidebar */}
      {showArtifacts && (
        <aside className="fixed right-0 top-0 h-full w-96 bg-gray-800 border-l border-gray-700 overflow-y-auto p-4">
          <h2 className="text-lg font-semibold mb-4">Artifacts</h2>
          <div className="space-y-4">
            {messages.filter(m => m.artifact).map((msg, i) => (
              <div key={i} className="bg-gray-900 rounded p-2">
                <Artifact code={msg.artifact!} />
              </div>
            ))}
          </div>
        </aside>
      )}

      {/* Terminal Panel */}
      {showTerminal && (
        <footer className="fixed bottom-0 left-0 right-0 h-64 bg-black bg-opacity-90 border-t border-gray-600 p-2 font-mono text-xs text-green-400 overflow-auto">
          <div className="flex justify-between items-center mb-1">
            <span>Claude Code Terminal (Read‑Only)</span>
            <button onClick={() => setShowTerminal(false)} className="text-gray-400 hover:text-white">_close</button>
          </div>
          <TerminalPanel messages={messages} />
        </footer>
      )}
    </div>
  );
}
"""

ARTIFACT_TSX = """'use client';
import { useState } from 'react';

export default function Artifact({ code }: { code: string }) {
  const [language] = useState('html'); // simplistic: detect later
  // For MVP, we’ll render as plain text with basic syntax highlight could be added
  return (
    <div className="bg-gray-900 rounded p-2 text-sm font-mono overflow-x-auto">
      <pre>{code}</pre>
    </div>
  );
}
"""

TERMINAL_TSX = """'use client';
export default function TerminalPanel({ messages }: { messages: Array<{role: string, content: string}> }) {
  // Concatenate assistant code blocks to simulate terminal output
  const lines = messages.filter(m => m.role === 'assistant')
    .flatMap(m => m.content.split('\\n'))
    .map(line => `<span>${line}</span>`)
    .join('\\n');
  return (
    <pre className="whitespace-pre-wrap" dangerouslySetInnerHTML={{ __html: lines || '# No terminal output yet' }} />
  );
}
"""

PAGE_TSX = """import Chat from './components/Chat';
export default function Home() {
  return <Chat />;
}
"""

LAYOUT_TSX = """export const metadata = {
  title: 'Private Claude — Gunna Powered',
  description: 'A private chat interface powered by Agent Gunna on your own infrastructure.',
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-900 text-gray-100">{children}</body>
    </html>
  );
}
"""

TAILWIND_CONFIG_JS = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
};
"""

ENV_LOCAL_EXAMPLE = """# OpenClaw connection (optional if gateway runs on localhost)
NEXT_PUBLIC_OPENCLAW_URL=http://localhost:3000
# Or full gateway URL if different
# OPENCLAW_GATEWAY_URL=http://localhost:8080
"""

README_TEMPLATE = """# Claude Clone (Gunna-Powered Private Chat)

Inspired by: {target? if any}

This is a private, self-hosted chat UI that talks to Agent Gunna via OpenClaw sub‑agent sessions.

## Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS
- OpenClaw session bridge

## Setup

1. `npm install`
2. Copy `.env.local.example` to `.env.local` if you need to point to a non‑default OpenClaw gateway.
3. `npm run dev`
4. Open http://localhost:3000

## How It Works

- The frontend sends user messages to `/api/chat`.
- The API route spawns a persistent OpenClaw sub‑agent session (label: `claude-clone-chat`) and forwards messages.
- Assistant replies are returned, with optional artifact code blocks.
- Artifacts render in a sandboxed iframe (MVP shows code only).
- A terminal‑style panel displays code snippets from assistant messages.

## Adding Real Artifact Execution

Later, you can extend the artifact renderer to execute JavaScript in a sandbox (e.g., using an iframe with sandbox attributes or a Node VM backend).

## Privacy

All traffic stays on your own infrastructure. No external API calls except to your OpenClaw gateway (which in turn uses OpenRouter).

Generated on {created}
"""

if __name__ == "__main__":
    main()
