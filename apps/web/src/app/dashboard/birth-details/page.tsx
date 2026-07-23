'use client';

import React, { useState } from 'react';
import { useAuth } from '../../providers';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { MapPin, Calendar, Clock, Globe, Plus, AlertCircle, CheckCircle2 } from 'lucide-react';
import { GlassCard, GradientButton, Badge, Spinner } from '@vedai/ui';
import { API_BASE } from '../../../lib/api';

// Form validation schema using Zod
const birthDetailsSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  date_of_birth: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Date must be in YYYY-MM-DD format'),
  time_of_birth: z.string().regex(/^\d{2}:\d{2}$/, 'Time must be in HH:MM format'),
  location_name: z.string().min(3, 'Location name must be at least 3 characters'),
  latitude: z.number().min(-90).max(90),
  longitude: z.number().min(-180).max(180),
  timezone: z.string().min(3, 'Timezone string is required')
});

type BirthDetailsFormData = z.infer<typeof birthDetailsSchema>;

export default function BirthDetailsPage() {
  const { token } = useAuth();
  const queryClient = useQueryClient();
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Fetch profiles
  const { data: profiles, isLoading: loadingProfiles } = useQuery({
    queryKey: ['birth-details'],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/api/birth-details`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to load profiles');
      return res.json();
    },
    enabled: !!token
  });

  const { register, handleSubmit, setValue, formState: { errors }, reset } = useForm<BirthDetailsFormData>({
    resolver: zodResolver(birthDetailsSchema),
    defaultValues: {
      name: '',
      date_of_birth: '',
      time_of_birth: '',
      location_name: '',
      latitude: 0,
      longitude: 0,
      timezone: 'Asia/Kolkata'
    }
  });

  // Pre-fill helper to make it easy for the user
  const prefillSample = () => {
    setValue('name', 'Arjun');
    setValue('date_of_birth', '1995-10-25');
    setValue('time_of_birth', '08:30');
    setValue('location_name', 'Mumbai, India');
    setValue('latitude', 19.076);
    setValue('longitude', 72.877);
    setValue('timezone', 'Asia/Kolkata');
  };

  // Submit Mutation
  const createProfileMutation = useMutation({
    mutationFn: async (payload: BirthDetailsFormData) => {
      const res = await fetch(`${API_BASE}/api/birth-details`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Failed to submit profile');
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['birth-details'] });
      setSuccessMsg('Birth profile constructed successfully!');
      setErrorMsg('');
      reset();
    },
    onError: (err: any) => {
      setErrorMsg(err.message || 'An error occurred during submission');
      setSuccessMsg('');
    }
  });

  const onSubmit = (data: BirthDetailsFormData) => {
    createProfileMutation.mutate(data);
  };

  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-extrabold text-white">Birth Profiles</h1>
        <p className="text-slate-400 text-sm mt-1">Configure coordinates and times to compute astronomical alignments.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Profile Construction Form */}
        <div className="lg:col-span-7">
          <GlassCard className="space-y-6" hoverEffect>
            <div className="flex justify-between items-center border-b border-white/5 pb-2">
              <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                <Plus className="h-5 w-5 text-indigo-400" />
                <span>Construct Profile</span>
              </h3>
              <button 
                type="button" 
                onClick={prefillSample} 
                className="text-xs text-indigo-400 hover:text-indigo-300 transition hover:underline"
              >
                🪄 Load Sample Data
              </button>
            </div>

            {successMsg && (
              <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs p-3 rounded-lg flex items-center space-x-2">
                <CheckCircle2 className="h-4 w-4 shrink-0" />
                <span>{successMsg}</span>
              </div>
            )}

            {errorMsg && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs p-3 rounded-lg flex items-center space-x-2">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1.5">FULL NAME</label>
                <input
                  type="text"
                  placeholder="e.g. Arjun Dev"
                  {...register('name')}
                  className="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none transition"
                />
                {errors.name && <p className="text-red-400 text-[10px] mt-1">{errors.name.message}</p>}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">DATE OF BIRTH (YYYY-MM-DD)</label>
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="1995-10-25"
                      {...register('date_of_birth')}
                      className="w-full rounded-lg border border-white/10 bg-slate-900/50 pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none transition"
                    />
                    <Calendar className="absolute left-3.5 top-3.5 h-4 w-4 text-slate-500" />
                  </div>
                  {errors.date_of_birth && <p className="text-red-400 text-[10px] mt-1">{errors.date_of_birth.message}</p>}
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">TIME OF BIRTH (HH:MM)</label>
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="08:30"
                      {...register('time_of_birth')}
                      className="w-full rounded-lg border border-white/10 bg-slate-900/50 pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none transition"
                    />
                    <Clock className="absolute left-3.5 top-3.5 h-4 w-4 text-slate-500" />
                  </div>
                  {errors.time_of_birth && <p className="text-red-400 text-[10px] mt-1">{errors.time_of_birth.message}</p>}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1.5">LOCATION (CITY, COUNTRY)</label>
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Mumbai, India"
                    {...register('location_name')}
                    className="w-full rounded-lg border border-white/10 bg-slate-900/50 pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none transition"
                  />
                  <MapPin className="absolute left-3.5 top-3.5 h-4 w-4 text-slate-500" />
                </div>
                {errors.location_name && <p className="text-red-400 text-[10px] mt-1">{errors.location_name.message}</p>}
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">LATITUDE</label>
                  <input
                    type="number"
                    step="0.0001"
                    placeholder="19.076"
                    {...register('latitude', { valueAsNumber: true })}
                    className="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-2.5 text-sm text-white focus:border-indigo-500 focus:outline-none transition"
                  />
                  {errors.latitude && <p className="text-red-400 text-[10px] mt-1">{errors.latitude.message}</p>}
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">LONGITUDE</label>
                  <input
                    type="number"
                    step="0.0001"
                    placeholder="72.877"
                    {...register('longitude', { valueAsNumber: true })}
                    className="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-2.5 text-sm text-white focus:border-indigo-500 focus:outline-none transition"
                  />
                  {errors.longitude && <p className="text-red-400 text-[10px] mt-1">{errors.longitude.message}</p>}
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">TIMEZONE ID</label>
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Asia/Kolkata"
                      {...register('timezone')}
                      className="w-full rounded-lg border border-white/10 bg-slate-900/50 pl-10 pr-4 py-2.5 text-sm text-white focus:border-indigo-500 focus:outline-none transition"
                    />
                    <Globe className="absolute left-3.5 top-3.5 h-4 w-4 text-slate-500" />
                  </div>
                  {errors.timezone && <p className="text-red-400 text-[10px] mt-1">{errors.timezone.message}</p>}
                </div>
              </div>

              <GradientButton type="submit" className="w-full justify-center mt-4" disabled={createProfileMutation.isPending}>
                {createProfileMutation.isPending ? (
                  <>
                    <Spinner className="mr-2 h-4 w-4" />
                    <span>Computing coordinates...</span>
                  </>
                ) : (
                  <span>Calculate & Save Profile</span>
                )}
              </GradientButton>
            </form>
          </GlassCard>
        </div>

        {/* Existing profiles column */}
        <div className="lg:col-span-5 space-y-6">
          <GlassCard className="space-y-4">
            <h3 className="text-lg font-bold text-white border-b border-white/5 pb-2">Configured Profiles</h3>
            
            {loadingProfiles ? (
              <div className="flex h-20 items-center justify-center">
                <Spinner className="h-5 w-5 text-indigo-500" />
              </div>
            ) : profiles && profiles.length > 0 ? (
              <div className="space-y-4">
                {profiles.map((p: any) => (
                  <div key={p.id} className="p-4 rounded-xl bg-white/5 border border-white/5 space-y-2">
                    <div className="flex justify-between items-start">
                      <span className="font-bold text-sm text-white">{p.name}</span>
                      <Badge variant="info">Active</Badge>
                    </div>
                    <p className="text-xs text-slate-400">{p.date_of_birth} at {p.time_of_birth}</p>
                    <p className="text-[11px] text-slate-500 truncate">{p.location_name}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400 text-center py-6">No profiles compiled yet.</p>
            )}
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
