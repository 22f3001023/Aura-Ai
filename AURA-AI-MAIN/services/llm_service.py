



# # # # # services/llm_service.py
# # # # import google.generativeai as genai
# # # # import logging
# # # # from typing import Dict, List
# # # # import random
# # # # import os

# # # # logger = logging.getLogger(__name__)

# # # # class LLMService:
# # # #     def __init__(self, gemini_api_key: str):
# # # #         self.gemini_api_key = 'AIzaSyA2RlQlMPZgju5FmSkItPdsP4rQqTVMFCA'
        
# # # #         # Configure Gemini
# # # #         genai.configure(api_key=gemini_api_key)
        
# # # #         # Initialize the model
# # # #         self.model = genai.GenerativeModel('gemini-2.5-flash')
        
# # # #         # Configure Gemini
        
        
# # # #     async def generate_enhanced_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
# # # #                                        trending_topics: List[str], news_count: int, tweet_count: int, 
# # # #                                        basic_headline: str) -> str:
# # # #         """Generate enhanced Gen-Z headline using Google Gemini based on news+tweets+weather"""
# # # #         try:
# # # #             # Check if we have sufficient data for meaningful headline generation
# # # #             if not self._has_sufficient_data(news_count, tweet_count, mood_metrics):
# # # #                 logger.warning(f"Insufficient data for {city}: {news_count} news, {tweet_count} tweets")
# # # #                 return basic_headline  # Return basic headline if not enough data
            
# # # #             # Prepare context from actual data
# # # #             temp = weather.get('temperature_c', 20)
# # # #             condition = weather.get('condition', 'Clear')
# # # #             mood_label = mood_metrics.get('mood_label', 'Neutral')
# # # #             sentiment_score = mood_metrics.get('avg_sentiment', 0)
# # # #             sample_size = mood_metrics.get('sample_size', 0)
            
# # # #             # Build context with news and tweet emphasis
# # # #             context = self._build_news_tweet_context(city, weather, mood_metrics, trending_topics, news_count, tweet_count)
            
# # # #             prompt = f"""
# # # # Create a VIRAL Gen-Z style headline about {city} right NOW based on REAL SOCIAL DATA and NEWS.

# # # # CURRENT DATA ANALYSIS:
# # # # - City: {city}
# # # # - Weather: {condition}, {temp}°C (background context only)
# # # # - Overall Mood: {mood_label} (Sentiment Score: {sentiment_score})
# # # # - Data Sources: {news_count} news articles + {tweet_count} tweets analyzed
# # # # - Trending Topics: {', '.join(trending_topics) if trending_topics else 'No strong trends'}
# # # # - Total Social Posts Analyzed: {sample_size}

# # # # REQUIREMENTS:
# # # # ✅ Focus on NEWS and SOCIAL MEDIA TRENDS, not just weather
# # # # ✅ Use authentic Gen-Z slang (no cap, periodt, slay, vibes, fr, rn, lowkey, highkey, etc.)
# # # # ✅ Keep under 10 words
# # # # ✅ Include 1-2 emojis MAX
# # # # ✅ Sound like a viral TikTok/Instagram story caption
# # # # ✅ Reference actual trending topics if available
# # # # ✅ Make it feel current and relatable to social media

# # # # EXAMPLES (news/tweet focused):
# # # # "Mumbai metro expansion got everyone hyped fr 🚇✨"
# # # # "Delhi protests are trending but resilience stays strong 💪"
# # # # "Bangalore tech layoffs got the city in their feels 😔"
# # # # "Chennai food festival is absolutely bussin rn 🍛🔥"
# # # # "Kolkata art scene is giving main character energy 🎨"

# # # # Generate ONE perfect viral headline based on the NEWS and SOCIAL TRENDS:
# # # #             """

# # # #             # Generate response using Gemini
# # # #             response = self.model.generate_content(prompt)
            
# # # #             if response and response.text:
# # # #                 headline = self._clean_headline(response.text)
# # # #                 if self._validate_genz_headline(headline):
# # # #                     logger.info(f"Generated Gen-Z headline for {city}: {headline}")
# # # #                     return headline
            
# # # #             # If Gemini fails, create data-driven fallback focused on news/tweets
# # # #             return self._create_news_driven_fallback(city, mood_metrics, trending_topics, news_count, tweet_count)
            
# # # #         except Exception as e:
# # # #             logger.error(f"Gemini headline generation failed for {city}: {e}")
# # # #             return self._create_news_driven_fallback(city, mood_metrics, trending_topics, news_count, tweet_count)
    
# # # #     def _has_sufficient_data(self, news_count: int, tweet_count: int, mood_metrics: Dict) -> bool:
# # # #         """Check if we have enough data to generate meaningful headlines"""
# # # #         total_data_points = news_count + tweet_count
# # # #         if total_data_points < 5:  # Minimum 5 data points
# # # #             return False
        
# # # #         # Check if sentiment data is meaningful
# # # #         sentiment = mood_metrics.get('avg_sentiment', 0)
# # # #         sample_size = mood_metrics.get('sample_size', 0)
        
# # # #         if sample_size < 3:  # Need at least 3 sentiment samples
# # # #             return False
            
# # # #         return True
    
# # # #     def _build_news_tweet_context(self, city: str, weather: Dict, mood_metrics: Dict, 
# # # #                                 trending_topics: List[str], news_count: int, tweet_count: int) -> str:
# # # #         """Build rich context focusing on news and social media trends"""
# # # #         context_parts = []
        
# # # #         # Data volume context
# # # #         if news_count > 10:
# # # #             context_parts.append("significant news coverage")
# # # #         elif news_count > 5:
# # # #             context_parts.append("moderate news activity")
# # # #         elif news_count > 0:
# # # #             context_parts.append("some news mentions")
            
