export interface User {
  id: string;
  email: string;
  fullName: string;
  createdAt: string;
}

export interface BirthDetails {
  id: string;
  userId: string;
  name: string;
  dateOfBirth: string; // ISO date string (YYYY-MM-DD)
  timeOfBirth: string; // HH:MM
  locationName: string;
  latitude: number;
  longitude: number;
  timezone: string; // timezone string, e.g., 'Asia/Kolkata'
  createdAt: string;
}

export interface PlanetPosition {
  id: string;
  birthChartId: string;
  planetName: string; // e.g., Sun, Moon, Mars, etc.
  longitude: number; // 0 to 360 degrees
  sign: string; // e.g., Aries, Taurus, etc.
  degree: number; // 0 to 30 degrees within the sign
  houseNumber: number; // 1 to 12
  isRetrograde: boolean;
}

export interface House {
  id: string;
  birthChartId: string;
  houseNumber: number; // 1 to 12
  sign: string; // e.g., Aries, Taurus, etc.
  startDegree: number;
  midDegree: number;
  endDegree: number;
}

export interface BirthChart {
  id: string;
  birthDetailsId: string;
  chartType: string; // e.g., Rasi (D1), Navamsha (D9)
  ascendantSign: string;
  ascendantDegree: number;
  planets: PlanetPosition[];
  houses: House[];
  createdAt: string;
}

export interface Report {
  id: string;
  userId: string;
  birthDetailsId: string;
  reportType: 'comprehensive' | 'career' | 'relationship' | 'transit';
  inputDetails: {
    name: string;
    dateTime: string;
    location: string;
  };
  calculationResults: {
    ascendantSign: string;
    ascendantDegree: number;
    planets: Array<{
      name: string;
      longitude: number;
      sign: string;
      degree: number;
      house: number;
      isRetrograde: boolean;
    }>;
    houses: Array<{
      number: number;
      sign: string;
      midDegree: number;
    }>;
  };
  traditionalInterpretations: {
    ascendantReading: string;
    planetaryPlacements: Array<{
      planet: string;
      reading: string;
    }>;
    housePlacements: Array<{
      house: number;
      reading: string;
    }>;
  };
  aiExplanation: string;
  generatedAt: string;
  pdfUrl?: string;
}

export interface ChatSession {
  id: string;
  userId: string;
  birthDetailsId: string;
  title: string;
  createdAt: string;
}

export interface ChatMessage {
  id: string;
  chatSessionId: string;
  role: 'user' | 'assistant';
  content: string;
  astronomicalData?: any; // deterministic calculations reference
  interpretationData?: any; // traditional reading reference
  aiInsights?: string;
  createdAt: string;
}
