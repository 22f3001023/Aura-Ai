

# services/database.py
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import threading
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "aura_data.db"):
        self.db_path = db_path
        self._lock = threading.Lock()
        
        self.city_coordinates = {
            "Mumbai": {"lat": 19.0760, "lon": 72.8777},
            "Delhi": {"lat": 28.7041, "lon": 77.1025},
            "Bangalore": {"lat": 12.9716, "lon": 77.5946},
            "Chennai": {"lat": 13.0827, "lon": 80.2707},
            "Kolkata": {"lat": 22.5726, "lon": 88.3639},
            "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
            "Pune": {"lat": 18.5204, "lon": 73.8567},
            "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
            "Jaipur": {"lat": 26.9124, "lon": 75.7873},
            "Lucknow": {"lat": 26.8467, "lon": 80.9462}
        }
        
        self._init_database()
        
    def _init_database(self):
        """Initialize database with complete schema"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS city_moods (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        headline TEXT,
                        mood_data TEXT NOT NULL,
                        weather_data TEXT,
                        trending_topics TEXT,
                        raw_content TEXT,
                        sentiment_score REAL,
                        mood_label TEXT,
                        confidence REAL,
                        sample_size INTEGER,
                        data_quality TEXT,
                        collection_time REAL,
                        coordinates TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes
                conn.execute("CREATE INDEX IF NOT EXISTS idx_city_timestamp ON city_moods(city, timestamp)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON city_moods(timestamp)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_city ON city_moods(city)")
                
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Thread-safe database connection"""
        with self._lock:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise
            finally:
                conn.close()
    
    def store_city_data(self, city_data: Dict) -> bool:
        """Store complete city data in database"""
        try:
            with self.get_connection() as conn:
                coordinates = city_data.get('coordinates', self.city_coordinates.get(city_data['city'], {}))
                
                conn.execute("""
                    INSERT INTO city_moods (
                        city, timestamp, headline, mood_data, weather_data, 
                        trending_topics, raw_content, sentiment_score, mood_label, 
                        confidence, sample_size, data_quality, collection_time, coordinates
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    city_data['city'],
                    city_data['collection_metadata']['timestamp'],
                    city_data.get('headline', ''),
                    json.dumps(city_data.get('mood_metrics', {})),
                    json.dumps(city_data.get('weather', {})),
                    json.dumps(city_data.get('trending_topics', [])),
                    json.dumps(city_data.get('raw_data', {})),
                    city_data.get('mood_metrics', {}).get('avg_sentiment', 0),
                    city_data.get('mood_metrics', {}).get('mood_label', ''),
                    city_data.get('mood_metrics', {}).get('confidence', 0),
                    city_data.get('mood_metrics', {}).get('sample_size', 0),
                    city_data.get('collection_metadata', {}).get('data_quality', 'unknown'),
                    city_data.get('collection_metadata', {}).get('collection_time_seconds', 0),
                    json.dumps(coordinates)
                ))
                
            logger.info(f"Stored complete data for {city_data['city']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store data for {city_data.get('city', 'unknown')}: {e}")
            return False
    
    def get_latest_cities_data(self) -> List[Dict]:
        """Get latest mood data for all cities"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM (
                        SELECT *, ROW_NUMBER() OVER (
                            PARTITION BY city ORDER BY timestamp DESC
                        ) as rn FROM city_moods
                    ) WHERE rn = 1
                    ORDER BY city
                """)
                
                results = []
                for row in cursor.fetchall():
                    coordinates = json.loads(row['coordinates'] or '{}')
                    if not coordinates:
                        coordinates = self.city_coordinates.get(row['city'], {'lat': 0, 'lon': 0})
                    
                    city_data = {
                        'city': row['city'],
                        'timestamp': row['timestamp'],
                        'headline': row['headline'] or f"{row['city']} vibes loading...",
                        'mood_metrics': json.loads(row['mood_data']),
                        'weather': json.loads(row['weather_data'] or '{}'),
                        'trending_topics': json.loads(row['trending_topics'] or '[]'),
                        'coordinates': coordinates,
                        'confidence': row['confidence'],
                        'sample_size': row['sample_size'],
                        'data_quality': row['data_quality']
                    }
                    results.append(city_data)
                
                return results
                
        except Exception as e:
            logger.error(f"Failed to get latest cities data: {e}")
            return []
    
    def get_city_data(self, city_name: str) -> Optional[Dict]:
        """Get latest complete data for a specific city"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM city_moods 
                    WHERE city = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """, (city_name,))
                
                row = cursor.fetchone()
                if row:
                    coordinates = json.loads(row['coordinates'] or '{}')
                    if not coordinates:
                        coordinates = self.city_coordinates.get(city_name, {'lat': 0, 'lon': 0})
                    
                    return {
                        'city': row['city'],
                        'timestamp': row['timestamp'],
                        'headline': row['headline'],
                        'mood_metrics': json.loads(row['mood_data']),
                        'weather': json.loads(row['weather_data'] or '{}'),
                        'trending_topics': json.loads(row['trending_topics'] or '[]'),
                        'raw_content': json.loads(row['raw_content'] or '{}'),
                        'coordinates': coordinates,
                        'confidence': row['confidence'],
                        'sample_size': row['sample_size']
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Failed to get city data for {city_name}: {e}")
            return None
    
    def search_content_by_query(self, query: str, city_filter: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Search historical content for RAG"""
        try:
            query_parts = query.lower().split()
            
            with self.get_connection() as conn:
                base_sql = """
                    SELECT city, timestamp, raw_content, mood_data, sentiment_score, headline
                    FROM city_moods 
                    WHERE (raw_content LIKE ? OR headline LIKE ?)
                """
                
                search_term = f"%{' '.join(query_parts)}%"
                params = [search_term, search_term]
                
                if city_filter:
                    base_sql += " AND city = ?"
                    params.append(city_filter)
                
                base_sql += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(base_sql, params)
                
                results = []
                for row in cursor.fetchall():
                    raw_content = json.loads(row['raw_content'] or '{}')
                    
                    matching_content = []
                    for content_type in ['news', 'tweets']:
                        for item in raw_content.get(content_type, []):
                            text = item.get('text', '').lower()
                            if any(part in text for part in query_parts):
                                matching_content.append({
                                    'type': content_type,
                                    'text': item.get('text', ''),
                                    'sentiment': item.get('sentiment_compound', 0)
                                })
                    
                    if matching_content:
                        results.append({
                            'city': row['city'],
                            'timestamp': row['timestamp'],
                            'matching_content': matching_content,
                            'overall_sentiment': row['sentiment_score']
                        })
                
                return results
                
        except Exception as e:
            logger.error(f"Content search failed: {e}")
            return []
    
    def get_analytics_summary(self) -> Dict:
        """Get analytics summary"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) as total FROM city_moods")
                total_records = cursor.fetchone()['total']
                
                cutoff_time = (datetime.now() - timedelta(hours=24)).isoformat()
                cursor = conn.execute("""
                    SELECT 
                        AVG(sentiment_score) as avg_sentiment,
                        COUNT(*) as recent_records,
                        COUNT(DISTINCT city) as cities_tracked
                    FROM city_moods 
                    WHERE timestamp > ?
                """, (cutoff_time,))
                
                recent_stats = cursor.fetchone()
                
                cursor = conn.execute("""
                    SELECT mood_label, COUNT(*) as count
                    FROM city_moods 
                    WHERE timestamp > ?
                    GROUP BY mood_label
                """, (cutoff_time,))
                
                mood_distribution = {row['mood_label']: row['count'] for row in cursor.fetchall()}
                
                return {
                    'total_records': total_records,
                    'recent_records': recent_stats['recent_records'],
                    'cities_tracked': recent_stats['cities_tracked'],
                    'avg_sentiment_24h': round(recent_stats['avg_sentiment'] or 0, 3),
                    'mood_distribution': mood_distribution,
                    'last_updated': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get analytics summary: {e}")
            return {}
    
    def close(self):
        """Close database connections"""
        logger.info("Database connections closed")