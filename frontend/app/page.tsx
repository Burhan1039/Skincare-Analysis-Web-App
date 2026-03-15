import SkinAnalyzerForm from "@/components/SkinAnalyzerForm";

export default function HomePage() {
  return (
    <main className="page">
      <header className="hero">
        <p className="eyebrow">Consumer Skincare Assistant</p>
        <h1>SkinSense AI</h1>
        <p>
          Facial image signals + personalized questionnaire to generate custom, easy-to-follow skincare plans.
        </p>
      </header>
      <SkinAnalyzerForm />
    </main>
  );
}
