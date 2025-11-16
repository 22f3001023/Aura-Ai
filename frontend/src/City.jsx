import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

// Utility: emoji by mood
const getMoodEmoji = (mood) => {
  switch (mood?.toLowerCase()) {
    case "positive":
      return "😀";
    case "negative":
      return "😡";
    case "neutral":
      return "😐";
    default:
      return "🤔";
  }
};

function City() {
  const { city_name } = useParams();
  const navigate = useNavigate();
  const [cityData, setCityData] = useState(null);
  const [headline, setHeadline] = useState("");

  useEffect(() => {
    try {
      // get all saved vibes from localStorage
      const raw = JSON.parse(localStorage.getItem("aura_fetch_data")) || {};
      const storedData = raw.data || [];

      // find current city
      const foundCity = storedData.find(
        (c) => c.city.toLowerCase() === city_name.toLowerCase()
      );

      if (!foundCity) {
        alert(`⚠️ No data found for ${city_name}. Please Get All The Vibes first.`);
        setTimeout(() => navigate("/"), 3000);
        return;
      }

      setCityData(foundCity);

      // ✅ pull from aura_headlines_batch
      const headlinesRaw = JSON.parse(localStorage.getItem("aura_headlines_batch")) || {};
      const headlinesData = headlinesRaw.data || [];

      const matchedHeadline = headlinesData.find(
        (h) => h.city.toLowerCase() === city_name.toLowerCase()
      );

      if (matchedHeadline?.enhanced_headline) {
        setHeadline(matchedHeadline.enhanced_headline);
      } else {
        setHeadline("✨ No headline available, but vibes are still alive!");
      }
    } catch (err) {
      console.error("Error loading city/headline:", err);
      setHeadline("⚠️ Couldn’t load headline.");
    }
  }, [city_name, navigate]);

  if (!cityData) {
    return (
      <div className="min-h-screen text-white flex items-center justify-center">
        Loading city data...
      </div>
    );
  }

  const {
    city,
    weather = {},
    news = [],
    tweets = [],
    trending_topics = [],
    mood_summary = {},
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
          {mood_summary.mood_label || "Unknown"} {getMoodEmoji(mood_summary.mood_label)}
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

      {/* Tweets & News */}
      <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto w-full">
        {/* Tweets */}
        <div className="p-6 rounded-2xl shadow-lg bg-black/30 backdrop-blur-md">
          <h3 className="text-xl font-bold mb-4">🐦 Live Tweets</h3>
          <ul className="space-y-3 max-h-96 overflow-y-auto">
            {(tweets || []).map((tweet, idx) => (
              <li key={idx} className="border-b border-zinc-700 pb-2">
                <p>{tweet.text}</p>
                <p className="text-sm text-zinc-400">
                  👍 {tweet.like_count || 0} • 🔁 {tweet.retweet_count || 0}
                </p>
              </li>
            ))}
          </ul>
        </div>

        {/* News */}
        <div className="p-6 rounded-2xl shadow-lg bg-black/30 backdrop-blur-md">
          <h3 className="text-xl font-bold mb-4">📰 News</h3>
          <ul className="space-y-3 max-h-96 overflow-y-auto">
            {(news || []).map((article, idx) => (
              <li key={idx} className="border-b border-zinc-700 pb-2">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:underline"
                >
                  {article.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
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

export default City;