# # # #         if tweet_count > 20:
# # # #             context_parts.append("high social media engagement")
# # # #         elif tweet_count > 10:
# # # #             context_parts.append("active social media discussion")
# # # #         elif tweet_count > 5:
# # # #             context_parts.append("some social media buzz")
        
# # # #         # Trending topics context
# # # #         if trending_topics:
# # # #             context_parts.append(f"trending topics: {', '.join(trending_topics[:3])}")
        
# # # #         # Mood context
# # # #         sentiment = mood_metrics.get('avg_sentiment', 0)
# # # #         if sentiment > 0.4:
# # # #             context_parts.append("highly positive public sentiment")
# # # #         elif sentiment > 0.1:
# # # #             context_parts.append("generally positive mood")
# # # #         elif sentiment < -0.4:
# # # #             context_parts.append("strong negative sentiment")
# # # #         elif sentiment < -0.1:
# # # #             context_parts.append("somewhat negative public mood")
# # # #         else:
# # # #             context_parts.append("neutral public sentiment")
        
# # # #         # Weather context (secondary)
# # # #         temp = weather.get('temperature_c', 20)
# # # #         condition = weather.get('condition', '').lower()
# # # #         if 'rain' in condition:
# # # #             context_parts.append("rainy conditions")
# # # #         elif temp > 35:
# # # #             context_parts.append("hot weather")
# # # #         elif temp < 15:
# # # #             context_parts.append("cool weather")
        
# # # #         return ", ".join(context_parts) if context_parts else "general city atmosphere"
    
# # # #     def _clean_headline(self, headline: str) -> str:
# # # #         """Clean and format the headline"""
# # # #         headline = headline.replace('"', '').replace("'", '').strip()
        
# # # #         # Remove any markdown formatting
# # # #         headline = headline.replace('**', '').replace('*', '')
        
# # # #         if headline and not headline[0].isupper():
# # # #             headline = headline.capitalize()
            
# # # #         return headline
    
# # # #     def _validate_genz_headline(self, headline: str) -> bool:
# # # #         """Validate if headline uses Gen-Z language"""
# # # #         if not headline or len(headline) < 5 or len(headline) > 80:
# # # #             return False
            
# # # #         headline_lower = headline.lower()
# # # #         genz_indicators = [
# # # #             'no cap', 'fr', 'periodt', 'slay', 'vibes', 'lowkey', 'highkey',
# # # #             'rn', 'ngl', 'bet', 'valid', 'sus', 'fire', 'lit', 'ate',
# # # #             'understood', 'assignment', 'giving', 'energy', 'different',
# # # #             'immaculate', 'unmatched', 'absolutely', 'down bad', 'pressed',
# # # #             'bussin', 'main character', 'hits different', 'go off', 'say less'
# # # #         ]
        
# # # #         return any(indicator in headline_lower for indicator in genz_indicators)
    
# # # #     def _create_news_driven_fallback(self, city: str, mood_metrics: Dict, 
# # # #                                    trending_topics: List[str], news_count: int, tweet_count: int) -> str:
# # # #         """Create data-driven fallback headline when Gemini fails or data is limited"""
# # # #         sentiment = mood_metrics.get('avg_sentiment', 0)
# # # #         mood_emoji = mood_metrics.get('mood_emoji', '😐')
        
# # # #         # Headlines focused on data volume and trends
# # # #         if trending_topics and len(trending_topics) > 0:
# # # #             topic = trending_topics[0].lower()
# # # #             if sentiment > 0.3:
# # # #                 templates = [
# # # #                     f"{city} {topic} scene is absolutely fire rn {mood_emoji}",
# # # #                     f"{city} {topic} vibes are unmatched no cap {mood_emoji}",
# # # #                     f"{city} {topic} energy is giving main character {mood_emoji}"
# # # #                 ]
# # # #             elif sentiment < -0.3:
# # # #                 templates = [
# # # #                     f"{city} {topic} situation is lowkey sus {mood_emoji}",
# # # #                     f"{city} {topic} vibes are down bad rn {mood_emoji}",
# # # #                     f"{city} {topic} drama got everyone pressed {mood_emoji}"
# # # #                 ]
# # # #             else:
# # # #                 templates = [
# # # #                     f"{city} {topic} scene is mid but valid {mood_emoji}",
# # # #                     f"{city} {topic} vibes are giving neutral energy {mood_emoji}",
# # # #                     f"{city} {topic} mood is lowkey chill {mood_emoji}"
# # # #                 ]
        
# # # #         # Headlines based on data volume
# # # #         elif news_count + tweet_count > 15:
# # # #             if sentiment > 0.3:
# # # #                 templates = [
# # # #                     f"{city} buzzing with positive energy rn {mood_emoji}",
# # # #                     f"{city} social media is absolutely slaying {mood_emoji}",
# # # #                     f"{city} news cycle is giving main character {mood_emoji}"
# # # #                 ]
# # # #             elif sentiment < -0.3:
# # # #                 templates = [
# # # #                     f"{city} going through it in the news {mood_emoji}",
# # # #                     f"{city} social media mood is heavy rn {mood_emoji}",
# # # #                     f"{city} news cycle got everyone in their feels {mood_emoji}"
# # # #                 ]
# # # #             else:
# # # #                 templates = [
# # # #                     f"{city} keeping it real in the news {mood_emoji}",
# # # #                     f"{city} social media vibes are neutral {mood_emoji}",
# # # #                     f"{city} news cycle is mid but valid {mood_emoji}"
# # # #                 ]
        
