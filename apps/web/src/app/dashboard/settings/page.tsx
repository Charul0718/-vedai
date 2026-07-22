'use client';

import React, { useState } from 'react';
import { useAuth } from '../../providers';
import { Settings, Shield, Compass, Sparkles, Database, User, Bell, Lock } from 'lucide-react';

export default function SettingsPage() {
  const { user } = useAuth();
  const [ayanamsha, setAyanamsha] = useState('lahiri');

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Title */}
      <div>
        <h1 className="text-4xl font-extrabold text-white">
          Profile <span className="gold-gradient">Settings</span>
        </h1>
        <p className="text-slate-400 text-sm mt-2">Configure your preferences, calculation parameters, and account details.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left configurations column */}
        <div className="lg:col-span-8 space-y-6">
          {/* Profile Section */}
          <div className="glass-premium p-6 space-y-6">
            <div className="flex items-center space-x-3 border-b border-primary/10 pb-4">
              <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                <User className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-bold text-white">Profile Information</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
              <div>
                <span className="text-xs text-slate-400 block font-semibold mb-1">FULL NAME</span>
                <span className="text-white font-semibold block">{user?.fullName}</span>
              </div>
              <div>
                <span className="text-xs text-slate-400 block font-semibold mb-1">EMAIL ADDRESS</span>
                <span className="text-white font-semibold block">{user?.email}</span>
              </div>
              <div>
                <span className="text-xs text-slate-400 block font-semibold mb-1">MEMBERSHIP</span>
                <span className="px-2 py-1 bg-primary/10 border border-primary/30 text-primary text-xs rounded-full inline-block">Standard</span>
              </div>
              <div>
                <span className="text-xs text-slate-400 block font-semibold mb-1">MEMBER SINCE</span>
                <span className="text-white font-semibold block">January 2026</span>
              </div>
            </div>
          </div>

          {/* Astrological engine settings */}
          <div className="glass-premium p-6 space-y-6">
            <div className="flex items-center space-x-3 border-b border-primary/10 pb-4">
              <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                <Compass className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-bold text-white">Calculation Parameters</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-3">SIDEREAL AYANAMSHA SYSTEM</label>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {[
                    { id: 'lahiri', name: 'Lahiri (Chitra Paksha)', desc: 'Standard Vedic system. Corrected to Spica star.' },
                    { id: 'raman', name: 'B.V. Raman', desc: 'Traditional Indian calculation with different epoch.' },
                    { id: 'fagan', name: 'Fagan-Bradley', desc: 'Western sidereal standard. Synced to Aldebaran.' }
                  ].map((sys) => (
                    <button
                      key={sys.id}
                      type="button"
                      onClick={() => setAyanamsha(sys.id)}
                      className={`p-4 rounded-xl border text-left transition space-y-2 ${
                        ayanamsha === sys.id 
                          ? 'bg-primary/10 border-primary/30 text-white' 
                          : 'bg-surface/50 border-primary/10 text-slate-400 hover:bg-surface'
                      }`}
                    >
                      <span className="font-bold text-sm block">{sys.name}</span>
                      <p className="text-xs leading-relaxed">{sys.desc}</p>
                    </button>
                  ))}
                </div>
              </div>

              <div className="glass-card p-4 text-xs text-slate-300 space-y-2">
                <span className="font-bold text-primary block">About Ayanamsha</span>
                <p className="leading-relaxed">
                  Due to the precession of Earth's axis, the tropical zodiac shifts relative to stars. 
                  The Ayanamsha is the offset degrees (~24° in modern times). Lahiri is the official system used by the Indian Calendar Reform Committee.
                </p>
              </div>
            </div>
          </div>

          {/* Security Settings */}
          <div className="glass-premium p-6 space-y-6">
            <div className="flex items-center space-x-3 border-b border-primary/10 pb-4">
              <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                <Lock className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-bold text-white">Security</h3>
            </div>

            <div className="space-y-3">
              <button className="w-full flex items-center justify-between p-4 glass-card rounded-xl hover:border-primary/30 transition">
                <div className="flex items-center space-x-3">
                  <Shield className="h-5 w-5 text-primary" />
                  <div className="text-left">
                    <span className="text-sm font-semibold text-white block">Change Password</span>
                    <span className="text-xs text-slate-400">Update your account password</span>
                  </div>
                </div>
              </button>
              <button className="w-full flex items-center justify-between p-4 glass-card rounded-xl hover:border-primary/30 transition">
                <div className="flex items-center space-x-3">
                  <Bell className="h-5 w-5 text-primary" />
                  <div className="text-left">
                    <span className="text-sm font-semibold text-white block">Notification Preferences</span>
                    <span className="text-xs text-slate-400">Manage email and push notifications</span>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Right info details */}
        <div className="lg:col-span-4 space-y-6">
          <div className="glass-premium p-6 space-y-4">
            <h3 className="font-bold text-white border-b border-primary/10 pb-3 text-sm flex items-center space-x-2">
              <Database className="h-4.5 w-4.5 text-primary" />
              <span>System Information</span>
            </h3>
            
            <div className="space-y-3 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Backend</span>
                <span className="font-semibold text-white">FastAPI</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Database</span>
                <span className="font-semibold text-white">SQLite</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">AI Engine</span>
                <span className="font-semibold text-white">Gemini</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Framework</span>
                <span className="font-semibold text-white">Next.js 15</span>
              </div>
            </div>
          </div>

          <div className="glass-card bg-primary/5 border-primary/20 p-6 space-y-3">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <h4 className="font-bold text-white text-sm">Premium Features</h4>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Upgrade to VedAI Oracle for unlimited AI chat, downloadable PDF reports, and custom Ayanamsha configurations.
            </p>
            <button className="w-full px-4 py-2 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow text-sm">
              Upgrade Now
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
