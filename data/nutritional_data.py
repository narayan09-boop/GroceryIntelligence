"""
Nutritional database with scoring and information for common grocery items.
Score scale: 1-10 (10 being the healthiest)
"""

NUTRITIONAL_DATABASE = {
    # Fruits (High nutrition scores: 8-10)
    'apple': {
        'score': 9,
        'category': 'Fruit',
        'benefits': ['High in fiber', 'Rich in vitamin C', 'Contains antioxidants'],
        'concerns': []
    },
    'banana': {
        'score': 8,
        'category': 'Fruit',
        'benefits': ['High in potassium', 'Good source of vitamin B6', 'Natural energy'],
        'concerns': ['Higher in sugar than some fruits']
    },
    'orange': {
        'score': 9,
        'category': 'Fruit',
        'benefits': ['Excellent vitamin C source', 'High fiber', 'Folate'],
        'concerns': []
    },
    'strawberry': {
        'score': 9,
        'category': 'Fruit',
        'benefits': ['Very high vitamin C', 'Antioxidants', 'Low calories'],
        'concerns': []
    },
    'blueberry': {
        'score': 10,
        'category': 'Fruit',
        'benefits': ['Highest antioxidant content', 'Brain health', 'Anti-inflammatory'],
        'concerns': []
    },
    'avocado': {
        'score': 9,
        'category': 'Fruit',
        'benefits': ['Healthy fats', 'High fiber', 'Potassium'],
        'concerns': ['High calorie density']
    },
    
    # Vegetables (High nutrition scores: 8-10)
    'broccoli': {
        'score': 10,
        'category': 'Vegetable',
        'benefits': ['Vitamin K, C, folate', 'Fiber', 'Cancer-fighting compounds'],
        'concerns': []
    },
    'spinach': {
        'score': 10,
        'category': 'Vegetable',
        'benefits': ['Iron', 'Vitamin K', 'Folate', 'Very low calories'],
        'concerns': []
    },
    'kale': {
        'score': 10,
        'category': 'Vegetable',
        'benefits': ['Vitamin A, C, K', 'Calcium', 'Antioxidants'],
        'concerns': []
    },
    'carrot': {
        'score': 8,
        'category': 'Vegetable',
        'benefits': ['Beta-carotene', 'Vitamin A', 'Fiber'],
        'concerns': []
    },
    'bell pepper': {
        'score': 9,
        'category': 'Vegetable',
        'benefits': ['Vitamin C', 'Vitamin A', 'Low calories'],
        'concerns': []
    },
    'tomato': {
        'score': 8,
        'category': 'Vegetable',
        'benefits': ['Lycopene', 'Vitamin C', 'Potassium'],
        'concerns': []
    },
    'cucumber': {
        'score': 7,
        'category': 'Vegetable',
        'benefits': ['Hydrating', 'Low calories', 'Vitamin K'],
        'concerns': ['Lower nutrient density']
    },
    'lettuce': {
        'score': 7,
        'category': 'Vegetable',
        'benefits': ['Low calories', 'Vitamin K', 'Folate'],
        'concerns': ['Lower nutrient density than dark greens']
    },
    
    # Proteins (Moderate to high scores: 6-9)
    'chicken breast': {
        'score': 8,
        'category': 'Protein',
        'benefits': ['Lean protein', 'B vitamins', 'Low saturated fat'],
        'concerns': []
    },
    'salmon': {
        'score': 9,
        'category': 'Protein',
        'benefits': ['Omega-3 fatty acids', 'High quality protein', 'Vitamin D'],
        'concerns': ['Can be high in mercury if farm-raised']
    },
    'tuna': {
        'score': 8,
        'category': 'Protein',
        'benefits': ['Lean protein', 'Omega-3s', 'Selenium'],
        'concerns': ['Mercury content']
    },
    'eggs': {
        'score': 8,
        'category': 'Protein',
        'benefits': ['Complete protein', 'Choline', 'Vitamin D'],
        'concerns': ['Cholesterol content']
    },
    'tofu': {
        'score': 7,
        'category': 'Protein',
        'benefits': ['Plant protein', 'Isoflavones', 'Low saturated fat'],
        'concerns': ['Processed food']
    },
    'ground beef': {
        'score': 5,
        'category': 'Protein',
        'benefits': ['High protein', 'Iron', 'B vitamins'],
        'concerns': ['High saturated fat', 'Calories', 'Processing']
    },
    'bacon': {
        'score': 3,
        'category': 'Protein',
        'benefits': ['Protein'],
        'concerns': ['Very high sodium', 'High saturated fat', 'Processed meat', 'Nitrates']
    },
    'hot dog': {
        'score': 2,
        'category': 'Protein',
        'benefits': ['Protein'],
        'concerns': ['Highly processed', 'High sodium', 'Preservatives', 'Low quality meat']
    },
    
    # Dairy (Moderate scores: 5-7)
    'milk': {
        'score': 6,
        'category': 'Dairy',
        'benefits': ['Calcium', 'Protein', 'Vitamin D'],
        'concerns': ['Saturated fat (whole milk)', 'Lactose']
    },
    'yogurt': {
        'score': 7,
        'category': 'Dairy',
        'benefits': ['Probiotics', 'Protein', 'Calcium'],
        'concerns': ['Added sugars in flavored varieties']
    },
    'cheese': {
        'score': 5,
        'category': 'Dairy',
        'benefits': ['Calcium', 'Protein'],
        'concerns': ['High saturated fat', 'High sodium', 'Calories']
    },
    'butter': {
        'score': 3,
        'category': 'Dairy',
        'benefits': ['Vitamin A'],
        'concerns': ['Very high saturated fat', 'High calories', 'Low nutrients']
    },
    'ice cream': {
        'score': 2,
        'category': 'Dairy',
        'benefits': ['Calcium'],
        'concerns': ['High sugar', 'High saturated fat', 'High calories', 'Low nutrients']
    },
    
    # Grains and Starches (Variable scores: 4-8)
    'brown rice': {
        'score': 7,
        'category': 'Grain',
        'benefits': ['Whole grain', 'Fiber', 'B vitamins'],
        'concerns': []
    },
    'white rice': {
        'score': 5,
        'category': 'Grain',
        'benefits': ['Energy', 'Some B vitamins'],
        'concerns': ['Refined grain', 'Low fiber', 'High glycemic index']
    },
    'quinoa': {
        'score': 8,
        'category': 'Grain',
        'benefits': ['Complete protein', 'Fiber', 'Minerals'],
        'concerns': []
    },
    'oats': {
        'score': 8,
        'category': 'Grain',
        'benefits': ['Soluble fiber', 'Beta-glucan', 'Protein'],
        'concerns': []
    },
    'whole wheat bread': {
        'score': 6,
        'category': 'Grain',
        'benefits': ['Fiber', 'B vitamins', 'Iron'],
        'concerns': ['Gluten', 'Some processing']
    },
    'white bread': {
        'score': 4,
        'category': 'Grain',
        'benefits': ['Fortified with vitamins'],
        'concerns': ['Refined flour', 'Low fiber', 'High glycemic index', 'Added sugars']
    },
    'pasta': {
        'score': 5,
        'category': 'Grain',
        'benefits': ['Energy', 'Some B vitamins'],
        'concerns': ['Refined carbs (unless whole grain)', 'High glycemic index']
    },
    
    # Processed/Packaged Foods (Low scores: 2-5)
    'chips': {
        'score': 2,
        'category': 'Snack',
        'benefits': [],
        'concerns': ['High sodium', 'High calories', 'Trans fats', 'Low nutrients']
    },
    'cookies': {
        'score': 2,
        'category': 'Snack',
        'benefits': [],
        'concerns': ['High sugar', 'High calories', 'Saturated fat', 'Low nutrients']
    },
    'candy': {
        'score': 1,
        'category': 'Snack',
        'benefits': [],
        'concerns': ['Very high sugar', 'Empty calories', 'Dental problems', 'No nutrients']
    },
    'soda': {
        'score': 1,
        'category': 'Beverage',
        'benefits': [],
        'concerns': ['Very high sugar', 'Empty calories', 'Dental problems', 'No nutrients']
    },
    'energy drink': {
        'score': 2,
        'category': 'Beverage',
        'benefits': ['Caffeine for energy'],
        'concerns': ['Very high sugar', 'High caffeine', 'Artificial ingredients']
    },
    'beer': {
        'score': 3,
        'category': 'Beverage',
        'benefits': ['Some B vitamins'],
        'concerns': ['Alcohol', 'Empty calories', 'Potential addiction']
    },
    'wine': {
        'score': 4,
        'category': 'Beverage',
        'benefits': ['Antioxidants (red wine)', 'Resveratrol'],
        'concerns': ['Alcohol', 'Calories', 'Potential addiction']
    },
    
    # Beverages (Variable scores: 1-8)
    'water': {
        'score': 10,
        'category': 'Beverage',
        'benefits': ['Essential for life', 'Zero calories', 'Hydration'],
        'concerns': []
    },
    'green tea': {
        'score': 9,
        'category': 'Beverage',
        'benefits': ['Antioxidants', 'Metabolism boost', 'L-theanine'],
        'concerns': ['Caffeine (mild)']
    },
    'coffee': {
        'score': 7,
        'category': 'Beverage',
        'benefits': ['Antioxidants', 'Mental alertness', 'Metabolism boost'],
        'concerns': ['Caffeine dependency', 'Can cause jitters']
    },
    'orange juice': {
        'score': 5,
        'category': 'Beverage',
        'benefits': ['Vitamin C', 'Folate'],
        'concerns': ['High sugar', 'Low fiber compared to whole fruit', 'Calories']
    },
    
    # Nuts and Seeds (High scores: 7-8)
    'almonds': {
        'score': 8,
        'category': 'Nuts/Seeds',
        'benefits': ['Healthy fats', 'Protein', 'Vitamin E', 'Fiber'],
        'concerns': ['High calories']
    },
    'walnuts': {
        'score': 8,
        'category': 'Nuts/Seeds',
        'benefits': ['Omega-3 fatty acids', 'Protein', 'Antioxidants'],
        'concerns': ['High calories']
    },
    'chia seeds': {
        'score': 9,
        'category': 'Nuts/Seeds',
        'benefits': ['Omega-3s', 'Fiber', 'Protein', 'Calcium'],
        'concerns': ['High calories']
    },
    
    # Legumes (High scores: 7-8)
    'black beans': {
        'score': 8,
        'category': 'Legume',
        'benefits': ['High protein', 'High fiber', 'Folate', 'Iron'],
        'concerns': ['Can cause gas']
    },
    'lentils': {
        'score': 8,
        'category': 'Legume',
        'benefits': ['High protein', 'High fiber', 'Folate', 'Iron'],
        'concerns': []
    },
    'chickpeas': {
        'score': 8,
        'category': 'Legume',
        'benefits': ['Protein', 'Fiber', 'Folate', 'Manganese'],
        'concerns': []
    }
}

def get_nutrition_info(item_name):
    """Get nutrition information for a specific item"""
    return NUTRITIONAL_DATABASE.get(item_name.lower(), {
        'score': 5,
        'category': 'Unknown',
        'benefits': ['Nutritional information not available'],
        'concerns': []
    })

def get_items_by_score_range(min_score, max_score):
    """Get all items within a specific nutrition score range"""
    return {
        item: data for item, data in NUTRITIONAL_DATABASE.items()
        if min_score <= data['score'] <= max_score
    }

def get_healthiest_items(limit=10):
    """Get the healthiest items from the database"""
    sorted_items = sorted(
        NUTRITIONAL_DATABASE.items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )
    return dict(sorted_items[:limit])

def get_least_healthy_items(limit=10):
    """Get the least healthy items from the database"""
    sorted_items = sorted(
        NUTRITIONAL_DATABASE.items(),
        key=lambda x: x[1]['score']
    )
    return dict(sorted_items[:limit])