# # # #         # Generic fallback based on sentiment
# # # #         else:
# # # #             if sentiment > 0.4:
# # # #                 templates = [
# # # #                     f"{city} vibes are immaculate today no cap {mood_emoji}",
# # # #                     f"{city} energy is giving main character {mood_emoji}",
# # # #                     f"{city} absolutely slaying rn periodt {mood_emoji}"
# # # #                 ]
# # # #             elif sentiment < -0.4:
# # # #                 templates = [
# # # #                     f"{city} going through it today ngl {mood_emoji}",
# # # #                     f"{city} vibes are sus but we'll survive {mood_emoji}",
# # # #                     f"{city} mood is giving struggle energy {mood_emoji}"
# # # #                 ]
# # # #             else:
# # # #                 templates = [
# # # #                     f"{city} keeping it real today fr {mood_emoji}",
# # # #                     f"{city} vibes are mid but that's valid {mood_emoji}",
# # # #                     f"{city} energy is giving neutral {mood_emoji}"
# # # #                 ]
        
# # # #         return random.choice(templates) if templates else f"{city} vibes rn {mood_emoji}"



# # # # services/llm_service.py
# # # import google.generativeai as genai
# # # import logging
# # # from typing import Dict, List
# # # import random
# # # import os

# # # logger = logging.getLogger(__name__)

# # # class LLMService:
# # #     def __init__(self, gemini_api_key: str):
# # #         self.gemini_api_key = gemini_api_key
        
# # #         # Configure Gemini
# # #         genai.configure(api_key=gemini_api_key)
        
# # #         # Initialize the model
# # #         self.model = genai.GenerativeModel('gemini-2.5-flash')
        
# # #     async def generate_catchy_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
# # #                                     trending_topics: List[str], news_count: int, tweet_count: int) -> str:
# # #         """Generate catchy headline combining news+tweets+weather data"""
# # #         try:
# # #             # Check if we have sufficient data
# # #             if not self._has_sufficient_data(news_count, tweet_count):
# # #                 logger.warning(f"Insufficient data for {city}: {news_count} news, {tweet_count} tweets")
# # #                 return self._create_fallback_headline(city, mood_metrics)
            
# # #             # Prepare data for headline generation
# # #             temp = weather.get('temperature_c', 20)
# # #             condition = weather.get('condition', 'Clear')
# # #             mood_label = mood_metrics.get('mood_label', 'Neutral')
# # #             sentiment_score = mood_metrics.get('avg_sentiment', 0)
            
# # #             prompt = f"""
# # # Create a CATCHY NEWS HEADLINE about {city} that combines current weather, social media trends, and news.

# # # CURRENT SITUATION:
# # # - City: {city}
# # # - Weather: {condition}, {temp}°C
# # # - Public Mood: {mood_label} (Sentiment: {sentiment_score:.2f})
# # # - Data Sources: {news_count} news articles + {tweet_count} social media posts
# # # - Trending Topics: {', '.join(trending_topics[:5]) if trending_topics else 'No strong trends'}

# # # REQUIREMENTS:
# # # ✅ Combine weather + social trends + news in one catchy headline
# # # ✅ Keep it under 10 words maximum
# # # ✅ Make it engaging and attention-grabbing
# # # ✅ Focus on what's happening RIGHT NOW in the city
# # # ✅ Reference specific trends if they're significant
# # # ✅ Use professional but engaging news-style language

# # # EXAMPLES:
# # # "Delhi Heatwave Sparks Social Media Frenzy as Temperatures Soar"
# # # "Mumbai Rains Dampen Spirits but Twitter Buzzes with Resilience"
# # # "Bangalore Tech News Dominates Social Media Amid Pleasant Weather"
# # # "Chennai Food Festival Trends Online Despite Humid Conditions"
# # # "Kolkata Cultural Events Brighten Mood Despite Cloudy Skies"

# # # Generate ONE perfect catchy headline:
# # #             """

# # #             # Generate response using Gemini
# # #             response = self.model.generate_content(prompt)
            
# # #             if response and response.text:
# # #                 headline = self._clean_headline(response.text)
# # #                 if self._validate_headline(headline, city):
# # #                     logger.info(f"Generated catchy headline for {city}: {headline}")
# # #                     return headline
            
# # #             # If Gemini fails, create data-driven fallback
# # #             return self._create_data_driven_headline(city, weather, mood_metrics, trending_topics)
            
# # #         except Exception as e:
# # #             logger.error(f"Headline generation failed for {city}: {e}")
# # #             return self._create_data_driven_headline(city, weather, mood_metrics, trending_topics)
    
# # #     def _has_sufficient_data(self, news_count: int, tweet_count: int) -> bool:
# # #         """Check if we have enough data to generate meaningful headlines"""
# # #         return (news_count + tweet_count) >= 3  # Minimum 3 data points
    
# # #     def _clean_headline(self, headline: str) -> str:
# # #         """Clean and format the headline"""
# # #         headline = headline.replace('"', '').replace("'", '').strip()
# # #         headline = headline.replace('**', '').replace('*', '')  # Remove markdown
# # #         if headline and not headline[0].isupper():
# # #             headline = headline.capitalize()
# # #         return headline
    
# # #     def _validate_headline(self, headline: str, city: str) -> bool:
# # #         """Validate if headline is appropriate"""
# # #         if not headline or len(headline) < 5 or len(headline) > 100:
# # #             return False
# # #         if city.lower() not in headline.lower():
# # #             return False
# # #         return True
    
# # #     def _create_data_driven_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
# # #                                   trending_topics: List[str]) -> str:
# # #         """Create data-driven headline when LLM fails"""
# # #         temp = weather.get('temperature_c', 20)
# # #         condition = weather.get('condition', '').lower()
# # #         mood_label = mood_metrics.get('mood_label', 'Neutral')
# # #         sentiment = mood_metrics.get('avg_sentiment', 0)
        
