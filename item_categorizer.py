import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class ItemCategorizer:
    def __init__(self):
        self.categories = {
            'Fruits': [
                'apple', 'banana', 'orange', 'grape', 'strawberry', 'blueberry', 'raspberry',
                'pear', 'peach', 'plum', 'cherry', 'kiwi', 'mango', 'pineapple', 'watermelon',
                'cantaloupe', 'honeydew', 'lemon', 'lime', 'grapefruit', 'avocado', 'berry',
                'fruit', 'citrus'
            ],
            'Vegetables': [
                'carrot', 'broccoli', 'spinach', 'lettuce', 'tomato', 'cucumber', 'pepper',
                'onion', 'garlic', 'potato', 'sweet potato', 'corn', 'peas', 'beans',
                'celery', 'cabbage', 'cauliflower', 'zucchini', 'squash', 'eggplant',
                'mushroom', 'asparagus', 'artichoke', 'vegetable', 'veggie', 'salad'
            ],
            'Dairy': [
                'milk', 'cheese', 'yogurt', 'butter', 'cream', 'sour cream', 'cottage cheese',
                'cream cheese', 'mozzarella', 'cheddar', 'swiss', 'parmesan', 'dairy',
                'ice cream', 'frozen yogurt', 'whipped cream'
            ],
            'Meat': [
                'chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna', 'shrimp',
                'bacon', 'ham', 'sausage', 'ground beef', 'steak', 'roast', 'meat',
                'poultry', 'seafood', 'deli', 'lunch meat'
            ],
            'Bakery': [
                'bread', 'bagel', 'muffin', 'croissant', 'cake', 'cookie', 'pie',
                'donut', 'pastry', 'roll', 'baguette', 'loaf', 'bakery', 'baked'
            ],
            'Beverages': [
                'water', 'juice', 'soda', 'coffee', 'tea', 'beer', 'wine', 'energy drink',
                'sports drink', 'lemonade', 'beverage', 'drink', 'cola', 'sprite',
                'pepsi', 'coca cola', 'alcohol'
            ],
            'Snacks': [
                'chips', 'crackers', 'nuts', 'pretzels', 'popcorn', 'candy', 'chocolate',
                'granola bar', 'trail mix', 'cookies', 'snack', 'treats'
            ],
            'Frozen': [
                'frozen', 'ice cream', 'frozen pizza', 'frozen vegetables', 'frozen fruit',
                'frozen dinner', 'frozen meal', 'popsicle', 'frozen foods'
            ],
            'Canned': [
                'canned', 'can', 'soup', 'beans', 'tomatoes', 'corn', 'peas',
                'tuna', 'salmon', 'sauce', 'paste', 'broth', 'stock'
            ]
        }
        
        # Build keyword mappings
        self.keyword_to_category = {}
        for category, keywords in self.categories.items():
            for keyword in keywords:
                self.keyword_to_category[keyword.lower()] = category
    
    def categorize_item(self, item_name):
        """Categorize a grocery item based on its name"""
        if not item_name:
            return 'Other'
        
        item_lower = item_name.lower()
        
        # Direct keyword matching
        for keyword, category in self.keyword_to_category.items():
            if keyword in item_lower:
                return category
        
        # Fuzzy matching for partial words
        for category, keywords in self.categories.items():
            for keyword in keywords:
                # Check if keyword is part of any word in the item name
                item_words = re.findall(r'\b\w+\b', item_lower)
                for word in item_words:
                    if keyword in word or word in keyword:
                        if len(word) > 2 and len(keyword) > 2:  # Avoid very short matches
                            return category
        
        # Special rules for common patterns
        if re.search(r'\b(organic|fresh|raw)\b', item_lower):
            if any(veg in item_lower for veg in ['salad', 'greens', 'mix']):
                return 'Vegetables'
            if any(fruit in item_lower for fruit in ['apple', 'berry', 'fruit']):
                return 'Fruits'
        
        if re.search(r'\b(ground|lean|boneless)\b', item_lower):
            return 'Meat'
        
        if re.search(r'\b(whole|skim|2%|1%)\s*milk\b', item_lower):
            return 'Dairy'
        
        if re.search(r'\b(wheat|white|grain)\s*bread\b', item_lower):
            return 'Bakery'
        
        return 'Other'
    
    def get_category_suggestions(self, item_name):
        """Get possible category suggestions for an item"""
        suggestions = []
        item_lower = item_name.lower()
        
        # Score each category
        category_scores = {}
        for category, keywords in self.categories.items():
            score = 0
            for keyword in keywords:
                if keyword in item_lower:
                    score += len(keyword)  # Longer matches get higher scores
            if score > 0:
                category_scores[category] = score
        
        # Return top 3 categories by score
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, score in sorted_categories[:3]]
    
    def add_custom_mapping(self, item_name, category):
        """Add a custom item-to-category mapping"""
        # This could be extended to save custom mappings to a file or database
        pass
    
    def get_all_categories(self):
        """Get list of all available categories"""
        return list(self.categories.keys()) + ['Other']
