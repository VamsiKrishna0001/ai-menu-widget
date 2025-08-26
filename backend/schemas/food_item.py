from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class FoodItemRequest(BaseModel):
    """Request model for food item description generation"""
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Name of the food item to generate description for",
        example="Margherita Pizza"
    )
    model: str = Field(
        "gpt-3.5-turbo", 
        description="LLM model for description generation (gpt-3.5 or gpt-4.1-mini)",
        example="gpt-4.1-mini"
    )
    
    @field_validator('name')
    @classmethod
    def validate_and_sanitize_name(cls, v):
        """Validate and sanitize the food item name"""
        if not v or not v.strip():
            raise ValueError('Food item name cannot be empty')
        
        # Remove extra whitespace and normalize
        sanitized = ' '.join(v.strip().split())
        
        # Check for valid characters (letters, numbers, spaces, hyphens, apostrophes)
        if not re.match(r'^[a-zA-Z0-9\s\-\']+$', sanitized):
            raise ValueError('Food item name contains invalid characters')
        
        # Check length after sanitization
        if len(sanitized) > 100:
            raise ValueError('Food item name is too long (max 100 characters)')
        
        return sanitized
    
    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Ensure only supported models are allowed"""
        allowed = ["gpt-3.5-turbo", "gpt-4.1-mini"]
        if v not in allowed:
            raise ValueError(f"Invalid model. Allowed values: {allowed}")
        return v
    

class FoodItemResponse(BaseModel):
    """Response model for generated food item description"""
    name: str = Field(..., description="Name of the food item")
    model: str = Field(..., description="Selected model option")
    description: str = Field(..., description="Generated description for the food item")
    upsell: str = Field(..., description="Upsell message for the food item")
    success: bool = Field(..., description="Whether the generation was successful")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

class FoodItemHistory(BaseModel):
    """Model for storing food item generation history"""
    id: Optional[str] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Name of the food item")
    model: str = Field(..., description="Model used for generation")
    description: str = Field(..., description="Generated description")
    upsell: str = Field(..., description="Generated upsell message")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    usage_count: int = Field(default=1, description="Number of times this item was requested")

class FoodItemCache(BaseModel):
    """Model for caching food item descriptions"""
    id: Optional[str] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Name of the food item")
    model: str = Field(..., description="Model used for generation")
    description: str = Field(..., description="Generated description")
    upsell: str = Field(..., description="Generated upsell message")
    last_accessed: datetime = Field(default_factory=datetime.utcnow, description="Last access timestamp")
    access_count: int = Field(default=1, description="Number of times accessed")
