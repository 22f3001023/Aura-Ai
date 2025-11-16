# # # # services/data_collector.py
# # # import requests
# # # import time
# # # from datetime import datetime, timedelta
# # # from typing import Dict, List
# # # import re
# # # import logging
# # # from google import genai
# # # from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# # # from concurrent.futures import ThreadPoolExecutor, as_completed

# # # logger = logging.getLogger(__name__)

# # # class AuraDataCollector:
# # #     def __init__(self, gemini_api_key: str):
# # #         self.news_api_key = "47e7597b3e51433a81fcc3d908b1a792"
# # #         self.weather_api_key = "5a5c9571ba254b1c90b152042243103"
# # #         self.twitter_api_key = "984d78e1femsh2af122397b07360p15059bjsn900a6a3b90fa"
# # #         self.gemini_api_key = 'AIzaSyA2RlQlMPZgju5FmSkItPdsP4rQqTVMFCA'
        
# # #         self.analyzer = SentimentIntensityAnalyzer()
# # #         self.gemini_client = genai.Client(api_key=gemini_api_key)
        
# # #         self.indian_cities = {
# # #             "Mumbai": {"lat": 19.0760, "lon": 72.8777, "keywords": ["mumbai", "bombay"]},
# # #             "Delhi": {"lat": 28.7041, "lon": 77.1025, "keywords": ["delhi", "new delhi"]},
# # #             "Bangalore": {"lat": 12.9716, "lon": 77.5946, "keywords": ["bangalore", "bengaluru"]},
# # #             "Chennai": {"lat": 13.0827, "lon": 80.2707, "keywords": ["chennai", "madras"]},
# # #             "Kolkata": {"lat": 22.5726, "lon": 88.3639, "keywords": ["kolkata", "calcutta"]},
# # #             "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "keywords": ["hyderabad"]},
# # #             "Pune": {"lat": 18.5204, "lon": 73.8567, "keywords": ["pune"]},
# # #             "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "keywords": ["ahmedabad"]},
# # #             "Jaipur": {"lat": 26.9124, "lon": 75.7873, "keywords": ["jaipur"]},
# # #             "Lucknow": {"lat": 26.8467, "lon": 80.9462, "keywords": ["lucknow"]}
# # #         }

# # #     def get_weather_data(self, city: str) -> Dict:
# # #         """Fetch current weather data for a city"""
# # #         try:
# # #             city_info = self.indian_cities[city]
# # #             url = "http://api.weatherapi.com/v1/current.json"
# # #             params = {
# # #                 'key': self.weather_api_key,
# # #                 'q': f"{city_info['lat']},{city_info['lon']}",
# # #                 'aqi': 'yes'
# # #             }
            
# # #             response = requests.get(url, params=params, timeout=10)
# # #             response.raise_for_status()
# # #             data = response.json()
            
# # #             return {
# # #                 'temperature_c': data['current']['temp_c'],
# # #                 'condition': data['current']['condition']['text'],
# # #                 'humidity': data['current']['humidity'],
# # #                 'wind_kph': data['current']['wind_kph'],
# # #                 'feels_like_c': data['current']['feelslike_c'],
# # #                 'air_quality_pm25': data['current'].get('air_quality', {}).get('pm2_5', 0),
# # #             }
# # #         except Exception as e:
# # #             logger.error(f"Weather API error for {city}: {e}")
# # #             return {}

# # #     def get_news_data(self, city: str) -> List[Dict]:
# # #         """Fetch exactly 10 news articles"""
# # #         try:
# # #             news_items = []
# # #             for keyword in self.indian_cities[city]["keywords"]:
# # #                 if len(news_items) >= 10:
# # #                     break
                    
# # #                 url = "https://newsapi.org/v2/everything"
# # #                 params = {
# # #                     'apiKey': self.news_api_key,
# # #                     'q': f"{keyword} AND india",
# # #                     'language': 'en',
# # #                     'sortBy': 'publishedAt',
# # #                     'pageSize': 10 - len(news_items),
# # #                     'from': (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
# # #                 }
                
# # #                 response = requests.get(url, params=params, timeout=15)
# # #                 response.raise_for_status()
# # #                 data = response.json()
                
# # #                 for article in data.get('articles', [])[:10-len(news_items)]:
# # #                     title = article.get('title', '') or ''
# # #                     description = article.get('description', '') or ''
                    
# # #                     if title or description:
# # #                         text = f"{title} {description}"
# # #                         sentiment = self.analyzer.polarity_scores(text)
                        
# # #                         news_items.append({
# # #                             'text': text,
# # #                             'sentiment_compound': sentiment['compound'],
# # #                         })
                
# # #                 time.sleep(1)
            
# # #             return news_items[:10]
# # #         except Exception as e:
# # #             logger.error(f"News API error for {city}: {e}")
# # #             return []

# # #     def get_twitter_data(self, city: str) -> List[Dict]:
# # #         """Fetch exactly 10 tweets"""
# # #         try:
# # #             tweets = []
# # #             keyword = self.indian_cities[city]["keywords"][0]
            
# # #             url = "https://twitter-api45.p.rapidapi.com/search.php"
# # #             querystring = {
# # #                 "query": f"{keyword} india",
# # #                 "search_type": "Latest",
# # #                 "count": "10"
# # #             }
            
# # #             headers = {
# # #                 'x-rapidapi-key': self.twitter_api_key,
# # #                 'x-rapidapi-host': "twitter-api45.p.rapidapi.com"
# # #             }
            
# # #             response = requests.get(url, headers=headers, params=querystring, timeout=15)
# # #             response.raise_for_status()
# # #             data = response.json()
            
# # #             if isinstance(data, dict) and 'timeline' in data:
# # #                 for tweet in data['timeline'][:10]:
# # #                     text = tweet.get('text', '')
# # #                     if text:
# # #                         cleaned_text = re.sub(r'http\S+|@\w+|#(\w+)', '', text)
# # #                         sentiment = self.analyzer.polarity_scores(cleaned_text)
                        
# # #                         tweets.append({
# # #                             'text': cleaned_text,
# # #                             'sentiment_compound': sentiment['compound'],
# # #                         })
            
# # #             return tweets[:10]
# # #         except Exception as e:
# # #             logger.error(f"Twitter API error for {city}: {e}")
# # #             return []

# # #     def calculate_city_mood(self, sentiment_data: List[Dict]) -> Dict:
# # #         """Calculate mood metrics with color coding"""
# # #         if not sentiment_data:
# # #             return {
# # #                 'avg_sentiment': 0,
# # #                 'mood_label': 'No Data',
# # #                 'color_value': 50,
# # #                 'confidence': 0,
# # #                 'sample_size': 0
# # #             }
        
# # #         sentiments = [item['sentiment_compound'] for item in sentiment_data]
# # #         avg_sentiment = sum(sentiments) / len(sentiments)
        
# # #         # Enhanced mood classification
# # #         if avg_sentiment > 0.5:
# # #             mood_label, color_value = "Extremely Positive", 90
# # #         elif avg_sentiment > 0.3:
# # #             mood_label, color_value = "Very Positive", 80
# # #         elif avg_sentiment > 0.1:
# # #             mood_label, color_value = "Positive", 70
# # #         elif avg_sentiment > -0.1:
# # #             mood_label, color_value = "Neutral", 50
# # #         elif avg_sentiment > -0.3:
# # #             mood_label, color_value = "Negative", 30
# # #         elif avg_sentiment > -0.5:
# # #             mood_label, color_value = "Very Negative", 20
# # #         else:
# # #             mood_label, color_value = "Extremely Negative", 10
        
