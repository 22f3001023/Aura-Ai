# Aura-AI 🌐

## Installation

Install the required dependencies using the following command:

```bash
npm install
```

## Running the Web App

Start the web application with the following command. The app will be available at `http://localhost:5173`:

```bash
npm run dev
```

# 🌐 Aura.AI

Aura.AI is a **Real-Time City Vibe Tracker** that decodes the emotional heartbeat of cities worldwide using **AI, social media, news, and weather signals**.  
It provides insights into how different cities are "feeling" at any given time and helps users explore moods, trends, and vibes around the globe.  

---

## ✨ Features

- 📍 **City Vibes** → Get live emotional sentiment of cities with mood score & emoji.
- 🌦 **Weather Data** → Displays temperature, humidity, wind speed, and condition.
- 📈 **Trending Topics** → Shows what’s buzzing in each city.
- 🔍 **Vibe Explorer** → Explore detailed metrics for individual cities.
- 😎 **Mood Feed** → Quick overview of vibes across multiple cities.
- ℹ️ **About** → Learn more about the project and its mission.

---

## 📸 Screenshots

### Homepage
Fetch and save the vibes of all cities.  
*(Button changes from **Get All The Vibes** → **Update The Vibes** if data exists in local storage)*  

### Mood Feed
Displays a grid of mood cards with:
- Mood label & emoji
- Sentiment score
- Headline
- Weather details
- Trending topics

---

## 🛠️ Tech Stack

- **Frontend:** React + Tailwind CSS  
- **Routing:** React Router  
- **Storage:** LocalStorage (for vibes & mood data persistence)  
- **UI/UX:** Glassmorphism, gradient hover effects, responsive design  

---

## 🚀 Getting Started

### 1️⃣ Install dependencies
```bash
npm install
```

### 2️⃣ Run the app
```bash
npm run dev
```

App runs at → http://localhost:5173

---

## 📂 Project Structure
```
src/
 │── Navbar.jsx       # Navigation bar
 │── Mood.jsx         # Mood Feed page
 │── City.jsx         # Vibe Explorer page
 │── AboutUs.jsx      # About page
 │── App.jsx          # Main landing page
 ├── assets/          # Backgrounds & images
 └── main.jsx         # Entry point
```

---

## 📌 How It Works

1. On landing page → Click **Get All The Vibes** (or **Update The Vibes** if data exists).
2. Data is stored in **localStorage**:
   - `aura_fetch_data`
   - `aura_mood_data`
3. Navigate to **Mood Feed** or **Vibe Explorer** to see city-wise vibes.
4. If data is missing, the app redirects back to homepage to fetch it first.

---

## 🎯 Future Improvements

- 🌍 Live API integration for real-time vibes.
- 📊 Advanced analytics (mood trends over time).
- 🗺️ Interactive world map with city vibes.
- 📱 Mobile PWA support.