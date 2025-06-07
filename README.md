
# 🛒 Smart Grocery Management System

A comprehensive Streamlit-based application for managing grocery receipts, tracking spending, and analyzing nutritional habits through OCR technology and intelligent categorization.

## ✨ Features

### 📸 Receipt Processing
- **OCR Text Extraction**: Upload receipt images and automatically extract text using Tesseract OCR
- **Smart Item Parsing**: Intelligent parsing of grocery items and prices from receipt text
- **Item Categorization**: Automatic categorization of items into food groups (Fruits, Vegetables, Dairy, etc.)
- **Nutrition Scoring**: 1-10 nutrition score for each item based on health benefits

### 📊 Dashboard & Analytics
- **Spending Overview**: Total spending, average receipt amount, and item statistics
- **Time-based Analysis**: Spending trends over time with interactive charts
- **Category Breakdown**: Visual pie charts showing spending distribution by category
- **Recent Receipts**: Quick view of your latest shopping trips

### 💰 Budget Tracking
- **Monthly Budget Setting**: Set and track monthly grocery budgets
- **Real-time Monitoring**: Progress bars and alerts for budget usage
- **Weekly Breakdown**: Analyze spending patterns by week
- **Category Analysis**: See which categories consume most of your budget
- **Smart Recommendations**: Get personalized suggestions for budget optimization

### 🥗 Nutrition Analysis
- **Health Scoring**: Average nutrition scores with health status indicators
- **Category Nutrition**: Compare nutritional value across different food categories
- **Shopping Pattern Analysis**: Insights into healthy vs. unhealthy purchasing habits
- **Personalized Recommendations**: Suggestions for improving nutritional choices

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Tesseract OCR (for receipt text extraction)

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   uv add pandas plotly pytesseract pillow scikit-learn streamlit
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

4. **Access the app** at `http://0.0.0.0:5000`

## 📱 Usage Guide

### Uploading Receipts
1. Navigate to the "📸 Upload Receipt" page
2. Upload a clear image of your grocery receipt (PNG, JPG, JPEG)
3. Click "Process Receipt" to extract and parse items
4. Review and edit the detected items if needed
5. Save the receipt data to your database

### Viewing Analytics
- **Dashboard**: Get an overview of your spending patterns and trends
- **Budget Tracker**: Monitor your monthly budget and get spending insights
- **Nutrition Analysis**: Understand the nutritional quality of your purchases

### Tips for Best Results
- Take clear, well-lit photos of receipts
- Ensure text is readable and not blurry
- Keep receipts flat when photographing
- Try different angles if OCR doesn't detect items correctly

## 🏗️ Project Structure

```
├── app.py                 # Main Streamlit application
├── database.py           # SQLite database operations
├── ocr_processor.py      # OCR and receipt parsing logic
├── item_categorizer.py   # Item categorization system  
├── nutrition_analyzer.py # Nutrition scoring and analysis
├── budget_tracker.py     # Budget tracking functionality
├── data/
│   └── nutritional_data.py # Nutrition database
├── grocery_manager.db    # SQLite database (created automatically)
└── README.md            # This file
```

## 🛠️ Technical Details

### OCR Processing
- Uses Tesseract OCR with multiple configuration attempts for optimal text extraction
- Implements image preprocessing (contrast enhancement, sharpening, noise reduction)
- Advanced regex patterns for parsing items and prices from receipt text
- Fallback parsing methods for challenging receipt formats

### Database Schema
- **receipts**: Stores receipt metadata (date, total amount)
- **items**: Individual grocery items with categories and nutrition scores
- **budget_settings**: User budget preferences and limits

### Nutrition Database
- Comprehensive database of 100+ common grocery items
- Scoring system based on nutritional value (1-10 scale)
- Category-based scoring for unknown items
- Health benefits and concerns for each item

## 🎯 Key Components

### ItemCategorizer
Automatically categorizes grocery items into:
- Fruits & Vegetables
- Dairy & Protein
- Grains & Bakery
- Beverages & Snacks
- Frozen & Canned goods

### NutritionAnalyzer  
- Provides nutrition scores based on scientific nutritional data
- Offers personalized recommendations for healthier choices
- Analyzes shopping patterns for health insights

### BudgetTracker
- Tracks monthly spending against set budgets
- Provides weekly and category-based breakdowns
- Generates alerts and recommendations for budget optimization

## 📈 Future Enhancements

- 🤖 Machine learning for improved item recognition
- 📊 Advanced analytics and reporting features
- 🔄 Data export/import functionality
- 📱 Mobile-responsive design improvements
- 🛒 Shopping list generation based on nutrition goals

## 🤝 Contributing

This project is designed for personal grocery management. Feel free to fork and customize for your own needs!

## 📄 License

This project is open source and available under the MIT License.

---

**Built by Narayan using Streamlit, Python, and OCR technology**