# # #         confidence = min(1.0, len(sentiments) / 20)
        
# # #         return {
# # #             'avg_sentiment': round(avg_sentiment, 3),
# # #             'mood_label': mood_label,
# # #             'color_value': color_value,
# # #             'confidence': round(confidence, 2),
# # #             'sample_size': len(sentiments)
# # #         }

# # #     def generate_genz_headline(self, city: str, weather: Dict, news: List[Dict], tweets: List[Dict]) -> str:
# # #         """Generate Gen-Z headline using Gemini"""
# # #         try:
# # #             weather_desc = f"{weather.get('condition', 'unknown')}, {weather.get('temperature_c', 0)}°C"
            
# # #             prompt = f"""
# # #             Create a catchy, Gen-Z style headline about {city} based on:
# # #             - Weather: {weather_desc}
# # #             - Recent sentiment trends
            
# # #             Make it short, use emojis, and make it viral!
# # #             Examples: "Mumbai vibing rn 🌊😎", "Delhi mood: chaotic but iconic 💅"
# # #             """
            
# # #             response = self.gemini_client.models.generate_content(
# # #                 model="gemini-2.0-flash",
# # #                 contents=prompt
# # #             )
            
# # #             return response.text.strip()
# # #         except Exception as e:
# # #             logger.error(f"Headline generation error for {city}: {e}")
# # #             return f"{city} is having a moment 🌆"

# # #     def collect_city_data(self, city: str) -> Dict:
# # #         """Collect data for a single city"""
# # #         try:
# # #             weather = self.get_weather_data(city)
# # #             news = self.get_news_data(city)
# # #             tweets = self.get_twitter_data(city)
            
# # #             # Combine sentiment data
# # #             sentiment_data = news + tweets
# # #             mood_metrics = self.calculate_city_mood(sentiment_data)
            
# # #             # Generate headline
# # #             headline = self.generate_genz_headline(city, weather, news, tweets)
            
# # #             return {
# # #                 'city': city,
# # #                 'coordinates': {
# # #                     'lat': self.indian_cities[city]['lat'],
# # #                     'lon': self.indian_cities[city]['lon']
# # #                 },
# # #                 'headline': headline,
# # #                 'mood_metrics': mood_metrics,
# # #                 'weather': weather,
# # #                 'news_count': len(news),
# # #                 'twitter_count': len(tweets),
# # #                 'total_samples': mood_metrics['sample_size'],
# # #                 'timestamp': datetime.now().isoformat(),
# # #                 'color_value': mood_metrics['color_value']
# # #             }
# # #         except Exception as e:
# # #             logger.error(f"Error collecting data for {city}: {e}")
# # #             return self._get_fallback_data(city)

# # #     def collect_all_cities_data(self) -> List[Dict]:
# # #         """Collect data for all cities in parallel"""
# # #         cities_data = []
        
# # #         with ThreadPoolExecutor(max_workers=3) as executor:
# # #             future_to_city = {
# # #                 executor.submit(self.collect_city_data, city): city 
# # #                 for city in self.indian_cities.keys()
# # #             }
            
# # #             for future in as_completed(future_to_city):
# # #                 city_data = future.result()
# # #                 cities_data.append(city_data)
        
# # #         return cities_data

# # #     def _get_fallback_data(self, city: str) -> Dict:
# # #         """Return fallback data when collection fails"""
# # #         return {
# # #             'city': city,
# # #             'coordinates': self.indian_cities[city],
# # #             'headline': f"{city} data coming soon! 🔄",
# # #             'mood_metrics': {
# # #                 'avg_sentiment': 0,
# # #                 'mood_label': 'No Data',
# # #                 'color_value': 50,
# # #                 'confidence': 0,
# # #                 'sample_size': 0
# # #             },
# # #             'weather': {},
# # #             'news_count': 0,
# # #             'twitter_count': 0,
# # #             'total_samples': 0,
# # #             'timestamp': datetime.now().isoformat(),
# # #             'color_value': 50
# # #         }





# # # services/data_collector.py
# # import requests
# # import json
# # import time
# # from datetime import datetime, timedelta
# # from typing import Dict, List, Tuple
# # import re
# # import logging
# # from collections import Counter
# # from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# # from concurrent.futures import ThreadPoolExecutor, as_completed

# # logger = logging.getLogger(__name__)

# # class AuraDataCollector:
# #     def __init__(self, openrouter_api_key: str):
# #         self.news_api_key = "47e7597b3e51433a81fcc3d908b1a792"
# #         self.weather_api_key = "5a5c9571ba254b1c90b152042243103"
# #         self.twitter_api_key = "984d78e1femsh2af122397b07360p15059bjsn900a6a3b90fa"
# #         self.openrouter_api_key = "open_router_api"

        
# #         self.analyzer = SentimentIntensityAnalyzer()
        
# #         self.indian_cities = {
# #             "Mumbai": {"lat": 19.0760, "lon": 72.8777, "keywords": ["mumbai", "bombay"]},
# #             "Delhi": {"lat": 28.7041, "lon": 77.1025, "keywords": ["delhi", "new delhi"]},
# #             "Bangalore": {"lat": 12.9716, "lon": 77.5946, "keywords": ["bangalore", "bengaluru"]},
# #             "Chennai": {"lat": 13.0827, "lon": 80.2707, "keywords": ["chennai", "madras"]},
# #             "Kolkata": {"lat": 22.5726, "lon": 88.3639, "keywords": ["kolkata", "calcutta"]},
# #             "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "keywords": ["hyderabad"]},
# #             "Pune": {"lat": 18.5204, "lon": 73.8567, "keywords": ["pune"]},
# #             "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "keywords": ["ahmedabad"]},
# #             "Jaipur": {"lat": 26.9124, "lon": 75.7873, "keywords": ["jaipur"]},
# #             "Lucknow": {"lat": 26.8467, "lon": 80.9462, "keywords": ["lucknow"]}
# #         }

# #         # Gen-Z slang dictionary for better content understanding
# #         self.genz_slang = {
# #             'amazing': 'slay', 'awesome': 'fire', 'great': 'vibing', 'good': 'valid',
# #             'bad': 'sus', 'terrible': 'cursed', 'problem': 'issue', 'issue': 'drama',
# #             'excited': 'hyped', 'happy': 'lit', 'sad': 'down bad', 'angry': 'pressed',
# #             'cool': 'drip', 'fashion': 'fit', 'money': 'bag', 'rich': 'stacked',
# #             'party': 'vibe', 'fun': 'vibes', 'best': 'goated', 'worst': 'mid',
# #             'friend': 'bestie', 'car': 'whip', 'house': 'crib', 'phone': 'device',
# #             'internet': 'wifi', 'food': 'grub', 'coffee': 'brew', 'tea': 'spill',
# #             'news': 'tea', 'gossip': 'spill', 'drama': 'mess', 'problem': 'situation',
# #             'beautiful': 'stan', 'perfect': 'ate', 'win': 'W', 'lose': 'L',
# #             'easy': 'ez', 'difficult': 'struggle', 'tired': 'burnt out', 'relax': 'chill'
# #         }

