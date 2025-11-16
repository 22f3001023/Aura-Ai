import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import TicTac from "./TicTac";

function App() {
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showLoader, setShowLoader] = useState(false);
  const navigate = useNavigate();

  // ✅ Helper: Check if data is stale (>7 hours old)
  const isDataStale = (timestamp) => {
    if (!timestamp) return true;
    const currentTime = new Date();
    const lastTime = new Date(timestamp);
    const diffHours = (currentTime - lastTime) / (1000 * 60 * 60);
    return diffHours >= 7;
  };

  // ✅ On mount check localStorage
  useEffect(() => {
    try {
      const fetchData = JSON.parse(localStorage.getItem("aura_fetch_data"));
      const moodData = JSON.parse(localStorage.getItem("aura_mood_data"));
      const forecastData = JSON.parse(localStorage.getItem("aura_future_forecast"));
      const headlinesBatch = JSON.parse(localStorage.getItem("aura_headlines_batch"));

      if (fetchData && moodData && forecastData && headlinesBatch) {
        // Check timestamp from headlinesBatch
        const firstCity = headlinesBatch.data?.[0];
        if (firstCity && isDataStale(firstCity.headline_generated_at)) {
          console.warn("⚠️ Data stale. Clearing localStorage...");
          localStorage.removeItem("aura_fetch_data");
          localStorage.removeItem("aura_mood_data");
          localStorage.removeItem("aura_future_forecast");
          localStorage.removeItem("aura_headlines_batch");
          setSaved(false);
        } else {
          setSaved(true);
        }
      }
    } catch (err) {
      console.error("Error checking localStorage:", err);
    }
  }, []);

  const handleFetchAndSave = async () => {
    setLoading(true);
    setShowLoader(true); // show fun loader

    try {
      // POST /api/cities/fetch-and-save
      const fetchRes = await axios.post("/api/cities/fetch-and-save");
      if (fetchRes.data) {
        localStorage.setItem("aura_fetch_data", JSON.stringify(fetchRes.data));
      }

      // GET /api/cities/mood
      const moodRes = await axios.get("/api/cities/mood");
      if (moodRes.data) {
        localStorage.setItem("aura_mood_data", JSON.stringify(moodRes.data));
      }

      // POST /api/headlines/future_mood_forecast_batch
      const forecastRes = await axios.post(
        "/api/headlines/future_mood_forecast_batch",
        fetchRes.data // send aura_fetch_data
      );
      if (forecastRes.data) {
        localStorage.setItem("aura_future_forecast", JSON.stringify(forecastRes.data));
      }

      // POST /api/headlines/generate-batch
      const headlinesBatch = await axios.post(
        "/api/headlines/generate-batch",
        fetchRes.data // send aura_fetch_data
      );
      if (headlinesBatch.data) {
        localStorage.setItem("aura_headlines_batch", JSON.stringify(headlinesBatch.data));
      }

      setSaved(true);
    } catch (err) {
      console.error("Error fetching vibes:", err);
    }

    setLoading(false);
    setTimeout(() => setShowLoader(false), 2000); // hide loader after a short delay
  };

  return (
    <div
      className="min-h-screen w-full text-white flex flex-col items-center justify-center"
      style={{
        background:
          "url('/src/assets/a9b58400-ad48-45d4-b449-ba5a326eff15.png') no-repeat center center fixed",
        backgroundSize: "cover",
      }}
    >
      {/* Overlay */}
      <div className="min-h-screen w-full bg-black/50 flex flex-col items-center justify-center px-6">
        {/* Loader / Game */}
        {showLoader && (
  <div className="fixed inset-0 flex items-center justify-center bg-black/80 z-50">
    <div className="flex flex-col items-center gap-6">
      <TicTac />
      <p className="text-lg text-zinc-200 animate-pulse">
        🌍 Fetching vibes... this may take up to 2 minutes
      </p>
    </div>
  </div>
)}

        {/* Hero Card */}
        <div className="relative backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl rounded-3xl p-10 max-w-3xl text-center overflow-hidden">
          {/* Card Glow */}
          <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-cyan-400/20 via-fuchsia-500/20 to-purple-600/20 blur-3xl"></div>

          <div className="relative z-10">
            <h1 className="text-6xl font-extrabold mb-6 drop-shadow-lg">
              🌐 Aura.AI
            </h1>
            <p className="text-xl text-zinc-200 mb-4">
              The Real-Time City Vibe Tracker
            </p>
            <p className="text-lg text-zinc-300 mb-10">
              Decode the emotional heartbeat of cities worldwide using AI,
              social media, news, and weather signals.
            </p>

            {/* Main Fetch Button */}
            <button
              onClick={handleFetchAndSave}
              disabled={loading}
              className="relative px-10 py-4 rounded-3xl text-2xl font-bold transition backdrop-blur-lg bg-white/10 border border-white/20 shadow-xl group"
            >
              <span className="absolute inset-0 rounded-3xl border-2 border-transparent group-hover:bg-gradient-to-r group-hover:from-cyan-400 group-hover:to-fuchsia-500 group-hover:shadow-[0_0_25px_rgba(168,85,247,0.8)] transition-all duration-500"></span>
              <span className="relative z-10 group-hover:text-cyan-300 group-hover:drop-shadow-lg transition">
                {loading
                  ? "Fetching..."
                  : saved
                  ? "Update The Vibes"
                  : "Get All The Vibes"}
              </span>
            </button>

            {/* Success Message */}
            {saved && !loading && (
              <p className="mt-6 text-green-400 font-semibold">
                ✅ Vibes are ready! Explore how your cities feel 🌍🔥
              </p>
            )}
          </div>
        </div>

        {/* Navigation Buttons */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
          {[
            { path: "/vibe", label: "🌍 Vibe Explorer", glow: "from-blue-400 to-purple-500" },
            { path: "/mood", label: "😎 Mood Feed", glow: "from-cyan-400 to-teal-500" },
            { path: "/about", label: "ℹ️ About", glow: "from-pink-400 to-fuchsia-500" },
          ].map((btn, i) => (
            <button
              key={i}
              onClick={() => navigate(btn.path)}
              className="relative w-full py-8 rounded-3xl text-xl font-semibold text-white shadow-xl backdrop-blur-lg bg-white/10 border border-white/20 transition overflow-hidden group"
            >
              <span
                className={`absolute inset-0 rounded-3xl border-2 border-transparent group-hover:bg-gradient-to-r group-hover:${btn.glow} group-hover:shadow-[0_0_25px_rgba(255,255,255,0.5)] transition-all duration-500`}
              ></span>
              <span className="relative z-10 group-hover:scale-105 transition">
                {btn.label}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
