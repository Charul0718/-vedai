'use client';

import React, { useState } from 'react';
import { useAuth } from '../../providers';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { FileText, Download, Sparkles, Cpu, BookOpen, Scroll, ShieldAlert } from 'lucide-react';
import Link from 'next/link';

export default function ReportPage() {
  const { token } = useAuth();
  const queryClient = useQueryClient();
  const [activeReportId, setActiveReportId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'calculations' | 'traditional' | 'ai' | 'explainability'>('calculations');

  // Fetch birth profiles (to verify if we have profiles to run reports on)
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

  // Fetch reports list
  const { data: reports, isLoading: loadingReports } = useQuery({
    queryKey: ['reports'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/reports', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to load reports');
      return res.json();
    },
    enabled: !!token
  });

  // Mutator to compile a new report
  const generateReportMutation = useMutation({
    mutationFn: async () => {
      if (!activeProfile) throw new Error('No birth profile configured');
      const res = await fetch('http://localhost:8000/api/reports', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          birth_details_id: activeProfile.id,
          report_type: 'comprehensive'
        })
      });
      if (!res.ok) throw new Error('Failed to compile report');
      return res.json();
    },
    onSuccess: (newReport) => {
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      setActiveReportId(newReport.id);
    }
  });

  const selectedReport = reports?.find((r: any) => r.id === activeReportId) || (reports && reports.length > 0 ? reports[0] : null);

  // Fetch explainability data
  const { data: explainability, isLoading: loadingExplainability } = useQuery({
    queryKey: ['explainability', activeProfile?.id],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/explainability', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ birth_details_id: activeProfile!.id })
      });
      if (!res.ok) throw new Error('Failed to load explainability');
      return res.json();
    },
    enabled: !!token && !!activeProfile && activeTab === 'explainability'
  });

  const handleGenerateReport = () => {
    generateReportMutation.mutate();
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-extrabold text-white">
            Reports <span className="gold-gradient">Library</span>
          </h1>
          <p className="text-slate-400 text-sm mt-2">Generate and download comprehensive astrological analysis reports.</p>
        </div>

        {activeProfile && (
          <button
            onClick={handleGenerateReport}
            disabled={generateReportMutation.isPending}
            className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow flex items-center space-x-2"
          >
            {generateReportMutation.isPending ? (
              <>
                <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                <span>Compiling...</span>
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                <span>Generate Report</span>
              </>
            )}
          </button>
        )}
      </div>

      {!activeProfile ? (
        <div className="glass-premium p-12 text-center space-y-6 animate-slide-up">
          <FileText className="mx-auto h-16 w-16 text-primary animate-glow" />
          <div className="space-y-3">
            <h3 className="text-2xl font-bold text-white">Setup Required</h3>
            <p className="text-slate-400 text-sm max-w-md mx-auto">
              Please register your Birth Details profile first to trigger the report compilation engines.
            </p>
          </div>
          <Link href="/onboarding">
            <button className="px-6 py-3 bg-primary text-black font-semibold rounded-lg hover:bg-primary-light transition gold-glow">
              Create Birth Chart
            </button>
          </Link>
        </div>
      ) : loadingReports ? (
        <div className="flex h-40 items-center justify-center">
          <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      ) : !selectedReport ? (
        <div className="glass-premium p-12 text-center space-y-6 animate-slide-up">
          <FileText className="mx-auto h-16 w-16 text-primary animate-glow" />
          <div className="space-y-3">
            <h3 className="text-2xl font-bold text-white">No Reports Yet</h3>
            <p className="text-slate-400 text-sm max-w-md mx-auto">
              Generate your first comprehensive report combining astronomical math, traditional scriptures, and AI insights.
            </p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* List Sidebar */}
          <div className="lg:col-span-4 space-y-4">
            <div className="glass-premium p-4 space-y-4">
              <h3 className="font-bold text-white border-b border-primary/10 pb-3 text-sm">Report Archive</h3>
              <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
                {reports?.map((r: any) => {
                  const isActive = selectedReport.id === r.id;
                  return (
                    <button
                      key={r.id}
                      onClick={() => {
                        setActiveReportId(r.id);
                        setActiveTab('calculations');
                      }}
                      className={`w-full text-left p-3 rounded-xl border text-xs transition ${
                        isActive 
                          ? 'bg-primary/10 border-primary/30 text-white' 
                          : 'bg-surface/50 border-primary/10 text-slate-400 hover:bg-surface hover:text-white'
                      }`}
                    >
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-bold truncate">{r.input_details?.name || 'Vedic Profile'}</span>
                        <span className="px-2 py-0.5 bg-primary/20 text-primary text-[10px] rounded-full">{r.report_type}</span>
                      </div>
                      <p className="text-[10px] text-slate-500">{new Date(r.generated_at).toLocaleDateString()}</p>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Main Viewer Card */}
          <div className="lg:col-span-8 space-y-6">
            <div className="glass-premium p-6 space-y-6">
              {/* Report Header */}
              <div className="flex justify-between items-start border-b border-primary/10 pb-4">
                <div>
                  <h3 className="text-xl font-bold text-white">Vedic Report for {selectedReport.input_details?.name}</h3>
                  <p className="text-xs text-slate-400 mt-1">Generated: {new Date(selectedReport.generated_at).toLocaleString()}</p>
                </div>
                {selectedReport.pdf_url && (
                  <a
                    href={`http://localhost:8000${selectedReport.pdf_url}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <button className="px-4 py-2 bg-primary/10 border border-primary/30 text-primary font-semibold rounded-lg hover:bg-primary/20 transition flex items-center space-x-2">
                      <Download className="h-4 w-4" />
                      <span>Download PDF</span>
                    </button>
                  </a>
                )}
              </div>

              {/* Navigation Tab Row */}
              <div className="flex space-x-2 border-b border-primary/10 pb-3">
                {[
                  { id: 'calculations', label: 'Calculations', icon: Cpu },
                  { id: 'traditional', label: 'Traditional', icon: BookOpen },
                  { id: 'ai', label: 'AI Insights', icon: Scroll },
                  { id: 'explainability', label: 'Explainability', icon: Sparkles }
                ].map((tab) => {
                  const Icon = tab.icon;
                  const isActive = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
                        isActive 
                          ? 'bg-primary/10 text-primary border border-primary/30' 
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      <Icon className="h-3.5 w-3.5" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </div>

              {/* Tab views */}
              <div className="space-y-4 min-h-[300px]">
                {activeTab === 'calculations' && (
                  <div className="space-y-4">
                    <div className="glass-card p-4 space-y-2">
                      <span className="text-[10px] font-bold text-primary tracking-wider uppercase block">CALCULATION BOUNDARY</span>
                      <p className="text-xs text-slate-300">
                        Deterministic calculations using the sidereal coordinates system. Physical positions of celestial objects at birth.
                      </p>
                    </div>

                    <div className="flex justify-between items-center text-xs glass-card p-3">
                      <span className="text-slate-400">Ascendant Sign: <strong className="text-white">{selectedReport.calculation_results?.ascendantSign}</strong></span>
                      <span className="text-slate-400">Degree: <strong className="text-white">{selectedReport.calculation_results?.ascendantDegree?.toFixed(2)}°</strong></span>
                    </div>

                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-xs border-collapse">
                        <thead>
                          <tr className="text-slate-400 border-b border-primary/10">
                            <th className="pb-2 font-semibold">PLANET</th>
                            <th className="pb-2 font-semibold">LONGITUDE</th>
                            <th className="pb-2 font-semibold">SIGN</th>
                            <th className="pb-2 font-semibold">HOUSE</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-primary/10">
                          {selectedReport.calculation_results?.planets?.map((p: any) => (
                            <tr key={p.name} className="text-slate-200">
                              <td className="py-2.5 font-bold text-white">{p.name}</td>
                              <td className="py-2.5">{p.longitude?.toFixed(4)}°</td>
                              <td className="py-2.5">{p.sign} ({p.degree?.toFixed(2)}°)</td>
                              <td className="py-2.5 font-semibold text-primary">{p.house}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {activeTab === 'traditional' && (
                  <div className="space-y-4 text-xs text-slate-300">
                    <div className="glass-card p-4 space-y-2">
                      <span className="text-[10px] font-bold text-primary tracking-wider uppercase block">SCRIPTURE INTERPRETATIONS</span>
                      <p className="text-xs text-slate-300">
                        Interpretations mapped from ancient Sanskrit scriptures (e.g. Hora Shastra). Classical rules of astrology.
                      </p>
                    </div>

                    <div className="space-y-3">
                      <div className="glass-card p-3">
                        <span className="font-bold text-white block mb-1">Ascendant placement:</span>
                        <p className="leading-relaxed">{selectedReport.traditional_interpretations?.ascendantReading}</p>
                      </div>

                      <div className="space-y-2.5">
                        <span className="font-bold text-white block">Planetary Placements:</span>
                        {selectedReport.traditional_interpretations?.planetaryPlacements?.map((p: any) => (
                          <div key={p.planet} className="glass-card p-3 space-y-1">
                            <span className="font-semibold text-primary block">{p.planet} Placement:</span>
                            <p className="leading-relaxed">{p.reading}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'ai' && (
                  <div className="space-y-4">
                    <div className="glass-card p-4 space-y-2">
                      <span className="text-[10px] font-bold text-primary tracking-wider uppercase block">AI NARRATIVE SYNTHESIS</span>
                      <p className="text-xs text-slate-300">
                        Google Gemini models synthesize raw math coordinates and Parashara translations into a unified growth guide.
                      </p>
                    </div>

                    <div className="glass-card p-4 text-sm text-slate-300 leading-relaxed whitespace-pre-line">
                      {selectedReport.ai_explanation}
                    </div>
                  </div>
                )}

                {activeTab === 'explainability' && (
                  <div className="space-y-4">
                    <div className="glass-card p-4 space-y-2">
                      <span className="text-[10px] font-bold text-primary tracking-wider uppercase block">DETERMINISTIC EXPLAINABILITY</span>
                      <p className="text-xs text-slate-300">
                        Scores derived from planetary dignities, house placements, yogas, doshas, and current dasha — no AI involved.
                      </p>
                    </div>

                    {loadingExplainability ? (
                      <div className="flex h-40 items-center justify-center">
                        <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                      </div>
                    ) : explainability ? (
                      <div className="space-y-4">
                        {Object.entries(explainability).map(([domain, data]: [string, any]) => (
                          <div key={domain} className="glass-card p-4 space-y-3">
                            <div className="flex justify-between items-center">
                              <span className="font-bold text-white capitalize">{domain}</span>
                              <div className="flex items-center space-x-3">
                                <span className="text-xs text-slate-400">Confidence: {(data.confidence * 100).toFixed(0)}%</span>
                                <span className={`text-lg font-bold ${data.score >= 7 ? 'text-green-400' : data.score >= 4 ? 'text-yellow-400' : 'text-red-400'}`}>
                                  {data.score.toFixed(1)}
                                </span>
                              </div>
                            </div>

                            {/* Score bar */}
                            <div className="w-full bg-slate-800 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full ${data.score >= 7 ? 'bg-green-400' : data.score >= 4 ? 'bg-yellow-400' : 'bg-red-400'}`}
                                style={{ width: `${(data.score / 10) * 100}%` }}
                              />
                            </div>

                            <p className="text-xs text-slate-400 leading-relaxed">{data.explanationSummary}</p>

                            {/* Supporting Factors */}
                            {data.supportingFactors?.length > 0 && (
                              <div className="space-y-1">
                                <span className="text-[10px] font-bold text-green-400 tracking-wider uppercase">Supporting</span>
                                {data.supportingFactors.slice(0, 3).map((f: any, i: number) => (
                                  <div key={i} className="text-[11px] text-slate-300 flex items-start space-x-2">
                                    <span className="text-green-400 mt-0.5">+</span>
                                    <span>{f.explanation}</span>
                                  </div>
                                ))}
                              </div>
                            )}

                            {/* Challenging Factors */}
                            {data.challengingFactors?.length > 0 && (
                              <div className="space-y-1">
                                <span className="text-[10px] font-bold text-red-400 tracking-wider uppercase">Challenging</span>
                                {data.challengingFactors.slice(0, 3).map((f: any, i: number) => (
                                  <div key={i} className="text-[11px] text-slate-300 flex items-start space-x-2">
                                    <span className="text-red-400 mt-0.5">-</span>
                                    <span>{f.explanation}</span>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center text-slate-400 text-xs py-8">
                        Click "Generate Report" first to enable explainability analysis.
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Scientific disclaimer */}
              <div className="glass-card bg-primary/5 border-primary/20 p-4 flex items-start space-x-3 text-xs">
                <ShieldAlert className="h-5 w-5 shrink-0 text-primary mt-0.5" />
                <div className="space-y-1">
                  <span className="font-bold text-white">Scientific Disclaimer</span>
                  <p className="leading-relaxed text-slate-400">
                    Vedic Astrology is not a scientifically verified prediction system. All readings and reports are designed as self-reflection frameworks. Do not substitute this advice for licensed professional financial, legal, or health services.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