# #     def get_weather_data(self, city: str) -> Dict:
# #         """Fetch current weather data for a city"""
# #         try:
# #             city_info = self.indian_cities[city]
# #             url = "http://api.weatherapi.com/v1/current.json"
# #             params = {
# #                 'key': self.weather_api_key,
# #                 'q': f"{city_info['lat']},{city_info['lon']}",
# #                 'aqi': 'yes'
# #             }
            
# #             response = requests.get(url, params=params, timeout=10)
# #             response.raise_for_status()
# #             data = response.json()
            
# #             return {
# #                 'temperature_c': data['current']['temp_c'],
# #                 'condition': data['current']['condition']['text'],
# #                 'humidity': data['current']['humidity'],
# #                 'wind_kph': data['current']['wind_kph'],
# #                 'feels_like_c': data['current']['feelslike_c'],
# #                 'air_quality_pm25': data['current'].get('air_quality', {}).get('pm2_5', 0),
# #             }
# #         except Exception as e:
# #             logger.error(f"Weather API error for {city}: {e}")
# #             return {}

# #     def get_news_data(self, city: str) -> List[Dict]:
# #         """Fetch exactly 10 news articles"""
# #         try:
# #             news_items = []
# #             for keyword in self.indian_cities[city]["keywords"]:
# #                 if len(news_items) >= 10:
# #                     break
                    
# #                 url = "https://newsapi.org/v2/everything"
# #                 params = {
# #                     'apiKey': self.news_api_key,
# #                     'q': f"{keyword} AND india",
# #                     'language': 'en',
# #                     'sortBy': 'publishedAt',
# #                     'pageSize': 10 - len(news_items),
# #                     'from': (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
# #                 }
                
# #                 response = requests.get(url, params=params, timeout=15)
# #                 response.raise_for_status()
# #                 data = response.json()
                
# #                 for article in data.get('articles', [])[:10-len(news_items)]:
# #                     title = article.get('title', '') or ''
# #                     description = article.get('description', '') or ''
                    
# #                     if title or description:
# #                         text = f"{title} {description}"
# #                         sentiment = self.analyzer.polarity_scores(text)
                        
# #                         news_items.append({
# #                             'text': text,
# #                             'sentiment_compound': sentiment['compound'],
# #                             'published_at': article.get('publishedAt', ''),
# #                             'source': article.get('source', {}).get('name', '')
# #                         })
                
# #                 time.sleep(1)
            
# #             return news_items[:10]
# #         except Exception as e:
# #             logger.error(f"News API error for {city}: {e}")
# #             return []

# #     def get_twitter_data(self, city: str) -> List[Dict]:
# #         """Fetch exactly 10 tweets"""
# #         try:
# #             tweets = []
# #             keyword = self.indian_cities[city]["keywords"][0]
            
# #             url = "https://twitter-api45.p.rapidapi.com/search.php"
# #             querystring = {
# #                 "query": f"{keyword} india",
# #                 "search_type": "Latest",
# #                 "count": "10"
# #             }
            
# #             headers = {
# #                 'x-rapidapi-key': self.twitter_api_key,
# #                 'x-rapidapi-host': "twitter-api45.p.rapidapi.com"
# #             }
            
# #             response = requests.get(url, headers=headers, params=querystring, timeout=15)
# #             response.raise_for_status()
# #             data = response.json()
            
# #             if isinstance(data, dict) and 'timeline' in data:
# #                 for tweet in data['timeline'][:10]:
# #                     text = tweet.get('text', '')
# #                     if text:
# #                         cleaned_text = re.sub(r'http\S+|@\w+|#(\w+)', '', text)
# #                         sentiment = self.analyzer.polarity_scores(cleaned_text)
                        
# #                         tweets.append({
# #                             'text': cleaned_text,
# #                             'sentiment_compound': sentiment['compound'],
# #                             'created_at': tweet.get('created_at', ''),
# #                             'user_followers': tweet.get('user', {}).get('followers_count', 0)
# #                         })
            
# #             return tweets[:10]
# #         except Exception as e:
# #             logger.error(f"Twitter API error for {city}: {e}")
# #             return []

# #     def calculate_city_mood(self, sentiment_data: List[Dict]) -> Dict:
# #         """Calculate mood metrics with color coding"""
# #         if not sentiment_data:
# #             return {
# #                 'avg_sentiment': 0,
# #                 'mood_label': 'No Data',
# #                 'color_value': 50,
# #                 'confidence': 0,
# #                 'sample_size': 0
# #             }
        
# #         sentiments = [item['sentiment_compound'] for item in sentiment_data]
# #         avg_sentiment = sum(sentiments) / len(sentiments)
        
# #         # Enhanced mood classification
# #         if avg_sentiment > 0.5:
# #             mood_label, color_value = "Extremely Positive", 90
# #         elif avg_sentiment > 0.3:
# #             mood_label, color_value = "Very Positive", 80
# #         elif avg_sentiment > 0.1:
# #             mood_label, color_value = "Positive", 70
# #         elif avg_sentiment > -0.1:
# #             mood_label, color_value = "Neutral", 50
# #         elif avg_sentiment > -0.3:
# #             mood_label, color_value = "Negative", 30
# #         elif avg_sentiment > -0.5:
# #             mood_label, color_value = "Very Negative", 20
# #         else:
# #             mood_label, color_value = "Extremely Negative", 10
        
# #         confidence = min(1.0, len(sentiments) / 20)
        
# #         return {
# #             'avg_sentiment': round(avg_sentiment, 3),
# #             'mood_label': mood_label,
# #             'color_value': color_value,
# #             'confidence': round(confidence, 2),
# #             'sample_size': len(sentiments)
# #         }

# #     def translate_to_genz(self, text: str) -> str:
# #         """Translate regular text to Gen-Z slang"""
# #         words = text.lower().split()
# #         translated_words = []
        
# #         for word in words:
# #             # Remove punctuation for matching
# #             clean_word = re.sub(r'[^\w]', '', word)
# #             if clean_word in self.genz_slang:
# #                 translated_words.append(self.genz_slang[clean_word])
# #             else:
# #                 translated_words.append(word)
        
# #         return ' '.join(translated_words)

# #     def extract_key_topics(self, texts: List[str]) -> List[Tuple[str, int]]:
# #         """Extract key topics from news and tweets with Gen-Z flavor"""
# #         all_words = []
# #         stop_words = {'the', 'and', 'is', 'in', 'to', 'of', 'for', 'on', 'with', 'at', 'by', 'an', 'a', 'this', 'that', 'are', 'as', 'be', 'was', 'were', 'has', 'have', 'had', 'but', 'or', 'not'}
        
# #         for text in texts:
# #             if not text:
# #                 continue
                
# #             # Clean and tokenize text
# #             words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
# #             filtered_words = [word for word in words if word not in stop_words and not word.isdigit()]
# #             all_words.extend(filtered_words)
        
# #         # Count word frequencies
# #         word_counts = Counter(all_words)
# #         return word_counts.most_common(8)  # Top 8 topics

# #     def analyze_content_themes(self, news: List[Dict], tweets: List[Dict]) -> Dict:
# #         """Analyze content to identify main themes and sentiment"""
# #         all_texts = [item.get('text', '') for item in news + tweets if item.get('text')]
        
# #         if not all_texts:
# #             return {
# #                 'main_topics': [],
# #                 'overall_sentiment': 'neutral',
# #                 'trending_hashtags': [],
# #                 'key_events': []
# #             }
        
# #         # Extract key topics
# #         key_topics = self.extract_key_topics(all_texts)
        
