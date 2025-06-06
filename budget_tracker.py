from datetime import datetime, timedelta
import pandas as pd
import calendar

class BudgetTracker:
    def __init__(self, database):
        self.db = database
    
    def set_monthly_budget(self, amount):
        """Set monthly budget limit"""
        self.db.save_budget_setting(amount)
    
    def get_monthly_budget(self):
        """Get current monthly budget"""
        return self.db.get_budget_setting()
    
    def get_current_month_spending(self):
        """Get total spending for current month"""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], 23, 59, 59)
        
        receipts = self.db.get_receipts()
        if not receipts:
            return 0.0
        
        df = pd.DataFrame(receipts)
        df['date'] = pd.to_datetime(df['date'])
        
        current_month_receipts = df[
            (df['date'] >= start_of_month) & (df['date'] <= end_of_month)
        ]
        
        return current_month_receipts['total_amount'].sum() if not current_month_receipts.empty else 0.0
    
    def get_weekly_spending(self):
        """Get spending breakdown by week for current month"""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        
        receipts = self.db.get_receipts()
        if not receipts:
            return []
        
        df = pd.DataFrame(receipts)
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter to current month
        current_month_receipts = df[df['date'] >= start_of_month]
        if current_month_receipts.empty:
            return []
        
        # Group by week
        current_month_receipts['week'] = current_month_receipts['date'].dt.isocalendar().week
        weekly_spending = current_month_receipts.groupby('week')['total_amount'].sum().reset_index()
        
        # Format week labels
        weekly_spending['week'] = weekly_spending['week'].apply(lambda x: f"Week {x}")
        
        return weekly_spending.to_dict('records')
    
    def get_category_spending(self):
        """Get spending by category for current month"""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], 23, 59, 59)
        
        category_spending = self.db.get_spending_by_category(start_of_month, end_of_month)
        
        # Format for display
        formatted_spending = []
        for item in category_spending:
            formatted_spending.append({
                'category': item['category'],
                'amount': item['total_amount']
            })
        
        return formatted_spending
    
    def get_budget_alerts(self):
        """Get budget alerts and warnings"""
        alerts = []
        budget = self.get_monthly_budget()
        current_spending = self.get_current_month_spending()
        
        if budget <= 0:
            return alerts
        
        percentage_used = (current_spending / budget) * 100
        
        if percentage_used >= 100:
            alerts.append({
                'type': 'error',
                'message': f"🚨 Budget exceeded! You've spent ${current_spending:.2f} of your ${budget:.2f} monthly budget."
            })
        elif percentage_used >= 80:
            alerts.append({
                'type': 'warning',
                'message': f"⚠️ Approaching budget limit! You've used {percentage_used:.1f}% of your monthly budget."
            })
        elif percentage_used >= 60:
            alerts.append({
                'type': 'info',
                'message': f"📊 You've used {percentage_used:.1f}% of your monthly budget so far."
            })
        
        return alerts
    
    def get_spending_trends(self, months=6):
        """Get spending trends over the last N months"""
        receipts = self.db.get_receipts()
        if not receipts:
            return []
        
        df = pd.DataFrame(receipts)
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter to last N months
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        recent_receipts = df[df['date'] >= cutoff_date]
        
        if recent_receipts.empty:
            return []
        
        # Group by month
        recent_receipts['month_year'] = recent_receipts['date'].dt.to_period('M')
        monthly_spending = recent_receipts.groupby('month_year')['total_amount'].sum().reset_index()
        
        # Format for display
        monthly_spending['month_year'] = monthly_spending['month_year'].astype(str)
        
        return monthly_spending.to_dict('records')
    
    def get_daily_average(self):
        """Get daily average spending for current month"""
        current_spending = self.get_current_month_spending()
        days_in_month = datetime.now().day
        
        return current_spending / days_in_month if days_in_month > 0 else 0.0
    
    def get_projected_monthly_spending(self):
        """Project total monthly spending based on current rate"""
        daily_average = self.get_daily_average()
        days_in_month = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
        
        return daily_average * days_in_month
    
    def get_budget_recommendations(self):
        """Get budget optimization recommendations"""
        recommendations = []
        
        current_spending = self.get_current_month_spending()
        budget = self.get_monthly_budget()
        category_spending = self.get_category_spending()
        
        if not category_spending:
            return recommendations
        
        # Find highest spending categories
        category_spending.sort(key=lambda x: x['amount'], reverse=True)
        top_categories = category_spending[:3]
        
        total_spending = sum(item['amount'] for item in category_spending)
        
        for category in top_categories:
            percentage = (category['amount'] / total_spending) * 100 if total_spending > 0 else 0
            if percentage > 30:
                recommendations.append(
                    f"💰 Consider reducing spending on {category['category']} - it's {percentage:.1f}% of your total spending."
                )
        
        # Budget vs spending analysis
        if current_spending > budget * 0.8:
            projected = self.get_projected_monthly_spending()
            if projected > budget:
                recommendations.append(
                    f"📈 You're on track to exceed your budget by ${projected - budget:.2f} this month."
                )
        
        return recommendations
