
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import logging
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

from services.data_collector import AuraDataCollector
from services.database import DatabaseManager
from services.llm_service import LLMService
from services.rag_service import RAGService

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for services
data_collector = None
db_manager = None
llm_service = None
rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global data_collector, db_manager, llm_service, rag_service
    
    try:
        gemini_api_key = 'AIzaSyA2RlQlMPZgju5FmSkItPdsP4rQqTVMFCA'
        
        # Initialize services
        data_collector = AuraDataCollector(gemini_api_key)
        db_manager = DatabaseManager()
        llm_service = LLMService(gemini_api_key)
        rag_service = RAGService(db_manager)
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    yield
    
    if db_manager:
        db_manager.close()
    logger.info("Application shutdown complete")

app = FastAPI(
    title="Aura.AI Backend",
    description="Real-time emotional sentiment tracking across Indian cities",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_services():
    if not all([data_collector, db_manager, llm_service, rag_service]):
        raise HTTPException(status_code=503, detail="Services not initialized")
    return {
        "data_collector": data_collector,
        "db_manager": db_manager,
        "llm_service": llm_service,
        "rag_service": rag_service
    }

@app.post("/api/cities/fetch-and-save")
async def fetch_save_and_return_raw_data(services=Depends(get_services)):
    """
    Collect data + Save to DB + Return RAW content for headline generation
    """
    try:
        logger.info("Starting data collection with raw content...")
        
        # Step 1: Collect data for all cities
        cities_data = services["data_collector"].collect_all_cities_data()
        
        if not cities_data:
            raise HTTPException(status_code=500, detail="Failed to collect city data")
        
        # Step 2: Save each city's data to database
        saved_cities = []
        for city_data in cities_data:
            try:
                success = services["db_manager"].store_city_data(city_data)
                if success:
                    logger.info(f"Saved data for {city_data['city']} to database")
                    saved_cities.append(city_data['city'])
                else:
                    logger.error(f"Failed to save {city_data['city']} to database")
            except Exception as e:
                logger.error(f"Error saving {city_data.get('city', 'unknown')} to database: {e}")
        
        # Step 3: Format and return COMPLETE raw data for headline generation
        formatted_response = []
        for city_data in cities_data:
            # Extract ALL raw data exactly as collected
            raw_data = city_data.get("raw_data", {})
            news_items = raw_data.get("news", [])
            tweet_items = raw_data.get("tweets", [])
            weather_data = city_data.get("weather", {})
            
            # Return COMPLETE raw news with all fields
            complete_news = []
            for item in news_items:
                complete_news.append({
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "url": item.get("url", ""),
                    "source_name": item.get("source_name", ""),
                    "published_at": item.get("published_at", ""),
                    "sentiment_compound": item.get("sentiment_compound", 0),
                    "sentiment_positive": item.get("sentiment_positive", 0),
                    "sentiment_negative": item.get("sentiment_negative", 0),
                    "sentiment_neutral": item.get("sentiment_neutral", 0)
                })
            
            # Return COMPLETE raw tweets with all fields
            complete_tweets = []
            for item in tweet_items:
                complete_tweets.append({
                    "text": item.get("text", ""),
                    "sentiment_compound": item.get("sentiment_compound", 0),
                    "sentiment_positive": item.get("sentiment_positive", 0),
                    "sentiment_negative": item.get("sentiment_negative", 0),
                    "sentiment_neutral": item.get("sentiment_neutral", 0),
                    "created_at": item.get("created_at", ""),
                    "user_followers": item.get("user_followers", 0),
                    "retweet_count": item.get("retweet_count", 0),
                    "like_count": item.get("like_count", 0)
                })
            
            # Complete city data with ALL raw content
            formatted_city = {
                "city": city_data["city"],
                "coordinates": city_data.get("coordinates", {}),
                "weather": weather_data,
                "news": complete_news,      # ALL actual news headlines & descriptions
                "tweets": complete_tweets,  # ALL actual tweet texts
                "trending_topics": city_data.get("trending_topics", []),
                "data_counts": {
                    "news": len(complete_news),
                    "tweets": len(complete_tweets),
                    "total": len(complete_news) + len(complete_tweets)
                },
                "mood_summary": {
                    "avg_sentiment": city_data.get("mood_metrics", {}).get("avg_sentiment", 0),
                    "mood_label": city_data.get("mood_metrics", {}).get("mood_label", "No Data"),
                    "confidence": city_data.get("mood_metrics", {}).get("confidence", 0)
                },
                "timestamp": city_data.get("collection_metadata", {}).get("timestamp", datetime.now().isoformat()),
                "saved_to_db": city_data["city"] in saved_cities
            }
            formatted_response.append(formatted_city)
        
        return {
            "status": "success",
            "message": "Data collected, saved to database, raw content ready for headline generation",
            "data": formatted_response,
            "total_cities": len(formatted_response),
            "cities_saved_to_db": len(saved_cities),
            "collection_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in fetch-save-and-return operation: {e}")
        raise HTTPException(status_code=500, detail=f"Operation failed: {str(e)}")

@app.post("/api/headlines/generate-single")
async def generate_headline_single_city(
    city_data: Dict, 
    services=Depends(get_services)
):
    """
    Generate Gen-Z headline for ONE city with its raw news, tweets, weather data
    Input: Single city object with news[], tweets[], weather{}
    """
    try:
        city_name = city_data.get("city")
        if not city_name:
            raise HTTPException(status_code=400, detail="City name is required")
        
        news_items = city_data.get("news", [])
        tweet_items = city_data.get("tweets", [])
        weather_data = city_data.get("weather", {})
        trending_topics = city_data.get("trending_topics", [])
        
        # Generate headline using LLM with ALL raw content
        enhanced_headline = await services["llm_service"].generate_genz_headline_from_raw_data(
            city=city_name,
            news_items=news_items,
            tweet_items=tweet_items,
            weather=weather_data,
            trending_topics=trending_topics
        )
        
        return {
            "status": "success",
            "city": city_name,
            "enhanced_headline": enhanced_headline,
            "headline_generated_at": datetime.now().isoformat(),
            "data_used": {
                "news_count": len(news_items),
                "tweets_count": len(tweet_items),
                "weather_included": bool(weather_data),
                "trending_topics": trending_topics
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating headline for {city_data.get('city', 'unknown')}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Future Mood Forecast for single city
@app.post("/api/headlines/future_mood_forecast")
async def generate_headlines_forecast(
    request_data: Dict,
    services=Depends(get_services)
):
    """
    Predict mood for single city from the fetch-and-save response
    Input: Single city object with news[], tweets[], weather{}
    """

    try:
        city_name = request_data.get("city")
        if not city_name:
            raise HTTPException(status_code=400, detail="City name is required")
        
        news_items = request_data.get("news", [])
        tweet_items = request_data.get("tweets", [])
        weather_data = request_data.get("weather", {})
        trending_topics = request_data.get("trending_topics", [])
        
        # Generate headline using LLM with ALL raw content
        future_mood = await services["llm_service"].generate_future_mood_from_raw_data(
            city=city_name,
            news_items=news_items,
            tweet_items=tweet_items,
            weather=weather_data,
            trending_topics=trending_topics
        )
        
        return {
            "status": "success",
            "city": city_name,
            "future_mood": future_mood,
            "mood_generated_at": datetime.now().isoformat(),
            "data_used": {
                "news_count": len(news_items),
                "tweets_count": len(tweet_items),
                "weather_included": bool(weather_data),
                "trending_topics": trending_topics
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating future mood for {city_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Future Mood Forecast for multiple cities
@app.post("/api/headlines/future_mood_forecast_batch")
async def generate_headlines_forecast(
    request_data: Dict,
    services=Depends(get_services)
):
    """
    Predict mood for multiple cities from the fetch-and-save response
    Input: {"data": [city1_obj, city2_obj, ...]}
    """
    try:
        cities_data = request_data.get("data", [])
        if not cities_data:
            raise HTTPException(status_code=400, detail="No cities data provided")
        
        future_moods = []
        
        for city_info in cities_data:
            try:
                city_name = city_info.get("city")
                
                # Generate headline for this city
                future_mood = await services["llm_service"].generate_future_mood_from_raw_data(
                    city=city_name,
                    news_items=city_info.get("news", []),
                    tweet_items=city_info.get("tweets", []),
                    weather=city_info.get("weather", {}),
                    trending_topics=city_info.get("trending_topics", [])
                )
                
                future_moods.append({
                    "city": city_name,
                    "future_mood": future_mood,
                    "mood_generated_at": datetime.now().isoformat(),
                    "data_used": {
                        "news_count": len(city_info.get("news", [])),
                        "tweets_count": len(city_info.get("tweets", [])),
                        "weather_included": bool(city_info.get("weather", {})),
                        "trending_topics": city_info.get("trending_topics", [])
                    }
                })
                
            except Exception as e:
                logger.error(f"Error generating future mood for {city_name}: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        return {
            "status": "success",
            "future_moods": future_moods
        }
        
    except Exception as e:
        logger.error(f"Error generating future mood for multiple cities: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return {
            "status": "success",
            "future_moods": future_moods    
        }


@app.post("/api/headlines/generate-batch")
async def generate_headlines_batch(
    request_data: Dict,
    services=Depends(get_services)
):
    """
    Generate headlines for multiple cities from the fetch-and-save response
    Input: {"data": [city1_obj, city2_obj, ...]}
    """
    try:
        cities_data = request_data.get("data", [])
        if not cities_data:
            raise HTTPException(status_code=400, detail="No cities data provided")
        
        enhanced_cities = []
        
        for city_info in cities_data:
            try:
                city_name = city_info.get("city")
                
                # Generate headline for this city
                enhanced_headline = await services["llm_service"].generate_genz_headline_from_raw_data(
                    city=city_name,
                    news_items=city_info.get("news", []),
                    tweet_items=city_info.get("tweets", []),
                    weather=city_info.get("weather", {}),
                    trending_topics=city_info.get("trending_topics", [])
                )
                
                enhanced_city = {
                    "city": city_name,
                    "enhanced_headline": enhanced_headline,
                    "headline_generated_at": datetime.now().isoformat(),
                    "success": True,
                    "data_used": {
                        "news_count": len(city_info.get("news", [])),
                        "tweets_count": len(city_info.get("tweets", [])),
                        "trending_topics": city_info.get("trending_topics", [])
                    }
                }
                
                enhanced_cities.append(enhanced_city)
                logger.info(f"Generated headline for {city_name}: {enhanced_headline}")
                
            except Exception as e:
                logger.error(f"Failed to generate headline for {city_info.get('city', 'unknown')}: {e}")
                # Skip failed cities - no fallbacks as requested
                continue
        
        return {
            "status": "success",
            "data": enhanced_cities,
            "successful_generations": len(enhanced_cities),
            "generation_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in batch headline generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cities/mood")
async def get_latest_mood_data(services=Depends(get_services)):
    """Get latest mood data from database"""
    try:
        cities_data = services["db_manager"].get_latest_cities_data()
        
        if not cities_data:
            return {
                "status": "no_data",
                "message": "No city data found. Use /api/cities/fetch-and-save first.",
                "data": []
            }
        
        return {
            "status": "success",
            "data": cities_data,
            "count": len(cities_data)
        }
        
    except Exception as e:
        logger.error(f"Error fetching latest mood data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mood/archive")
async def query_mood_archive(query_request: dict, services=Depends(get_services)):
    """Query mood archive using RAG"""
    try:
        if not query_request.get('query', '').strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        response = await services["rag_service"].query_mood_archive(
            query=query_request['query'],
            limit=query_request.get('limit', 10),
            city_filter=query_request.get('city_filter'),
            date_range=query_request.get('date_range')
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error querying mood archive: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Aura.AI Backend with Raw Data Processing",
        "timestamp": datetime.now().isoformat(),
        "services_initialized": all([data_collector, db_manager, llm_service, rag_service]),
        "endpoints": {
            "collect_raw_data": "POST /api/cities/fetch-and-save",
            "generate_single_headline": "POST /api/headlines/generate-single", 
            "generate_batch_headlines": "POST /api/headlines/generate-batch",
            "latest_mood": "GET /api/cities/mood",
            "rag_query": "POST /api/mood/archive"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)