# #         # Analyze sentiment distribution
# #         sentiments = [item.get('sentiment_compound', 0) for item in news + tweets if 'sentiment_compound' in item]
# #         avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
# #         sentiment_label = "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral"
        
# #         # Extract potential events (news with high engagement)
# #         key_events = []
# #         for item in news[:3]:  # Top 3 news items
# #             if item.get('text'):
# #                 key_events.append(item['text'][:100] + "...")
        
# #         return {
# #             'main_topics': [topic for topic, count in key_topics],
# #             'overall_sentiment': sentiment_label,
# #             'key_events': key_events[:2],  # Top 2 events
# #             'content_sample_count': len(all_texts)
# #         }

# #     def generate_genz_headline(self, city: str, weather: Dict, news: List[Dict], tweets: List[Dict]) -> str:
# #         """Generate proper Gen-Z style headline based on actual content"""
# #         try:
# #             # Analyze content to understand what's happening
# #             content_analysis = self.analyze_content_themes(news, tweets)
            
# #             # Prepare context from actual content
# #             weather_desc = f"{weather.get('condition', 'unknown')}, {weather.get('temperature_c', 0)}°C"
# #             main_topics = ", ".join(content_analysis['main_topics'][:3]) if content_analysis['main_topics'] else "vibes"
# #             sentiment = content_analysis['overall_sentiment']
            
# #             # Get some actual content snippets for context
# #             content_snippets = []
# #             for item in (news + tweets)[:4]:  # Get 4 snippets from both news and tweets
# #                 if item.get('text'):
# #                     snippet = item['text'][:60] + "..." if len(item['text']) > 60 else item['text']
# #                     content_snippets.append(snippet)
            
# #             prompt = f"""
# #             Create a VIRAL Gen-Z style headline about what's happening RIGHT NOW in {city} based on ACTUAL NEWS and TWEETS.

# #             CONTEXT:
# #             - City: {city}
# #             - Weather: {weather_desc}
# #             - Trending Topics: {main_topics}
# #             - Overall Vibe: {sentiment.upper()}
            
# #             ACTUAL CONTENT SNIPPETS (use these for inspiration):
# #             {chr(10).join(f'• {snippet}' for snippet in content_snippets[:3])}

# #             REQUIREMENTS:
# #             - MUST use CURRENT Gen-Z slang and internet culture references
# #             - Include 2-3 relevant emojis MAX
# #             - Keep it UNDER 10 words
# #             - Make it SOUND LIKE A VIRAL TWEET or IG STORY
# #             - Reference ACTUAL CONTENT from above snippets
# #             - Match the {sentiment.upper()} vibe
            
# #             GEN-Z SLANG EXAMPLES TO USE:
# #             slay, fire, vibing, valid, sus, cursed, drama, hyped, lit, down bad, 
# #             pressed, drip, fit, bag, stacked, vibe, vibes, goated, mid, bestie, 
# #             whip, crib, device, wifi, grub, brew, spill, tea, mess, situation, 
# #             stan, ate, W, L, ez, struggle, burnt out, chill, no cap, fr, lowkey, 
# #             highkey, bet, periodt, sheesh, oof, yikes, snatched, extra, sent, 
# #             ghosted, main character energy, it's giving, rizz, skibidi, fanum tax

# #             VIRAL HEADLINE EXAMPLES:
# #             "Mumbai rains got everyone in their feels 🌧️🚗 no cap"
# #             "Delhi protest drama = main character energy fr ✊📢"
# #             "Bangalore tech layoffs got us down bad 💼😬 sheesh"
# #             "Chennai biryani festival absolutely ATE today 🍛🔥"
# #             "Kolkata Durga Puja vibes are IMMACULATE rn 🎉🙌"
# #             "Pune startup W got everyone hyped 💰🚀 periodt"
# #             "Hyderabad traffic is giving cursed energy rn 🚗💀"
# #             "Jaipur tourism absolutely SLAYING today 🏰✨"
# #             "Ahmedabad food scene is valid no cap 🍲🔥"
# #             "Lucknow culture vibes are elite fr 🎭💫"

# #             Create the MOST VIRAL headline possible based on the actual content above:
# #             """

# #             response = requests.post(
# #                 url="https://openrouter.ai/api/v1/chat/completions",
# #                 headers={
# #                     "Authorization": f"Bearer {self.openrouter_api_key}",
# #                     "Content-Type": "application/json",
# #                     "HTTP-Referer": "https://aura-ai.com",
# #                     "X-Title": "Aura.AI Emotional Sentiment Platform",
# #                 },
# #                 data=json.dumps({
# #                     "model": "google/gemini-2.5-flash-lite",
# #                     "messages": [
# #                         {
# #                             "role": "user",
# #                             "content": prompt
# #                         }
# #                     ],
# #                     "max_tokens": 70,
# #                     "temperature": 0.9
# #                 }),
# #                 timeout=20
# #             )
            
# #             response.raise_for_status()
# #             result = response.json()
            
# #             headline = result['choices'][0]['message']['content'].strip()
# #             headline = headline.replace('"', '').strip()
            
# #             # Validate that headline is Gen-Z style and content-based
# #             if self.is_genz_headline(headline) and self.is_headline_content_based(headline, content_analysis):
# #                 return headline
# #             else:
# #                 return self.create_genz_fallback_headline(city, content_analysis, weather)
            
# #         except Exception as e:
# #             logger.error(f"OpenRouter headline generation error for {city}: {e}")
# #             return self.create_genz_fallback_headline(city, self.analyze_content_themes(news, tweets), weather)

# #     def is_genz_headline(self, headline: str) -> bool:
# #         """Check if headline uses Gen-Z slang"""
# #         headline_lower = headline.lower()
# #         genz_indicators = [
# #             'slay', 'fire', 'vibing', 'valid', 'sus', 'cursed', 'drama', 'hyped', 
# #             'lit', 'down bad', 'pressed', 'drip', 'fit', 'bag', 'stacked', 'vibe', 
# #             'vibes', 'goated', 'mid', 'bestie', 'whip', 'crib', 'device', 'wifi', 
# #             'grub', 'brew', 'spill', 'tea', 'mess', 'situation', 'stan', 'ate', 
# #             ' W ', ' L ', ' ez ', 'struggle', 'burnt out', 'chill', 'no cap', ' fr ', 
# #             'lowkey', 'highkey', 'bet', 'periodt', 'sheesh', 'oof', 'yikes', 
# #             'snatched', 'extra', 'sent', 'ghosted', 'main character', 'it\'s giving', 
# #             'rizz', 'skibidi', 'fanum tax', 'rn ', ' rn', ' rn,'
# #         ]
        
# #         return any(indicator in headline_lower for indicator in genz_indicators)

# #     def is_headline_content_based(self, headline: str, content_analysis: Dict) -> bool:
# #         """Check if headline actually references the content"""
# #         headline_lower = headline.lower()
# #         content_words = set()
        
# #         for topic in content_analysis['main_topics']:
# #             content_words.update(topic.lower().split())
        
# #         # Check if headline contains any content-related words
# #         for word in content_words:
# #             if word in headline_lower and len(word) > 3:
# #                 return True
        
# #         return False

# #     def create_genz_fallback_headline(self, city: str, content_analysis: Dict, weather: Dict) -> str:
# #         """Create Gen-Z style fallback headline based on content analysis"""
# #         topics = content_analysis['main_topics']
# #         sentiment = content_analysis['overall_sentiment']
# #         weather_cond = weather.get('condition', '').lower()
        
