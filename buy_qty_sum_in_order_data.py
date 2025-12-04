import pandas as pd

def calculate_order_effect(df):
    """
    Calculate final buy/sell quantities based on valid order lifecycle rules:
    
    NEW → AMEND* → (CANCEL / EXECUTED / NONE)
    
    Rules:
        - Use only the latest version of each order_id.
        - NEW/AMEND → add latest quantity
        - CANCEL → add previous latest quantity - cancel quantity
        - EXECUTED → add previous latest quantity (ignore executed quantity)
    """
    
    df = df.copy()

    # Ensure tradetime is datetime (required for sorting)
    df['tradetime'] = pd.to_datetime(df['tradetime'])

    # Sort to get order life in correct chronological order
    df = df.sort_values(['order_id', 'tradetime'])

    results = []   # store final quantity per order

    for order_id, group in df.groupby("order_id"):
        group = group.sort_values("tradetime")

        # determine the latest event
        latest_row = group.iloc[-1]
        latest_event = latest_row['event_type'].lower()
        latest_qty = latest_row['quantity']
        side = latest_row['side'].lower()

        # find last non-cancel & non-executed quantity (latest workable quantity)
        valid_prev = group[group['event_type'].str.lower().isin(['new', 'amend'])]
        if not valid_prev.empty:
            prev_qty = valid_prev.iloc[-1]['quantity']
        else:
            prev_qty = 0  # if missing NEW (rare), use 0

        # apply rules
        if latest_event in ['new', 'amend']:
            final_qty = latest_qty

        elif latest_event == 'cancel':
            final_qty = prev_qty - latest_qty

        elif latest_event == 'executed':
            final_qty = prev_qty   # executed qty ignored completely

        else:
            final_qty = 0  # unknown event types ignored

        results.append({
            "order_id": order_id,
            "side": side,
            "final_qty": final_qty
        })

    # Convert results to DataFrame
    res_df = pd.DataFrame(results)

    # Final buy/sell totals
    buy_total = res_df.loc[res_df['side'] == 'buy', 'final_qty'].sum()
    sell_total = res_df.loc[res_df['side'] == 'sell', 'final_qty'].sum()

    return res_df, buy_total, sell_total

# Generate timestamps
base_time = datetime.now()
times = [base_time + timedelta(minutes=i) for i in range(25)]

df = pd.DataFrame({
    "order_id": [
        # Order 1: NEW → AMEND → EXEC
        "101","101","101",
        
        # Order 2: NEW → CANCEL
        "102","102",
        
        # Order 3: NEW only
        "103",
        
        # Order 4: NEW → AMEND → AMEND
        "104","104","104",
        
        # Order 5: NEW → AMEND → CANCEL
        "105","105","105",
        
        # Order 6: NEW → EXEC
        "106","106",
        
        # Order 7: NEW → AMEND
        "107","107",
        
        # Order 8: NEW only
        "108",
        
        # Order 9: NEW → CANCEL (different qty)
        "109","109",
        
        # Order 10: Long chain NEW → AMEND → AMEND → EXEC
        "110","110","110","110"
    ],
    
    "side": [
        "Buy","Buy","Buy",
        "Sell","Sell",
        "Buy",
        "Sell","Sell","Sell",
        "Buy","Buy","Buy",
        "Sell","Sell",
        "Buy","Buy",
        "Sell",
        "Buy","Buy",
        "Sell","Sell","Sell","Sell"
    ],
    
    "event_type": [
        # 101
        "NEW","AMEND","EXECUTED",
        # 102
        "NEW","CANCEL",
        # 103
        "NEW",
        # 104
        "NEW","AMEND","AMEND",
        # 105
        "NEW","AMEND","CANCEL",
        # 106
        "NEW","EXECUTED",
        # 107
        "NEW","AMEND",
        # 108
        "NEW",
        # 109
        "NEW","CANCEL",
        # 110
        "NEW","AMEND","AMEND","EXECUTED"
    ],
    
    "quantity": [
        # 101
        50, 70, 70,
        # 102
        40, 40,
        # 103
        90,
        # 104
        10, 20, 30,
        # 105
        100, 120, 120,
        # 106
        60, 60,
        # 107
        33, 50,
        # 108
        200,
        # 109
        150, 100,
        # 110
        80, 100, 130, 130
    ],
    
    "price": np.random.randint(100, 300, 25),
    "tradetime": times,
    "symbol": ["AAPL","AAPL","AAPL",
               "MSFT","MSFT",
               "TSLA",
               "NVDA","NVDA","NVDA",
               "GOOG","GOOG","GOOG",
               "META","META",
               "BTC","BTC",
               "ETH",
               "BRK","BRK",
               "NFLX","NFLX","NFLX","NFLX"
              ],
    "account": ["ACC1","ACC1","ACC1",
                "ACC2","ACC2",
                "ACC1",
                "ACC3","ACC3","ACC3",
                "ACC2","ACC2","ACC2",
                "ACC4","ACC4",
                "ACC5","ACC5",
                "ACC1",
                "ACC3","ACC3",
                "ACC6","ACC6","ACC6","ACC6"
               ]
})

print(df)

res_df, buy_total, sell_total = calculate_order_effect(df)

print("Per-order final quantities:")
print(res_df)

print("\nFinal BUY total:", buy_total)
print("Final SELL total:", sell_total)