# # #         # Weather-based templates
# # #         if 'rain' in condition:
# # #             templates = [
# # #                 f"{city} Battles Rainy Weather Amid {mood_label} Public Mood",
# # #                 f"Rains in {city} Affect Daily Life, Social Media Reacts",
# # #                 f"{city} Weather: Rain Dampens Streets but Not Spirits"
# # #             ]
# # #         elif temp > 35:
# # #             templates = [
# # #                 f"{city} Heatwave Sparks Conversations Online and Offline",
# # #                 f"Scorching Temperatures in {city} Dominate Local Discussions",
# # #                 f"{city} Swelters as Heat Becomes Top Conversation Topic"
# # #             ]
# # #         elif temp < 15:
# # #             templates = [
# # #                 f"{city} Chill Sets In, Becomes Talk of the Town",
# # #                 f"Cold Snap in {city} Generates Buzz on Social Media",
# # #                 f"{city} Weather: Cold Front Brings heated Online Discussions"
# # #             ]
# # #         else:
# # #             templates = [
# # #                 f"{city} News and Weather Combine in Today's Headlines",
# # #                 f"{city} Current Events Capture Public Attention",
# # #                 f"{city} in the Spotlight: Weather and Trends Collide"
# # #             ]
        
# # #         # Add trending topics if available
# # #         if trending_topics:
# # #             topic = trending_topics[0]
# # #             templates.extend([
# # #                 f"{city}: {topic} Trends Amid {condition} Weather Conditions",
# # #                 f"{topic} Dominates {city} News Despite Weather Challenges",
# # #                 f"{city} Weather and {topic} Share Headline Space"
# # #             ])
        
# # #         # Mood-based adjustments
# # #         if sentiment > 0.3:
# # #             templates.extend([
# # #                 f"{city} Buzzes with Positive Energy Despite Weather",
# # #                 f"Good Vibes in {city} as Multiple Stories Unfold",
# # #                 f"{city} Residents Stay Positive Through Weather and News"
# # #             ])
# # #         elif sentiment < -0.3:
# # #             templates.extend([
# # #                 f"{city} Faces Challenges: Weather and Mood Align",
# # #                 f"Tough Day in {city} as Multiple Factors Converge",
# # #                 f"{city} Weather Reflects Subdued Public Sentiment"
# # #             ])
        
# # #         return random.choice(templates)
    
# # #     def _create_fallback_headline(self, city: str, mood_metrics: Dict) -> str:
# # #         """Create fallback headline when data is insufficient"""
# # #         mood_label = mood_metrics.get('mood_label', 'Neutral')
# # #         fallbacks = [
# # #             f"{city} in the News Today",
# # #             f"{city} Current Events Roundup",
# # #             f"{city} Today: Weather and Mood Update",
# # #             f"{city} Daily Situation Report",
# # #             f"{mood_label} Mood in {city} Today"
# # #         ]
# # #         return random.choice(fallbacks)



# # # services/llm_service.py - Updated with both method names for compatibility
# # import google.generativeai as genai
# # import logging
# # from typing import Dict, List
# # import random
# # import os

# # logger = logging.getLogger(__name__)

# # class LLMService:
# #     def __init__(self, gemini_api_key: str):
# #         self.gemini_api_key = gemini_api_key
        
# #         # Configure Gemini
# #         genai.configure(api_key=gemini_api_key)
        
# #         # Initialize the model
# #         self.model = genai.GenerativeModel('gemini-2.5-flash')
        
# #     async def generate_catchy_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
# #                                     trending_topics: List[str], news_count: int, tweet_count: int) -> str:
# #         """Generate catchy headline - main method for new API flow"""
# #         return await self._generate_headline_internal(city, weather, mood_metrics, trending_topics, news_count, tweet_count, style="catchy")
    
# #     async def generate_enhanced_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
# #                                        trending_topics: List[str], news_count: int, tweet_count: int, 
# #                                        basic_headline: str) -> str:
# #         """Generate enhanced Gen-Z headline - compatibility method"""
# #         return await self._generate_headline_internal(city, weather, mood_metrics, trending_topics, news_count, tweet_count, style="genz")
    
# #     async def _generate_headline_internal(self, city: str, weather: Dict, mood_metrics: Dict, 
# #                                         trending_topics: List[str], news_count: int, tweet_count: int,
# #                                         style: str = "catchy") -> str:
# #         """Internal method for headline generation"""
# #         try:
# #             # Check if we have sufficient data
# #             if not self._has_sufficient_data(news_count, tweet_count):
# #                 logger.warning(f"Insufficient data for {city}: {news_count} news, {tweet_count} tweets")
# #                 return self._create_fallback_headline(city, mood_metrics, style)
            
# #             # Prepare data for headline generation
# #             temp = weather.get('temperature_c', 20)
# #             condition = weather.get('condition', 'Clear')
# #             mood_label = mood_metrics.get('mood_label', 'Neutral')
# #             sentiment_score = mood_metrics.get('avg_sentiment', 0)
            
# #             if style == "genz":
# #                 prompt = self._create_genz_prompt(city, temp, condition, mood_label, sentiment_score, 
# #                                                 trending_topics, news_count, tweet_count)
# #             else:
# #                 prompt = self._create_catchy_prompt(city, temp, condition, mood_label, sentiment_score, 
# #                                                   trending_topics, news_count, tweet_count)

# #             # Generate response using Gemini
# #             response = self.model.generate_content(prompt)
            
# #             if response and response.text:
# #                 headline = self._clean_headline(response.text)
# #                 if self._validate_headline(headline, city):
# #                     logger.info(f"Generated {style} headline for {city}: {headline}")
# #                     return headline
            
# #             # If Gemini fails, create data-driven fallback
# #             return self._create_data_driven_headline(city, weather, mood_metrics, trending_topics, style)
            
# #         except Exception as e:
# #             logger.error(f"Headline generation failed for {city}: {e}")
# #             return self._create_data_driven_headline(city, weather, mood_metrics, trending_topics, style)
    
