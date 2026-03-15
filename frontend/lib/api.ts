import { AnalysisResult, Questionnaire } from "@/lib/types";

export async function analyzeSkin(image: File, questionnaire: Questionnaire): Promise<AnalysisResult> {
  const form = new FormData();
  form.append("image", image);
  form.append("age_range", questionnaire.age_range);
  form.append("lifestyle", questionnaire.lifestyle);
  form.append("primary_concern", questionnaire.primary_concern);
  form.append("sensitivity_level", questionnaire.sensitivity_level);

  const res = await fetch("/api/analyze", {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown server error" }));
    throw new Error(err.detail || "Failed to analyze skin");
  }

  return res.json();
}
