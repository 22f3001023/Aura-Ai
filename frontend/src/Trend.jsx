import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

// Utility: emoji by mood
const getMoodEmoji = (mood) => {
  switch (mood?.toLowerCase()) {
    case "positive":
    case "very positive":
      return "😀";
    case "negative":
    case "very negative":
      return "😡";
    case "neutral":
      return "😐";
    default:
      return "🤔";
  }
};

function Trend() {
  const { city_name } = useParams();
  const navigate = useNavigate();
  const [cityData, setCityData] = useState(null);
  const [headline, setHeadline] = useState("");
  const [futureMood, setFutureMood] = useState("");

  useEffect(() => {
    // check local storage
    const rawMood = JSON.parse(localStorage.getItem("aura_mood_data")) || {};
    const rawHeadlines = JSON.parse(localStorage.getItem("aura_headlines_batch")) || {};
    const rawFuture = JSON.parse(localStorage.getItem("aura_future_forecast")) || {};

    const storedData = rawMood.data || [];
    const foundCity = storedData.find(
      (c) => c.city.toLowerCase() === city_name.toLowerCase()
    );

    if (!foundCity) {
      alert(`⚠️ No trend data for ${city_name}. Please Get All The Vibes first.`);
      setTimeout(() => navigate("/"), 3000);
      return;
    }

    setCityData(foundCity);

    // headline lookup
    const headlineEntry =
      rawHeadlines?.data?.find(
        (h) => h.city.toLowerCase() === city_name.toLowerCase()
      ) || null;
    if (headlineEntry) {
      setHeadline(headlineEntry.enhanced_headline);
    }

    // future mood lookup
    const futureEntry =
      rawFuture?.future_moods?.find(
        (f) => f.city.toLowerCase() === city_name.toLowerCase()
      ) || null;
    if (futureEntry) {
      setFutureMood(futureEntry.future_mood);
    }
  }, [city_name, navigate]);

  if (!cityData) {
    return (
      <div className="min-h-screen text-white flex items-center justify-center">
        Loading trends...
      </div>
    );
  }

  const {
    city,
    mood_metrics = {},
    weather = {},
    trending_topics = [],
  } = cityData;

  return (
    <div className="min-h-screen text-white p-6 flex flex-col gap-8">
      {/* Navbar */}
      <nav className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-extrabold">🌐 Aura.AI</h1>
        <a
          href="/vibe"
          className="px-4 py-2 bg-zinc-800 rounded-xl hover:bg-zinc-700 transition"
        >
          ⬅ Back
        </a>
      </nav>

      {/* City Header */}
      <div className="text-center">
        <h1 className="text-4xl font-extrabold mb-2">{city}</h1>
        <p className="text-lg font-semibold">
          {mood_metrics.mood_label || "Unknown"}{" "}
          {mood_metrics.mood_emoji || getMoodEmoji(mood_metrics.mood_label)}
        </p>
      </div>

      {/* Headline */}
      {headline && (
        <div className="text-center">
          <p className="text-2xl font-bold text-cyan-300 drop-shadow-lg">
            📰 {headline}
          </p>
        </div>
      )}

      {/* Future Mood */}
      {futureMood && (
        <div className="text-center">
          <p className="text-xl italic text-pink-300 drop-shadow">
            🔮 {futureMood}
          </p>
        </div>
      )}

      {/* Weather */}
      <div className="flex justify-center">
        <div className="p-6 rounded-2xl shadow-lg w-72 bg-black/30 backdrop-blur-md">
          <h3 className="text-xl font-semibold mb-2">🌦 Weather</h3>
          <p>
            {weather.temperature_c}°C • {weather.condition}
          </p>
          <p className="text-sm text-zinc-400">
            Humidity: {weather.humidity}% • Wind: {weather.wind_kph} km/h
          </p>
        </div>
      </div>

      {/* Sentiment Distribution */}
      <div className="max-w-3xl mx-auto p-6 rounded-2xl shadow-lg bg-black/30 backdrop-blur-md">
        <h3 className="text-xl font-bold mb-4">📊 Sentiment Distribution</h3>
        <ul className="space-y-2">
          <li>😀 Positive: {mood_metrics.sentiment_distribution?.positive || 0}%</li>
          <li>😡 Negative: {mood_metrics.sentiment_distribution?.negative || 0}%</li>
          <li>😐 Neutral: {mood_metrics.sentiment_distribution?.neutral || 0}%</li>
        </ul>
      </div>

      {/* Trending Topics */}
      <div className="max-w-3xl mx-auto p-6 rounded-2xl shadow-lg bg-black/30 backdrop-blur-md">
        <h3 className="text-xl font-bold mb-4">📈 Trending Topics</h3>
        <div className="flex flex-wrap gap-3">
          {(trending_topics || []).map((topic, idx) => (
            <span
              key={idx}
              className="px-4 py-2 bg-indigo-600 rounded-full text-sm shadow"
            >
              #{topic}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Trend;