# #         # Gen-Z templates for different scenarios
# #         genz_templates = {
# #             'positive': [
# #                 f"{city} absolutely SLAYING today no cap 🔥✨",
# #                 f"{city} vibes are IMMACULATE rn fr 🌟💫",
# #                 f"{city} giving main character energy today 🎭⚡",
# #                 f"{city} W today periodt 💯👑",
# #                 f"{city} ate and left no crumbs fr 🍽️🔥"
# #             ],
# #             'negative': [
# #                 f"{city} going through it rn sheesh 😬🌧️",
# #                 f"{city} vibes are sus today ngl 💀⚠️",
# #                 f"{city} taking the L today oof 😓📉",
# #                 f"{city} drama got everyone pressed fr 🎭😤",
# #                 f"{city} situation is cursed rn yikes 🔮💀"
# #             ],
# #             'neutral': [
# #                 f"{city} just chilling lowkey 😌☕",
# #                 f"{city} vibes are mid but valid 🤷‍♂️⚖️",
# #                 f"{city} keeping it real today fr 💭📱",
# #                 f"{city} energy is giving neutral but it's okay 🎭😐",
# #                 f"{city} just existing and that's valid 🌆✨"
# #             ]
# #         }
        
# #         # If we have specific topics, incorporate them
# #         if topics:
# #             main_topic = topics[0]
# #             topic_templates = {
# #                 'positive': [
# #                     f"{city} {main_topic} scene is FIRE rn 🔥👏",
# #                     f"{main_topic.capitalize()} in {city} absolutely ATE 🍽️✨",
# #                     f"{city} {main_topic} vibes are ELITE today 🎯🌟",
# #                     f"{main_topic.capitalize()} W for {city} today 💯🏆"
# #                 ],
# #                 'negative': [
# #                     f"{city} {main_topic} situation is SUS rn 💀⚠️",
# #                     f"{main_topic.capitalize()} L for {city} today 😓📉",
# #                     f"{city} {main_topic} drama got everyone PRESSED 🎭😤",
# #                     f"{main_topic.capitalize()} in {city} is CURSED sheesh 🔮💀"
# #                 ],
# #                 'neutral': [
# #                     f"{city} {main_topic} scene is mid but valid 🤷‍♂️⚖️",
# #                     f"{main_topic.capitalize()} in {city} just existing fr 💭📱",
# #                     f"{city} {main_topic} vibes are giving neutral 🎭😐",
# #                     f"{main_topic.capitalize()} in {city} is lowkey chill 😌☕"
# #                 ]
# #             }
            
# #             return topic_templates[sentiment][hash(city + main_topic) % len(topic_templates[sentiment])]
        
# #         # Weather-based fallback
# #         elif weather_cond:
# #             weather_templates = {
# #                 'sunny': f"{city} weather is giving good vibes fr ☀️😎",
# #                 'rain': f"{city} rains got everyone in their feels 🌧️🚗",
# #                 'cloud': f"{city} cloud cover is lowkey moody ☁️😌",
# #                 'clear': f"{city} clear skies = main character energy 🌞✨",
# #                 'storm': f"{city} storm drama is wild rn ⛈️😳",
# #                 'fog': f"{city} fog giving mysterious vibes 🌫️🔮"
# #             }
            
# #             for condition, template in weather_templates.items():
# #                 if condition in weather_cond:
# #                     return template
            
# #             return f"{city} weather vibes are {sentiment} rn 🌤️✨"
        
# #         # Generic sentiment-based fallback
# #         return genz_templates[sentiment][hash(city) % len(genz_templates[sentiment])]

# #     def collect_city_data(self, city: str) -> Dict:
# #         """Collect data for a single city"""
# #         try:
# #             logger.info(f"Collecting data for {city}...")
            
# #             weather = self.get_weather_data(city)
# #             news = self.get_news_data(city)
# #             tweets = self.get_twitter_data(city)
            
# #             # Combine sentiment data
# #             sentiment_data = [item for item in news + tweets if 'sentiment_compound' in item]
# #             mood_metrics = self.calculate_city_mood(sentiment_data)
            
# #             # Generate Gen-Z headline
# #             headline = self.generate_genz_headline(city, weather, news, tweets)
            
# #             result = {
# #                 'city': city,
# #                 'coordinates': {
# #                     'lat': self.indian_cities[city]['lat'],
# #                     'lon': self.indian_cities[city]['lon']
# #                 },
# #                 'headline': headline,
# #                 'mood_metrics': mood_metrics,
# #                 'weather': weather,
# #                 'news_count': len(news),
# #                 'twitter_count': len(tweets),
# #                 'total_samples': mood_metrics['sample_size'],
# #                 'timestamp': datetime.now().isoformat(),
# #                 'color_value': mood_metrics['color_value']
# #             }
            
# #             logger.info(f"✅ {city} data collected successfully")
# #             return result
            
# #         except Exception as e:
# #             logger.error(f"Error collecting data for {city}: {e}")
# #             return self._get_fallback_data(city)

# #     def collect_all_cities_data(self) -> List[Dict]:
# #         """Collect data for all cities in parallel"""
# #         logger.info("Starting data collection for all cities...")
# #         cities_data = []
        
# #         with ThreadPoolExecutor(max_workers=3) as executor:
# #             future_to_city = {
# #                 executor.submit(self.collect_city_data, city): city 
# #                 for city in self.indian_cities.keys()
# #             }
            
# #             for future in as_completed(future_to_city):
# #                 city_data = future.result()
# #                 cities_data.append(city_data)
# #                 logger.info(f"Completed: {city_data['city']}")
        
# #         logger.info("All cities data collection completed")
# #         return cities_data

# #     def _get_fallback_data(self, city: str) -> Dict:
# #         """Return fallback data when collection fails"""
# #         return {
# #             'city': city,
# #             'coordinates': self.indian_cities[city],
# #             'headline': f"{city} vibes loading... 🔄✨",
# #             'mood_metrics': {
# #                 'avg_sentiment': 0,
# #                 'mood_label': 'No Data',
# #                 'color_value': 50,
# #                 'confidence': 0,
# #                 'sample_size': 0
# #             },
# #             'weather': {},
# #             'news_count': 0,
# #             'twitter_count': 0,
# #             'total_samples': 0,
# #             'timestamp': datetime.now().isoformat(),
# #             'color_value': 50
# #         }







# # services/data_collector.py
# import requests
# import json
# import time
# import asyncio
# from datetime import datetime, timedelta
# from typing import Dict, List, Tuple
# import re
# import logging
# from collections import Counter
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import random

# logger = logging.getLogger(__name__)

# class AuraDataCollector:
#     def __init__(self, openrouter_api_key: str):
#         self.news_api_key = "47e7597b3e51433a81fcc3d908b1a792"
#         self.weather_api_key = "5a5c9571ba254b1c90b152042243103"
#         self.twitter_api_key = "984d78e1femsh2af122397b07360p15059bjsn900a6a3b90fa"
#         self.openrouter_api_key = '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'
        
#         self.analyzer = SentimentIntensityAnalyzer()
        
