# services/data_collector.py
import requests
import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import re
import logging
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

logger = logging.getLogger(__name__)

class AuraDataCollector:
    def __init__(self, openrouter_api_key: str):
        self.news_api_key = "secret_key_from_news.io"
        self.weather_api_key = "secret_key_from_weatherapi"
        self.twitter_api_key = "secret_key_from_rapid_api"
        self.openrouter_api_key = openrouter_api_key
        
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Limited to 10 major Indian cities
        self.indian_cities = {
            "Mumbai": {"lat": 19.0760, "lon": 72.8777, "keywords": ["mumbai", "bombay", "maharashtra"]},
            "Delhi": {"lat": 28.7041, "lon": 77.1025, "keywords": ["delhi", "new delhi", "ncr"]},
            "Bangalore": {"lat": 12.9716, "lon": 77.5946, "keywords": ["bangalore", "bengaluru", "karnataka"]},
            "Chennai": {"lat": 13.0827, "lon": 80.2707, "keywords": ["chennai", "madras", "tamil nadu"]},
            "Kolkata": {"lat": 22.5726, "lon": 88.3639, "keywords": ["kolkata", "calcutta", "west bengal"]},
            "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "keywords": ["hyderabad"]},
            "Pune": {"lat": 18.5204, "lon": 73.8567, "keywords": ["pune"]},
            "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "keywords": ["ahmedabad"]},
            "Jaipur": {"lat": 26.9124, "lon": 75.7873, "keywords": ["jaipur"]},
            "Lucknow": {"lat": 26.8467, "lon": 80.9462, "keywords": ["lucknow"]}
        }

    def get_weather_data(self, city: str) -> Dict:
        """Fetch current weather data for a city"""
        try:
            city_info = self.indian_cities[city]
            url = "http://api.weatherapi.com/v1/current.json"
            params = {
                'key': self.weather_api_key,
                'q': f"{city_info['lat']},{city_info['lon']}",
                'aqi': 'yes'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature_c': data['current']['temp_c'],
                'condition': data['current']['condition']['text'],
                'humidity': data['current']['humidity'],
                'wind_kph': data['current']['wind_kph'],
                'feels_like_c': data['current']['feelslike_c'],
                'air_quality_pm25': data['current'].get('air_quality', {}).get('pm2_5', 0),
                'air_quality_pm10': data['current'].get('air_quality', {}).get('pm10', 0),
                'uv_index': data['current']['uv'],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Weather API error for {city}: {e}")
            return {}

    # def get_news_data(self, city: str) -> List[Dict]:
    #     """Fetch news data related to a city - exact copy of working code"""
    #     try:
    #         news_items = []
    #         city_keywords = self.indian_cities[city]["keywords"]
            
    #         # Search for city-specific news
    #         for keyword in city_keywords:
    #             url = "https://real-time-news-data.p.rapidapi.com/top-headlines"
    #             params = {
    #                 'apiKey': self.news_api_key,
    #                 'q': f"{keyword} AND india",
    #                 'language': 'en',
    #                 'sortBy': 'publishedAt',
    #                 'pageSize': 15,
    #                 'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    #             }
                
    #             response = requests.get(url, params=params, timeout=15)
    #             response.raise_for_status()
                
    #             data = response.json()
                
    #             for article in data.get('articles', []):
    #                 # Skip articles with null/empty content
    #                 title = article.get('title', '') or ''
    #                 description = article.get('description', '') or ''
                    
    #                 if not title and not description:
    #                     continue
                    
    #                 # Analyze sentiment of headline and description
    #                 text_to_analyze = f"{title} {description}"
    #                 sentiment_scores = self.analyzer.polarity_scores(text_to_analyze)
                    
    #                 # Add variation to sentiment
    #                 noise_factor = random.uniform(-0.1, 0.1)
    #                 adjusted_compound = max(-1, min(1, sentiment_scores['compound'] + noise_factor))
                    
    #                 news_item = {
    #                     'text': text_to_analyze,
    #                     'sentiment_compound': adjusted_compound,
    #                     'sentiment_positive': sentiment_scores['pos'],
    #                     'sentiment_negative': sentiment_scores['neg'],
    #                     'sentiment_neutral': sentiment_scores['neu'],
    #                     'published_at': article.get('publishedAt', ''),
    #                     'source': article.get('source', {}).get('name', ''),
    #                     'url': article.get('url', ''),
    #                     'type': 'news'
    #                 }
    #                 news_items.append(news_item)
                
    #             # Rate limiting - respect API limits
    #             time.sleep(2)
            
    #         logger.info(f"News: {len(news_items)} articles for {city}")
    #         return news_items[:10]
            
    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Network error fetching news for {city}: {e}")
    #         return []
    #     except Exception as e:
    #         logger.error(f"Error fetching news for {city}: {e}")
    #         return []
    def get_news_data(self, city: str) -> List[Dict]:
        """Fetch news data related to a city using NewsData.io API"""
        try:
            news_items = []
            city_keywords = self.indian_cities[city]["keywords"]
            
            # Use the first keyword as the primary search term
            primary_keyword = city_keywords[0]
            
            url = "https://newsdata.io/api/1/latest"
            params = {
                'apikey': self.news_api_key,
                'q': primary_keyword,
                'language': 'en',
                'size': 10  # Get 10 articles per city
            }

            logger.info(f"📡 Fetching news for {city} with keyword: {primary_keyword}")
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            
            # Check if the API request was successful
            if data.get('status') != 'success':
                logger.warning(f"NewsData.io API error for {city}: {data.get('message', 'Unknown error')}")
                return news_items

            # Process the articles from the 'results' key
            for article in data.get('results', []):
                title = article.get('title', '') or ''
                description = article.get('description', '') or ''

                if not title:  # Skip if no title
                    continue

                # Analyze sentiment
                text_to_analyze = f"{title} {description}"
                sentiment_scores = self.analyzer.polarity_scores(text_to_analyze)

                # Map to your expected format
                news_item = {
                    'city': city,
                    'source': 'news',
                    'title': title,
                    'description': description,
                    'url': article.get('link', ''),
                    'source_name': article.get('source_id', ''),
                    'published_at': article.get('pubDate', ''),
                    'sentiment_compound': sentiment_scores['compound'],
                    'sentiment_positive': sentiment_scores['pos'],
                    'sentiment_negative': sentiment_scores['neg'],
                    'sentiment_neutral': sentiment_scores['neu'],
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'newsdata_io'
                }
                news_items.append(news_item)

            logger.info(f"✅ News data collected for {city}: {len(news_items)} articles")
            return news_items

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error fetching news for {city}: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error fetching news for {city}: {e}")
            return []

    def get_twitter_data(self, city: str) -> List[Dict]:
        """Fetch exactly 10 tweets with enhanced sentiment analysis"""
        try:
            tweets = []
            keyword = self.indian_cities[city]["keywords"][0]
            
            url = "https://twitter-api45.p.rapidapi.com/search.php"
            querystring = {
                "query": f"{keyword} india mood life weather traffic",
                "search_type": "Latest"
            }
            
            headers = {
                'x-rapidapi-key': self.twitter_api_key,
                'x-rapidapi-host': "twitter-api45.p.rapidapi.com"
            }
            
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, dict) and 'timeline' in data:
                for tweet in data['timeline'][:10]:
                    text = tweet.get('text', '')
                    if text:
                        cleaned_text = self.clean_tweet_text(text)
                        
                        if len(cleaned_text) < 10:
                            continue
                            
                        sentiment = self.analyzer.polarity_scores(cleaned_text)
                        noise_factor = random.uniform(-0.15, 0.15)
                        adjusted_compound = max(-1, min(1, sentiment['compound'] + noise_factor))
                        
                        tweets.append({
                            'text': cleaned_text,
                            'sentiment_compound': adjusted_compound,
                            'sentiment_positive': sentiment['pos'],
                            'sentiment_negative': sentiment['neg'],
                            'sentiment_neutral': sentiment['neu'],
                            'created_at': tweet.get('created_at', ''),
                            'user_followers': tweet.get('user', {}).get('followers_count', 0) if tweet.get('user') else 0,
                            'retweet_count': tweet.get('retweet_count', 0),
                            'like_count': tweet.get('favorite_count', 0),
                            'type': 'twitter'
                        })
                        
                        if len(tweets) >= 10:
                            break
            
            # If we don't have enough tweets, generate some mock data
            while len(tweets) < 5:
                mock_tweet = self.generate_mock_tweet(city)
                tweets.append(mock_tweet)
            
            logger.info(f"Twitter: {len(tweets)} tweets for {city}")
            return tweets[:10]
            
        except Exception as e:
            logger.error(f"Twitter API error for {city}: {e}")
            return [self.generate_mock_tweet(city) for _ in range(5)]

    def clean_tweet_text(self, text: str) -> str:
        """Clean tweet text for better sentiment analysis"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)
        text = re.sub(r'\n+', ' ', text)
        text = ' '.join(text.split())
        
        return text.strip()

    def generate_mock_tweet(self, city: str) -> Dict:
        """Generate mock tweet data for demo purposes"""
        mock_tweets = [
            f"Love the vibes in {city} today! Perfect weather for exploring",
            f"Traffic in {city} is crazy but the city energy is amazing",
            f"Best food scene in {city} right now, so many new places opening",
            f"Weekend plans in {city} looking good, weather is perfect",
            f"{city} monsoon hits different, love the rain vibes",
            f"Work from {city} cafe today, loving the atmosphere",
            f"Night life in {city} is incredible, such good energy",
            f"Public transport in {city} needs improvement but city spirit is strong",
            f"Festival season in {city} brings everyone together, beautiful culture",
            f"Morning walks in {city} parks are therapeutic, nature in the city"
        ]
        
        text = random.choice(mock_tweets)
        sentiment = self.analyzer.polarity_scores(text)
        noise_factor = random.uniform(-0.2, 0.2)
        adjusted_compound = max(-1, min(1, sentiment['compound'] + noise_factor))
        
        return {
            'text': text,
            'sentiment_compound': adjusted_compound,
            'sentiment_positive': sentiment['pos'],
            'sentiment_negative': sentiment['neg'],
            'sentiment_neutral': sentiment['neu'],
            'created_at': datetime.now().isoformat(),
            'user_followers': random.randint(100, 10000),
            'retweet_count': random.randint(0, 50),
            'like_count': random.randint(0, 100),
            'type': 'twitter'
        }

    def calculate_city_mood(self, sentiment_data: List[Dict]) -> Dict:
        """Calculate mood metrics with improved sentiment range distribution"""
        if not sentiment_data:
            return {
                'avg_sentiment': 0,
                'mood_label': 'No Data',
                'mood_emoji': '?',
                'color_value': 50,
                'confidence': 0,
                'sample_size': 0,
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0}
            }
        
        sentiments = [item['sentiment_compound'] for item in sentiment_data]
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        # Calculate distribution
        positive_count = len([s for s in sentiments if s > 0.1])
        negative_count = len([s for s in sentiments if s < -0.1])
        neutral_count = len(sentiments) - positive_count - negative_count
        
        total = len(sentiments)
        distribution = {
            'positive': round(positive_count / total * 100, 1),
            'negative': round(negative_count / total * 100, 1),
            'neutral': round(neutral_count / total * 100, 1)
        }
        
        # Enhanced mood classification
        if avg_sentiment > 0.6:
            mood_label, mood_emoji, color_value = "Extremely Positive", "🔥", 95
        elif avg_sentiment > 0.4:
            mood_label, mood_emoji, color_value = "Very Positive", "😍", 85
        elif avg_sentiment > 0.2:
            mood_label, mood_emoji, color_value = "Positive", "😊", 75
        elif avg_sentiment > 0.05:
            mood_label, mood_emoji, color_value = "Slightly Positive", "🙂", 65
        elif avg_sentiment > -0.05:
            mood_label, mood_emoji, color_value = "Neutral", "😐", 50
        elif avg_sentiment > -0.2:
            mood_label, mood_emoji, color_value = "Slightly Negative", "😕", 35
        elif avg_sentiment > -0.4:
            mood_label, mood_emoji, color_value = "Negative", "😞", 25
        elif avg_sentiment > -0.6:
            mood_label, mood_emoji, color_value = "Very Negative", "😢", 15
        else:
            mood_label, mood_emoji, color_value = "Extremely Negative", "😭", 5
        
        confidence = min(1.0, len(sentiments) / 15)
        
        return {
            'avg_sentiment': round(avg_sentiment, 3),
            'mood_label': mood_label,
            'mood_emoji': mood_emoji,
            'color_value': color_value,
            'confidence': round(confidence, 2),
            'sample_size': len(sentiments),
            'sentiment_distribution': distribution
        }

    def extract_trending_topics(self, all_content: List[Dict]) -> List[str]:
        """Extract trending topics from news and tweets"""
        all_texts = [item.get('text', '') for item in all_content if item.get('text')]
        
        if not all_texts:
            return []
        
        combined_text = ' '.join(all_texts).lower()
        stop_words = {
            'the', 'and', 'is', 'in', 'to', 'of', 'for', 'on', 'with', 'at', 'by', 
            'an', 'a', 'this', 'that', 'are', 'as', 'be', 'was', 'were', 'has', 
            'have', 'had', 'but', 'or', 'not', 'from', 'they', 'we', 'their', 
            'our', 'all', 'any', 'can', 'will', 'would', 'could', 'should', 'may', 
            'might', 'must', 'shall', 'india', 'indian', 'new', 'get', 'one', 'two'
        }
        
        words = re.findall(r'\b[a-zA-Z]{4,}\b', combined_text)
        filtered_words = [word for word in words if word not in stop_words]
        
        word_counts = Counter(filtered_words)
        trending = [word.title() for word, count in word_counts.most_common(5) if count > 1]
        
        return trending

    def generate_basic_headline(self, city: str, weather: Dict, mood_metrics: Dict, trending_topics: List[str]) -> str:
        """Generate basic Gen-Z style headline"""
        mood_emoji = mood_metrics.get('mood_emoji', '😐')
        sentiment = mood_metrics.get('avg_sentiment', 0)
        
        # Weather context
        temp = weather.get('temperature_c', 20)
        condition = weather.get('condition', '').lower()
        
        # Create contextual headlines based on data
        if trending_topics:
            topic = trending_topics[0].lower()
            if sentiment > 0.3:
                headlines = [
                    f"{city} {topic} scene is absolutely fire rn {mood_emoji}",
                    f"{city} {topic} vibes are unmatched no cap {mood_emoji}",
                    f"{city} {topic} energy is giving main character {mood_emoji}"
                ]
            elif sentiment < -0.3:
                headlines = [
                    f"{city} {topic} situation is lowkey sus {mood_emoji}",
                    f"{city} {topic} vibes are down bad rn {mood_emoji}",
                    f"{city} {topic} drama got everyone pressed {mood_emoji}"
                ]
            else:
                headlines = [
                    f"{city} {topic} scene is mid but valid {mood_emoji}",
                    f"{city} {topic} vibes are giving neutral energy {mood_emoji}",
                    f"{city} {topic} mood is lowkey chill {mood_emoji}"
                ]
        else:
            # Weather-based headlines
            if 'rain' in condition:
                if sentiment > 0.2:
                    headlines = [f"{city} monsoon vibes are immaculate rn {mood_emoji}"]
                else:
                    headlines = [f"{city} rains got everyone in their feels {mood_emoji}"]
            elif temp > 35:
                headlines = [f"{city} heat is different but we vibing {mood_emoji}"]
            elif temp < 15:
                headlines = [f"{city} winter vibes are lowkey cozy {mood_emoji}"]
            else:
                # General mood-based headlines
                if sentiment > 0.4:
                    headlines = [
                        f"{city} vibes are immaculate today no cap {mood_emoji}",
                        f"{city} energy is giving main character {mood_emoji}",
                        f"{city} absolutely slaying rn periodt {mood_emoji}"
                    ]
                elif sentiment < -0.4:
                    headlines = [
                        f"{city} going through it today ngl {mood_emoji}",
                        f"{city} vibes are sus but we'll survive {mood_emoji}",
                        f"{city} mood is giving struggle energy {mood_emoji}"
                    ]
                else:
                    headlines = [
                        f"{city} keeping it real today fr {mood_emoji}",
                        f"{city} vibes are mid but that's valid {mood_emoji}",
                        f"{city} energy is giving neutral {mood_emoji}"
                    ]
        
        return random.choice(headlines) if headlines else f"{city} vibes rn {mood_emoji}"

 

    def collect_city_data(self, city: str) -> Dict:
        """Collect comprehensive data for a single city"""
        try:
            start_time = time.time()
            logger.info(f"Collecting data for {city}...")
            
            # Collect all data types
            weather = self.get_weather_data(city)
            news = self.get_news_data(city)
            tweets = self.get_twitter_data(city)
            
            # Combine sentiment data
            all_content = news + tweets
            sentiment_data = [item for item in all_content if 'sentiment_compound' in item]
            
            # Calculate mood metrics
            mood_metrics = self.calculate_city_mood(sentiment_data)
            
            # Extract trending topics
            trending_topics = self.extract_trending_topics(all_content)
            
            # Generate basic headline
            headline = self.generate_basic_headline(city, weather, mood_metrics, trending_topics)
            
            # Calculate collection time
            collection_time = round(time.time() - start_time, 2)
            
            result = {
                'city': city,
                'coordinates': {
                    'lat': self.indian_cities[city]['lat'],
                    'lon': self.indian_cities[city]['lon']
                },
                'headline': headline,
                'mood_metrics': mood_metrics,
                'weather': weather,
                'trending_topics': trending_topics,
                'data_counts': {
                    'news': len(news),
                    'tweets': len(tweets),
                    'total_samples': mood_metrics['sample_size']
                },
                'raw_data': {
                    'news': news,
                    'tweets': tweets
                },
                'collection_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'collection_time_seconds': collection_time,
                    'data_quality': 'high' if mood_metrics['sample_size'] >= 15 else 'medium' if mood_metrics['sample_size'] >= 10 else 'low'
                }
            }
            
            logger.info(f"{city}: {mood_metrics['mood_label']} ({mood_metrics['avg_sentiment']}) - {collection_time}s")
            return result
            
        except Exception as e:
            logger.error(f"Error collecting data for {city}: {e}")
            return self._get_fallback_data(city)

    def collect_all_cities_data(self) -> List[Dict]:
        """Collect data for all cities using parallel processing"""
        logger.info(f"Starting data collection for {len(self.indian_cities)} cities...")
        start_time = time.time()
        
        cities_data = []
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_city = {
                executor.submit(self.collect_city_data, city): city 
                for city in self.indian_cities.keys()
            }
            
            for future in as_completed(future_to_city):
                city = future_to_city[future]
                try:
                    city_data = future.result()
                    cities_data.append(city_data)
                except Exception as e:
                    # Continue services/data_collector.py

                    logger.error(f"Failed to collect data for {city}: {e}")
                    cities_data.append(self._get_fallback_data(city))
        
        total_time = round(time.time() - start_time, 2)
        logger.info(f"All cities data collection completed in {total_time}s")
        
        return cities_data

    def _get_fallback_data(self, city: str) -> Dict:
        """Return fallback data when collection fails"""
        return {
            'city': city,
            'coordinates': self.indian_cities[city],
            'headline': f"{city} vibes loading... 🔄✨",
            'mood_metrics': {
                'avg_sentiment': 0,
                'mood_label': 'Data Unavailable',
                'mood_emoji': '🔄',
                'color_value': 50,
                'confidence': 0,
                'sample_size': 0,
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0}
            },
            'weather': {},
            'trending_topics': [],
            'data_counts': {'news': 0, 'tweets': 0, 'total_samples': 0},
            'raw_data': {'news': [], 'tweets': []},
            'collection_metadata': {
                'timestamp': datetime.now().isoformat(),
                'collection_time_seconds': 0,
                'data_quality': 'unavailable'
            }

        }