# #     def _create_genz_prompt(self, city: str, temp: int, condition: str, mood_label: str, 
# #                            sentiment_score: float, trending_topics: List[str], 
# #                            news_count: int, tweet_count: int) -> str:
# #         """Create Gen-Z style prompt"""
# #         return f"""
# # Create a VIRAL Gen-Z style headline about {city} right NOW based on REAL SOCIAL DATA and NEWS.

# # CURRENT DATA ANALYSIS:
# # - City: {city}
# # - Weather: {condition}, {temp}°C (background context only)
# # - Overall Mood: {mood_label} (Sentiment Score: {sentiment_score})
# # - Data Sources: {news_count} news articles + {tweet_count} tweets analyzed
# # - Trending Topics: {', '.join(trending_topics) if trending_topics else 'No strong trends'}

# # REQUIREMENTS:
# # ✅ Focus on NEWS and SOCIAL MEDIA TRENDS, not just weather
# # ✅ Use authentic Gen-Z slang (no cap, periodt, slay, vibes, fr, rn, lowkey, highkey, etc.)
# # ✅ Keep under 10 words
# # ✅ Include 1-2 emojis MAX
# # ✅ Sound like a viral TikTok/Instagram story caption
# # ✅ Reference actual trending topics if available
# # ✅ Make it feel current and relatable to social media

# # EXAMPLES (news/tweet focused):
# # "Mumbai metro expansion got everyone hyped fr 🚇✨"
# # "Delhi protests are trending but resilience stays strong 💪"
# # "Bangalore tech layoffs got the city in their feels 😔"
# # "Chennai food festival is absolutely bussin rn 🍛🔥"
# # "Kolkata art scene is giving main character energy 🎨"

# # Generate ONE perfect viral headline based on the NEWS and SOCIAL TRENDS:
# #         """
    
# #     def _create_catchy_prompt(self, city: str, temp: int, condition: str, mood_label: str, 
# #                              sentiment_score: float, trending_topics: List[str], 
# #                              news_count: int, tweet_count: int) -> str:
# #         """Create catchy news-style prompt"""
# #         return f"""
# # Create a CATCHY NEWS HEADLINE about {city} that combines current weather, social media trends, and news.

# # CURRENT SITUATION:
# # - City: {city}
# # - Weather: {condition}, {temp}°C
# # - Public Mood: {mood_label} (Sentiment: {sentiment_score:.2f})
# # - Data Sources: {news_count} news articles + {tweet_count} social media posts
# # - Trending Topics: {', '.join(trending_topics[:5]) if trending_topics else 'No strong trends'}

# # REQUIREMENTS:
# # ✅ Combine weather + social trends + news in one catchy headline
# # ✅ Keep it under 10 words maximum
# # ✅ Make it engaging and attention-grabbing
# # ✅ Focus on what's happening RIGHT NOW in the city
# # ✅ Reference specific trends if they're significant
# # ✅ Use professional but engaging news-style language

# # EXAMPLES:
# # "Delhi Heatwave Sparks Social Media Frenzy as Temperatures Soar"
# # "Mumbai Rains Dampen Spirits but Twitter Buzzes with Resilience"
# # "Bangalore Tech News Dominates Social Media Amid Pleasant Weather"
# # "Chennai Food Festival Trends Online Despite Humid Conditions"
# # "Kolkata Cultural Events Brighten Mood Despite Cloudy Skies"

# # Generate ONE perfect catchy headline:
# #         """
    
# #     def _has_sufficient_data(self, news_count: int, tweet_count: int) -> bool:
# #         """Check if we have enough data to generate meaningful headlines"""
# #         return (news_count + tweet_count) >= 3
    
# #     def _clean_headline(self, headline: str) -> str:
# #         """Clean and format the headline"""
# #         headline = headline.replace('"', '').replace("'", '').strip()
# #         headline = headline.replace('**', '').replace('*', '')
# #         if headline and not headline[0].isupper():
# #             headline = headline.capitalize()
# #         return headline
    
# #     def _validate_headline(self, headline: str, city: str) -> bool:
# #         """Validate if headline is appropriate"""
# #         if not headline or len(headline) < 5 or len(headline) > 100:
# #             return False
# #         if city.lower() not in headline.lower():
# #             return False
# #         return True
    
# #     def _create_data_driven_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
# #                                   trending_topics: List[str], style: str = "catchy") -> str:
# #         """Create data-driven headline when LLM fails"""
# #         temp = weather.get('temperature_c', 20)
# #         condition = weather.get('condition', '').lower()
# #         mood_label = mood_metrics.get('mood_label', 'Neutral')
# #         sentiment = mood_metrics.get('avg_sentiment', 0)
# #         mood_emoji = mood_metrics.get('mood_emoji', '😐')
        
# #         if style == "genz":
# #             return self._create_genz_fallback(city, sentiment, mood_emoji, trending_topics)
# #         else:
# #             return self._create_catchy_fallback(city, temp, condition, mood_label, sentiment, trending_topics)
    
