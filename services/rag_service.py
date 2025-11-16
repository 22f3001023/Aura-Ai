# services/rag_service.py
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from services.database import DatabaseManager

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
    async def query_mood_archive(
        self, 
        query: str, 
        limit: int = 10, 
        city_filter: Optional[str] = None,
        date_range: Optional[int] = None
    ) -> Dict:
        """Query mood archive using RAG approach"""
        try:
            search_results = self.db_manager.search_content_by_query(
                query=query,
                city_filter=city_filter,
                limit=limit * 2
            )
            
            if not search_results:
                return {
                    'query': query,
                    'found_results': False,
                    'message': f"No historical data found matching '{query}'",
                    'suggestions': self._generate_query_suggestions(query),
                    'timestamp': datetime.now().isoformat()
                }
            
            processed_results = self._process_search_results(search_results, query)
            summary = self._generate_summary(processed_results, query, city_filter)
            
            return {
                'query': query,
                'found_results': True,
                'summary': summary,
                'results_count': len(processed_results),
                'results': processed_results[:limit],
                'cities_mentioned': list(set([r['city'] for r in processed_results])),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return {
                'query': query,
                'found_results': False,
                'message': "Search temporarily unavailable",
                'timestamp': datetime.now().isoformat()
            }
    
    def _process_search_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Process and rank search results"""
        processed = []
        query_terms = query.lower().split()
        
        for result in results:
            for content in result['matching_content']:
                text = content['text'].lower()
                relevance_score = sum(1 for term in query_terms if term in text)
                
                processed.append({
                    'city': result['city'],
                    'timestamp': result['timestamp'],
                    'content_type': content['type'],
                    'text': content['text'],
                    'sentiment': content['sentiment'],
                    'relevance_score': relevance_score
                })
        
        processed.sort(key=lambda x: (x['relevance_score'], x['timestamp']), reverse=True)
        return processed
    
    def _generate_summary(self, results: List[Dict], query: str, city_filter: Optional[str]) -> str:
        """Generate summary of search results"""
        if not results:
            return f"No relevant information found for '{query}'"
        
        sentiments = [r['sentiment'] for r in results]
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        news_count = len([r for r in results if r['content_type'] == 'news'])
        tweet_count = len([r for r in results if r['content_type'] == 'tweets'])
        cities = list(set([r['city'] for r in results]))
        
        sentiment_desc = "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "mixed"
        
        if city_filter:
            summary = f"Found {len(results)} mentions of '{query}' in {city_filter}. "
        else:
            summary = f"Found {len(results)} mentions of '{query}' across {len(cities)} cities. "
        
        summary += f"Overall sentiment is {sentiment_desc} ({avg_sentiment:.2f}). "
        summary += f"Sources: {news_count} news articles, {tweet_count} social media posts."
        
        return summary
    
    def _generate_query_suggestions(self, query: str) -> List[str]:
        """Generate query suggestions"""
        common_topics = [
            "weather", "traffic", "festivals", "food", "monsoon", "pollution",
            "events", "culture", "business", "technology", "startup"
        ]
        
        return [topic for topic in common_topics if topic not in query.lower()][:5]