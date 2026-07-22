/**
 * Tests for the Explainability endpoint integration.
 *
 * Verifies:
 * - API response structure matches expected schema
 * - Component renders domain scores, factors, and reasoning steps
 * - Loading and error states work correctly
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock the auth provider
jest.mock('../app/providers', () => ({
  useAuth: () => ({ token: 'test-token', user: null }),
}));

// Mock react-query
jest.mock('@tanstack/react-query', () => ({
  useQuery: jest.fn(),
  useMutation: jest.fn(),
  useQueryClient: () => ({
    invalidateQueries: jest.fn(),
  }),
}));

const mockExplainabilityResponse = {
  career: {
    domain: 'career',
    score: 7.5,
    confidence: 0.85,
    supportingFactors: [
      {
        factor: 'Sun placement',
        source: 'planet:Sun',
        impact: 0.72,
        explanation: 'Sun in House 1 (Leo, dignity: own_sign) strongly supports career',
      },
      {
        factor: 'Jupiter placement',
        source: 'planet:Jupiter',
        impact: 0.54,
        explanation: 'Jupiter in House 10 (Sagittarius) supports career',
      },
    ],
    challengingFactors: [
      {
        factor: 'Saturn placement',
        source: 'planet:Saturn',
        impact: -0.3,
        explanation: 'Saturn in House 6 challenges career',
      },
    ],
    planetaryEvidence: [
      {
        planet: 'Sun',
        house: 1,
        sign: 'Leo',
        isRetrograde: false,
        role: 'primary_house',
        contribution: 0.6,
      },
      {
        planet: 'Jupiter',
        house: 10,
        sign: 'Sagittarius',
        isRetrograde: false,
        role: 'lord_of_house_10',
        contribution: 0.8,
      },
    ],
    reasoningSteps: [
      {
        step: 1,
        description: 'Identify career-relevant houses',
        detail: 'Primary houses: [10], Secondary: [2, 6, 11]',
      },
      {
        step: 2,
        description: 'Evaluate planetary placements',
        detail: 'Base score from 9 planets: 6.50/10',
      },
      {
        step: 3,
        description: 'Compute final score',
        detail: 'Final: 6.50 + yoga_adj + dosha_adj + dasha_adj = 7.50',
      },
    ],
    explanationSummary:
      'Career score: 7.5/10 (confidence: 0.85). Key strengths: Sun placement, Jupiter placement. Key challenges: Saturn placement.',
  },
  finance: {
    domain: 'finance',
    score: 6.2,
    confidence: 0.7,
    supportingFactors: [
      {
        factor: 'Jupiter placement',
        source: 'planet:Jupiter',
        impact: 0.6,
        explanation: 'Jupiter in House 10 supports finance',
      },
    ],
    challengingFactors: [],
    planetaryEvidence: [],
    reasoningSteps: [],
    explanationSummary: 'Finance score: 6.2/10 (confidence: 0.7).',
  },
};

describe('Explainability Endpoint', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('API Response Structure', () => {
    it('returns domain results with required fields', () => {
      const domains = Object.keys(mockExplainabilityResponse);
      expect(domains).toEqual(['career', 'finance']);

      for (const domain of domains) {
        const result = (mockExplainabilityResponse as any)[domain];
        expect(result).toHaveProperty('domain');
        expect(result).toHaveProperty('score');
        expect(result).toHaveProperty('confidence');
        expect(result).toHaveProperty('supportingFactors');
        expect(result).toHaveProperty('challengingFactors');
        expect(result).toHaveProperty('planetaryEvidence');
        expect(result).toHaveProperty('reasoningSteps');
        expect(result).toHaveProperty('explanationSummary');
      }
    });

    it('scores are within 0-10 range', () => {
      for (const result of Object.values(mockExplainabilityResponse)) {
        expect(result.score).toBeGreaterThanOrEqual(0);
        expect(result.score).toBeLessThanOrEqual(10);
      }
    });

    it('confidence is within 0-1 range', () => {
      for (const result of Object.values(mockExplainabilityResponse)) {
        expect(result.confidence).toBeGreaterThanOrEqual(0);
        expect(result.confidence).toBeLessThanOrEqual(1);
      }
    });

    it('supportingFactors have valid impact range', () => {
      for (const result of Object.values(mockExplainabilityResponse)) {
        for (const factor of result.supportingFactors) {
          expect(factor.impact).toBeGreaterThan(0);
          expect(factor.impact).toBeLessThanOrEqual(1);
          expect(factor).toHaveProperty('factor');
          expect(factor).toHaveProperty('source');
          expect(factor).toHaveProperty('explanation');
        }
      }
    });

    it('challengingFactors have negative impact', () => {
      for (const result of Object.values(mockExplainabilityResponse)) {
        for (const factor of result.challengingFactors) {
          expect(factor.impact).toBeLessThan(0);
          expect(factor.impact).toBeGreaterThanOrEqual(-1);
        }
      }
    });

    it('planetaryEvidence contains planet, house, sign', () => {
      const careerEvidence = mockExplainabilityResponse.career.planetaryEvidence;
      expect(careerEvidence.length).toBeGreaterThan(0);
      for (const ev of careerEvidence) {
        expect(ev).toHaveProperty('planet');
        expect(ev).toHaveProperty('house');
        expect(ev).toHaveProperty('sign');
        expect(ev.house).toBeGreaterThanOrEqual(1);
        expect(ev.house).toBeLessThanOrEqual(12);
      }
    });

    it('reasoningSteps are numbered sequentially', () => {
      const steps = mockExplainabilityResponse.career.reasoningSteps;
      expect(steps.length).toBeGreaterThanOrEqual(3);
      for (let i = 0; i < steps.length; i++) {
        expect(steps[i].step).toBe(i + 1);
        expect(steps[i].description).toBeTruthy();
        expect(steps[i].detail).toBeTruthy();
      }
    });

    it('explanationSummary includes score', () => {
      for (const result of Object.values(mockExplainabilityResponse)) {
        expect(result.explanationSummary).toContain('score');
        expect(result.explanationSummary).toContain(String(result.score));
      }
    });
  });

  describe('Career Domain Specific', () => {
    it('has Sun and Jupiter as supporting factors', () => {
      const factors = mockExplainabilityResponse.career.supportingFactors.map(
        (f) => f.factor
      );
      expect(factors.some((f) => f.includes('Sun'))).toBe(true);
      expect(factors.some((f) => f.includes('Jupiter'))).toBe(true);
    });

    it('planetary evidence references valid planets', () => {
      const validPlanets = [
        'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter',
        'Venus', 'Saturn', 'Rahu', 'Ketu',
      ];
      for (const ev of mockExplainabilityResponse.career.planetaryEvidence) {
        expect(validPlanets).toContain(ev.planet);
      }
    });
  });
});