# #     def _create_genz_fallback(self, city: str, sentiment: float, mood_emoji: str, trending_topics: List[str]) -> str:
# #         """Create Gen-Z style fallback"""
# #         if trending_topics:
# #             topic = trending_topics[0].lower()
# #             if sentiment > 0.3:
# #                 templates = [
# #                     f"{city} {topic} scene is absolutely fire rn {mood_emoji}",
# #                     f"{city} {topic} vibes are unmatched no cap {mood_emoji}",
# #                     f"{city} {topic} energy is giving main character {mood_emoji}"
# #                 ]
# #             elif sentiment < -0.3:
# #                 templates = [
# #                     f"{city} {topic} situation is lowkey sus {mood_emoji}",
# #                     f"{city} {topic} vibes are down bad rn {mood_emoji}",
# #                     f"{city} {topic} drama got everyone pressed {mood_emoji}"
# #                 ]
# #             else:
# #                 templates = [
# #                     f"{city} {topic} scene is mid but valid {mood_emoji}",
# #                     f"{city} {topic} vibes are giving neutral energy {mood_emoji}",
# #                     f"{city} {topic} mood is lowkey chill {mood_emoji}"
# #                 ]
# #         else:
# #             if sentiment > 0.4:
# #                 templates = [
# #                     f"{city} vibes are immaculate today no cap {mood_emoji}",
# #                     f"{city} energy is giving main character {mood_emoji}",
# #                     f"{city} absolutely slaying rn periodt {mood_emoji}"
# #                 ]
# #             elif sentiment < -0.4:
# #                 templates = [
# #                     f"{city} going through it today ngl {mood_emoji}",
# #                     f"{city} vibes are sus but we'll survive {mood_emoji}",
# #                     f"{city} mood is giving struggle energy {mood_emoji}"
# #                 ]
# #             else:
# #                 templates = [
# #                     f"{city} keeping it real today fr {mood_emoji}",
# #                     f"{city} vibes are mid but that's valid {mood_emoji}",
# #                     f"{city} energy is giving neutral {mood_emoji}"
# #                 ]
        
# #         return random.choice(templates)
    
# #     def _create_catchy_fallback(self, city: str, temp: int, condition: str, mood_label: str, 
# #                                sentiment: float, trending_topics: List[str]) -> str:
# #         """Create catchy news-style fallback"""
# #         # Weather-based templates
# #         if 'rain' in condition:
# #             templates = [
# #                 f"{city} Battles Rainy Weather Amid {mood_label} Public Mood",
# #                 f"Rains in {city} Affect Daily Life, Social Media Reacts",
# #                 f"{city} Weather: Rain Dampens Streets but Not Spirits"
# #             ]
# #         elif temp > 35:
# #             templates = [
# #                 f"{city} Heatwave Sparks Conversations Online and Offline",
# #                 f"Scorching Temperatures in {city} Dominate Local Discussions",
# #                 f"{city} Swelters as Heat Becomes Top Conversation Topic"
# #             ]
# #         elif temp < 15:
# #             templates = [
# #                 f"{city} Chill Sets In, Becomes Talk of the Town",
# #                 f"Cold Snap in {city} Generates Buzz on Social Media",
# #                 f"{city} Weather: Cold Front Brings Heated Online Discussions"
# #             ]
# #         else:
# #             templates = [
# #                 f"{city} News and Weather Combine in Today's Headlines",
# #                 f"{city} Current Events Capture Public Attention",
# #                 f"{city} in the Spotlight: Weather and Trends Collide"
# #             ]
        
# #         # Add trending topics if available
# #         if trending_topics:
# #             topic = trending_topics[0]
# #             templates.extend([
# #                 f"{city}: {topic} Trends Amid {condition} Weather Conditions",
# #                 f"{topic} Dominates {city} News Despite Weather Challenges",
# #                 f"{city} Weather and {topic} Share Headline Space"
# #             ])
        
# #         return random.choice(templates)
    
# #     def _create_fallback_headline(self, city: str, mood_metrics: Dict, style: str = "catchy") -> str:
# #         """Create fallback headline when data is insufficient"""
# #         mood_label = mood_metrics.get('mood_label', 'Neutral')
# #         mood_emoji = mood_metrics.get('mood_emoji', '😐')
        
# #         if style == "genz":
# #             fallbacks = [
# #                 f"{city} vibes rn {mood_emoji}",
# #                 f"{city} keeping it real fr {mood_emoji}",
# #                 f"{city} energy is giving neutral {mood_emoji}"
# #             ]
# #         else:
# #             fallbacks = [
# #                 f"{city} in the News Today",
# #                 f"{city} Current Events Roundup",
# #                 f"{city} Today: Weather and Mood Update",
# #                 f"{city} Daily Situation Report",
# #                 f"{mood_label} Mood in {city} Today"
# #             ]
        
# #         return random.choice(fallbacks)



# # services/llm_service.py - Updated for raw data processing with no fallbacks
# import google.generativeai as genai
# import logging
# from typing import Dict, List
# import json

# logger = logging.getLogger(__name__)

# class LLMService:
#     def __init__(self, gemini_api_key: str):
#         self.gemini_api_key = gemini_api_key
#         genai.configure(api_key=gemini_api_key)
#         self.model = genai.GenerativeModel('gemini-2.5-flash')
        
#     async def generate_genz_headline_from_raw_data(
#         self, 
#         city: str, 
#         news_items: List[Dict], 
#         tweet_items: List[Dict], 
#         weather: Dict, 
#         trending_topics: List[str]
#     ) -> str:
#         """
#         Generate Gen-Z headline from raw news, tweets, and weather data
#         NO FALLBACKS - pure LLM generation only
#         """
#         try:
#             # Prepare raw content for LLM
#             news_content = self._format_news_for_llm(news_items)
#             tweet_content = self._format_tweets_for_llm(tweet_items)
#             weather_content = self._format_weather_for_llm(weather)
            
#             prompt = f"""
# You are a Gen-Z social media expert creating VIRAL headlines about {city} based on REAL-TIME DATA.

# ANALYZE THIS RAW DATA FROM {city}:

# WEATHER DATA:
# {weather_content}

# NEWS HEADLINES ({len(news_items)} articles):
# {news_content}

# SOCIAL MEDIA POSTS ({len(tweet_items)} posts):
# {tweet_content}

# TRENDING TOPICS:
# {', '.join(trending_topics) if trending_topics else 'No strong trends detected'}

# TASK: Create ONE viral Gen-Z headline that captures the MAIN VIBE of {city} right now.

