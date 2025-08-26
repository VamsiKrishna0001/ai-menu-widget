from fastapi import APIRouter, HTTPException, Depends, Request
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas.food_item import (
    FoodItemRequest, 
    FoodItemResponse
)
from models.food_item_manager import FoodItemManager
from utils.openai_client import openai_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize the food item manager
food_manager = FoodItemManager()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def get_food_manager() -> FoodItemManager:
    """Dependency to get the food item manager instance"""
    return food_manager

@router.post("/generate-description", response_model=FoodItemResponse)
@limiter.limit("5/minute")
async def generate_food_description(
    request: Request,
    manager: FoodItemManager = Depends(get_food_manager)
):
    """
    Generate a description and upsell message for a food item based on the model selection.
    - **name**: Name of the food item (validated and sanitized)
    - **model**: Model selection (A or B) for description generation
    """
    try:
        # Parse request body manually
        body = await request.json()
        food_request = FoodItemRequest(**body)
        
        logger.info(f"Generating description for: {food_request.name} with model {food_request.model}")
        
        # Check cache first
        cached_result = manager.get_cached_description(food_request.name, food_request.model)
        if cached_result:
            logger.info(f"Cache hit for: {food_request.name} with model {food_request.model}")
            description, upsell = cached_result
            return FoodItemResponse(
                name=food_request.name,
                model=food_request.model,
                description=description,
                upsell=upsell,
                success=True
            )
        
        # Generate new description using OpenAI client
        description, upsell = await openai_client.generate_food_description(
            food_name=food_request.name,
            model_type=food_request.model
        )
        # Store the generated description
        manager.store_generated_description(food_request, description, upsell)
        
        logger.info(f"Successfully generated description for: {food_request.name}")
        
        return FoodItemResponse(
            name=food_request.name,
            model=food_request.model,
            description=description,
            upsell=upsell,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error generating description: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating description: {str(e)}"
        )

@router.post("/regenerate-description", response_model=FoodItemResponse)
@limiter.limit("5/minute")
async def regenerate_food_description(
    request: Request,
    manager: FoodItemManager = Depends(get_food_manager)
):
    """
    Regenerate a description and upsell message for a food item.
    This will create a new generation attempt even if one already exists.
    
    - **name**: Name of the food item (validated and sanitized)
    - **model**: Model selection (gpt-3.5 or gpt-4.1-mini) for description generation
    """
    try:
        # Parse request body manually
        body = await request.json()
        food_request = FoodItemRequest(**body)
        
        logger.info(f"Regenerating description for: {food_request.name} with model {food_request.model}")
        
        # Always generate new description using OpenAI client (no cache check for regeneration)
        description, upsell = await openai_client.generate_food_description(
            food_name=food_request.name,
            model_type=food_request.model
        )
        
        # Store the regenerated description
        manager.store_generated_description(food_request, description, upsell)
        
        logger.info(f"Successfully regenerated description for: {food_request.name}")
        
        return FoodItemResponse(
            name=food_request.name,
            model=food_request.model,
            description=description,
            upsell=upsell,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error regenerating description: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error regenerating description: {str(e)}"
        )