#         # Limited to 10 major Indian cities for better focus
#         self.indian_cities = {
#             "Mumbai": {"lat": 19.0760, "lon": 72.8777, "keywords": ["mumbai", "bombay"]},
#             "Delhi": {"lat": 28.7041, "lon": 77.1025, "keywords": ["delhi", "new delhi"]},
#             "Bangalore": {"lat": 12.9716, "lon": 77.5946, "keywords": ["bangalore", "bengaluru"]},
#             "Chennai": {"lat": 13.0827, "lon": 80.2707, "keywords": ["chennai", "madras"]},
#             "Kolkata": {"lat": 22.5726, "lon": 88.3639, "keywords": ["kolkata", "calcutta"]},
#             "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "keywords": ["hyderabad"]},
#             "Pune": {"lat": 18.5204, "lon": 73.8567, "keywords": ["pune"]},
#             "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "keywords": ["ahmedabad"]},
#             "Jaipur": {"lat": 26.9124, "lon": 75.7873, "keywords": ["jaipur"]},
#             "Lucknow": {"lat": 26.8467, "lon": 80.9462, "keywords": ["lucknow"]}
#         }

#     def get_weather_data(self, city: str) -> Dict:
#         """Fetch current weather data for a city"""
#         try:
#             city_info = self.indian_cities[city]
#             url = "http://api.weatherapi.com/v1/current.json"
#             params = {
#                 'key': self.weather_api_key,
#                 'q': f"{city_info['lat']},{city_info['lon']}",
#                 'aqi': 'yes'
#             }
            
#             response = requests.get(url, params=params, timeout=10)
#             response.raise_for_status()
#             data = response.json()
            
#             return {
#                 'temperature_c': data['current']['temp_c'],
#                 'condition': data['current']['condition']['text'],
#                 'humidity': data['current']['humidity'],
#                 'wind_kph': data['current']['wind_kph'],
#                 'feels_like_c': data['current']['feelslike_c'],
#                 'air_quality_pm25': data['current'].get('air_quality', {}).get('pm2_5', 0),
#                 'air_quality_pm10': data['current'].get('air_quality', {}).get('pm10', 0),
#                 'uv_index': data['current']['uv'],
#                 'timestamp': datetime.now().isoformat()
#             }
#         except Exception as e:
#             logger.error(f"Weather API error for {city}: {e}")
#             return {}

#     # def get_news_data(self, city: str) -> List[Dict]:
#     #     """Fetch exactly 10 news articles with enhanced sentiment analysis"""
#     #     try:
#     #         news_items = []
#     #         city_keywords = self.indian_cities[city]["keywords"]
            
#     #         for keyword in city_keywords:
#     #             if len(news_items) >= 10:
#     #                 break
                    
#     #             url = "https://newsapi.org/v2/everything"
#     #             params = {
#     #                 'apiKey': self.news_api_key,
#     #                 'q': f"{keyword} AND india",
#     #                 'language': 'en',
#     #                 'sortBy': 'publishedAt',
#     #                 'pageSize': 10 - len(news_items),
#     #                 'from': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')
#     #             }
                
#     #             response = requests.get(url, params=params, timeout=15)
#     #             response.raise_for_status()
#     #             data = response.json()
                
#     #             for article in data.get('articles', [])[:10-len(news_items)]:
#     #                 title = article.get('title', '') or ''
#     #                 description = article.get('description', '') or ''
                    
#     #                 if title or description:
#     #                     text = f"{title} {description}"
                        
#     #                     # Enhanced sentiment analysis
#     #                     sentiment = self.analyzer.polarity_scores(text)
                        
#     #                     # Add noise to create more varied sentiment distribution
#     #                     noise_factor = random.uniform(-0.1, 0.1)
#     #                     adjusted_compound = max(-1, min(1, sentiment['compound'] + noise_factor))
                        
#     #                     news_items.append({
#     #                         'text': text,
#     #                         'sentiment_compound': adjusted_compound,
#     #                         'sentiment_positive': sentiment['pos'],
#     #                         'sentiment_negative': sentiment['neg'],
#     #                         'sentiment_neutral': sentiment['neu'],
#     #                         'published_at': article.get('publishedAt', ''),
#     #                         'source': article.get('source', {}).get('name', ''),
#     #                         'url': article.get('url', ''),
#     #                         'type': 'news'
#     #                     })
                
#     #             time.sleep(1)  # Rate limiting
            
#     #         logger.info(f"✅ News: {len(news_items)} articles for {city}")
#     #         return news_items[:10]
            
#     #     except Exception as e:
#     #         logger.error(f"News API error for {city}: {e}")
#     #         return []
#     def get_news_data(self, city: str) -> List[Dict]:
#         """Fetch exactly 10 news articles with quota-aware fetching"""
#         try:
#             news_items = []
#             city_keywords = self.indian_cities[city]["keywords"]
            
#             # With only 100 requests/month, we need to be very conservative
#             # Try only the primary keyword for each city
#             primary_keyword = city_keywords[0]  # Use only first keyword
            
#             url = "https://newsapi.org/v2/everything"
#             params = {
#                 'apiKey': self.news_api_key,
#                 'q': f'"{primary_keyword}" AND india',  # More specific query
#                 'language': 'en',
#                 'sortBy': 'publishedAt',
#                 'pageSize': 10,
#                 'from': (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d')  # Wider time window
#             }
            
#             response = requests.get(url, params=params, timeout=15)
            
#             # Check for rate limiting or quota exceeded
#             if response.status_code == 429:
#                 logger.warning(f"NewsAPI rate limited for {city} - using mock data")
#                 return self.generate_mock_news(city, 10)
#             elif response.status_code == 426:
#                 logger.warning(f"NewsAPI quota exceeded for {city} - using mock data") 
#                 return self.generate_mock_news(city, 10)
#             elif response.status_code != 200:
#                 logger.warning(f"NewsAPI error {response.status_code} for {city} - using mock data")
#                 return self.generate_mock_news(city, 10)
            
#             data = response.json()
            
#             if data.get('status') == 'error':
#                 logger.error(f"NewsAPI error for {city}: {data.get('message', 'Unknown error')}")
#                 return self.generate_mock_news(city, 10)
            
#             articles = data.get('articles', [])
#             logger.info(f"NewsAPI returned {len(articles)} articles for {city}")
            
#             for article in articles:
#                 title = article.get('title', '') or ''
#                 description = article.get('description', '') or ''
                
#                 # Skip removed/null articles
#                 if title in ['[Removed]', None] or description in ['[Removed]', None]:
#                     continue
                    
#                 if title and description:  # Require both title and description
#                     text = f"{title} {description}"
#                     sentiment = self.analyzer.polarity_scores(text)
                    
#                     # Add variation to sentiment
#                     noise_factor = random.uniform(-0.15, 0.15)
#                     adjusted_compound = max(-1, min(1, sentiment['compound'] + noise_factor))
                    
#                     news_items.append({
#                         'text': text,
#                         'sentiment_compound': adjusted_compound,
#                         'sentiment_positive': sentiment['pos'],
#                         'sentiment_negative': sentiment['neg'], 
#                         'sentiment_neutral': sentiment['neu'],
#                         'published_at': article.get('publishedAt', ''),
#                         'source': article.get('source', {}).get('name', ''),
#                         'url': article.get('url', ''),
#                         'type': 'news'
#                     })
            
#             # If we got some real news but not enough, fill with mock
#             if len(news_items) > 0 and len(news_items) < 5:
#                 mock_count = 5 - len(news_items)
#                 news_items.extend(self.generate_mock_news(city, mock_count))
#             elif len(news_items) == 0:
#                 # No real news, use all mock
#                 news_items = self.generate_mock_news(city, 10)
            
