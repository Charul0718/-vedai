'use client';

import React, { useState } from 'react';
import { useAuth } from '../../providers';
import { useQuery } from '@tanstack/react-query';
import { TrendingUp, Calendar, Clock, ChevronRight, Sparkles } from 'lucide-react';
import Link from 'next/link';

export default function TimelinePage() {
  const { token } = useAuth();
  const [selectedPeriod, setSelectedPeriod] = useState<'major' | 'minor'>('major');

  // Fetch birth profiles
  const { data: profiles } = useQuery({
    queryKey: ['birth-details'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/birth-details', {
        headers: { Authorization: `Bearer ${token}` }
      });
      return res.json();
    },
    enabled: !!token
  });

  const activeProfile = profiles && profiles.length > 0 ? profiles[0] : null;

  // Sample Vimshottari Dasha data (would come from backend)
  const dashaData = {
    major: [
      { planet: 'Ketu', period: 7, startYear: 1990, endYear: 1997, ageRange: '0-7' },
      { planet: 'Venus', period: 20, startYear: 1997, endYear: 2017, ageRange: '7-27' },
      { planet: 'Sun', period: 6, startYear: 2017, endYear: 2023, ageRange: '27-33' },
      { planet: 'Moon', period: 10, startYear: 2023, endYear: 2033, ageRange: '33-43', current: true },
      { planet: 'Mars', period: 7, startYear: 2033, endYear: 2040, ageRange: '43-50' },
      { planet: 'Rahu', period: 18, startYear: 2040, endYear: 2058, ageRange: '50-68' },
      { planet: 'Jupiter', period: 16, startYear: 2058, endYear: 2074, ageRange: '68-84' },
      { planet: 'Saturn', period: 19, startYear: 2074, endYear: 2093, ageRange: '84-103' },
      { planet: 'Mercury', period: 17, startYear: 2093, endYear: 2110, ageRange: '103-120' },
    ],
    minor: [
      { planet: 'Moon', subPlanet: 'Saturn', startYear: 2023, endYear: 2026, duration: 3, current: true },
      { planet: 'Moon', subPlanet: 'Mercury', startYear: 2026, endYear: 2029, duration: 3 },
      { planet: 'Moon', subPlanet: 'Ketu', startYear: 2029, endYear: 2030, duration: 1 },
      { planet: 'Moon', subPlanet: 'Venus', startYear: 2030, endYear: 2032, duration: 2 },
      { planet: 'Moon', subPlanet: 'Sun', startYear: 2032, endYear: 2033, duration: 1 },
    ]
  };

  const currentMajorDasha = dashaData.major.find(d => d.current);
  const currentMinorDasha = dashaData.minor.find(d => d.current);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-extrabold text-white">
            Dasha <span className="gold-gradient">Timeline</span>
          </h1>
          <p className="text-slate-400 text-sm mt-2">Vimshottari planetary periods and their influence on your life journey.</p>
        </div>
      </div>

      {!activeProfile ? (
        <div className="glass-premium p-12 text-center space-y-6 animate-slide-up">
          <Calendar className="mx-auto h-16 w-16 text-primary animate-glow" />
          <div className="space-y-3">
            <h3 className="text-2xl font-bold text-white">Setup Required</h3>
            <p className="text-slate-400 text-sm max-w-md mx-auto">
              Please register your Birth Details profile first to view your personalized Dasha timeline.
            </p>
          </div>
          <Link href="/onboarding">
            <button className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow">
              Create Birth Chart
            </button>
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Current Periods */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-premium p-6 space-y-4">
              <div className="flex items-center space-x-3">
                <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center text-primary animate-glow">
                  <Clock className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">Current Major Period</h3>
                  <p className="text-xs text-slate-400">Mahadasha</p>
                </div>
              </div>
              {currentMajorDasha && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-3xl font-bold gold-gradient">{currentMajorDasha.planet}</span>
                    <span className="px-3 py-1 bg-primary/10 border border-primary/30 rounded-full text-xs font-semibold text-primary">
                      {currentMajorDasha.period} Years
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Age Range</span>
                    <span className="text-white font-semibold">{currentMajorDasha.ageRange}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Period</span>
                    <span className="text-white font-semibold">{currentMajorDasha.startYear} - {currentMajorDasha.endYear}</span>
                  </div>
                  <div className="w-full bg-surface rounded-full h-2 mt-2">
                    <div className="bg-primary h-2 rounded-full" style={{ width: '45%' }} />
                  </div>
                  <span className="text-xs text-slate-400">45% complete</span>
                </div>
              )}
            </div>

            <div className="glass-premium p-6 space-y-4">
              <div className="flex items-center space-x-3">
                <div className="h-12 w-12 rounded-full bg-accent-purple/20 flex items-center justify-center text-primary animate-glow">
                  <TrendingUp className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">Current Sub Period</h3>
                  <p className="text-xs text-slate-400">Antardasha</p>
                </div>
              </div>
              {currentMinorDasha && (
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-2xl font-bold text-white">{currentMinorDasha.planet}</span>
                    <ChevronRight className="h-4 w-4 text-primary" />
                    <span className="text-2xl font-bold gold-gradient">{currentMinorDasha.subPlanet}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Duration</span>
                    <span className="text-white font-semibold">{currentMinorDasha.duration} Years</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Period</span>
                    <span className="text-white font-semibold">{currentMinorDasha.startYear} - {currentMinorDasha.endYear}</span>
                  </div>
                  <div className="w-full bg-surface rounded-full h-2 mt-2">
                    <div className="bg-primary h-2 rounded-full" style={{ width: '30%' }} />
                  </div>
                  <span className="text-xs text-slate-400">30% complete</span>
                </div>
              )}
            </div>
          </div>

          {/* Timeline Toggle */}
          <div className="flex space-x-2">
            <button
              onClick={() => setSelectedPeriod('major')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition ${
                selectedPeriod === 'major'
                  ? 'bg-primary text-black'
                  : 'bg-surface/50 border border-primary/20 text-slate-400 hover:bg-surface'
              }`}
            >
              Major Periods (Mahadasha)
            </button>
            <button
              onClick={() => setSelectedPeriod('minor')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition ${
                selectedPeriod === 'minor'
                  ? 'bg-primary text-black'
                  : 'bg-surface/50 border border-primary/20 text-slate-400 hover:bg-surface'
              }`}
            >
              Minor Periods (Antardasha)
            </button>
          </div>

          {/* Timeline Display */}
          <div className="glass-premium p-6 space-y-4">
            <h3 className="text-lg font-bold text-white">
              {selectedPeriod === 'major' ? 'Major Period Timeline' : 'Minor Period Timeline'}
            </h3>
            
            <div className="space-y-3">
              {selectedPeriod === 'major' ? (
                dashaData.major.map((dasha, index) => (
                  <div
                    key={index}
                    className={`glass-card p-4 rounded-xl flex items-center justify-between ${
                      dasha.current ? 'border-primary/50 bg-primary/5' : ''
                    }`}
                  >
                    <div className="flex items-center space-x-4">
                      <div className={`h-10 w-10 rounded-full flex items-center justify-center font-bold ${
                        dasha.current
                          ? 'bg-primary text-black animate-glow'
                          : 'bg-surface/50 text-slate-400'
                      }`}>
                        {dasha.planet.charAt(0)}
                      </div>
                      <div>
                        <span className={`font-semibold ${dasha.current ? 'text-white' : 'text-slate-300'}`}>
                          {dasha.planet} Mahadasha
                        </span>
                        <span className="text-xs text-slate-500 block">
                          {dasha.startYear} - {dasha.endYear} ({dasha.ageRange})
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className={`text-sm font-semibold ${dasha.current ? 'text-primary' : 'text-slate-400'}`}>
                        {dasha.period} Years
                      </span>
                      {dasha.current && (
                        <span className="text-xs text-primary block">Current</span>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                dashaData.minor.map((dasha, index) => (
                  <div
                    key={index}
                    className={`glass-card p-4 rounded-xl flex items-center justify-between ${
                      dasha.current ? 'border-primary/50 bg-primary/5' : ''
                    }`}
                  >
                    <div className="flex items-center space-x-4">
                      <div className={`h-10 w-10 rounded-full flex items-center justify-center font-bold ${
                        dasha.current
                          ? 'bg-primary text-black animate-glow'
                          : 'bg-surface/50 text-slate-400'
                      }`}>
                        {dasha.subPlanet.charAt(0)}
                      </div>
                      <div>
                        <span className={`font-semibold ${dasha.current ? 'text-white' : 'text-slate-300'}`}>
                          {dasha.planet} → {dasha.subPlanet}
                        </span>
                        <span className="text-xs text-slate-500 block">
                          {dasha.startYear} - {dasha.endYear}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className={`text-sm font-semibold ${dasha.current ? 'text-primary' : 'text-slate-400'}`}>
                        {dasha.duration} Years
                      </span>
                      {dasha.current && (
                        <span className="text-xs text-primary block">Current</span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Info Card */}
          <div className="glass-card p-6 space-y-4">
            <div className="flex items-start space-x-3">
              <Sparkles className="h-5 w-5 text-primary mt-0.5" />
              <div>
                <h4 className="font-bold text-white mb-2">About Vimshottari Dasha</h4>
                <p className="text-sm text-slate-400 leading-relaxed">
                  Vimshottari Dasha is a 120-year planetary period system in Vedic astrology. Each planet rules a specific number of years, influencing different aspects of life during its period. The current major period (Mahadasha) and sub-period (Antardasha) provide insights into the prevailing cosmic influences on your life journey.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
