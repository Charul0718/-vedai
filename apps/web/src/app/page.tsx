'use client';

import React, { useState } from 'react';
import { useAuth } from './providers';
import Link from 'next/link';
import { Compass, Moon, Cpu, BookOpen, Key, AlertTriangle, ArrowRight, ShieldCheck, Check } from 'lucide-react';
import { GlassCard, GradientButton, Badge } from '@vedai/ui';

export default function LandingPage() {
  const { token, login, logout, user } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    const endpoint = isRegister ? '/api/auth/register' : '/api/auth/login';
    const payload = isRegister 
      ? { email, password, full_name: fullName } 
      : { email, password };

    try {
      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      if (isRegister) {
        setSuccessMsg('Account created successfully! Please log in.');
        setIsRegister(false);
        setPassword('');
      } else {
        login(data.access_token);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred. Please try again.');
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-background text-slate-100 selection:bg-primary/30">
      {/* Premium Background Effects */}
      <div className="absolute top-[-10%] left-[-10%] h-[600px] w-[600px] rounded-full bg-accent-navy/20 blur-[120px] pointer-events-none animate-pulse-slow" />
      <div className="absolute bottom-[20%] right-[-10%] h-[700px] w-[700px] rounded-full bg-accent-purple/10 blur-[150px] pointer-events-none animate-pulse-slow" />
      <div className="absolute top-[40%] left-[30%] h-[400px] w-[400px] rounded-full bg-primary/5 blur-[100px] pointer-events-none animate-float" />

      {/* Header / Nav */}
      <header className="sticky top-0 z-50 border-b border-primary/10 glass-premium">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center space-x-3">
            <Compass className="h-8 w-8 text-primary animate-spin-slow" />
            <span className="text-2xl font-bold tracking-tight text-white">
              Ved<span className="gold-gradient">AI</span>
            </span>
          </div>

          <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
            <a href="#features" className="hover:text-primary transition">Features</a>
            <a href="#methodology" className="hover:text-primary transition">Methodology</a>
            <a href="#pricing" className="hover:text-primary transition">Pricing</a>
          </nav>

          <div className="flex items-center space-x-4">
            {token ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-slate-300">Hello, {user?.fullName || 'User'}</span>
                <Link href="/dashboard">
                  <button className="px-4 py-2 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow">
                    Go to Dashboard
                  </button>
                </Link>
                <button onClick={logout} className="text-xs text-slate-400 hover:text-primary transition">
                  Logout
                </button>
              </div>
            ) : (
              <a href="#auth-card">
                <button className="px-4 py-2 border border-primary/30 text-primary font-semibold rounded-lg hover:bg-primary/10 transition">
                  Access Portal
                </button>
              </a>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="mx-auto max-w-7xl px-6 pt-20 pb-32">
        <div className="text-center space-y-8 animate-slide-up">
          <div className="inline-flex items-center px-4 py-2 rounded-full border border-primary/30 bg-primary/10">
            <span className="text-sm font-semibold text-primary">✨ AI-Powered Vedic Astrology</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold tracking-tight leading-[1.05] text-white">
            Your Cosmic<br />
            <span className="gold-gradient">
              Blueprint
            </span>
          </h1>

          <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Discover your Vedic birth chart with AI-powered insights. Ancient wisdom meets modern technology.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            {token ? (
              <Link href="/dashboard" className="w-full sm:w-auto">
                <button className="w-full sm:w-auto px-8 py-4 bg-primary text-black font-semibold rounded-xl hover:bg-primary-light transition gold-glow text-lg">
                  Go to Dashboard <ArrowRight className="ml-2 h-5 w-5 inline" />
                </button>
              </Link>
            ) : (
              <>
                <Link href="/onboarding" className="w-full sm:w-auto">
                  <button className="w-full sm:w-auto px-8 py-4 bg-primary text-black font-semibold rounded-xl hover:bg-primary-light transition gold-glow text-lg">
                    Generate My Birth Chart <ArrowRight className="ml-2 h-5 w-5 inline" />
                  </button>
                </Link>
                <a href="#auth-card" className="w-full sm:w-auto">
                  <button className="w-full sm:w-auto px-8 py-4 border border-primary/30 text-primary font-semibold rounded-xl hover:bg-primary/10 transition text-lg">
                    Sign In
                  </button>
                </a>
              </>
            )}
          </div>

          <div className="flex items-center justify-center gap-8 text-sm text-slate-500">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-primary" />
              <span>Swiss Ephemeris</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-primary" />
              <span>Lahiri Ayanamsha</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-primary" />
              <span>AI-Powered</span>
            </div>
          </div>
        </div>
      </main>

      {/* Auth Section */}
      <section id="auth-card" className="mx-auto max-w-md px-6 pb-32">
        {token ? (
          <div className="glass-premium p-8 space-y-6 text-center animate-slide-up">
            <ShieldCheck className="mx-auto h-16 w-16 text-primary animate-glow" />
            <h2 className="text-2xl font-bold text-white">Welcome Back</h2>
            <p className="text-sm text-slate-400">
              You are logged in as {user?.fullName || 'User'}. Access your dashboard to view your charts and insights.
            </p>
            <Link href="/dashboard" className="block w-full">
              <button className="w-full px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow">
                Go to Dashboard <ArrowRight className="ml-2 h-4 w-4 inline" />
              </button>
            </Link>
          </div>
        ) : (
          <div className="glass-premium p-8 space-y-6 animate-slide-up">
            <div>
              <h3 className="text-xl font-bold text-white">
                {isRegister ? 'Create Account' : 'Sign In'}
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                {isRegister 
                  ? 'Start your cosmic journey today' 
                  : 'Access your personalized insights'}
              </p>
            </div>

            {errorMsg && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs p-3 rounded-lg flex items-center space-x-2">
                <AlertTriangle className="h-4 w-4 shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            {successMsg && (
              <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs p-3 rounded-lg flex items-center space-x-2">
                <ShieldCheck className="h-4 w-4 shrink-0" />
                <span>{successMsg}</span>
              </div>
            )}

            <form onSubmit={handleAuthSubmit} className="space-y-4">
              {isRegister && (
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">FULL NAME</label>
                  <input
                    type="text"
                    required
                    placeholder="Your name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full rounded-lg border border-primary/20 bg-surface/50 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
                  />
                </div>
              )}

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1.5">EMAIL</label>
                <input
                  type="email"
                  required
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-lg border border-primary/20 bg-surface/50 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1.5">PASSWORD</label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-lg border border-primary/20 bg-surface/50 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
                />
              </div>

              <button type="submit" className="w-full px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow">
                {isRegister ? 'Create Account' : 'Sign In'}
              </button>
            </form>

            <div className="text-center">
              <button
                onClick={() => {
                  setIsRegister(!isRegister);
                  setErrorMsg('');
                  setSuccessMsg('');
                }}
                className="text-xs text-primary hover:underline"
              >
                {isRegister 
                  ? 'Already have an account? Sign in' 
                  : "Don't have an account? Create one"}
              </button>
            </div>
          </div>
        )}
      </section>

      {/* Features Grid */}
      <section id="features" className="mx-auto max-w-7xl px-6 py-24 border-t border-primary/10">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white">How It Works</h2>
          <p className="text-slate-400 text-sm mt-4">
            Three layers of astrological intelligence working together
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass-card p-8 space-y-4 hover:border-primary/30 transition">
            <div className="h-12 w-12 rounded-xl bg-accent-navy/20 flex items-center justify-center text-primary">
              <Cpu className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Precise Calculations</h3>
            <p className="text-sm text-slate-400">
              Swiss Ephemeris engine computes exact planetary positions using Lahiri Ayanamsha for Vedic accuracy.
            </p>
          </div>

          <div className="glass-card p-8 space-y-4 hover:border-primary/30 transition">
            <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <BookOpen className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Traditional Wisdom</h3>
            <p className="text-sm text-slate-400">
              Classical interpretations from Brihat Parashara and ancient Sanskrit scriptures.
            </p>
          </div>

          <div className="glass-card p-8 space-y-4 hover:border-primary/30 transition">
            <div className="h-12 w-12 rounded-xl bg-accent-purple/20 flex items-center justify-center text-primary">
              <Moon className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">AI Insights</h3>
            <p className="text-sm text-slate-400">
              Google Gemini synthesizes calculations and wisdom into personalized, actionable guidance.
            </p>
          </div>
        </div>
      </section>

      {/* Methodology Section */}
      <section id="methodology" className="mx-auto max-w-5xl px-6 py-20 border-t border-primary/10 glass-premium rounded-3xl">
        <div className="text-center mb-12">
          <h2 className="text-2xl font-bold text-white">VedAI Clean Architecture Boundaries</h2>
          <p className="text-xs text-slate-400 mt-2">
            The platform architecture isolates calculations from interpretative layers to maintain scientific integrity.
          </p>
        </div>

        {/* Process Flow mockup */}
        <div className="flex flex-col md:flex-row items-center justify-around gap-6 text-center">
          <div className="bg-surface/60 border border-primary/20 rounded-xl p-4 w-full md:w-60">
            <span className="text-xs font-semibold text-primary block mb-1">INPUT STAGE</span>
            <span className="text-sm font-bold text-white">Birth Date, Time, Location</span>
          </div>
          <ArrowRight className="hidden md:block h-6 w-6 text-primary" />
          <div className="bg-surface/60 border border-primary/20 rounded-xl p-4 w-full md:w-60">
            <span className="text-xs font-semibold text-primary block mb-1">CALCULATION LAYER</span>
            <span className="text-sm font-bold text-white">Sidereal Longitudes (Lahiri)</span>
          </div>
          <ArrowRight className="hidden md:block h-6 w-6 text-primary" />
          <div className="bg-surface/60 border border-primary/20 rounded-xl p-4 w-full md:w-60">
            <span className="text-xs font-semibold text-primary block mb-1">INTERPRETATION ENGINE</span>
            <span className="text-sm font-bold text-white">Text Translations + AI Guide</span>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="mx-auto max-w-7xl px-6 py-24 border-t border-primary/10">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-white">SaaS Pricing Plans</h2>
          <p className="text-slate-400 text-sm mt-2">
            Generate unlimited charts or purchase comprehensive AI compiled reports.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div className="glass-card p-8 space-y-6">
            <div>
              <span className="text-xs font-semibold text-primary tracking-wider uppercase">STANDARD</span>
              <h3 className="text-2xl font-bold text-white mt-1">Cosmic Explorer</h3>
              <div className="mt-4 flex items-baseline">
                <span className="text-4xl font-extrabold text-white">$0</span>
                <span className="text-sm text-slate-400 ml-2">/ lifetime</span>
              </div>
            </div>
            <p className="text-xs text-slate-400">Perfect for checking basic placements and charts.</p>
            <ul className="space-y-3 text-xs text-slate-300">
              <li className="flex items-center"><Check className="h-4 w-4 text-primary mr-2" /> Unlimited D1 Rasi Charts</li>
              <li className="flex items-center"><Check className="h-4 w-4 text-primary mr-2" /> Basic Planetary Coordinates</li>
              <li className="flex items-center"><Check className="h-4 w-4 text-primary mr-2" /> Standard Traditional Interpretations</li>
            </ul>
            <a href="#auth-card" className="block text-center bg-surface/50 border border-primary/20 py-2.5 rounded-xl text-xs hover:bg-surface transition">
              Get Started
            </a>
          </div>

          <div className="glass-premium p-8 space-y-6 border-primary/30 relative">
            <div className="absolute -top-3 right-4">
              <span className="px-3 py-1 bg-primary text-black text-xs font-bold rounded-full">RECOMMENDED</span>
            </div>
            <div>
              <span className="text-xs font-semibold text-primary tracking-wider uppercase">PREMIUM</span>
              <h3 className="text-2xl font-bold text-white mt-1">VedAI Oracle</h3>
              <div className="mt-4 flex items-baseline">
                <span className="text-4xl font-extrabold text-white">$19</span>
                <span className="text-sm text-slate-400 ml-2">/ month</span>
              </div>
            </div>
            <p className="text-xs text-slate-400">Unlock full AI narrative interpretations and downloads.</p>
            <ul className="space-y-3 text-xs text-slate-300">
              <li className="flex items-center"><Check className="h-4 w-4 text-primary mr-2" /> Advanced AI Synthesized Reports</li>
              <li className="flex items-center"><Check className="h-4 w-4 text-primary mr-2" /> Downloadable High Fidelity PDFs</li>
              <li className="flex items-center"><Check className="h-4 w-4 text-primary mr-2" /> Unlimited Chat with AI Astrologer</li>
              <li className="flex items-center"><Check className="h-4 w-4 text-primary mr-2" /> Custom Ayanamsha configurations</li>
            </ul>
            <a href="#auth-card" className="block">
              <button className="w-full px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow">
                Subscribe Now
              </button>
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-primary/10 bg-surface/60 py-12 text-slate-500 text-xs">
        <div className="mx-auto max-w-7xl px-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <Compass className="h-6 w-6 text-primary" />
              <span className="text-lg font-bold text-white">VedAI</span>
            </div>
            <p className="max-w-md">
              Disclaimer: Vedic Astrology is a traditional system of symbolic analysis and reflection. 
              Interpretations are not scientifically verified predictions, nor should they substitute for professional financial, legal, or medical advice.
            </p>
          </div>
          <div className="md:text-right space-y-2">
            <p>© {new Date().getFullYear()} VedAI SaaS. All rights reserved.</p>
            <p>Clean Monorepo Architecture • Next.js 15 • FastAPI</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