#             # Mandatory 1 second delay due to rate limit
#             time.sleep(1.1)
            
#             logger.info(f"✅ News: {len(news_items)} articles for {city} ({len([n for n in news_items if 'mock' not in n.get('source', '').lower()])} real)")
#             return news_items[:10]
            
#         except Exception as e:
#             logger.error(f"News API error for {city}: {e}")
#             return self.generate_mock_news(city, 10)

#     def generate_mock_news(self, city: str, count: int) -> List[Dict]:
#         """Generate realistic mock news for demo purposes"""
#         mock_templates = [
#             f"{city} Municipal Corporation announces new infrastructure development projects",
#             f"Weather update: {city} experiences seasonal changes affecting daily life", 
#             f"{city} Metro Rail project reaches new milestone in construction",
#             f"Festival celebrations in {city} draw crowds, boost local economy",
#             f"{city} startup ecosystem shows growth, new companies establish presence",
#             f"Traffic management initiatives launched in {city} to ease congestion",
#             f"{city} schools implement new digital learning programs",
#             f"Healthcare facilities in {city} receive upgrades and new equipment",
#             f"{city} police launch community safety initiatives",
#             f"Environmental conservation efforts gain momentum in {city}",
#             f"{city} cultural events showcase local art and traditions",
#             f"Public transportation in {city} sees increased usage and improvements"
#         ]
        
#         mock_news = []
#         for i in range(count):
#             template = random.choice(mock_templates)
            
#             # Create varied sentiment
#             base_sentiment = random.uniform(-0.3, 0.5)  # Slightly positive bias for news
#             sentiment = self.analyzer.polarity_scores(template)
            
#             mock_news.append({
#                 'text': template,
#                 'sentiment_compound': base_sentiment,
#                 'sentiment_positive': sentiment['pos'],
#                 'sentiment_negative': sentiment['neg'],
#                 'sentiment_neutral': sentiment['neu'],
#                 'published_at': (datetime.now() - timedelta(hours=random.randint(1, 12))).isoformat(),
#                 'source': f'{city} Mock News',
#                 'url': f'https://example.com/news/{city.lower()}-{i+1}',
#                 'type': 'news'
#             })
        
#         return mock_news
#     def get_twitter_data(self, city: str) -> List[Dict]:
#         """Fetch exactly 10 tweets with enhanced sentiment analysis"""
#         try:
#             tweets = []
#             keyword = self.indian_cities[city]["keywords"][0]
            
#             url = "https://twitter-api45.p.rapidapi.com/search.php"
#             querystring = {
#                 "query": f"{keyword} india mood life weather traffic",
#                 "search_type": "Latest"
#             }
            
#             headers = {
#                 'x-rapidapi-key': self.twitter_api_key,
#                 'x-rapidapi-host': "twitter-api45.p.rapidapi.com"
#             }
            
#             response = requests.get(url, headers=headers, params=querystring, timeout=15)
#             response.raise_for_status()
#             data = response.json()
            
#             if isinstance(data, dict) and 'timeline' in data:
#                 for tweet in data['timeline'][:10]:
#                     text = tweet.get('text', '')
#                     if text:
#                         cleaned_text = self.clean_tweet_text(text)
                        
#                         if len(cleaned_text) < 10:  # Skip very short tweets
#                             continue
                            
#                         # Enhanced sentiment analysis
#                         sentiment = self.analyzer.polarity_scores(cleaned_text)
                        
#                         # Add variation to sentiment scores
#                         noise_factor = random.uniform(-0.15, 0.15)
#                         adjusted_compound = max(-1, min(1, sentiment['compound'] + noise_factor))
                        
#                         tweets.append({
#                             'text': cleaned_text,
#                             'sentiment_compound': adjusted_compound,
#                             'sentiment_positive': sentiment['pos'],
#                             'sentiment_negative': sentiment['neg'],
#                             'sentiment_neutral': sentiment['neu'],
#                             'created_at': tweet.get('created_at', ''),
#                             'user_followers': tweet.get('user', {}).get('followers_count', 0) if tweet.get('user') else 0,
#                             'retweet_count': tweet.get('retweet_count', 0),
#                             'like_count': tweet.get('favorite_count', 0),
#                             'type': 'twitter'
#                         })
                        
#                         if len(tweets) >= 10:
#                             break
            
#             # If we don't have enough tweets, generate some mock data for demo
#             while len(tweets) < 5:  # Ensure at least 5 tweets
#                 mock_tweet = self.generate_mock_tweet(city)
#                 tweets.append(mock_tweet)
            
#             logger.info(f"✅ Twitter: {len(tweets)} tweets for {city}")
#             return tweets[:10]
            
#         except Exception as e:
#             logger.error(f"Twitter API error for {city}: {e}")
#             # Return mock data for demo purposes
#             return [self.generate_mock_tweet(city) for _ in range(5)]

#     def clean_tweet_text(self, text: str) -> str:
#         """Clean tweet text for better sentiment analysis"""
#         if not text:
#             return ""
        
#         # Remove URLs
#         text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
#         # Remove user mentions and hashtags (keep the text after #)
#         text = re.sub(r'@\w+', '', text)
#         text = re.sub(r'#(\w+)', r'\1', text)
        
#         # Remove extra whitespace and special characters
#         text = re.sub(r'\n+', ' ', text)
#         text = ' '.join(text.split())
        
#         return text.strip()

#     def generate_mock_tweet(self, city: str) -> Dict:
#         """Generate mock tweet data for demo purposes"""
#         mock_tweets = [
#             f"Love the vibes in {city} today! Perfect weather for exploring 🌟",
#             f"Traffic in {city} is crazy but the city energy is amazing",
#             f"Best food scene in {city} right now, so many new places opening",
#             f"Weekend plans in {city} looking good, weather is perfect",
#             f"{city} monsoon hits different, love the rain vibes",
#             f"Work from {city} cafe today, loving the atmosphere",
#             f"Night life in {city} is incredible, such good energy",
#             f"Public transport in {city} needs improvement but city spirit is strong",
#             f"Festival season in {city} brings everyone together, beautiful culture",
#             f"Morning walks in {city} parks are therapeutic, nature in the city"
#         ]
        
#         text = random.choice(mock_tweets)
#         sentiment = self.analyzer.polarity_scores(text)
        
#         # Add variation
#         noise_factor = random.uniform(-0.2, 0.2)
#         adjusted_compound = max(-1, min(1, sentiment['compound'] + noise_factor))
        
#         return {
#             'text': text,
#             'sentiment_compound': adjusted_compound,
#             'sentiment_positive': sentiment['pos'],
#             'sentiment_negative': sentiment['neg'],
#             'sentiment_neutral': sentiment['neu'],
#             'created_at': datetime.now().isoformat(),
#             'user_followers': random.randint(100, 10000),
#             'retweet_count': random.randint(0, 50),
#             'like_count': random.randint(0, 100),
#             'type': 'twitter'
#         }

#     def calculate_city_mood(self, sentiment_data: List[Dict]) -> Dict:
#         """Calculate mood metrics with improved sentiment range distribution"""
#         if not sentiment_data:
#             return {
#                 'avg_sentiment': 0,
#                 'mood_label': 'No Data',
#                 'mood_emoji': '❓',
#                 'color_value': 50,
#                 'confidence': 0,
#                 'sample_size': 0,
#                 'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0}
#             }
        
