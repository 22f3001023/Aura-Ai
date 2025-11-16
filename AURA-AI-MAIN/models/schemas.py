

# # models/schemas.py
# from pydantic import BaseModel, Field
# from typing import List, Dict, Optional
# from datetime import datetime

# class MoodMetrics(BaseModel):
#     avg_sentiment: float
#     mood_label: str
#     mood_emoji: str
#     color_value: int
#     confidence: float
#     sample_size: int

# class CityMoodResponse(BaseModel):
#     city: str
#     timestamp: str
#     headline: str
#     mood_metrics: MoodMetrics
#     weather: Dict
#     coordinates: Dict

# class RefreshResponse(BaseModel):
#     status: str
#     message: str
#     estimated_completion: datetime
#     last_update: Optional[datetime]

# class RAGQueryRequest(BaseModel):
#     query: str = Field(..., min_length=3)
#     limit: int = Field(default=10, ge=1, le=50)
#     city_filter: Optional[str] = None
#     date_range: Optional[int] = None

# class RAGQueryResponse(BaseModel):
#     query: str
#     found_results: bool
#     summary: Optional[str] = None
#     results_count: int = 0
#     results: List[Dict] = []
#     timestamp: str

# class HealthResponse(BaseModel):
#     status: str
#     message: str
#     timestamp: datetime
#     services_initialized: bool


# models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class MoodMetrics(BaseModel):
    avg_sentiment: float
    mood_label: str
    mood_emoji: str
    color_value: int
    confidence: float
    sample_size: int

class CityMoodResponse(BaseModel):
    city: str
    timestamp: str
    headline: str
    mood_metrics: MoodMetrics
    weather: Dict
    coordinates: Dict

class RefreshResponse(BaseModel):
    status: str
    message: str
    estimated_completion: datetime
    last_update: Optional[datetime] = None

class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=3)
    limit: int = Field(default=10, ge=1, le=50)
    city_filter: Optional[str] = None
    date_range: Optional[int] = None

class RAGQueryResponse(BaseModel):
    query: str
    found_results: bool
    summary: Optional[str] = None
    results_count: int = 0
    results: List[Dict] = []
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime
    services_initialized: bool

# New schemas for your updated main.py
class HeadlineRequest(BaseModel):
    city: str
    weather: Dict[str, Any]
    mood_metrics: Dict[str, Any]
    trending_topics: List[str]
    news_count: int
    tweet_count: int

class HeadlineResponse(BaseModel):
    city: str
    headline: str
    mood: str
    sentiment: float
    weather: Dict[str, Any]
    temperature: float
    trending_topics: List[str]

class DataCollectionResponse(BaseModel):
    status: str
    message: str
    estimated_completion: Optional[datetime] = None
    last_update: Optional[datetime] = None
    data_available_at: Optional[str] = None

class LatestDataResponse(BaseModel):
    collection_time: datetime
    cities_count: int
    data: List[Dict[str, Any]]

class DataStatusResponse(BaseModel):
    update_in_progress: bool
    last_update: Optional[datetime] = None
    latest_data_available: bool
    cities_in_latest_data: int
    services_healthy: bool

class HeadlineGenerationResponse(BaseModel):
    status: str
    message: str
    cities_count: int
    estimated_completion: datetime

class LatestHeadlinesResponse(BaseModel):
    generated_at: datetime
    headlines: List[HeadlineResponse]

class AnalyticsSummaryResponse(BaseModel):
    total_cities: int
    total_records: int
    avg_sentiment: float
    most_common_mood: str
    mood_distribution: Dict[str, int]
    data_collection_stats: Dict[str, Any]
    last_updated: datetime

class CityData(BaseModel):
    city: str
    timestamp: str
    mood_metrics: MoodMetrics
    weather: Dict[str, Any]
    coordinates: Dict[str, float]
    trending_topics: List[str]
    data_counts: Dict[str, int]
    generated_headline: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime