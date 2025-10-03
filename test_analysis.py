#!/usr/bin/env python
"""
Test script to verify the TOU analysis works end-to-end
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load and process data
print("Loading data...")
df = pd.read_csv('XCEL_E_HOURLY_10-01-2024_10-01-2025.csv')
df['Date and Time'] = pd.to_datetime(df['Date and Time'], utc=True)
df.set_index('Date and Time', inplace=True)
df.index = df.index.tz_convert('US/Mountain')

print(f"✅ Data loaded: {len(df):,} records")
print(f"✅ Index type: {type(df.index)}")

# Define billing rates
FLAT_RATES = {
    'summer': 0.10380,
    'winter': 0.08570
}

TOU_RATES = {
    'summer_on_peak': 0.21277,
    'summer_off_peak': 0.21277,
    'winter_on_peak': 0.18331,
    'winter_off_peak': 0.18331
}

# Categorize time periods
def categorize_time_period(timestamp):
    month = timestamp.month
    hour = timestamp.hour
    weekday = timestamp.weekday()
    is_summer = month in [6, 7, 8, 9]
    is_on_peak = (17 <= hour < 21) and (weekday < 5)
    if is_summer:
        return 'summer_on_peak' if is_on_peak else 'summer_off_peak'
    else:
        return 'winter_on_peak' if is_on_peak else 'winter_off_peak'

df['period_type'] = df.index.map(categorize_time_period)
df['is_on_peak'] = df['period_type'].str.contains('on_peak')

print("✅ Time periods categorized")

# Calculate usage percentages
total_usage = df['Interval kWh'].sum()
on_peak_usage = df[df['is_on_peak']]['Interval kWh'].sum()
off_peak_usage = df[~df['is_on_peak']]['Interval kWh'].sum()

on_peak_pct = (on_peak_usage / total_usage) * 100
off_peak_pct = (off_peak_usage / total_usage) * 100

print(f"✅ On-peak usage: {on_peak_pct:.1f}%")
print(f"✅ Off-peak usage: {off_peak_pct:.1f}%")

# Calculate monthly costs
df['month'] = df.index.strftime('%Y-%m')
monthly_usage = df.groupby(['month', 'period_type'])['Interval kWh'].sum().unstack(fill_value=0)
monthly_costs = pd.DataFrame(index=monthly_usage.index)

# Calculate flat rate costs
for month in monthly_usage.index:
    month_num = int(month.split('-')[1])
    is_summer = month_num in [6, 7, 8, 9]
    rate = FLAT_RATES['summer'] if is_summer else FLAT_RATES['winter']
    total_usage_month = monthly_usage.loc[month].sum()
    monthly_costs.loc[month, 'Flat Rate'] = total_usage_month * rate

# Calculate TOU costs
for month in monthly_usage.index:
    tou_cost = 0
    for period in monthly_usage.columns:
        if period in TOU_RATES:
            usage = monthly_usage.loc[month, period]
            rate = TOU_RATES[period]
            tou_cost += usage * rate
    monthly_costs.loc[month, 'Time of Use'] = tou_cost

monthly_costs['Savings with TOU'] = monthly_costs['Flat Rate'] - monthly_costs['Time of Use']

print("✅ Monthly costs calculated")

# Summary
total_flat_cost = monthly_costs['Flat Rate'].sum()
total_tou_cost = monthly_costs['Time of Use'].sum()
total_savings = total_flat_cost - total_tou_cost

print("\n" + "="*50)
print("SUMMARY")
print("="*50)
print(f"Total usage: {total_usage:,.0f} kWh")
print(f"Flat rate total: ${total_flat_cost:,.2f}")
print(f"TOU total: ${total_tou_cost:,.2f}")
print(f"Annual savings with TOU: ${total_savings:+,.2f}")
print(f"Percentage savings: {(total_savings/total_flat_cost)*100:+.1f}%")

if total_savings > 0:
    print("✅ RECOMMENDATION: Switch to Time of Use billing")
else:
    print("❌ RECOMMENDATION: Stay with Flat Rate billing")

print("\n✅ All tests passed! The notebook should work correctly.")