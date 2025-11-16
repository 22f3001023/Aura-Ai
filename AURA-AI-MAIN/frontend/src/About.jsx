import React from "react";
import Navbar from "./Navbar";

export default function AboutUS() {
  return (
    <div className="min-h-screen text-white flex flex-col">
      {/* Navbar */}
      <Navbar />

      {/* Content */}
      <div className="mt-20 px-6 max-w-4xl mx-auto flex flex-col gap-8">
        {/* Title */}
        <div className="text-center">
          <h1 className="text-4xl font-extrabold mb-4">🌐 About Aura.AI</h1>
          <p className="text-lg text-zinc-300">
            Aura.AI is your real-time companion for exploring{" "}
            <span className="font-semibold text-indigo-400">urban moods</span>,
            understanding{" "}
            <span className="font-semibold text-indigo-400">
              community sentiment
            </span>
            , and making sense of{" "}
            <span className="font-semibold text-indigo-400">
              everyday city life
            </span>
            .
          </p>
        </div>

        {/* Mission */}
        <section className="bg-black/30 backdrop-blur-md p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold mb-2">🚀 Our Mission</h2>
          <p className="text-zinc-300">
            We aim to empower people with{" "}
            <span className="font-semibold">actionable insights</span> about
            their environment — from{" "}
            <span className="text-teal-400">air quality</span> to{" "}
            <span className="text-pink-400">social vibes</span>. By blending
            real-time data with AI-powered analysis, Aura.AI helps you
            understand how your city feels — and where it’s headed.
          </p>
        </section>

        {/* Features */}
        <section className="bg-black/30 backdrop-blur-md p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold mb-2">✨ Features</h2>
          <ul className="list-disc list-inside space-y-2 text-zinc-300">
            <li>
              <span className="font-semibold text-indigo-400">Vibe Explorer</span>{" "}
              → Visualize live city moods on an interactive map.
            </li>
            <li>
              <span className="font-semibold text-indigo-400">Mood Feed</span>{" "}
              → Stay updated with trending vibes across cities.
            </li>
            <li>
              <span className="font-semibold text-indigo-400">City Insights</span>{" "}
              → Explore detailed sentiment, weather, and topics per city.
            </li>
            <li>
              <span className="font-semibold text-indigo-400">Trends</span>{" "}
              → Discover how moods shift over time and forecast future vibes.
            </li>
          </ul>
        </section>

        {/* Get Involved */}
        <section className="bg-black/30 backdrop-blur-md p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold mb-2">🤝 Get Involved</h2>
          <p className="text-zinc-300">
            Aura.AI is for{" "}
            <span className="font-semibold">citizens, city planners, and
            innovators</span>. Whether you want to{" "}
            <span className="text-teal-400">analyze vibes</span>,{" "}
            <span className="text-indigo-400">build smarter cities</span>, or{" "}
            <span className="text-pink-400">connect with communities</span>,
            we’d love to collaborate.
          </p>
          <p className="mt-4 text-zinc-400 italic">
            Together, let’s make cities more vibrant, connected, and
            sustainable 🌍.
          </p>
        </section>
      </div>
    </div>
  );
}