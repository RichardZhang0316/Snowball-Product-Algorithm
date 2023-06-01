'''
近几年来,雪球产品在国内发展很快,规模达到了5,000亿之多。假设现在是三年前的今天,一个券商想发行挂钩中证500指数的雪球产品。
设定雪球产品结构类型为75~102,敲出票息为年化20%,募集资金2亿元。
试计算一下在发生敲出、未敲入未敲出、敲入未敲出三种情况下,券商的留存收益年化会有多少？
'''

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 这个函数计算券商留存年化收益率
def calculate_annualized_return(principal, brokerInterest, investmentYears):
    if brokerInterest > 0:
        return (1 + (brokerInterest / principal)) ** (1 / investmentYears) - 1
    else:
        return (brokerInterest / principal) / investmentYears
    
# 主体功能函数。支持代入不同的起始日期。
def calculate_returns(start_date_str):
    
    # 读取Excel文件。Excel格式为： Date | Index （示例：2020/5/22	5328.23）
    df = pd.read_excel('/Users/zhangkaixin/Desktop/雪球/中证500指数行情序列.xlsx', engine='openpyxl')
    # 找到开始日期在数据框中的位置
    start_index = df[df['Date'] == start_date_str].index[0]
    # 仅处理开始日期后的数据
    df = df.loc[start_index:]
    
    # 解析起始日期字符串
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    # 计算结束日期（起始日期后的两年）
    final_end_date = start_date + timedelta(days=2*365)
    
    # 本金2亿元
    principal = 200000000
    # 年化票息20%
    annualizedCouponRate = 0.2
    # 原始价格
    initialPrice = df.loc[start_index, 'Index']
    # 初始化状态
    knockInEvent = False
    knockOutEvent = False
    # 总买入股本
    totalShare = 0
    # 总资产价值
    totalAsset = principal
    # 现金
    cash = principal

    last_check_out_check_date = pd.to_datetime(start_date_str)

    # 遍历价格数据，使用 df 的实际索引
    for i in df.index:
        price = df.loc[i, 'Index']
        current_date = df.loc[i, 'Date']
        
        # 判断是否已经到达结束日期
        if current_date >= final_end_date:
            # 假如产品到期,卖出所有已买入股本,产品即刻停止
            totalAsset = totalShare * price + cash
            totalShare = 0
            knockOutEventDate = df.loc[i, 'Date']
            print("卖出日 :", current_date)
            print("交易后额度 0%")
            print("卖出额度 ", totalShare * price / totalAsset)
            # 到期后跳出循环
            break

        if price <= initialPrice * 0.75:
            # 假如触发敲入事件，则满仓，花费所有现金
            knockInEvent = True
            purchasedAmount = cash / price
            totalShare += cash / price
            cash = 0
            totalAsset = 0 + totalShare * price
            print("敲入 买入日 :", current_date)
            print("交易后额度 100%")
            print("买入额 （元） ", purchasedAmount * price)            
        elif price >= initialPrice * 0.95 and price < initialPrice * 1.02:
            # 假如现价等于原始价格102% （不包括102%） - 95%,则持有30%的总资产规模
            if totalShare * price < totalAsset * 0.3:
                # 持有股票价值小于总资产价值的30%，需要买入以达到总资产的30%
                disposableFund = totalAsset * 0.3 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("买入日 :", current_date)
                print("交易后额度 30%")
                print("买入额 （元） ", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.3:
                # 持有股票价值大于总资产价值的30%，需要卖出以达到总资产的30%
                reclaimedFund = totalShare * price - totalAsset * 0.3
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset =  cash + totalShare * price
                print("卖出日 :", current_date)
                print("交易后额度 30%")
                print("卖出额 （元）", selledAmount * price)
        elif price >= initialPrice * 0.90 and price < initialPrice * 0.95:
            # 假如跌至原始价格90% - 95%,则持有40%的总资产规模
            if totalShare * price < totalAsset * 0.4:
                # 持有股票价值小于总资产价值的40%，需要买入以达到总资产的40%
                disposableFund = totalAsset * 0.4 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("买入日 :", current_date)
                print("交易后额度 40%")
                print("买入额 （元） ", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.4:
                # 持有股票价值大于总资产价值的40%，需要卖出以达到总资产的40%
                reclaimedFund = totalShare * price - totalAsset * 0.4
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset =  cash + totalShare * price
                print("卖出日 :", current_date)
                print("交易后额度 40%")
                print("卖出额 （元）", selledAmount * price)
        elif price >= initialPrice * 0.85 and price < initialPrice * 0.90:
            # 假如跌至原始价格85% - 90%,则持有50%的总资产规模
            if totalShare * price < totalAsset * 0.5:
                # 持有股票价值小于总资产价值的50%，需要买入以达到总资产的50%
                disposableFund = totalAsset * 0.5 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("买入日 :", current_date)
                print("交易后额度 50%")
                print("买入额 （元） ", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.5:
                # 持有股票价值大于总资产价值的50%，需要卖出以达到总资产的50%
                reclaimedFund = totalShare * price - totalAsset * 0.5
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset =  cash + totalShare * price
                print("卖出日 :", current_date)
                print("交易后额度 50%")
                print("卖出额 （元）", selledAmount * price)
        elif price >= initialPrice * 0.85 and price < initialPrice * 0.80:
            # 假如跌至原始价格80% - 85%,则持有70%的总资产规模
            if totalShare * price < totalAsset * 0.7:
                # 持有股票价值小于总资产价值的70%，需要买入以达到总资产的70%
                disposableFund = totalAsset * 0.7 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("买入日 :", current_date)
                print("交易后额度 70%")
                print("买入额 （元） ", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.7:
                # 持有股票价值大于总资产价值的70%，需要卖出以达到总资产的70%
                reclaimedFund = totalShare * price - totalAsset * 0.7
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset =  cash + totalShare * price
                print("卖出日 :", current_date)
                print("交易后额度 70%")
                print("卖出额 （元）", selledAmount * price)
        elif price >= initialPrice * 0.80 and price <= initialPrice * 0.75:
            # 假如跌至原始价格75% - 80%,则持有90%的总资产规模
            if totalShare * price < totalAsset * 0.9:
                # 持有股票价值小于总资产价值的90%，需要买入以达到总资产的90%
                disposableFund = totalAsset * 0.9 - totalShare * price
                purchasedAmount = disposableFund / price
                totalShare += disposableFund / price
                cash -= disposableFund
                totalAsset = cash + totalShare * price
                print("买入日 :", current_date)
                print("交易后额度 90%")
                print("买入额 （元） ", purchasedAmount * price)
            elif totalShare * price > totalAsset * 0.9:
                # 持有股票价值大于总资产价值的90%，需要卖出以达到总资产的90%
                reclaimedFund = totalShare * price - totalAsset * 0.9
                selledAmount = reclaimedFund / price
                totalShare -= reclaimedFund / price
                cash += reclaimedFund
                totalAsset =  cash + totalShare * price
                print("卖出日 :", current_date)
                print("交易后额度 90%")
                print("卖出额 （元）", selledAmount * price)
        
        # （每隔30天只检查一次是否发生敲出事件）假如触发敲出事件,卖出所有已买入股本,产品即刻停止
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
                print("敲出 卖出日 :", current_date)
                print("交易后额度 0%")
                print("卖出额 （元）", reclaimedFund)
                break

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    knockOutEventDateStr = knockOutEventDate.strftime('%Y/%m/%d')
    end_date = datetime.strptime(knockOutEventDateStr, '%Y/%m/%d')
    # Calculate the number of days between two dates
    days = (end_date - start_date).days
    # 计算投资年数
    investmentYears = days / 365.25

    if knockInEvent and not knockOutEvent:
        # 敲入且未敲出,则投资者承担相当于标的指数跌幅的损失。
        payable = principal * (price / initialPrice)
        # 券商盈余
        brokerInterest = totalAsset - payable
        # 计算年化收益率
        annualizedReturn = calculate_annualized_return(principal, brokerInterest, investmentYears)
    elif not knockInEvent and not knockOutEvent:
        # 未发生敲入和敲出事件。投资者获得20%年化票息。
        payable = principal + principal * annualizedCouponRate * investmentYears
        brokerInterest = totalAsset - payable
        annualizedReturn = calculate_annualized_return(principal, brokerInterest, investmentYears)
    elif knockOutEvent:
        # 发生敲出事件。投资者获得20%年化票息。
        payable = principal + principal * annualizedCouponRate * investmentYears
        brokerInterest = totalAsset - payable
        annualizedReturn = calculate_annualized_return(principal, brokerInterest, investmentYears)
    
    # 返回一个字典，包含所有的结果
    return {
        "是否敲出": knockOutEvent,
        "是否敲入": knockInEvent,
        "结束时总资产价值": totalAsset,
        "券商留存利润": brokerInterest,
        "本金": principal,
        "投资年限": investmentYears,
        "利润率": brokerInterest / principal,
        "产品激活天数": days,
        "券商留存年化收益率": annualizedReturn,
        "起始日期": start_date,
        "结束日期": end_date,
        "应偿付给投资者的资金总额": payable,
        "应偿付给投资者的资金总额 + 券商利润": brokerInterest + payable,
        "初始价格": initialPrice,
        "产品结束时中证500指数价格": price
    }

# 选择一个起始日期，并遍历并打印出利润最高的起始日期（100个日期以内）
def calculate_returns_for_all_dates(start_date_str: str):
    df = pd.read_excel('/Users/zhangkaixin/Desktop/雪球/中证500指数行情序列.xlsx', engine='openpyxl')
    
    # 将字符串格式的日期转换为datetime对象
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')

    # 仅选择在给定起始日期之后的数据
    df = df[df['Date'] >= start_date]

    # 如果数据点不足100个，则返回
    if len(df) < 100:
        print("Insufficient data points after the start date")
        return

    # 截取起始日期之后的前100个数据点
    df = df.iloc[:100]

    # 初始化一个列表来保存所有的结果
    results_list = []

    # 遍历所有日期
    for date_str in df['Date'].dt.strftime('%Y/%m/%d'):
        result = calculate_returns(date_str)

        # 将结果保存在列表中
        results_list.append(result)

    # 找出利润最大的结果并打印
    max_profit_result = max(results_list, key=lambda x: x['券商留存利润'])
    for key, value in max_profit_result.items():
        print(key, ":", value)


            
# 以下是运行函数的过程（主程序）
# 定义开始日期
start_date_str = '2010/1/4'
# start_date_str = '2010/1/21'
# start_date_str = '2020/5/22'
# start_date_str = '2011/4/22'
# 调用函数并保存结果
result = calculate_returns(start_date_str)
# 遍历结果并打印每个键值对
for key, value in result.items():
    print(key, ":", value)

# 或者找出最大利润的起始日期
# calculate_returns_for_all_dates('2010/1/21')