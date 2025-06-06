import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import io

from database import Database
from ocr_processor import OCRProcessor
from item_categorizer import ItemCategorizer
from nutrition_analyzer import NutritionAnalyzer
from budget_tracker import BudgetTracker

# Initialize components
@st.cache_resource
def init_components():
    db = Database()
    ocr = OCRProcessor()
    categorizer = ItemCategorizer()
    nutrition = NutritionAnalyzer()
    budget = BudgetTracker(db)
    return db, ocr, categorizer, nutrition, budget

def main():
    st.set_page_config(
        page_title="Smart Grocery Manager",
        page_icon="🛒",
        layout="wide"
    )
    
    st.title("🛒 Smart Grocery Management System")
    st.markdown("Upload receipts, track spending, and get nutritional insights!")
    
    # Initialize components
    db, ocr, categorizer, nutrition, budget = init_components()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📸 Upload Receipt", "📊 Dashboard", "💰 Budget Tracker", "🥗 Nutrition Analysis"]
    )
    
    if page == "📸 Upload Receipt":
        upload_receipt_page(db, ocr, categorizer, nutrition)
    elif page == "📊 Dashboard":
        dashboard_page(db)
    elif page == "💰 Budget Tracker":
        budget_tracker_page(budget)
    elif page == "🥗 Nutrition Analysis":
        nutrition_analysis_page(db, nutrition)

