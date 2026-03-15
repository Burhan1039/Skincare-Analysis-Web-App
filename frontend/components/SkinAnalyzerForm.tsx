"use client";

import { ChangeEvent, FormEvent, useMemo, useState } from "react";
import { analyzeSkin } from "@/lib/api";
import type { AnalysisResult, Questionnaire } from "@/lib/types";

const defaultQuestionnaire: Questionnaire = {
  age_range: "18-25",
  lifestyle: "Indoor",
  primary_concern: "Acne / Breakouts",
  sensitivity_level: "Medium",
};

export default function SkinAnalyzerForm() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [questionnaire, setQuestionnaire] = useState<Questionnaire>(defaultQuestionnaire);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const canSubmit = useMemo(() => Boolean(file) && !isLoading, [file, isLoading]);

  function onImageChange(e: ChangeEvent<HTMLInputElement>) {
    const chosen = e.target.files?.[0] ?? null;
    setFile(chosen);
    setError(null);
    setResult(null);

    if (!chosen) {
      setPreview(null);
      return;
    }

    const url = URL.createObjectURL(chosen);
    setPreview(url);
  }

  function setField<K extends keyof Questionnaire>(key: K, value: Questionnaire[K]) {
    setQuestionnaire((q) => ({ ...q, [key]: value }));
  }

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!file) {
      setError("Please upload a face photo first.");
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const analysis = await analyzeSkin(file, questionnaire);
      setResult(analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="shell">
      <section className="panel panel-elevated">
        <h2>1. Upload Face Photo</h2>
        <p className="muted">Use clear lighting and a front-facing photo for better skin signal detection.</p>

        <label className="uploadZone" htmlFor="imageInput">
          <input
            id="imageInput"
            type="file"
            accept="image/png,image/jpeg,image/webp"
            onChange={onImageChange}
          />
          <span>{file ? `Selected: ${file.name}` : "Drop or choose a JPG/PNG/WEBP image"}</span>
        </label>
        {preview ? <img className="preview" src={preview} alt="Preview" /> : null}
      </section>

      <form className="panel" onSubmit={onSubmit}>
        <h2>2. Personalized Questionnaire</h2>
        <p className="muted">Your answers combine with the image analysis for a tailored routine.</p>

        <label>
          Age range
          <select value={questionnaire.age_range} onChange={(e) => setField("age_range", e.target.value)}>
            <option value="13-17">13-17</option>
            <option value="18-25">18-25</option>
            <option value="26-35">26-35</option>
            <option value="36-50">36-50</option>
            <option value="50+">50+</option>
          </select>
        </label>

        <label>
          Lifestyle
          <select value={questionnaire.lifestyle} onChange={(e) => setField("lifestyle", e.target.value)}>
            <option value="Indoor">Mostly indoor</option>
            <option value="Outdoor">Mostly outdoor</option>
            <option value="Active">Active / sports</option>
          </select>
        </label>

        <label>
          Primary skin concern
          <select
            value={questionnaire.primary_concern}
            onChange={(e) => setField("primary_concern", e.target.value)}
          >
            <option value="Acne / Breakouts">Acne / Breakouts</option>
            <option value="Pigmentation / Dark spots">Pigmentation / Dark spots</option>
            <option value="Redness / Irritation">Redness / Irritation</option>
            <option value="Wrinkles / Fine lines">Wrinkles / Fine lines</option>
            <option value="General maintenance">General maintenance</option>
          </select>
        </label>

        <label>
          Skin sensitivity
          <select
            value={questionnaire.sensitivity_level}
            onChange={(e) => setField("sensitivity_level", e.target.value)}
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Very High">Very High</option>
          </select>
        </label>

        <button disabled={!canSubmit} type="submit">
          {isLoading ? "Analyzing..." : "Analyze & Get Routine"}
        </button>

        {error ? <p className="error">{error}</p> : null}
      </form>

      {result ? (
        <section className="panel results">
          <h2>3. Your Skin Insights</h2>
          <div className="metrics">
            <article>
              <h3>Detected Skin Type</h3>
              <strong>{result.skin_type}</strong>
            </article>
            <article>
              <h3>Dryness</h3>
              <strong>{Math.round(result.metrics.dryness_score * 100)}%</strong>
            </article>
            <article>
              <h3>Redness</h3>
              <strong>{Math.round(result.metrics.redness_score * 100)}%</strong>
            </article>
            <article>
              <h3>Oiliness</h3>
              <strong>{Math.round(result.metrics.oiliness_score * 100)}%</strong>
            </article>
          </div>

          <div className="routineGrid">
            <article>
              <h3>Morning Routine</h3>
              <ul>
                {result.recommendations.morning_routine.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article>
              <h3>Evening Routine</h3>
              <ul>
                {result.recommendations.evening_routine.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article>
              <h3>Targeted Treatments</h3>
              <ul>
                {result.recommendations.targeted_treatments.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article>
              <h3>Lifestyle Habits</h3>
              <ul>
                {result.recommendations.habits.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
          </div>

          <p className="disclaimer">{result.recommendations.disclaimer}</p>
          <p className="muted">Analysis ID: #{result.analysis_id}</p>
        </section>
      ) : null}
    </div>
  );
}
