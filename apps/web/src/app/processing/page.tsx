'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Compass, Cpu, Moon, BookOpen, Sparkles, CheckCircle, Globe, Star } from 'lucide-react';
import Link from 'next/link';

export default function ProcessingScreen() {
  const router = useRouter();
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [showPreview, setShowPreview] = useState(false);

  const processingSteps = [
    { icon: Globe, title: 'Calculating Planetary Positions', description: 'Using Swiss Ephemeris for precise astronomical calculations' },
    { icon: Moon, title: 'Computing House Cusps', description: 'Determining ascendant and 12 house divisions' },
    { icon: BookOpen, title: 'Analyzing Traditional Yogas', description: 'Identifying planetary combinations and their effects' },
    { icon: Sparkles, title: 'Generating AI Insights', description: 'Synthesizing data into personalized interpretations' },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            router.push('/dashboard');
          }, 1500);
          return 100;
        }
        return prev + 1;
      });
    }, 40);

    return () => clearInterval(interval);
  }, [router]);

  useEffect(() => {
    const stepIndex = Math.floor(progress / 25);
    setCurrentStep(stepIndex);
    if (progress > 60) {
      setShowPreview(true);
    }
  }, [progress]);

  return (
    <div className="min-h-screen bg-background text-slate-100 overflow-hidden flex flex-col">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] h-[800px] w-[800px] rounded-full bg-accent-navy/10 blur-[150px] pointer-events-none animate-pulse-slow" />
        <div className="absolute bottom-[-10%] right-[-10%] h-[600px] w-[600px] rounded-full bg-accent-purple/10 blur-[120px] pointer-events-none animate-pulse-slow" style={{ animationDelay: '1s' }} />
        <div className="absolute top-[30%] right-[20%] h-[300px] w-[300px] rounded-full bg-primary/5 blur-[80px] pointer-events-none animate-float" />
        {/* Floating stars */}
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-primary/30 rounded-full animate-pulse"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 2}s`,
              animationDuration: `${2 + Math.random() * 2}s`
            }}
          />
        ))}
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-primary/10 glass-premium">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center space-x-3">
            <Compass className="h-8 w-8 text-primary animate-spin-slow" />
            <span className="text-2xl font-bold tracking-tight text-white">
              Ved<span className="gold-gradient">AI</span>
            </span>
          </Link>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            <span className="text-sm text-slate-400">Building Your Cosmic Blueprint</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="max-w-4xl w-full space-y-8">
          {/* Progress Circle */}
          <div className="relative w-48 h-48 mx-auto">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="96"
                cy="96"
                r="88"
                stroke="rgba(212, 175, 55, 0.1)"
                strokeWidth="6"
                fill="none"
              />
              <circle
                cx="96"
                cy="96"
                r="88"
                stroke="url(#gradient)"
                strokeWidth="6"
                fill="none"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 88}`}
                strokeDashoffset={`${2 * Math.PI * 88 * (1 - progress / 100)}`}
                className="transition-all duration-300"
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#D4AF37" />
                  <stop offset="50%" stopColor="#F4D03F" />
                  <stop offset="100%" stopColor="#B8960C" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-bold text-white">{progress}</span>
              <span className="text-sm text-slate-400 mt-1">%</span>
            </div>
          </div>

          {/* Current Step Display */}
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-bold text-white animate-slide-up">
              {processingSteps[currentStep]?.title}
            </h2>
            <p className="text-slate-400 animate-slide-up" style={{ animationDelay: '0.1s' }}>
              {processingSteps[currentStep]?.description}
            </p>
          </div>

          {/* Processing Steps */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {processingSteps.map((step, index) => {
              const StepIcon = step.icon;
              const isActive = index === currentStep;
              const isCompleted = index < currentStep;
              const isPending = index > currentStep;

              return (
                <div
                  key={index}
                  className={`glass-card p-4 rounded-xl flex flex-col items-center text-center space-y-3 transition-all ${
                    isActive ? 'border-primary/50 bg-primary/10 scale-105' : 
                    isCompleted ? 'border-primary/30 bg-primary/5' : 
                    'border-primary/10 opacity-40'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all ${
                    isActive ? 'bg-primary text-black animate-glow' :
                    isCompleted ? 'bg-primary/20 text-primary' :
                    'bg-surface text-slate-500'
                  }`}>
                    {isCompleted ? (
                      <CheckCircle className="h-5 w-5" />
                    ) : (
                      <StepIcon className="h-5 w-5" />
                    )}
                  </div>
                  <div>
                    <h3 className={`font-semibold text-sm ${
                      isActive ? 'text-white' : isCompleted ? 'text-primary' : 'text-slate-500'
                    }`}>
                      {step.title}
                    </h3>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Live Data Preview */}
          {showPreview && (
            <div className="glass-premium p-6 rounded-xl animate-slide-up">
              <div className="flex items-center space-x-2 mb-4">
                <Star className="h-5 w-5 text-primary animate-pulse" />
                <h3 className="text-lg font-semibold text-white">Your Cosmic Blueprint</h3>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="space-y-1">
                  <span className="text-xs text-slate-400 uppercase tracking-wider">Ascendant</span>
                  <span className="text-lg font-semibold gold-gradient block">Scorpio</span>
                  <span className="text-xs text-slate-500">2.47°</span>
                </div>
                <div className="space-y-1">
                  <span className="text-xs text-slate-400 uppercase tracking-wider">Sun</span>
                  <span className="text-lg font-semibold text-primary block">Pisces</span>
                  <span className="text-xs text-slate-500">15th House</span>
                </div>
                <div className="space-y-1">
                  <span className="text-xs text-slate-400 uppercase tracking-wider">Moon</span>
                  <span className="text-lg font-semibold text-primary block">Pisces</span>
                  <span className="text-xs text-slate-500">Uttara Bhadrapada</span>
                </div>
                <div className="space-y-1">
                  <span className="text-xs text-slate-400 uppercase tracking-wider">Dasha</span>
                  <span className="text-lg font-semibold text-white block">Moon</span>
                  <span className="text-xs text-slate-500">Mahadasha</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