def upload_receipt_page(db, ocr, categorizer, nutrition):
    st.header("📸 Upload Receipt")
    
    uploaded_file = st.file_uploader(
        "Choose a receipt image...",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of your grocery receipt"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Uploaded Receipt")
            st.image(image, caption="Receipt Image", use_column_width=True)
        
        with col2:
            st.subheader("Processing Results")
            
            if st.button("Process Receipt", type="primary"):
                with st.spinner("Processing receipt..."):
                    try:
                        # Extract text using OCR
                        extracted_text = ocr.extract_text(image)
                        
                        if not extracted_text.strip():
                            st.error("No text could be extracted from the image. Please try a clearer image.")
                            return
                        
                        # Show extracted text for debugging
                        with st.expander("🔍 View Extracted Text (Debug)"):
                            st.text_area("Raw OCR Output:", extracted_text, height=150)
                        
                        st.success("Text extracted successfully!")
                        
                        # Parse items and prices
                        items_data = ocr.parse_items_and_prices(extracted_text)
                        
                        if not items_data:
                            st.warning("No grocery items could be identified in the receipt.")
                            st.markdown("**Troubleshooting tips:**")
                            st.markdown("• Make sure the receipt image is clear and well-lit")
                            st.markdown("• Ensure item names and prices are clearly visible")
                            st.markdown("• Try taking the photo from directly above the receipt")
                            st.markdown("• Check that the receipt contains individual grocery items with prices")
                            
                            with st.expander("📝 Show Extracted Text for Manual Review"):
                                st.text_area("Extracted Text:", extracted_text, height=200)
                                st.markdown("*Look for item names followed by prices in the text above.*")
                            return
                        
                        # Create DataFrame for display
                        df = pd.DataFrame(items_data)
                        
                        # Categorize items
                        df['category'] = df['item'].apply(categorizer.categorize_item)
                        
                        # Get nutritional scores
                        df['nutrition_score'] = df['item'].apply(nutrition.get_nutrition_score)
                        
                        # Display parsed items
                        st.subheader("Identified Items")
                        edited_df = st.data_editor(
                            df,
                            column_config={
                                "item": "Item Name",
                                "price": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
                                "category": st.column_config.SelectboxColumn(
                                    "Category",
                                    options=[
                                        "Fruits", "Vegetables", "Dairy", "Meat", "Bakery",
                                        "Beverages", "Snacks", "Frozen", "Canned", "Other"
                                    ]
                                ),
                                "nutrition_score": st.column_config.NumberColumn(
                                    "Nutrition Score",
                                    help="1-10 scale (10 = healthiest)",
                                    min_value=1,
                                    max_value=10
                                )
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                        
                        # Save to database
                        if st.button("Save Receipt Data"):
                            receipt_id = db.save_receipt(
                                date=datetime.now(),
                                total_amount=edited_df['price'].sum(),
                                items=edited_df.to_dict('records')
                            )
                            st.success(f"Receipt saved successfully! Total: ${edited_df['price'].sum():.2f}")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error processing receipt: {str(e)}")
                        st.text_area("Extracted Text (for debugging):", extracted_text if 'extracted_text' in locals() else "No text extracted")

def dashboard_page(db):
    st.header("📊 Spending Dashboard")
    
    # Get recent receipts
    receipts = db.get_receipts(limit=50)
    
    if not receipts:
        st.info("No receipts found. Upload your first receipt to see analytics!")
        return
    
    # Convert to DataFrame
    df_receipts = pd.DataFrame(receipts)
    df_receipts['date'] = pd.to_datetime(df_receipts['date'])
    
    # Get all items
    items = db.get_all_items()
    df_items = pd.DataFrame(items)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spent = df_receipts['total_amount'].sum()
        st.metric("Total Spent", f"${total_spent:.2f}")
    
    with col2:
        avg_receipt = df_receipts['total_amount'].mean()
        st.metric("Average Receipt", f"${avg_receipt:.2f}")
    
    with col3:
        total_items = len(df_items)
        st.metric("Total Items", total_items)
    
    with col4:
        unique_items = df_items['item_name'].nunique() if not df_items.empty else 0
        st.metric("Unique Items", unique_items)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Spending Over Time")
        if len(df_receipts) > 1:
            fig_time = px.line(
                df_receipts.sort_values('date'),
                x='date',
                y='total_amount',
                title="Daily Spending Trend"
            )
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("Need more receipts to show spending trend")
    
    with col2:
        st.subheader("Spending by Category")
        if not df_items.empty:
            category_spending = df_items.groupby('category')['price'].sum().reset_index()
            fig_cat = px.pie(
                category_spending,
                values='price',
                names='category',
                title="Spending Distribution"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No items data available")
    
    # Recent receipts table
    st.subheader("Recent Receipts")
    display_receipts = df_receipts.sort_values('date', ascending=False).head(10)
    display_receipts['date'] = display_receipts['date'].dt.strftime('%Y-%m-%d %H:%M')
    st.dataframe(
        display_receipts[['date', 'total_amount']],
        column_config={
            "date": "Date",
            "total_amount": st.column_config.NumberColumn("Amount", format="$%.2f")
        },
        hide_index=True,
        use_container_width=True
    )

def budget_tracker_page(budget_tracker):
    st.header("💰 Budget Tracker")
    
    # Budget settings
    st.subheader("Budget Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_budget = st.number_input(
            "Monthly Budget ($)",
            min_value=0.0,
            value=budget_tracker.get_monthly_budget(),
            step=50.0
        )
        
        if st.button("Update Budget"):
            budget_tracker.set_monthly_budget(monthly_budget)
            st.success("Budget updated!")
            st.rerun()
    
    with col2:
        # Current month spending
        current_spending = budget_tracker.get_current_month_spending()
        remaining = monthly_budget - current_spending
        
        st.metric(
            "This Month's Spending",
            f"${current_spending:.2f}",
            delta=f"${remaining:.2f} remaining"
        )
        
        # Progress bar
        progress = min(current_spending / monthly_budget if monthly_budget > 0 else 0, 1.0)
        st.progress(progress)
        
        if progress > 0.8:
            st.warning("⚠️ You're approaching your budget limit!")
        elif progress > 1.0:
            st.error("❌ You've exceeded your monthly budget!")
    
    # Weekly breakdown
    st.subheader("Weekly Spending Breakdown")
    weekly_data = budget_tracker.get_weekly_spending()
    
    if weekly_data:
        df_weekly = pd.DataFrame(weekly_data)
        fig_weekly = px.bar(
            df_weekly,
            x='week',
            y='amount',
            title="Weekly Spending Pattern"
        )
        st.plotly_chart(fig_weekly, use_container_width=True)
    else:
        st.info("No spending data available for weekly breakdown")
    
    # Category budget analysis
    st.subheader("Category Spending Analysis")
    category_data = budget_tracker.get_category_spending()
    
    if category_data:
        df_categories = pd.DataFrame(category_data)
        
        # Create horizontal bar chart
        fig_categories = px.bar(
            df_categories,
            x='amount',
            y='category',
            orientation='h',
            title="Spending by Category This Month"
        )
        st.plotly_chart(fig_categories, use_container_width=True)
        
        # Top spending categories
        st.subheader("Top Spending Categories")
        top_categories = df_categories.nlargest(5, 'amount')
        for idx, row in top_categories.iterrows():
            st.write(f"**{row['category']}**: ${row['amount']:.2f}")
    else:
        st.info("No category data available")

def nutrition_analysis_page(db, nutrition_analyzer):
    st.header("🥗 Nutrition Analysis")
    
    # Get nutrition data
    items = db.get_all_items()
    
    if not items:
        st.info("No items found. Upload some receipts to see nutritional analysis!")
        return
    
    df_items = pd.DataFrame(items)
    
    # Overall nutrition score
    avg_nutrition_score = df_items['nutrition_score'].mean()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Nutrition Score", f"{avg_nutrition_score:.1f}/10")
        
        # Health status
        if avg_nutrition_score >= 7:
            st.success("🎉 Great healthy choices!")
        elif avg_nutrition_score >= 5:
            st.warning("⚠️ Room for improvement")
        else:
            st.error("❌ Consider healthier alternatives")
    
    with col2:
        healthy_items = len(df_items[df_items['nutrition_score'] >= 7])
        st.metric("Healthy Items", f"{healthy_items}/{len(df_items)}")
    
    with col3:
        unhealthy_items = len(df_items[df_items['nutrition_score'] <= 4])
        st.metric("Items to Improve", unhealthy_items)
    
    # Nutrition by category
    st.subheader("Nutrition Score by Category")
    category_nutrition = df_items.groupby('category')['nutrition_score'].mean().reset_index()
    category_nutrition = category_nutrition.sort_values('nutrition_score', ascending=True)
    
    fig_nutrition = px.bar(
        category_nutrition,
        x='nutrition_score',
        y='category',
        orientation='h',
        title="Average Nutrition Score by Category",
        color='nutrition_score',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_nutrition, use_container_width=True)
    
    # Recent items analysis
    st.subheader("Recent Items Analysis")
    recent_items = df_items.nlargest(20, 'id')[['item_name', 'category', 'nutrition_score', 'price']]
    
    # Color code by nutrition score
    def get_nutrition_color(score):
        if score >= 7:
            return "🟢"
        elif score >= 5:
            return "🟡"
        else:
            return "🔴"
    
    recent_items['health_indicator'] = recent_items['nutrition_score'].apply(get_nutrition_color)
    
    st.dataframe(
        recent_items,
        column_config={
            "item_name": "Item",
            "category": "Category",
            "nutrition_score": st.column_config.NumberColumn("Nutrition Score", format="%.1f"),
            "price": st.column_config.NumberColumn("Price", format="$%.2f"),
            "health_indicator": "Health"
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Recommendations
    st.subheader("🎯 Recommendations")
    recommendations = nutrition_analyzer.get_recommendations(df_items)
    
    if recommendations:
        for rec in recommendations:
            st.info(rec)
    else:
        st.success("Great job! Your grocery choices look healthy overall.")

if __name__ == "__main__":
    main()