# REQUIREMENTS:
# ✅ Use authentic Gen-Z slang (no cap, periodt, slay, vibes, fr, rn, lowkey, highkey, bussin, sus, etc.)
# ✅ Reference the ACTUAL news/social trends from the data above
# ✅ Keep under 10 words maximum
# ✅ Include 1-2 emojis that match the vibe
# ✅ Make it feel like a TikTok/Instagram story caption
# ✅ Focus on what's ACTUALLY happening based on the data
# ✅ Combine weather + news + social sentiment

# EXAMPLES:
# "Mumbai monsoon + startup funding got everyone hyped rn 🌧️✨"
# "Delhi pollution drama but tech scene still slaying fr 💻🔥"
# "Bangalore weather perfect but layoffs got ppl pressed 😅💼"

# Generate ONE perfect viral headline based on the ACTUAL DATA above:
#             """

#             # Generate using Gemini
#             response = self.model.generate_content(prompt)
            
#             if not response or not response.text:
#                 raise Exception("LLM returned empty response")
            
#             headline = self._clean_headline(response.text)
            
#             if not headline or len(headline) < 5:
#                 raise Exception("LLM generated invalid headline")
            
#             logger.info(f"Generated Gen-Z headline for {city}: {headline}")
#             return headline
            
#         except Exception as e:
#             logger.error(f"LLM headline generation failed for {city}: {e}")
#             raise Exception(f"Failed to generate headline: {str(e)}")
    
#     def _format_news_for_llm(self, news_items: List[Dict]) -> str:
#         """Format news items for LLM consumption"""
#         if not news_items:
#             return "No news data available"
        
#         formatted_news = []
#         for i, item in enumerate(news_items[:10], 1):  # Limit to top 10
#             title = item.get('title', '').strip()
#             description = item.get('description', '').strip()
#             sentiment = item.get('sentiment', 0)
            
#             if title:
#                 news_text = f"{i}. {title}"
#                 if description and len(description) < 100:
#                     news_text += f" - {description}"
#                 news_text += f" (Sentiment: {sentiment:.2f})"
#                 formatted_news.append(news_text)
        
#         return '\n'.join(formatted_news) if formatted_news else "No meaningful news content"
    
#     def _format_tweets_for_llm(self, tweet_items: List[Dict]) -> str:
#         """Format tweets for LLM consumption"""
#         if not tweet_items:
#             return "No social media data available"
        
#         formatted_tweets = []
#         for i, item in enumerate(tweet_items[:10], 1):  # Limit to top 10
#             text = item.get('text', '').strip()
#             sentiment = item.get('sentiment', 0)
            
#             if text:
#                 tweet_text = f"{i}. {text[:150]}..." if len(text) > 150 else f"{i}. {text}"
#                 tweet_text += f" (Sentiment: {sentiment:.2f})"
#                 formatted_tweets.append(tweet_text)
        
#         return '\n'.join(formatted_tweets) if formatted_tweets else "No meaningful social media content"
    
#     def _format_weather_for_llm(self, weather: Dict) -> str:
#         """Format weather data for LLM consumption"""
#         if not weather:
#             return "No weather data available"
        
#         temp = weather.get('temperature_c', 'Unknown')
#         condition = weather.get('condition', 'Unknown')
#         humidity = weather.get('humidity', 'Unknown')
#         wind = weather.get('wind_kph', 'Unknown')
#         feels_like = weather.get('feels_like_c', 'Unknown')
        
#         return f"Temperature: {temp}°C, Condition: {condition}, Feels like: {feels_like}°C, Humidity: {humidity}%, Wind: {wind} kph"
    
#     def _clean_headline(self, headline: str) -> str:
#         """Clean and format the headline"""
#         if not headline:
#             return ""
        
#         # Remove quotes and extra formatting
#         headline = headline.replace('"', '').replace("'", '').strip()
#         headline = headline.replace('**', '').replace('*', '')
        
#         # Remove any prefixes like "Headline:" or numbers
#         headline = headline.split(':', 1)[-1].strip()
#         headline = headline.lstrip('1234567890. ').strip()
        
#         # Ensure proper capitalization
#         if headline and not headline[0].isupper():
#             headline = headline.capitalize()
            
#         return headline
    
#     # Legacy method for compatibility with existing code
#     async def generate_catchy_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
#                                     trending_topics: List[str], news_count: int, tweet_count: int) -> str:
#         """Legacy method - redirects to raw data method if possible"""
#         # This is a fallback for existing code that doesn't provide raw data
#         # In practice, you should use generate_genz_headline_from_raw_data
        
#         fake_news = [{"title": f"{city} news update", "description": "General news", "sentiment": 0}] * min(news_count, 5)
#         fake_tweets = [{"text": f"{city} social media buzz", "sentiment": 0}] * min(tweet_count, 5)
        
#         return await self.generate_genz_headline_from_raw_data(
#             city=city,
#             news_items=fake_news,
#             tweet_items=fake_tweets,
#             weather=weather,
#             trending_topics=trending_topics
#         )


