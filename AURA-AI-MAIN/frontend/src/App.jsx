import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function App() {
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // ✅ On mount check localStorage
  useEffect(() => {
    const fetchData = localStorage.getItem("aura_fetch_data");
    const moodData = localStorage.getItem("aura_mood_data");
    if (fetchData && moodData) {
      setSaved(true);
    }
  }, []);

  const handleFetchAndSave = async () => {
    setLoading(true);
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

      setSaved(true);
    } catch (err) {
      console.error("Error fetching vibes:", err);
    }
    setLoading(false);
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
              {/* Glow border on hover (gradient) */}
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
            {
              path: "/vibe",
              label: "🌍 Vibe Explorer",
              glow: "from-blue-400 to-purple-500",
            },
            {
              path: "/mood",
              label: "😎 Mood Feed",
              glow: "from-cyan-400 to-teal-500",
            },
            {
              path: "/about",
              label: "ℹ️ About",
              glow: "from-pink-400 to-fuchsia-500",
            },
          ].map((btn, i) => (
            <button
              key={i}
              onClick={() => navigate(btn.path)}
              className="relative w-full py-8 rounded-3xl text-xl font-semibold text-white shadow-xl backdrop-blur-lg bg-white/10 border border-white/20 transition overflow-hidden group"
            >
              {/* Glow border on hover */}
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
