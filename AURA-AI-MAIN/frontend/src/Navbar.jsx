import React from "react";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const navItems = [
    { path: "/vibe", label: "🌍 Vibe Explorer", glow: "from-blue-400 to-purple-500" },
    { path: "/mood", label: "😎 Mood Feed", glow: "from-cyan-400 to-teal-500" },
    { path: "/about", label: "ℹ️ About", glow: "from-pink-400 to-fuchsia-500" },
  ];

  return (
    <nav className="w-full flex items-center justify-between px-8 py-4 backdrop-blur-lg bg-white/5 border-b border-white/20 fixed top-0 left-0 z-50">
      
      {/* Logo */}
      <div
        onClick={() => navigate("/")}
        className="flex items-center gap-2 text-2xl font-extrabold text-white cursor-pointer select-none"
      >
        <span className="inline-block transition-transform duration-700 hover:rotate-[360deg]">
          🌐
        </span>
        <span>AURA.AI</span>
      </div>

      {/* Nav Items */}
      <div className="flex gap-6">
        {navItems.map((btn, i) => (
          <button
            key={i}
            onClick={() => navigate(btn.path)}
            className="relative px-6 py-3 rounded-2xl text-lg font-semibold text-white shadow-lg backdrop-blur-lg bg-white/10 border border-white/20 transition overflow-hidden group"
          >
            {/* Glow border on hover */}
            <span
              className={`absolute inset-0 rounded-2xl border-2 border-transparent group-hover:bg-gradient-to-r group-hover:${btn.glow} group-hover:shadow-[0_0_20px_rgba(255,255,255,0.4)] transition-all duration-500`}
            ></span>

            <span className="relative z-10">{btn.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}

export default Navbar;
