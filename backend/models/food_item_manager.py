from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import os
import uuid
from schemas.food_item import FoodItemHistory, FoodItemCache, FoodItemRequest, FoodItemResponse

class FoodItemManager:
    """Manages food item data storage, caching, and retrieval"""
    
    def __init__(self, storage_file: str = "food_items_data.json", cache_file: str = "food_items_cache.json"):
        self.storage_file = storage_file
        self.cache_file = cache_file
        self.storage: Dict[str, FoodItemHistory] = {}
        self.cache: Dict[str, FoodItemCache] = {}
        self._load_data()
    
    def _load_data(self):
        """Load existing data from storage files"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item_data in data.values():
                        # Convert string timestamps back to datetime objects
                        item_data['created_at'] = datetime.fromisoformat(item_data['created_at'])
                        self.storage[item_data['name']] = FoodItemHistory(**item_data)
        except Exception as e:
            print(f"Warning: Could not load storage data: {e}")
            self.storage = {}
        
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item_data in data.values():
                        # Convert string timestamps back to datetime objects
                        item_data['last_accessed'] = datetime.fromisoformat(item_data['last_accessed'])
                        self.cache[item_data['name']] = FoodItemCache(**item_data)
        except Exception as e:
            print(f"Warning: Could not load cache data: {e}")
            self.cache = {}
    
    def _save_data(self):
        """Save data to storage files"""
        try:
            # Save storage data
            storage_data = {}
            for name, history_list in self.storage.items():
                storage_data[name] = []
                for item in history_list:  # iterate through FoodItemHistory objects
                    item_dict = item.model_dump()
                    item_dict['created_at'] = item.created_at.isoformat()
                    storage_data[name].append(item_dict)
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, indent=2, ensure_ascii=False)
            
            # Save cache data
            cache_data = {}
            for name, item in self.cache.items():
                item_dict = item.model_dump()
                item_dict['last_accessed'] = item.last_accessed.isoformat()
                cache_data[name] = item_dict
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_cached_description(self, name: str, model: str) -> Optional[Tuple[str, str]]:
        """
        Get cached description and upsell for a food item
        
        Returns:
            Tuple of (description, upsell) if found, None otherwise
        """
        cache_key = f"{name}_{model}"
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            print(f"Cached item: {cached_item}")
            # Update access count and timestamp
            cached_item.access_count += 1
            cached_item.last_accessed = datetime.utcnow()
            self._save_data()
            return cached_item.description, cached_item.upsell
        return None
    
    def store_generated_description(self, request: FoodItemRequest, description: str, upsell: str):
        """Store a newly generated description, handling regeneration"""
        # Generate unique ID for this generation attempt
        id = str(uuid.uuid4())
        
        # Create history item
        history_item = FoodItemHistory(
            id=id,
            name=request.name,
            model=request.model,
            description=description,
            upsell=upsell
        )
        
        # Store in main storage - append to list if multiple generations exist
        if request.name not in self.storage:
            self.storage[request.name] = []
        self.storage[request.name].append(history_item)
        
        # Update cache with latest version
        cache_key = f"{request.name}_{request.model}"
        cache_item = FoodItemCache(
            id=id,
            name=request.name,
            model=request.model,
            description=description,
            upsell=upsell
        )
        self.cache[cache_key] = cache_item
        
        self._save_data()
    
