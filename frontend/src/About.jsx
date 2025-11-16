import React from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";

export default function AboutUS() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen text-white flex flex-col">
      {/* Navbar */}
      <Navbar />
      <div></div>
      {/* Content */}
      <div className="mt-20 px-6 max-w-4xl mx-auto flex flex-col gap-8">
        {/* Title */}
        <div className="text-center">
          <h1 className="text-4xl font-extrabold mb-4"><span className="inline-block transition-transform duration-700 hover:rotate-[360deg]">
          🌐
        </span> About Aura.AI</h1>
          <p className="text-lg text-zinc-300">
            Aura.AI is your{" "}
            <span className="font-semibold text-indigo-400">
              real-time city companion
            </span>
            , helping you explore{" "}
            <span className="font-semibold text-indigo-400">urban moods</span>,
            track{" "}
            <span className="font-semibold text-indigo-400">
              community sentiment
            </span>
            , and understand{" "}
            <span className="font-semibold text-indigo-400">
              everyday city life
            </span>{" "}
            like never before.
          </p>
        </div>

        {/* Mission */}
        <section className="bg-black/30 backdrop-blur-md p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold mb-2">🚀 Our Mission</h2>
          <p className="text-zinc-300">
            We aim to transform{" "}
            <span className="font-semibold text-teal-400">raw city data</span>{" "}
            into{" "}
            <span className="font-semibold text-pink-400">meaningful insights</span>
            . From{" "}
            <span className="text-yellow-400">weather and news</span> to{" "}
            <span className="text-indigo-400">social media vibes</span>, Aura.AI
            blends real-time information with{" "}
            <span className="font-semibold">AI-powered analysis</span> to help
            people and cities thrive.
          </p>
        </section>

        {/* Features */}
        <section className="bg-black/30 backdrop-blur-md p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold mb-2">✨ Key Features</h2>
          <ul className="list-disc list-inside space-y-2 text-zinc-300">
            <li>
              <span className="font-semibold text-indigo-400">🌍 Vibe Explorer</span>{" "}
              → Visualize moods across cities with an{" "}
              <span className="text-cyan-400">interactive live map</span>.
            </li>
            <li>
              <span className="font-semibold text-indigo-400">📊 Mood Insights</span>{" "}
              → Track{" "}
              <span className="text-green-400">sentiment trends</span> and{" "}
              <span className="text-yellow-400">forecast future moods</span>.
            </li>
            <li>
              <span className="font-semibold text-indigo-400">🌦 City Dashboard</span>{" "}
              → Explore{" "}
              <span className="text-pink-400">weather, tweets, and news</span> in
              one place.
            </li>
            <li>
              <span className="font-semibold text-indigo-400">🎮 Fun Add-ons</span>{" "}
              → Take a break with built-in mini games like{" "}
              <span className="text-teal-400">Tic Tac Toe</span> while vibes load.
            </li>
          </ul>
        </section>

        {/* Get Involved */}
        <section className="bg-black/30 backdrop-blur-md p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold mb-2">🤝 Get Involved</h2>
          <p className="text-zinc-300">
            Aura.AI is built for{" "}
            <span className="font-semibold">citizens, city planners, and
            innovators</span>. Whether you want to{" "}
            <span className="text-teal-400">analyze vibes</span>,{" "}
            <span className="text-indigo-400">design smarter cities</span>, or{" "}
            <span className="text-pink-400">connect communities</span>, there’s a
            place for you here.
          </p>
          <p className="mt-4 text-zinc-400 italic">
            Together, let’s make cities more vibrant, resilient, and
            future-ready 🌍.
          </p>
        </section>

        {/* Play Game Button */}
        <div className="flex justify-center mt-6">
          <button
            onClick={() => navigate("/tictac")}
            className="px-6 py-3 rounded-2xl bg-gradient-to-r from-indigo-500 to-pink-500 
                       text-white font-semibold shadow-lg hover:from-pink-500 hover:to-indigo-500 
                       transition-all duration-300"
          >
            🎮 Play Tic Tac Toe
          </button>
        </div>
      </div>
    </div>
  );
}