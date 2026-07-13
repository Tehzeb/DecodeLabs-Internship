import { useEffect, useState } from "react";
import { ThemeProvider } from "./context/ThemeContext";
import Header from "./components/Header";
import Hero from "./components/Hero";
import ProfileForm from "./components/ProfileForm";
import ResultsDashboard from "./components/ResultsDashboard";
import Loader from "./components/Loader";
import { fetchSkillsTaxonomy, fetchInterestTags, getRecommendations } from "./api/client";

function AppInner() {
  const [allSkills, setAllSkills] = useState([]);
  const [allInterests, setAllInterests] = useState([]);

  const [skills, setSkills] = useState([]);
  const [interests, setInterests] = useState([]);
  const [experience, setExperience] = useState(1);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchSkillsTaxonomy().then(setAllSkills).catch(() => setAllSkills([]));
    fetchInterestTags().then(setAllInterests).catch(() => setAllInterests([]));
  }, []);

  const scrollToConsole = () => {
    document.getElementById("console")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const handleSubmit = async () => {
    setError("");
    setLoading(true);
    setResult(null);
    try {
      const data = await getRecommendations({
        skills, interests, experience_years: experience,
      });
      setResult(data);
      setTimeout(() => {
        document.getElementById("results")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch (e) {
      setError(
        e?.response?.data?.detail ||
        "Couldn't reach the recommendation API. Is the FastAPI backend running on http://127.0.0.1:8000?"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg text-text font-body">
      <Header />
      <Hero onStart={scrollToConsole} />
      <ProfileForm
        skills={skills} setSkills={setSkills}
        interests={interests} setInterests={setInterests}
        experience={experience} setExperience={setExperience}
        allSkills={allSkills} allInterests={allInterests}
        onSubmit={handleSubmit} loading={loading} error={error}
      />

      <div id="results">
        {loading && <Loader />}
        {!loading && result && <ResultsDashboard data={result} />}
      </div>

      <footer className="max-w-6xl mx-auto px-6 py-10 text-center text-xs text-dim font-mono">
        VANTAGE — Personalized Career &amp; Skill Path Advisor · FastAPI + React · built for internship project review
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AppInner />
    </ThemeProvider>
  );
}
