import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";

// Utility for emotion color
const getEmotionColor = (mood) => {
  if (!mood) return "text-gray-400";
  switch (mood.toLowerCase()) {
    case "positive":
    case "very positive":
    case "slightly positive":
      return "text-green-400";
    case "negative":
    case "very negative":
      return "text-red-400";
    case "neutral":
      return "text-gray-300";
    default:
      return "text-orange-400";
  }
};

function Mood() {
  const [cities, setCities] = useState([]);
  const [loadingMsg, setLoadingMsg] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = localStorage.getItem("aura_fetch_data");
    const moodData = localStorage.getItem("aura_mood_data");

    // ✅ If not available → warn + redirect
    if (!fetchData || !moodData) {
      setLoadingMsg("⚠️ First fetch all vibes!");
      setTimeout(() => navigate("/"), 3000);
      return;
    }

    try {
      const raw = JSON.parse(moodData) || {};
      setCities(raw.data || []);
    } catch (err) {
      console.error("Failed to load aura_mood_data:", err);
      setCities([]);
    }
  }, [navigate]);

  if (loadingMsg) {
    return (
      <div className="min-h-screen text-white flex items-center justify-center">
        {loadingMsg}
      </div>
    );
  }

  if (!cities || cities.length === 0) {
    return (
      <div className="min-h-screen text-white flex items-center justify-center">
        ⚠️ No mood data found. Please Get All The Vibes first.
      </div>
    );
  }

  return (
    <div className="min-h-screen text-white flex flex-col">
      {/* Navbar */}
      <Navbar />

      {/* Top spacing */}
      <div className="mt-20 px-6 flex flex-col gap-8">
        {/* Mood Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {cities.map((city, idx) => (
            <div
              key={idx}
              className="p-6 rounded-2xl shadow-lg bg-black/30 backdrop-blur-md"
            >
              {/* Header */}
              <h2 className="text-2xl font-bold mb-2">{city.city}</h2>
              <p className="text-sm text-zinc-400 mb-2">
                {new Date(city.timestamp).toLocaleString()}
              </p>

              {/* Mood */}
              <p
                className={`text-lg font-semibold flex items-center gap-2 ${getEmotionColor(
                  city.mood_metrics?.mood_label
                )}`}
              >
                {city.mood_metrics?.mood_label}{" "}
                {city.mood_metrics?.mood_emoji || "🤔"}
                • Score: {city.mood_metrics?.avg_sentiment?.toFixed(2)}
              </p>

              {/* Headline */}
              <p className="mt-2 italic text-indigo-300">“{city.headline}”</p>

              {/* Weather */}
              {city.weather && (
                <div className="mt-3 text-sm text-zinc-300">
                  🌦 {city.weather.temperature_c}°C • {city.weather.condition}
                  <br />
                  💨 {city.weather.wind_kph} km/h • Humidity:{" "}
                  {city.weather.humidity}%
                </div>
              )}

              {/* Trending topics */}
              <div className="mt-4">
                <h3 className="text-sm font-bold mb-1">📈 Trending</h3>
                <div className="flex flex-wrap gap-2">
                  {(city.trending_topics || []).map((topic, tIdx) => (
                    <span
                      key={tIdx}
                      className="px-3 py-1 bg-indigo-600/60 rounded-full text-xs shadow"
                    >
                      #{topic}
                    </span>
                  ))}
                </div>
              </div>

              {/* Data Quality */}
              <p className="text-xs text-zinc-500 mt-3">
                Confidence: {city.confidence} • Sample: {city.sample_size} •{" "}
                Quality: {city.data_quality}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Mood;