#         sentiments = [item['sentiment_compound'] for item in sentiment_data]
#         avg_sentiment = sum(sentiments) / len(sentiments)
        
#         # Calculate distribution
#         positive_count = len([s for s in sentiments if s > 0.1])
#         negative_count = len([s for s in sentiments if s < -0.1])
#         neutral_count = len(sentiments) - positive_count - negative_count
        
#         total = len(sentiments)
#         distribution = {
#             'positive': round(positive_count / total * 100, 1),
#             'negative': round(negative_count / total * 100, 1),
#             'neutral': round(neutral_count / total * 100, 1)
#         }
        
#         # Enhanced mood classification with better range coverage
#         if avg_sentiment > 0.6:
#             mood_label, mood_emoji, color_value = "Extremely Positive", "🔥", 95
#         elif avg_sentiment > 0.4:
#             mood_label, mood_emoji, color_value = "Very Positive", "😍", 85
#         elif avg_sentiment > 0.2:
#             mood_label, mood_emoji, color_value = "Positive", "😊", 75
#         elif avg_sentiment > 0.05:
#             mood_label, mood_emoji, color_value = "Slightly Positive", "🙂", 65
#         elif avg_sentiment > -0.05:
#             mood_label, mood_emoji, color_value = "Neutral", "😐", 50
#         elif avg_sentiment > -0.2:
#             mood_label, mood_emoji, color_value = "Slightly Negative", "😕", 35
#         elif avg_sentiment > -0.4:
#             mood_label, mood_emoji, color_value = "Negative", "😞", 25
#         elif avg_sentiment > -0.6:
#             mood_label, mood_emoji, color_value = "Very Negative", "😢", 15
#         else:
#             mood_label, mood_emoji, color_value = "Extremely Negative", "😭", 5
        
#         confidence = min(1.0, len(sentiments) / 15)  # Confidence based on sample size
        
#         return {
#             'avg_sentiment': round(avg_sentiment, 3),
#             'mood_label': mood_label,
#             'mood_emoji': mood_emoji,
#             'color_value': color_value,
#             'confidence': round(confidence, 2),
#             'sample_size': len(sentiments),
#             'sentiment_distribution': distribution
#         }

#     def extract_trending_topics(self, all_content: List[Dict]) -> List[str]:
#         """Extract trending topics from news and tweets"""
#         all_texts = [item.get('text', '') for item in all_content if item.get('text')]
        
#         if not all_texts:
#             return []
        
#         # Combine all text
#         combined_text = ' '.join(all_texts).lower()
        
#         # Extract meaningful words (excluding common stop words)
#         stop_words = {
#             'the', 'and', 'is', 'in', 'to', 'of', 'for', 'on', 'with', 'at', 'by', 
#             'an', 'a', 'this', 'that', 'are', 'as', 'be', 'was', 'were', 'has', 
#             'have', 'had', 'but', 'or', 'not', 'from', 'they', 'we', 'their', 
#             'our', 'all', 'any', 'can', 'will', 'would', 'could', 'should', 'may', 
#             'might', 'must', 'shall', 'india', 'indian', 'new', 'get', 'one', 'two'
#         }
        
#         # Find words that appear multiple times
#         words = re.findall(r'\b[a-zA-Z]{4,}\b', combined_text)
#         filtered_words = [word for word in words if word not in stop_words]
        
#         # Count occurrences and get top trending topics
#         word_counts = Counter(filtered_words)
#         trending = [word.title() for word, count in word_counts.most_common(5) if count > 1]
        
#         return trending

#     def collect_city_data(self, city: str) -> Dict:
#         """Collect comprehensive data for a single city"""
#         try:
#             start_time = time.time()
#             logger.info(f"🏙️ Collecting data for {city}...")
            
#             # Collect all data types
#             weather = self.get_weather_data(city)
#             news = self.get_news_data(city)
#             tweets = self.get_twitter_data(city)
            
#             # Combine sentiment data
#             all_content = news + tweets
#             sentiment_data = [item for item in all_content if 'sentiment_compound' in item]
            
#             # Calculate mood metrics
#             mood_metrics = self.calculate_city_mood(sentiment_data)
            
#             # Extract trending topics
#             trending_topics = self.extract_trending_topics(all_content)
            
#             # Calculate collection time
#             collection_time = round(time.time() - start_time, 2)
            
#             result = {
#                 'city': city,
#                 'coordinates': {
#                     'lat': self.indian_cities[city]['lat'],
#                     'lon': self.indian_cities[city]['lon']
#                 },
#                 'mood_metrics': mood_metrics,
#                 'weather': weather,
#                 'trending_topics': trending_topics,
#                 'data_counts': {
#                     'news': len(news),
#                     'tweets': len(tweets),
#                     'total_samples': mood_metrics['sample_size']
#                 },
#                 'raw_data': {
#                     'news': news,
#                     'tweets': tweets
#                 },
#                 'collection_metadata': {
#                     'timestamp': datetime.now().isoformat(),
#                     'collection_time_seconds': collection_time,
#                     'data_quality': 'high' if mood_metrics['sample_size'] >= 15 else 'medium' if mood_metrics['sample_size'] >= 10 else 'low'
#                 }
#             }
            
#             logger.info(f"✅ {city}: {mood_metrics['mood_label']} ({mood_metrics['avg_sentiment']}) - {collection_time}s")
#             return result
            
#         except Exception as e:
#             logger.error(f"❌ Error collecting data for {city}: {e}")
#             return self._get_fallback_data(city)

#     def collect_all_cities_data(self) -> List[Dict]:
#         """Collect data for all cities using parallel processing"""
#         logger.info(f"🚀 Starting data collection for {len(self.indian_cities)} cities...")
#         start_time = time.time()
        
#         cities_data = []
        
#         # Use ThreadPoolExecutor for parallel data collection
#         with ThreadPoolExecutor(max_workers=4) as executor:
#             future_to_city = {
#                 executor.submit(self.collect_city_data, city): city 
#                 for city in self.indian_cities.keys()
#             }
            
#             for future in as_completed(future_to_city):
#                 city = future_to_city[future]
#                 try:
#                     city_data = future.result()
#                     cities_data.append(city_data)
#                 except Exception as e:
#                     logger.error(f"❌ Failed to collect data for {city}: {e}")
#                     cities_data.append(self._get_fallback_data(city))
        
#         total_time = round(time.time() - start_time, 2)
#         logger.info(f"🎉 All cities data collection completed in {total_time}s")
        
#         return cities_data

#     def _get_fallback_data(self, city: str) -> Dict:
#         """Return fallback data when collection fails"""
#         return {
#             'city': city,
#             'coordinates': self.indian_cities[city],
#             'mood_metrics': {
#                 'avg_sentiment': 0,
#                 'mood_label': 'Data Unavailable',
#                 'mood_emoji': '🔄',
#                 'color_value': 50,
#                 'confidence': 0,
#                 'sample_size': 0,
#                 'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0}
#             },
#             'weather': {},
#             'trending_topics': [],
#             'data_counts': {'news': 0, 'tweets': 0, 'total_samples': 0},
#             'raw_data': {'news': [], 'tweets': []},
#             'collection_metadata': {
#                 'timestamp': datetime.now().isoformat(),
#                 'collection_time_seconds': 0,
#                 'data_quality': 'unavailable'
#             }
#         }