# services/llm_service.py - Process actual raw news headlines and tweet content
import google.generativeai as genai
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    async def generate_genz_headline_from_raw_data(
        self, 
        city: str, 
        news_items: List[Dict], 
        tweet_items: List[Dict], 
        weather: Dict, 
        trending_topics: List[str]
    ) -> str:
        """
        Generate Gen-Z headline from ACTUAL raw news headlines, tweet texts, and weather
        No fallbacks - pure LLM generation from real content
        """
        try:
            # Validate we have real content
            if not news_items and not tweet_items:
                raise Exception(f"No news or tweet content available for {city}")
            
            # Format ALL the actual content for LLM analysis
            news_content = self._format_actual_news_content(news_items)
            tweet_content = self._format_actual_tweet_content(tweet_items)
            weather_content = self._format_weather_content(weather)
            
            prompt = f"""
You are a Gen-Z social media expert creating VIRAL headlines about {city} based on REAL-TIME DATA.

ANALYZE THIS ACTUAL DATA FROM {city}:

CURRENT WEATHER:
{weather_content}

ACTUAL NEWS HEADLINES ({len(news_items)} articles):
{news_content}

ACTUAL SOCIAL MEDIA POSTS ({len(tweet_items)} posts):
{tweet_content}

TRENDING TOPICS:
{', '.join(trending_topics) if trending_topics else 'No specific trends detected'}

TASK: Create ONE viral Gen-Z headline that captures the REAL VIBE of {city} right now based on the ACTUAL CONTENT above.

REQUIREMENTS:
✅ Analyze the ACTUAL news headlines and social media content
✅ Use authentic Gen-Z slang (no cap, periodt, slay, vibes, fr, rn, lowkey, highkey, bussin, sus, etc.)
✅ Reference what's ACTUALLY happening from the real data
✅ Keep under 10 words maximum
✅ Include 1-2 emojis that match the actual mood from content
✅ Sound like a viral TikTok/Instagram story caption
✅ Combine the real weather + actual news themes + social sentiment
✅ Be specific about what's trending based on actual content

EXAMPLES OF STYLE:
"Mumbai startup funding + monsoon vibes got everyone hyped rn 🌧️✨"
"Delhi air quality protests but resilience stays strong fr 💪"
"Bangalore tech news + perfect weather = main character energy 💻☀️"

Based on the ACTUAL content analysis above, generate ONE perfect viral Gen-Z headline:
            """

            # Generate using Gemini
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("LLM returned empty response")
            
            headline = self._clean_headline(response.text)
            
            if not headline or len(headline) < 5:
                raise Exception("LLM generated invalid headline")
            
            logger.info(f"Generated Gen-Z headline for {city}: {headline}")
            return headline
            
        except Exception as e:
            logger.error(f"LLM headline generation failed for {city}: {e}")
            raise Exception(f"Failed to generate headline for {city}: {str(e)}")
    
    def _format_actual_news_content(self, news_items: List[Dict]) -> str:
        """Format ACTUAL news headlines and descriptions for LLM analysis"""
        if not news_items:
            return "No news content available"
        
        formatted_news = []
        for i, item in enumerate(news_items, 1):
            title = item.get('title', '').strip()
            description = item.get('description', '').strip()
            source = item.get('source_name', '')
            sentiment = item.get('sentiment_compound', 0)
            
            if title:
                # Include actual headline and description
                news_text = f"{i}. HEADLINE: {title}"
                if description and len(description) < 200:
                    news_text += f"\n   DESCRIPTION: {description}"
                news_text += f"\n   SOURCE: {source} | SENTIMENT: {sentiment:.2f}"
                formatted_news.append(news_text)
        
        return '\n\n'.join(formatted_news) if formatted_news else "No meaningful news content"
    
    def _format_actual_tweet_content(self, tweet_items: List[Dict]) -> str:
        """Format ACTUAL tweet texts for LLM analysis"""
        if not tweet_items:
            return "No social media content available"
        
        formatted_tweets = []
        for i, item in enumerate(tweet_items, 1):
            text = item.get('text', '').strip()
            sentiment = item.get('sentiment_compound', 0)
            likes = item.get('like_count', 0)
            retweets = item.get('retweet_count', 0)
            
            if text:
                # Include actual tweet text
                tweet_text = f"{i}. TWEET: {text}"
                tweet_text += f"\n   ENGAGEMENT: {likes} likes, {retweets} retweets | SENTIMENT: {sentiment:.2f}"
                formatted_tweets.append(tweet_text)
        
        return '\n\n'.join(formatted_tweets) if formatted_tweets else "No meaningful social media content"
    
    def _format_weather_content(self, weather: Dict) -> str:
        """Format weather data for LLM context"""
        if not weather:
            return "No weather data available"
        
        temp = weather.get('temperature_c', 'Unknown')
        condition = weather.get('condition', 'Unknown')
        humidity = weather.get('humidity', 'Unknown')
        feels_like = weather.get('feels_like_c', 'Unknown')
        wind = weather.get('wind_kph', 'Unknown')
        
        return f"Temperature: {temp}°C | Condition: {condition} | Feels like: {feels_like}°C | Humidity: {humidity}% | Wind: {wind} kph"
    
    def _clean_headline(self, headline: str) -> str:
        """Clean and format the generated headline"""
        if not headline:
            return ""
        
        # Remove quotes, formatting, and extra text
        headline = headline.replace('"', '').replace("'", '').strip()
        headline = headline.replace('**', '').replace('*', '')
        
        # Remove any prefixes like "Headline:" or numbering
        headline = headline.split(':', 1)[-1].strip()
        headline = headline.lstrip('1234567890. ').strip()
        
        # Remove any trailing explanation text
        if '\n' in headline:
            headline = headline.split('\n')[0].strip()
        
        # Ensure proper capitalization
        if headline and not headline[0].isupper():
            headline = headline.capitalize()
            
        return headline
    
    # Legacy compatibility method
    async def generate_catchy_headline(self, city: str, weather: Dict, mood_metrics: Dict, 
                                    trending_topics: List[str], news_count: int, tweet_count: int) -> str:
        """Legacy method - use generate_genz_headline_from_raw_data instead"""
        # This is for backward compatibility only
        # Create minimal fake data since we don't have raw content
        fake_news = [{"title": f"{city} general news update", "description": "General updates", "sentiment_compound": 0}]
        fake_tweets = [{"text": f"General {city} social media sentiment", "sentiment_compound": 0}]
        
        return await self.generate_genz_headline_from_raw_data(
            city=city,
            news_items=fake_news,
            tweet_items=fake_tweets,
            weather=weather,
            trending_topics=trending_topics
        )