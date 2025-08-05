"""
Market management endpoints.
Handles market creation, retrieval, and management operations.
"""

from typing import List, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from predictpesa.api.deps import get_current_user, get_db
from predictpesa.models.user import User
from predictpesa.schemas.market import (
    MarketCreate,
    MarketResponse,
    MarketUpdate,
    MarketListResponse,
    MarketStatsResponse
)
from predictpesa.services.market import MarketService
from predictpesa.services.ai import AIService

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.post("/create", response_model=MarketResponse)
async def create_market(
    market_data: MarketCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new prediction market.
    
    This endpoint allows authenticated users to create new prediction markets.
    The market will be processed by AI for validation and optimization.
    """
    logger.info(
        "Creating new market",
        user_id=current_user.id,
        title=market_data.title,
        category=market_data.category
    )
    
    # Check if user can create markets
    if not current_user.can_create_markets():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to create markets"
        )
    
    try:
        market_service = MarketService(db)
        ai_service = AIService()
        
        # Process market with AI if enabled
        if market_data.use_ai_processing:
            processed_data = await ai_service.process_market_creation(market_data)
            market_data = processed_data
        
        # Create the market
        market = await market_service.create_market(market_data, current_user.id)
        
        logger.info(
            "Market created successfully",
            market_id=market.id,
            user_id=current_user.id
        )
        
        return MarketResponse.from_orm(market)
    
    except Exception as e:
        logger.error(
            "Failed to create market",
            error=str(e),
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create market"
        )


@router.get("/", response_model=MarketListResponse)
async def list_markets(
    skip: int = Query(0, ge=0, description="Number of markets to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of markets to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    featured_only: bool = Query(False, description="Show only featured markets"),
    trending_only: bool = Query(False, description="Show only trending markets"),
    db: AsyncSession = Depends(get_db)
):
    """
    List prediction markets with filtering and pagination.
    
    Returns a paginated list of markets with optional filtering by category,
    status, and search terms.
    """
    try:
        market_service = MarketService(db)
        
        markets, total = await market_service.list_markets(
            skip=skip,
            limit=limit,
            category=category,
            status=status,
            search=search,
            featured_only=featured_only,
            trending_only=trending_only
        )
        
        return MarketListResponse(
            markets=[MarketResponse.from_orm(market) for market in markets],
            total=total,
            skip=skip,
            limit=limit
        )
    
    except Exception as e:
        logger.error("Failed to list markets", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve markets"
        )


@router.get("/{market_id}", response_model=MarketResponse)
async def get_market(
    market_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific market by ID.
    
    Returns detailed information about a single prediction market.
    """
    try:
        market_service = MarketService(db)
        market = await market_service.get_market(market_id)
        
        if not market:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Market not found"
            )
        
        return MarketResponse.from_orm(market)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get market", market_id=market_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve market"
        )


@router.put("/{market_id}", response_model=MarketResponse)
async def update_market(
    market_id: UUID,
    market_data: MarketUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a market (only by creator or admin).
    
    Allows market creators or administrators to update market details.
    """
    try:
        market_service = MarketService(db)
        market = await market_service.get_market(market_id)
        
        if not market:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Market not found"
            )
        
        # Check permissions
        if market.creator_id != current_user.id and not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this market"
            )
        
        updated_market = await market_service.update_market(market_id, market_data)
        
        logger.info(
            "Market updated",
            market_id=market_id,
            user_id=current_user.id
        )
        
        return MarketResponse.from_orm(updated_market)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update market", market_id=market_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update market"
        )


@router.delete("/{market_id}")
async def delete_market(
    market_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a market (only by creator or admin).
    
    Soft deletes a market if no stakes have been placed, otherwise cancels it.
    """
    try:
        market_service = MarketService(db)
        market = await market_service.get_market(market_id)
        
        if not market:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Market not found"
            )
        
        # Check permissions
        if market.creator_id != current_user.id and not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this market"
            )
        
        await market_service.delete_market(market_id)
        
        logger.info(
            "Market deleted",
            market_id=market_id,
            user_id=current_user.id
        )
        
        return {"message": "Market deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete market", market_id=market_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete market"
        )


@router.get("/{market_id}/stats", response_model=MarketStatsResponse)
async def get_market_stats(
    market_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed statistics for a market.
    
    Returns comprehensive statistics including stake distribution,
    participant counts, and probability calculations.
    """
    try:
        market_service = MarketService(db)
        stats = await market_service.get_market_stats(market_id)
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Market not found"
            )
        
        return stats
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get market stats", market_id=market_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve market statistics"
        )


@router.post("/{market_id}/resolve")
async def resolve_market(
    market_id: UUID,
    resolution_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Resolve a market with outcome data.
    
    Only available to market creators, oracles, or administrators.
    """
    try:
        market_service = MarketService(db)
        market = await market_service.get_market(market_id)
        
        if not market:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Market not found"
            )
        
        # Check permissions
        can_resolve = (
            market.creator_id == current_user.id or
            current_user.is_oracle() or
            current_user.is_admin()
        )
        
        if not can_resolve:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to resolve this market"
            )
        
        resolved_market = await market_service.resolve_market(
            market_id, 
            resolution_data,
            current_user.id
        )
        
        logger.info(
            "Market resolved",
            market_id=market_id,
            resolver_id=current_user.id,
            outcome=resolution_data.get("outcome")
        )
        
        return MarketResponse.from_orm(resolved_market)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to resolve market", market_id=market_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resolve market"
        )


@router.get("/trending/", response_model=List[MarketResponse])
async def get_trending_markets(
    limit: int = Query(10, ge=1, le=50, description="Number of trending markets"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get trending markets based on activity and volume.
    
    Returns markets with high recent activity and stake volume.
    """
    try:
        market_service = MarketService(db)
        trending_markets = await market_service.get_trending_markets(limit)
        
        return [MarketResponse.from_orm(market) for market in trending_markets]
    
    except Exception as e:
        logger.error("Failed to get trending markets", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve trending markets"
        )


@router.get("/featured/", response_model=List[MarketResponse])
async def get_featured_markets(
    limit: int = Query(10, ge=1, le=50, description="Number of featured markets"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get featured markets curated by administrators.
    
    Returns markets that have been marked as featured by the platform.
    """
    try:
        market_service = MarketService(db)
        featured_markets = await market_service.get_featured_markets(limit)
        
        return [MarketResponse.from_orm(market) for market in featured_markets]
    
    except Exception as e:
        logger.error("Failed to get featured markets", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve featured markets"
        )
