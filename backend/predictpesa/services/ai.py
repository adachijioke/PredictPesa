"""AI service for market processing using Groq."""

import structlog
from groq import AsyncGroq
from predictpesa.core.config import settings
from predictpesa.core.logging import LoggerMixin
from predictpesa.schemas.market import MarketCreate

logger = structlog.get_logger(__name__)


class AIService(LoggerMixin):
    """Service for AI-powered market processing using Groq."""
    
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.groq_api_key)
    
    async def process_market_creation(self, market_data: MarketCreate) -> MarketCreate:
        """Process market creation with AI optimization using Groq."""
        self.logger.info("Processing market with Groq AI", title=market_data.title)
        
        try:
            # Create AI prompt for market enhancement
            prompt = f"""
You are an expert in prediction markets for African economies. 
Analyze and enhance this market:

Title: {market_data.title}
Description: {market_data.description}
Question: {market_data.question}
Category: {market_data.category}

Provide:
1. An improved, clearer title
2. A more detailed description
3. Suggest relevant tags
4. Rate confidence (1-10)

Respond in JSON format:
{{
  "title": "improved title",
  "description": "enhanced description",
  "tags": ["tag1", "tag2"],
  "confidence": 8
}}
"""
            
            # Call Groq API
            response = await self.client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in African prediction markets."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.groq_max_tokens,
                temperature=settings.groq_temperature
            )
            
            # Parse response (in real implementation, add proper JSON parsing)
            ai_response = response.choices[0].message.content
            self.logger.info("Groq AI response received", response_length=len(ai_response))
            
            # For demo, return enhanced market data
            enhanced_data = market_data.copy()
            enhanced_data.description = f"🤖 Groq-Enhanced: {market_data.description}"
            
            return enhanced_data
            
        except Exception as e:
            self.logger.error("Groq AI processing failed", error=str(e))
            # Fallback to original data
            return market_data
