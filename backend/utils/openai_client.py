import os
import logging
from typing import Tuple
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIClient:
    """OpenAI client for AI-powered food item description generation"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
        
        # Model configurations
        self.models = {
            "gpt-3.5-turbo": {
                "name": "gpt-3.5-turbo",
                "max_tokens": 500,
                "temperature": 0.7,
                "style": "light and fresh"
            },
            "gpt-4.1-mini": {
                "name": "gpt-4.1-mini",
                "max_tokens": 800,
                "temperature": 0.8,
                "style": "sophisticated and detailed"
            }
        }
    
    def is_available(self) -> bool:
        """Check if OpenAI client is properly configured"""
        return self.client is not None and self.api_key is not None
    
    async def generate_food_description(
        self, 
        food_name: str, 
        model_type: str = "gpt-3.5"
    ) -> Tuple[str, str]:
        """
        Generate food description and upsell suggestions using OpenAI
        
        Args:
            food_name: Name of the food item
            model_type: Model type ('gpt-3.5-turbo' or 'gpt-4.1-mini')
            
        Returns:
            Tuple of (description, upsell_suggestions)
        """
        if not self.is_available():
            logger.warning("OpenAI client not available, using fallback generation")
            return self._fallback_generation(food_name, model_type)
        
        if model_type not in self.models:
            logger.warning(f"Unknown model type: {model_type}, falling back to gpt-3.5-turbo")
            model_type = "gpt-3.5-turbo"
        
        model_config = self.models[model_type]
        
        try:
            # Create system prompt
            system_prompt = f"""You are a professional AI food menu assistant and restaurant marketing expert. 
            Generate compelling descriptions and upsell messages for food items.
            Your Tasks:
            1. Generate a SHORT, catchy description (max 30 words).
                - Use engaging, food-friendly language.
                - Use sensory language (taste, smell, texture)
                - Style should be similar to professional menus (crispy, juicy, tender, spicy, etc.).
                - Do NOT exceed 30 words.
                - Include premium ingredients and preparation methods
            2. Suggest ONE upsell item (a side, drink, or dessert that pairs well).
                - suggest pairings or enhancements
                - Keep it short, fun, and appealing.
            """
            
            # Create user prompt
            user_prompt = f"""Please create a description and upsell suggestions for: {food_name}
            
            Format your response as:
            DESCRIPTION: [your description here]
            UPSELL: [your upsell message here]"""
            
            # Make API call
            response = self.client.chat.completions.create(
                model=model_config["name"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=model_config["max_tokens"],
                temperature=model_config["temperature"]
            )
            
            # Parse response
            content = response.choices[0].message.content
            description, upsell = self._parse_openai_response(content)
            
            logger.info(f"Successfully generated description for {food_name} using {model_type}")
            return description, upsell
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            logger.info("Falling back to template-based generation")
            return self._fallback_generation(food_name, model_type)
    
    def _parse_openai_response(self, content: str) -> Tuple[str, str]:
        """Parse OpenAI response to extract description and upsell"""
        try:
            lines = content.split('\n')
            description = ""
            upsell = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("DESCRIPTION:"):
                    description = line.replace("DESCRIPTION:", "").strip()
                elif line.startswith("UPSELL:"):
                    upsell = line.replace("UPSELL:", "").strip()
            
            # Fallback parsing if format is different
            if not description or not upsell:
                parts = content.split("UPSELL:")
                if len(parts) == 2:
                    description = parts[0].replace("DESCRIPTION:", "").strip()
                    upsell = parts[1].strip()
                else:
                    # If parsing fails, split content in half
                    mid = len(content) // 2
                    description = content[:mid].strip()
                    upsell = content[mid:].strip()
            
            return description, upsell
            
        except Exception as e:
            logger.error(f"Error parsing OpenAI response: {str(e)}")
            # Return fallback if parsing fails
            return self._fallback_generation("food item", "gpt-3.5")
    
    def _fallback_generation(self, food_name: str, model_type: str) -> Tuple[str, str]:
        """Fallback generation when OpenAI is not available"""
        if model_type == "gpt-3.5-turbo":
            description = f"A delightful {food_name} that brings light and freshness to your palate. "
            description += "This carefully crafted dish features premium ingredients and a balanced flavor profile "
            description += "that will brighten your dining experience."
            
            upsell = f"Pair your {food_name} with our signature house salad and a refreshing beverage "
            upsell += "for the perfect light meal combination!"
            
        else:  # gpt-4.1-mini
            description = f"An exquisite {food_name} with deep, rich flavors that create a sophisticated dining experience. "
            description += "This premium dish showcases complex taste profiles and elegant presentation, "
            description += "perfect for those who appreciate bold culinary artistry."
            
            upsell = f"Enhance your {food_name} experience with our premium wine pairing recommendations "
            upsell += "and decadent dessert selection for a truly memorable dining journey!"
        
        return description, upsell

openai_client = OpenAIClient()
