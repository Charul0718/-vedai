'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Compass, ArrowRight, ArrowLeft, MapPin, Calendar, Clock, User, Check, X } from 'lucide-react';
import Link from 'next/link';

export default function BirthDetailsWizard() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    birthDate: '',
    birthTime: '',
    location: '',
    latitude: '',
    longitude: '',
    timezone: '+05:30'
  });
  const [locationSuggestions, setLocationSuggestions] = useState<any[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const locationInputRef = useRef<HTMLInputElement>(null);

  const steps = [
    { number: 1, title: 'Personal Info', icon: User },
    { number: 2, title: 'Birth Date', icon: Calendar },
    { number: 3, title: 'Birth Time', icon: Clock },
    { number: 4, title: 'Location', icon: MapPin },
  ];

  // Mock location suggestions (replace with Google Places API in production)
  const mockLocations = [
    { name: 'Mumbai, Maharashtra, India', lat: 19.076, lng: 72.8777, tz: '+05:30' },
    { name: 'Delhi, India', lat: 28.7041, lng: 77.1025, tz: '+05:30' },
    { name: 'Bangalore, Karnataka, India', lat: 12.9716, lng: 77.5946, tz: '+05:30' },
    { name: 'New York, NY, USA', lat: 40.7128, lng: -74.006, tz: '-05:00' },
    { name: 'London, UK', lat: 51.5074, lng: -0.1278, tz: '+00:00' },
    { name: 'Los Angeles, CA, USA', lat: 34.0522, lng: -118.2437, tz: '-08:00' },
    { name: 'Chicago, IL, USA', lat: 41.8781, lng: -87.6298, tz: '-06:00' },
    { name: 'Toronto, Ontario, Canada', lat: 43.6532, lng: -79.3832, tz: '-05:00' },
    { name: 'Sydney, NSW, Australia', lat: -33.8688, lng: 151.2093, tz: '+11:00' },
    { name: 'Dubai, UAE', lat: 25.2048, lng: 55.2708, tz: '+04:00' },
  ];

  const handleLocationSearch = (value: string) => {
    updateFormData('location', value);
    if (value.length > 2) {
      const filtered = mockLocations.filter(loc => 
        loc.name.toLowerCase().includes(value.toLowerCase())
      );
      setLocationSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  const selectLocation = (loc: any) => {
    setFormData(prev => ({
      ...prev,
      location: loc.name,
      latitude: loc.lat.toString(),
      longitude: loc.lng.toString(),
      timezone: loc.tz
    }));
    setShowSuggestions(false);
  };

  const handleNext = () => {
    if (step < 4) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleSubmit = async () => {
    localStorage.setItem('birthDetails', JSON.stringify(formData));
    router.push('/processing');
  };

  const updateFormData = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (locationInputRef.current && !locationInputRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="min-h-screen bg-background text-slate-100 overflow-hidden">
      {/* Premium Background */}
      <div className="absolute top-[-10%] left-[-10%] h-[600px] w-[600px] rounded-full bg-accent-navy/20 blur-[120px] pointer-events-none animate-pulse-slow" />
      <div className="absolute bottom-[20%] right-[-10%] h-[700px] w-[700px] rounded-full bg-accent-purple/10 blur-[150px] pointer-events-none animate-pulse-slow" />

      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-primary/10 glass-premium">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center space-x-3">
            <Compass className="h-8 w-8 text-primary animate-spin-slow" />
            <span className="text-2xl font-bold tracking-tight text-white">
              Ved<span className="gold-gradient">AI</span>
            </span>
          </Link>
          <div className="text-sm text-slate-400">
            Step {step} of 4
          </div>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="mx-auto max-w-4xl px-6 pt-12 pb-8">
        <div className="flex items-center justify-between">
          {steps.map((s) => (
            <div key={s.number} className="flex items-center flex-1">
              <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all ${
                s.number <= step 
                  ? 'border-primary bg-primary text-black' 
                  : 'border-primary/30 bg-surface text-slate-500'
              }`}>
                {s.number < step ? (
                  <Check className="h-5 w-5" />
                ) : (
                  <s.icon className="h-5 w-5" />
                )}
              </div>
              <span className={`ml-3 text-sm font-medium ${
                s.number <= step ? 'text-primary' : 'text-slate-500'
              }`}>
                {s.title}
              </span>
              {s.number < 4 && (
                <div className={`flex-1 mx-4 h-0.5 ${
                  s.number < step ? 'bg-primary' : 'bg-primary/20'
                }`} />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Form Content */}
      <div className="mx-auto max-w-2xl px-6 pb-24">
        <div className="glass-premium p-8 animate-slide-up">
          {step === 1 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">Personal Information</h2>
                <p className="text-sm text-slate-400">Let's start with your basic details</p>
              </div>
              
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2">FULL NAME</label>
                <input
                  type="text"
                  placeholder="e.g. Arjun Dev"
                  value={formData.name}
                  onChange={(e) => updateFormData('name', e.target.value)}
                  className="w-full rounded-lg border border-primary/20 bg-surface/50 px-4 py-3 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
                />
              </div>

              <div className="flex justify-end">
                <button
                  onClick={handleNext}
                  disabled={!formData.name}
                  className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Continue <ArrowRight className="ml-2 h-4 w-4 inline" />
                </button>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">Birth Date</h2>
                <p className="text-sm text-slate-400">When were you born?</p>
              </div>
              
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2">DATE OF BIRTH</label>
                <input
                  type="date"
                  value={formData.birthDate}
                  onChange={(e) => updateFormData('birthDate', e.target.value)}
                  className="w-full rounded-lg border border-primary/20 bg-surface/50 px-4 py-3 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
                />
              </div>

              <div className="flex justify-between">
                <button
                  onClick={handleBack}
                  className="px-6 py-3 border border-primary/30 text-primary font-semibold rounded-lg hover:bg-primary/10 transition"
                >
                  <ArrowLeft className="mr-2 h-4 w-4 inline" /> Back
                </button>
                <button
                  onClick={handleNext}
                  disabled={!formData.birthDate}
                  className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Continue <ArrowRight className="ml-2 h-4 w-4 inline" />
                </button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">Birth Time</h2>
                <p className="text-sm text-slate-400">What time were you born?</p>
              </div>
              
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2">TIME OF BIRTH</label>
                <input
                  type="time"
                  value={formData.birthTime}
                  onChange={(e) => updateFormData('birthTime', e.target.value)}
                  className="w-full rounded-lg border border-primary/20 bg-surface/50 px-4 py-3 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
                />
              </div>

              <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg">
                <p className="text-xs text-slate-400">
                  <strong className="text-primary">Note:</strong> Accurate birth time is crucial for precise house calculations and Lagna determination.
                </p>
              </div>

              <div className="flex justify-between">
                <button
                  onClick={handleBack}
                  className="px-6 py-3 border border-primary/30 text-primary font-semibold rounded-lg hover:bg-primary/10 transition"
                >
                  <ArrowLeft className="mr-2 h-4 w-4 inline" /> Back
                </button>
                <button
                  onClick={handleNext}
                  disabled={!formData.birthTime}
                  className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Continue <ArrowRight className="ml-2 h-4 w-4 inline" />
                </button>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">Birth Location</h2>
                <p className="text-sm text-slate-400">Where were you born?</p>
              </div>
              
              <div className="relative" ref={locationInputRef}>
                <label className="block text-xs font-semibold text-slate-400 mb-2">SEARCH LOCATION</label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search city or country..."
                    value={formData.location}
                    onChange={(e) => handleLocationSearch(e.target.value)}
                    className="w-full rounded-lg border border-primary/20 bg-surface/50 pl-10 pr-10 py-3 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
                  />
                  {formData.location && (
                    <button
                      onClick={() => {
                        updateFormData('location', '');
                        updateFormData('latitude', '');
                        updateFormData('longitude', '');
                      }}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  )}
                </div>
                
                {/* Location Suggestions Dropdown */}
                {showSuggestions && locationSuggestions.length > 0 && (
                  <div className="absolute z-10 w-full mt-2 glass-premium border border-primary/20 rounded-lg overflow-hidden animate-slide-up">
                    {locationSuggestions.map((loc, index) => (
                      <button
                        key={index}
                        onClick={() => selectLocation(loc)}
                        className="w-full text-left px-4 py-3 hover:bg-primary/10 transition border-b border-primary/10 last:border-0 flex items-center space-x-3"
                      >
                        <MapPin className="h-4 w-4 text-primary shrink-0" />
                        <div>
                          <span className="text-sm text-white block">{loc.name}</span>
                          <span className="text-xs text-slate-400">{loc.lat}, {loc.lng} • {loc.tz}</span>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {formData.latitude && formData.longitude && (
                <div className="grid grid-cols-2 gap-4 animate-slide-up">
                  <div className="glass-card p-3">
                    <label className="block text-[10px] font-semibold text-slate-400 mb-1">LATITUDE</label>
                    <span className="text-sm text-white font-mono">{formData.latitude}</span>
                  </div>
                  <div className="glass-card p-3">
                    <label className="block text-[10px] font-semibold text-slate-400 mb-1">LONGITUDE</label>
                    <span className="text-sm text-white font-mono">{formData.longitude}</span>
                  </div>
                </div>
              )}

              <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg">
                <p className="text-xs text-slate-400">
                  <strong className="text-primary">Tip:</strong> Start typing to search for your birthplace. Coordinates will be auto-filled.
                </p>
              </div>

              <div className="flex justify-between">
                <button
                  onClick={handleBack}
                  className="px-6 py-3 border border-primary/30 text-primary font-semibold rounded-lg hover:bg-primary/10 transition"
                >
                  <ArrowLeft className="mr-2 h-4 w-4 inline" /> Back
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={!formData.location || !formData.latitude || !formData.longitude}
                  className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Generate Chart <ArrowRight className="ml-2 h-4 w-4 inline" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
