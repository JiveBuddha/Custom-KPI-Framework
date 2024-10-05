import pandas as pd
import numpy as np

class KPICalculator:
    def __init__(self, data):
        """
        Initialize the KPI calculator.

        :param data: pd.DataFrame - The dataset containing user activity data.
        """
        self.data = data

    def calculate_daily_active_users(self):
        """
        Calculate the number of daily active users (DAU).

        :return: pd.DataFrame - Daily active user count.
        """
        dau = self.data.groupby('date')['user_id'].nunique().reset_index(name='daily_active_users')
        return dau

    def calculate_monthly_active_users(self):
        """
        Calculate the number of monthly active users (MAU).

        :return: pd.DataFrame - Monthly active user count.
        """
        self.data['month'] = pd.to_datetime(self.data['date']).dt.to_period('M')
        mau = self.data.groupby('month')['user_id'].nunique().reset_index(name='monthly_active_users')
        return mau

    def calculate_user_engagement(self):
        """
        Calculate user engagement as average sessions per user.

        :return: float - Average sessions per user.
        """
        total_sessions = self.data.groupby('user_id')['session_id'].nunique()
        avg_sessions = total_sessions.mean()
        return avg_sessions

    def calculate_retention_rate(self, day_n=30):
        """
        Calculate user retention rate (percentage of users who return after N days).

        :param day_n: int - Number of days for retention (default: 30 days).
        :return: float - Retention rate.
        """
        first_date = self.data.groupby('user_id')['date'].min().reset_index(name='first_active_date')
        retention_users = self.data.groupby('user_id')['date'].max().reset_index(name='last_active_date')

        # Merge to track retention status
        retention_data = pd.merge(first_date, retention_users, on='user_id')
        retention_data['retained'] = retention_data['last_active_date'] >= retention_data['first_active_date'] + pd.Timedelta(days=day_n)

        retention_rate = retention_data['retained'].mean()
        return retention_rate

    def calculate_lifetime_value(self):
        """
        Calculate the Lifetime Value (LTV) based on user revenue and sessions.

        :return: float - Estimated lifetime value.
        """
        revenue_per_user = self.data.groupby('user_id')['revenue'].sum()
        avg_revenue = revenue_per_user.mean()
        avg_sessions = self.calculate_user_engagement()
        
        # Assume LTV is proportional to average revenue and average sessions
        ltv = avg_revenue * avg_sessions
        return ltv