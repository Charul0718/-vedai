'use client';

import React from 'react';
import { useAuth } from '../providers';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { UserPlus, FileText, MessageSquare, ShieldAlert, Sparkles, Compass, TrendingUp, Calendar, Clock, MapPin } from 'lucide-react';

export default function DashboardOverview() {
  const { token, user } = useAuth();

  // Fetch birth profiles
  const { data: profiles, isLoading: loadingProfiles } = useQuery({
    queryKey: ['birth-details'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/birth-details', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to load profiles');
      return res.json();
    },
    enabled: !!token
  });

  const activeProfile = profiles && profiles.length > 0 ? profiles[0] : null;

  // Fetch chart for active profile
  const { data: chart, isLoading: loadingChart } = useQuery({
    queryKey: ['chart', activeProfile?.id],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/birth-details/${activeProfile.id}/chart`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to load chart');
      return res.json();
    },
    enabled: !!token && !!activeProfile
  });

  if (loadingProfiles) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Greetings Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold text-white">
            Good {new Date().getHours() < 12 ? 'morning' : new Date().getHours() < 18 ? 'afternoon' : 'evening'}, <span className="gold-gradient">{user?.fullName?.split(' ')[0]}</span>
          </h1>
          <p className="text-slate-400 text-sm mt-2">Your cosmic insights are ready</p>
        </div>
        <Link href="/onboarding">
          <button className="px-4 py-2 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow text-sm">
            + New Chart
          </button>
        </Link>
      </div>

      {!activeProfile ? (
        /* Empty State */
        <div className="glass-premium p-16 text-center space-y-6 animate-slide-up">
          <div className="mx-auto h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary animate-glow">
            <UserPlus className="h-8 w-8" />
          </div>
          <div className="space-y-3">
            <h3 className="text-2xl font-bold text-white">Start Your Journey</h3>
            <p className="text-slate-400 text-sm max-w-md mx-auto">
              Create your birth chart to unlock personalized astrological insights
            </p>
          </div>
          <Link href="/onboarding">
            <button className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow">
              Create Birth Chart
            </button>
          </Link>
        </div>
      ) : (
        /* Modern Dashboard Layout */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Profile Card */}
          <div className="glass-premium p-6 space-y-4">
            <div className="flex items-center space-x-3">
              <div className="h-12 w-12 rounded-full bg-gradient-to-br from-primary to-primary-light flex items-center justify-center text-black font-bold text-lg">
                {activeProfile.name?.charAt(0)}
              </div>
              <div>
                <h3 className="font-semibold text-white">{activeProfile.name}</h3>
                <p className="text-xs text-slate-400">Birth Profile</p>
              </div>
            </div>
            <div className="pt-4 space-y-3">
              <div className="flex items-center space-x-2 text-sm">
                <Calendar className="h-4 w-4 text-primary" />
                <span className="text-slate-300">{activeProfile.date_of_birth}</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <Clock className="h-4 w-4 text-primary" />
                <span className="text-slate-300">{activeProfile.time_of_birth}</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <MapPin className="h-4 w-4 text-primary" />
                <span className="text-slate-300 truncate">{activeProfile.location_name}</span>
              </div>
            </div>
          </div>

          {/* Key Insights Card */}
          <div className="glass-premium p-6 space-y-4">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <h3 className="font-semibold text-white">Key Insights</h3>
            </div>
            {loadingChart ? (
              <div className="flex h-24 items-center justify-center">
                <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
              </div>
            ) : chart ? (
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Ascendant</span>
                  <span className="font-semibold gold-gradient">{chart.ascendantSign}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Moon Sign</span>
                  <span className="font-semibold text-white">{chart.moonSign}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Nakshatra</span>
                  <span className="font-semibold text-primary">{chart.moonNakshatra}</span>
                </div>
              </div>
            ) : null}
          </div>

          {/* Current Dasha Card */}
          <div className="glass-premium p-6 space-y-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-primary" />
              <h3 className="font-semibold text-white">Current Dasha</h3>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-400">Major</span>
                <span className="font-semibold text-white">Jupiter</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-400">Sub</span>
                <span className="font-semibold text-primary">Saturn</span>
              </div>
              <div className="w-full bg-surface rounded-full h-2">
                <div className="bg-primary h-2 rounded-full transition-all" style={{ width: '45%' }} />
              </div>
              <span className="text-xs text-slate-500">45% complete</span>
            </div>
          </div>

          {/* Quick Action Cards */}
          <Link href="/dashboard/chat" className="glass-card p-6 hover:border-primary/30 transition group cursor-pointer">
            <div className="flex items-center space-x-4">
              <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary group-hover:scale-110 transition">
                <MessageSquare className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-white">Ask VedAI</h4>
                <p className="text-xs text-slate-400">Chat with your AI guide</p>
              </div>
            </div>
          </Link>

          <Link href="/dashboard/report" className="glass-card p-6 hover:border-primary/30 transition group cursor-pointer">
            <div className="flex items-center space-x-4">
              <div className="h-12 w-12 rounded-xl bg-accent-purple/10 flex items-center justify-center text-primary group-hover:scale-110 transition">
                <FileText className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-white">Reports</h4>
                <p className="text-xs text-slate-400">Detailed analysis</p>
              </div>
            </div>
          </Link>

          <Link href="/dashboard/timeline" className="glass-card p-6 hover:border-primary/30 transition group cursor-pointer">
            <div className="flex items-center space-x-4">
              <div className="h-12 w-12 rounded-xl bg-accent-navy/10 flex items-center justify-center text-primary group-hover:scale-110 transition">
                <TrendingUp className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-white">Timeline</h4>
                <p className="text-xs text-slate-400">Dasha periods</p>
              </div>
            </div>
          </Link>

          {/* Planetary Positions - Full Width */}
          <div className="md:col-span-2 lg:col-span-3 glass-premium p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Compass className="h-5 w-5 text-primary" />
                <h3 className="font-semibold text-white">Planetary Positions</h3>
              </div>
              <span className="text-xs text-slate-400">Lahiri Ayanamsha</span>
            </div>
            {loadingChart ? (
              <div className="flex h-24 items-center justify-center">
                <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
              </div>
            ) : chart ? (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {chart.planets?.slice(0, 6).map((p: any) => (
                  <div key={p.planetName} className="glass-card p-3 text-center">
                    <span className="text-[10px] text-slate-400 block mb-1">{p.planet_name || p.planetName}</span>
                    <span className="text-sm font-semibold text-white block">{p.sign}</span>
                    <span className="text-xs text-primary">{p.degree?.toFixed(1)}°</span>
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
