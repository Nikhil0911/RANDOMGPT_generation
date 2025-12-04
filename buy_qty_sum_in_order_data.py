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

res_df, buy_total, sell_total = calculate_order_effect(df)

print("Per-order final quantities:")
print(res_df)

print("\nFinal BUY total:", buy_total)
print("Final SELL total:", sell_total)
