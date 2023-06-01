import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# This function calculates the annualized return retained by the broker
def calculate_annualized_return(principal, brokerInterest, investmentYears):
    if brokerInterest > 0:
        return (1 + (brokerInterest / principal)) ** (1 / investmentYears) - 1
    else:
        return (brokerInterest / principal) / investmentYears
    
# Main function. Supports substituting different start dates.
def calculate_returns(start_date_str):
    
    # Read the Excel file. Excel format: Date | Index (Example: 2020/5/22	5328.23)
    df = pd.read_excel('/Users/zhangkaixin/Desktop/雪球/中证500指数行情序列.xlsx', engine='openpyxl')
    # Find the position of the start date in the data frame
    start_index = df[df['Date'] == start_date_str].index[0]
    # Only process data after the start date
    df = df.loc[start_index:]
    
    # Parse start date string
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    # Calculate the end date (two years after the start date)
    final_end_date = start_date + timedelta(days=2*365)
    
    # Principal of 200 million
    principal = 200000000
    # Annualized coupon rate 20%
    annualizedCouponRate = 0.2
    # Initial price
    initialPrice = df.loc[start_index, 'Index']
    # Initialize status
    knockInEvent = False
    knockOutEvent = False
    # Total shares bought
    totalShare = 0
    # Total asset value
    totalAsset = principal
    # Cash
    cash = principal

    last_check_out_check_date = pd.to_datetime(start_date_str)

    # Traverse the price data using the actual index of df
    for i in df.index:
        price = df.loc[i, 'Index']
        current_date = df.loc[i, 'Date']
        
        # Determine if the end date has been reached
        if current_date >= final_end_date:
            # If the product expires, sell all shares bought, and stop the product immediately
            totalAsset = totalShare * price + cash
            totalShare = 0
            knockOutEventDate = df.loc[i, 'Date']
            print("Sell date:", current_date)
            print("Balance after transaction 0%")
            print("Sell amount", totalShare * price / totalAsset)
            # Jump out of the loop after expiration
            break

        if price <= initialPrice * 0.75:
            # If the knock-in event is triggered, go full position and spend all cash
            knockInEvent = True
            purchasedAmount = cash / price
            totalShare += cash / price
            cash = 0
            totalAsset = 0 + totalShare * price
            print("Knock-in buy date:", current_date)
            print("Balance after transaction 100%")
            print("Purchase amount (yuan)", purchasedAmount * price)            
        elif price >= initialPrice * 0.95 and price < initialPrice * 1.02:
            # If the current price equals the initial price 102% (excluding 102%) - 95%, then hold 30% of the total asset scale
            if totalShare * price < totalAsset * 0.3:
                # If the value of the shares held is less than 30% of the total asset
