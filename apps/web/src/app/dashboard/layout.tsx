'use client';

import React from 'react';
import { useAuth } from '../providers';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Compass, User, FileText, MessageSquare, Settings, LogOut, Loader2, ArrowLeft, TrendingUp } from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { token, user, isLoading, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="flex h-screen w-screen flex-col items-center justify-center bg-background text-slate-100">
        <div className="w-10 h-10 border-2 border-primary border-t-transparent rounded-full animate-spin" />
        <p className="mt-4 text-sm text-slate-400">Loading your cosmic alignment...</p>
      </div>
    );
  }

  if (!token) {
    return (
      <div className="flex h-screen w-screen flex-col items-center justify-center bg-background text-slate-100 p-6 text-center">
        <div className="max-w-md space-y-6">
          <h2 className="text-3xl font-extrabold text-white">Access Unauthorized</h2>
          <p className="text-sm text-slate-400">
            Please log in or register on the homepage to access your personalized Vedic dashboard.
          </p>
          <button
            onClick={() => router.push('/')}
            className="inline-flex items-center space-x-2 rounded-xl bg-primary px-6 py-3 text-sm font-semibold text-black shadow-lg hover:bg-primary-light transition"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Return to Homepage</span>
          </button>
        </div>
      </div>
    );
  }

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: Compass },
    { name: 'Ask VedAI', href: '/dashboard/chat', icon: MessageSquare },
    { name: 'Reports', href: '/dashboard/report', icon: FileText },
    { name: 'Timeline', href: '/dashboard/timeline', icon: TrendingUp },
    { name: 'Settings', href: '/dashboard/settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen bg-background text-slate-100 overflow-hidden">
      {/* Sidebar Navigation */}
      <aside className="hidden md:flex flex-col w-64 border-r border-primary/10 glass-premium shrink-0">
        <div className="p-6 flex items-center space-x-3 border-b border-primary/10">
          <Compass className="h-6 w-6 text-primary animate-spin-slow" />
          <span className="text-xl font-bold tracking-tight text-white">
            Ved<span className="gold-gradient">AI</span>
          </span>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link key={item.name} href={item.href}>
                <div
                  className={`flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium transition duration-200 cursor-pointer ${
                    isActive 
                      ? "bg-primary/10 text-primary border border-primary/30" 
                      : "text-slate-400 hover:text-white hover:bg-surface/50"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </div>
              </Link>
            );
          })}
        </nav>

        {/* User profile footer */}
        <div className="p-4 border-t border-primary/10 bg-surface/30">
          <div className="flex items-center justify-between">
            <div className="truncate pr-2">
              <p className="text-xs font-semibold text-white truncate">{user?.fullName}</p>
              <p className="text-[10px] text-slate-400 truncate">{user?.email}</p>
            </div>
            <button
              onClick={logout}
              className="p-2 rounded-lg bg-surface/50 text-slate-400 hover:text-white hover:bg-primary/10 hover:text-primary transition"
              title="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main viewport */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top greeting bar (Mobile toggle holder) */}
        <header className="flex md:hidden items-center justify-between px-6 py-4 border-b border-primary/10 glass-premium">
          <div className="flex items-center space-x-3">
            <Compass className="h-6 w-6 text-primary" />
            <span className="text-lg font-bold text-white">Ved<span className="gold-gradient">AI</span></span>
          </div>
          <button onClick={logout} className="text-xs text-slate-400 hover:text-primary flex items-center space-x-1">
            <LogOut className="h-4 w-4" />
            <span>Logout</span>
          </button>
        </header>

        {/* Content pane */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          <div className="mx-auto max-w-6xl">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
