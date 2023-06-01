# In recent years, Snowball products have developed rapidly in China, with a scale of over 500 billion yuan. Suppose today is three years ago, and a brokerage firm wants to issue a Snowball product linked to the CSI 500 Index.
# Set the structure type of the Snowball product to 75-102, with a knock-out coupon rate of 20% per annum and a fundraising amount of 200 million yuan.
# Try to calculate the annualized retained returns for the brokerage firm in three scenarios: knock-out, not knocked-in or knocked-out, and knocked-in but not knocked-out.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# This function calculates the annualized return rate for the brokerage firm.


def calculate_annualized_return(principal, brokerInterest, investmentYears):
    if brokerInterest > 0:
        return (1 + (brokerInterest / principal)) ** (1 / investmentYears) - 1
    else:
        return (brokerInterest / principal) / investmentYears

# Main function. Supports input of different start dates.


def calculate_returns(start_date_str):

    # Read Excel file. The Excel format is: Date | Index (Example: 2020/5/22 5328.23)
    df = pd.read_excel(
        '/Users/zhangkaixin/Desktop/雪球/中证500指数行情序列.xlsx', engine='openpyxl')
    # Find the position of the start date in the data frame
    start_index = df[df['Date'] == start_date_str].index[0]
    # Process only the data after the start date
    df = df.loc[start_index:]

    # Parse the start date string
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    # Calculate the end date (two years after the start date)
    final_end_date = start_date + timedelta(days=2*365)

    # Principal: 200 million yuan
    principal = 200000000
    # Annualized coupon rate: 20%
    annualizedCouponRate = 0.2
    # Initial price
    initialPrice = df.loc[start_index, 'Index']
    # Initialize states
    knockInEvent = False
    knockOutEvent = False
    # Total shares bought
    totalShare = 0
    # Total asset value
    totalAsset = principal
    # Cash
    cash = principal

    last_check_out_check_date = pd.to_datetime(start_date_str)
    # Traverse the price data using the actual index of the df
    for i in df.index:
        price = df.loc[i, 'Index']
        current_date = df.loc[i, 'Date']

        # Check if the final end date has been reached
        if current_date >= final_end_date:
            # If the product has expired, sell all the shares and stop the product immediately
            totalAsset = totalShare * price + cash
            totalShare = 0
            knockOutEventDate = df.loc[i, 'Date']
            print("Sell date:", current_date)
            print("Remaining portfolio 0%")
            print("Sell amount:", totalShare * price / totalAsset)
            # Break out of the loop after expiration
            break

        if price <= initialPrice * 0.75:
            # If the knock-in event is triggered, go all-in and spend all the cash
            knockInEvent = True
            purchasedAmount = cash / price
            totalShare += cash / price
            cash = 0
            totalAsset = 0 + totalShare * price
            print("Knock-in Buy date:", current_date)
            print("Remaining portfolio 100%")
            print("Buy amount (RMB):", purchasedAmount * price)
        elif price >= initialPrice * 0.95 and price < initialPrice * 1.02:
            # If the current price is equal to or greater than 95% but less than 102% (excluding 102%) of the initial price, hold 30% of the total asset value
            if totalShare * price < totalAsset * 0.3:
                # If the value of the stocks held is less than 30% of the total asset value, buy to reach 30%
                disposableFund = totalAsset * 0.3 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("Buy date:", current_date)
                print("Remaining portfolio 30%")
                print("Buy amount (RMB):", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.3:
                # If the value of the stocks held is greater than 30% of the total asset value, sell to reach 30%
                reclaimedFund = totalShare * price - totalAsset * 0.3
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset = cash + totalShare * price
                print("Sell date:", current_date)
                print("Remaining portfolio 30%")
                print("Sell amount (RMB):", selledAmount * price)
        elif price >= initialPrice * 0.90 and price < initialPrice * 0.95:
            # If the price falls to 90% - 95% of the initial price, hold 40% of the total asset value
            if totalShare * price < totalAsset * 0.4:
                # If the value of the stocks held is less than 40% of the total asset value, buy to reach 40%
                disposableFund = totalAsset * 0.4 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("Buy date:", current_date)
                print("Remaining portfolio 40%")
                print("Buy amount (RMB):", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.4:
                # If the value of the stocks held is greater than 40% of the total asset value, sell to reach 40%
                reclaimedFund = totalShare * price - totalAsset * 0.4
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset = cash + totalShare * price
                print("Sell date:", current_date)
                print("Remaining portfolio 40%")
                print("Sell amount (RMB):", selledAmount * price)
        elif price >= initialPrice * 0.85 and price < initialPrice * 0.90:
            # If the price falls to 85% - 90% of the initial price, hold 50% of the total asset value
            if totalShare * price < totalAsset * 0.5:
                # If the value of the stocks held is less than 50% of the total asset value, buy to reach 50%
                disposableFund = totalAsset * 0.5 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("Buy date:", current_date)
                print("Remaining portfolio 50%")
                print("Buy amount (RMB):", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.5:
                # If the value of the stocks held is greater than 50% of the total asset value, sell to reach 50%
                reclaimedFund = totalShare * price - totalAsset * 0.5
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset = cash + totalShare * price
                print("Sell date:", current_date)
                print("Remaining portfolio 50%")
                print("Sell amount (RMB):", selledAmount * price)
        elif price >= initialPrice * 0.85 and price < initialPrice * 0.80:
            # If the price falls to 80% - 85% of the initial price, hold 70% of the total asset value
            if totalShare * price < totalAsset * 0.7:
                # If the value of the stocks held is less than 70% of the total asset value, buy to reach 70%
                disposableFund = totalAsset * 0.7 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("Buy date:", current_date)
                print("Remaining portfolio 70%")
                print("Buy amount (RMB):", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.7:
                # If the value of the stocks held is greater than 70% of the total asset value, sell to reach 70%
                reclaimedFund = totalShare * price - totalAsset * 0.7
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset = cash + totalShare * price
                print("Sell date:", current_date)
                print("Remaining portfolio 70%")
                print("Sell amount (RMB):", selledAmount * price)
        elif price >= initialPrice * 0.80 and price <= initialPrice * 0.75:
            # If the price falls to 75% - 80% of the initial price, hold 90% of the total asset value
            if totalShare * price < totalAsset * 0.9:
                # If the value of the stocks held is less than 90% of the total asset value, buy to reach 90%
                disposableFund = totalAsset * 0.9 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("Buy date:", current_date)
                print("Remaining portfolio 90%")
                print("Buy amount (RMB):", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.9:
                # If the value of the stocks held is greater than 90% of the total asset value, sell to reach 90%
                reclaimedFund = totalShare * price - totalAsset * 0.9
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset = cash + totalShare * price
                print("Sell date:", current_date)
                print("Remaining portfolio 90%")
                print("Sell amount (RMB):", selledAmount * price)
            # Check knock-out event every 30 days. If triggered, sell all shares and stop the product
        if (current_date - last_check_out_check_date).days >= 30:
            last_check_out_check_date = current_date  # Update last_check_date
            if price >= initialPrice * 1.02:
                # If knock-out event happens, sell all shares and stop the product
                reclaimedFund = totalShare * price
                cash += reclaimedFund
                totalAsset = cash + 0
                totalShare = 0
                knockOutEvent = True
                knockOutEventDate = current_date
                print("Knock-out Sell date:", current_date)
                print("Remaining portfolio 0%")
                print("Sell amount (RMB):", reclaimedFund)
                break

        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
        knockOutEventDateStr = knockOutEventDate.strftime('%Y/%m/%d')
        end_date = datetime.strptime(knockOutEventDateStr, '%Y/%m/%d')
        # Calculate the number of days between two dates
        days = (end_date - start_date).days
        # Calculate investment years
        investmentYears = days / 365.25

        if knockInEvent and not knockOutEvent:
            # If knock-in event happens but not knocked-out, the investor bears the loss equivalent to the drop in the underlying index.
            payable = principal * (price / initialPrice)
            # Broker's interest
            brokerInterest = totalAsset - payable
            # Calculate annualized return rate
            annualizedReturn = calculate_annualized_return(
                principal, brokerInterest, investmentYears)
        elif not knockInEvent and not knockOutEvent:
            # If neither knock-in nor knock-out event happens. The investor receives a 20% annualized coupon.
            payable = principal + principal * annualizedCouponRate * investmentYears
            brokerInterest = totalAsset - payable
            annualizedReturn = calculate_annualized_return(
                principal, brokerInterest, investmentYears)
        elif knockOutEvent:
            # If knock-out event happens. The investor receives a 20% annualized coupon.
            payable = principal + principal * annualizedCouponRate * investmentYears
            brokerInterest = totalAsset - payable
            annualizedReturn = calculate_annualized_return(
                principal, brokerInterest, investmentYears)

        # Return a dictionary containing all the results
        return {
            "Knock-out Event": knockOutEvent,
            "Knock-in Event": knockInEvent,
            "Total Asset Value at the end": totalAsset,
            "Broker Retained Profit": brokerInterest,
            "Principal": principal,
            "Investment Years": investmentYears,
            "Profit Rate": brokerInterest / principal,
            "Product Active Days": days,
            "Broker's Annualized Return Rate": annualizedReturn,
            "Start Date": start_date,
            "End Date": end_date,
            "Total Payable to Investors": payable,
            "Total Payable to Investors + Broker's Profit": brokerInterest + payable,
            "Initial Price": initialPrice,
            "End Price of CSI 500 Index at Product End": price
        }

# Select a start date and iterate to find the start date with the highest profit (within 100 dates)
def calculate_returns_for_all_dates(start_date_str: str):
    df = pd.read_excel(
        '/Users/zhangkaixin/Desktop/雪球/中证500指数行情序列.xlsx', engine='openpyxl')

    # Convert the start date string to a datetime object
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')

    # Select only the data points after the given start date
    df = df[df['Date'] >= start_date]

    # If there are less than 100 data points, return
    if len(df) < 100:
        print("Insufficient data points after the start date")
        return

    # Select the first 100 data points after the start date
    df = df.iloc[:100]

    # Initialize a list to store all the results
    results_list = []

    # Iterate over all dates
    for date_str in df['Date'].dt.strftime('%Y/%m/%d'):
        result = calculate_returns(date_str)

        # Save the result in the list
        results_list.append(result)

    # Find the result with the highest profit and print it
    max_profit_result = max(results_list, key=lambda x: x['Broker Retained Profit'])
    for key, value in max_profit_result.items():
        print(key, ":", value)

# The following is the execution of the functions (main program)
# Define the start date
start_date_str = '2010/1/4'
# start_date_str = '2010/1/21'
# start_date_str = '2020/5/22'
# start_date_str = '2011/4/22'
# Call the function and save the result
result = calculate_returns(start_date_str)
# Iterate over the result and print each key-value pair
for key, value in result.items():
    print(key, ":", value)

# Or find the start date with the maximum profit
# calculate_returns_for_all_dates('2010/1/21')
