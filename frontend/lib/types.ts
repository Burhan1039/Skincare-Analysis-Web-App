export type Questionnaire = {
  age_range: string;
  lifestyle: string;
  primary_concern: string;
  sensitivity_level: string;
};

export type AnalysisResult = {
  analysis_id: number;
  skin_type: string;
  metrics: {
    dryness_score: number;
    redness_score: number;
    oiliness_score: number;
  };
  recommendations: {
    morning_routine: string[];
    evening_routine: string[];
    targeted_treatments: string[];
    habits: string[];
    disclaimer: string;
  };
};
