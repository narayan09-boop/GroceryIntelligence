import re
from data.nutritional_data import NUTRITIONAL_DATABASE

class NutritionAnalyzer:
    def __init__(self):
        self.nutritional_db = NUTRITIONAL_DATABASE
        
        # Nutrition scoring weights
        self.scoring_weights = {
            'fruits': 9,
            'vegetables': 9,
            'whole_grains': 8,
            'lean_protein': 8,
            'dairy': 6,
            'nuts_seeds': 7,
            'processed_foods': 3,
            'sugary_drinks': 2,
            'candy_sweets': 2,
            'fast_food': 2
        }
    
    def get_nutrition_score(self, item_name):
        """Get nutrition score for an item (1-10 scale, 10 being healthiest)"""
        if not item_name:
            return 5
        
        item_lower = item_name.lower()
        
        # Check direct matches in nutritional database
        if item_lower in self.nutritional_db:
            return self.nutritional_db[item_lower]['score']
        
        # Fuzzy matching for similar items
        for db_item, data in self.nutritional_db.items():
            if self._items_similar(item_lower, db_item):
                return data['score']
        
        # Category-based scoring
        return self._score_by_category(item_lower)
    
    def _items_similar(self, item1, item2):
        """Check if two items are similar enough for nutrition scoring"""
        # Simple similarity check - could be enhanced with fuzzy string matching
        words1 = set(re.findall(r'\b\w+\b', item1))
        words2 = set(re.findall(r'\b\w+\b', item2))
        
        # If they share significant words
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if len(union) == 0:
            return False
        
        similarity = len(intersection) / len(union)
        return similarity > 0.5
    
    def _score_by_category(self, item_name):
        """Score item based on food category patterns"""
        # Healthy foods (score 8-10)
        if any(pattern in item_name for pattern in [
            'apple', 'banana', 'orange', 'berry', 'grape', 'kiwi', 'mango',
            'broccoli', 'spinach', 'kale', 'carrot', 'pepper', 'tomato',
            'quinoa', 'brown rice', 'oats', 'whole wheat', 'whole grain',
            'salmon', 'tuna', 'chicken breast', 'turkey', 'tofu',
            'almond', 'walnut', 'chia', 'flax'
        ]):
            return 9
        
        # Moderately healthy (score 6-7)
        if any(pattern in item_name for pattern in [
            'milk', 'yogurt', 'cheese', 'egg', 'pasta', 'rice', 'potato',
            'bread', 'cereal', 'legume', 'bean'
        ]):
            return 6
        
        # Less healthy (score 3-5)
        if any(pattern in item_name for pattern in [
            'bacon', 'sausage', 'hot dog', 'pizza', 'burger',
            'french fries', 'chip', 'cracker', 'cookie'
        ]):
            return 4
        
        # Unhealthy (score 1-2)
        if any(pattern in item_name for pattern in [
            'soda', 'candy', 'chocolate', 'ice cream', 'donut',
            'energy drink', 'alcohol', 'beer', 'wine'
        ]):
            return 2
        
        # Default score for unrecognized items
        return 5
    
    def get_nutritional_info(self, item_name):
        """Get detailed nutritional information for an item"""
        item_lower = item_name.lower()
        
        if item_lower in self.nutritional_db:
            return self.nutritional_db[item_lower]
        
        # Return basic info for unknown items
        return {
            'score': self.get_nutrition_score(item_name),
            'category': 'Unknown',
            'benefits': ['Nutritional information not available'],
            'concerns': []
        }
    
    def analyze_shopping_patterns(self, items_df):
        """Analyze overall nutritional patterns in shopping"""
        if items_df.empty:
            return {}
        
        analysis = {
            'average_score': items_df['nutrition_score'].mean(),
            'healthy_items': len(items_df[items_df['nutrition_score'] >= 7]),
            'unhealthy_items': len(items_df[items_df['nutrition_score'] <= 4]),
            'total_items': len(items_df)
        }
        
        # Category breakdown
        category_scores = items_df.groupby('category')['nutrition_score'].mean().to_dict()
        analysis['category_scores'] = category_scores
        
        return analysis
    
    def get_recommendations(self, items_df):
        """Get personalized nutrition recommendations"""
        if items_df.empty:
            return []
        
        recommendations = []
        
        # Analyze current patterns
        avg_score = items_df['nutrition_score'].mean()
        category_counts = items_df['category'].value_counts().to_dict()
        
        # Low overall nutrition score
        if avg_score < 6:
            recommendations.append(
                "🍎 Consider adding more fruits and vegetables to improve your overall nutrition score."
            )
        
        # Too many processed foods
        processed_categories = ['Snacks', 'Beverages', 'Frozen']
        processed_count = sum(category_counts.get(cat, 0) for cat in processed_categories)
        total_items = len(items_df)
        
        if processed_count / total_items > 0.3:
            recommendations.append(
                "🥗 Try to reduce processed foods and increase fresh produce in your shopping."
            )
        
        # Category-specific recommendations
        if category_counts.get('Fruits', 0) < 3:
            recommendations.append(
                "🍓 Add more variety of fruits to your diet for essential vitamins and fiber."
            )
        
        if category_counts.get('Vegetables', 0) < 5:
            recommendations.append(
                "🥬 Include more vegetables in your shopping for better nutrition balance."
            )
        
        # Healthy alternatives
        unhealthy_items = items_df[items_df['nutrition_score'] <= 4]
        if not unhealthy_items.empty:
            recommendations.append(
                "💡 Consider healthier alternatives for items like chips, candy, and sugary drinks."
            )
        
        return recommendations
    
    def get_health_insights(self, spending_by_category):
        """Get health insights based on spending patterns"""
        insights = []
        
        total_spending = sum(spending_by_category.values())
        if total_spending == 0:
            return insights
        
        # Calculate percentages
        percentages = {cat: (amount/total_spending)*100 for cat, amount in spending_by_category.items()}
        
        # Analyze spending on healthy vs unhealthy categories
        healthy_categories = ['Fruits', 'Vegetables', 'Dairy']
        unhealthy_categories = ['Snacks', 'Beverages']
        
        healthy_spending = sum(percentages.get(cat, 0) for cat in healthy_categories)
        unhealthy_spending = sum(percentages.get(cat, 0) for cat in unhealthy_categories)
        
        if healthy_spending > 40:
            insights.append("🎉 Great job! You're spending a good portion on healthy foods.")
        elif healthy_spending < 20:
            insights.append("⚠️ Consider allocating more budget to fruits and vegetables.")
        
        if unhealthy_spending > 25:
            insights.append("💭 You might want to reduce spending on snacks and sugary beverages.")
        
        return insights
