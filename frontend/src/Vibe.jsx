import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import Navbar from "./Navbar";

function Vibe() {
  const [cities, setCities] = useState([]);
  const [headlines, setHeadlines] = useState([]);
  const [loadingMsg, setLoadingMsg] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = localStorage.getItem("aura_fetch_data");
    const moodData = localStorage.getItem("aura_mood_data");
    const headlinesData = localStorage.getItem("aura_headlines_batch");

    if (!fetchData || !moodData || !headlinesData) {
      setLoadingMsg("⚠️ First fetch all vibes!");
      setTimeout(() => navigate("/"), 3000);
      return;
    }

    try {
      const parsedData = JSON.parse(fetchData);
      const moodParsed = JSON.parse(moodData);
      const headlinesParsed = JSON.parse(headlinesData);

      let combinedData = [];
      if (moodParsed?.data) {
        combinedData = moodParsed.data;
      } else if (parsedData?.data) {
        combinedData = parsedData.data;
      }

      const indianCities = combinedData.filter((c) =>
        ["India"].includes(c.country) ||
        c.city.match(
          /Delhi|Mumbai|Chennai|Bangalore|Hyderabad|Kolkata|Ahmedabad|Jaipur|Lucknow|Pune/i
        )
      );

      setCities(indianCities);
      setHeadlines(headlinesParsed?.data || []);
    } catch (err) {
      console.error("Error parsing localStorage data:", err);
    }
  }, [navigate]);

  const getHeadlineForCity = (cityName) => {
    return headlines.find(
      (h) => h.city.toLowerCase() === cityName.toLowerCase()
    );
  };

  return (
    <div className="relative w-full h-screen bg-black text-white">
      <Navbar />
      {loadingMsg && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/80 text-white text-2xl font-semibold z-50">
          {loadingMsg}
        </div>
      )}

      {!loadingMsg && (
        <MapContainer
          center={[22, 78]}
          zoom={5}
          scrollWheelZoom={true}
          className="w-full h-full z-0"
        >
          {/* Dark Theme Tile Layer */}
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>'
            subdomains={["a", "b", "c"]}
            maxZoom={19}
          />

          {/* City Markers */}
          {cities.map((city, i) => {
            const headline = getHeadlineForCity(city.city);

            return (
              <CircleMarker
                key={i}
                center={[city.coordinates.lat, city.coordinates.lon]}
                pathOptions={{
                  color: "cyan",
                  fillColor: "cyan",
                  fillOpacity: 0.5,
                }}
                radius={15}
              >
                <Popup>
                  <div className="p-4 text-center bg-black/70 backdrop-blur-xl rounded-2xl border border-white/20 text-white shadow-xl">
                    <h2 className="font-bold text-lg mb-2">
                      {city.city}, {city.country}
                    </h2>

                    {/* Enhanced Headline */}
                    <p className="text-sm mb-3 italic text-indigo-300">
                      {headline?.enhanced_headline || city.headline || "✨ Mood detected"}
                    </p>

                    {/* News & Tweets Count */}
                    {headline?.data_used && (
                      <p className="text-xs text-zinc-400 mb-3">
                        📰 News: {headline.data_used.news_count} | 🐦 Tweets:{" "}
                        {headline.data_used.tweets_count}
                      </p>
                    )}

                    {/* Trending Topics */}
                    {headline?.data_used?.trending_topics && (
                      <div className="flex flex-wrap justify-center gap-2 mb-3">
                        {headline.data_used.trending_topics.map((topic, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-indigo-600/60 rounded-full text-xs shadow"
                          >
                            #{topic}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Buttons */}
                    <div className="flex flex-col gap-2">
                      <button
                        onClick={() => navigate(`/city/${city.city}`)}
                        className="relative w-full py-3 rounded-3xl text-lg font-semibold text-white shadow-xl 
                                   backdrop-blur-lg bg-gradient-to-r from-pink-500 to-yellow-500 
                                   hover:from-yellow-500 hover:to-pink-500 transition-all duration-500"
                      >
                        City Details
                      </button>

                      <button
                        onClick={() => navigate(`/trend/${city.city}`)}
                        className="relative w-full py-3 rounded-3xl text-lg font-semibold text-white shadow-xl 
                                   backdrop-blur-lg bg-gradient-to-r from-blue-500 to-green-500 
                                   hover:from-green-500 hover:to-blue-500 transition-all duration-500"
                      >
                        Trends
                      </button>
                    </div>
                  </div>
                </Popup>
              </CircleMarker>
            );
          })}
        </MapContainer>
      )}
    </div>
  );
}

export default Vibe;
