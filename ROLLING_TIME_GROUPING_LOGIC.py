import pandas as pd
from itertools import combinations

# Step 1: Create DataFrame and convert timestamps
df = pd.DataFrame(data)
df['O_timestamp'] = pd.to_datetime(df['O_timestamp'])

# Initialize group_id for matched groups
df = df.sort_values(by='O_timestamp')  # Ensure rows are sorted by time
group_id = 0
df['group_id'] = -1  # Initialize with -1 for ungrouped rows

# Step 2: Grouping by O_book_id and O_isin_code
for (book_id, isin_code), group in df.groupby(['O_book_id', 'O_isin_code']):
    for i, row in group.iterrows():
        # Step 3: Rolling 1-minute window
        within_window = group[(group['O_timestamp'] >= row['O_timestamp'])
                              & (group['O_timestamp'] <= row['O_timestamp'] + pd.Timedelta(minutes=1))]

        # Step 4: Check price and quantity conditions and opposite sides
        pairs = []
        for (index1, transaction1), (index2, transaction2) in combinations(within_window.iterrows(), 2):
            if (
                abs(transaction1['O_price'] - transaction2['O_price']) <= 1 and
                transaction1['O_qty'] == transaction2['O_qty'] and
                transaction1['O_buy_sell'] != transaction2['O_buy_sell']
            ):
                pairs.append((index1, index2))
        
        # Step 5: Assign group_id for matched pairs
        for index1, index2 in pairs:
            if df.at[index1, 'group_id'] == -1 and df.at[index2, 'group_id'] == -1:
                group_id += 1
                df.at[index1, 'group_id'] = group_id
                df.at[index2, 'group_id'] = group_id
            elif df.at[index1, 'group_id'] != -1:
                df.at[index2, 'group_id'] = df.at[index1, 'group_id']
            elif df.at[index2, 'group_id'] != -1:
                df.at[index1, 'group_id'] = df.at[index2, 'group_id']

# Step 6: Summarized DataFrame (Output 2)
summarized_df = df.groupby('group_id').agg({
    'O_qty': 'sum',
    'O_price': 'mean',
    'O_timestamp': ['min', 'max'],
}).reset_index()
summarized_df.columns = ['group_id', 'total_quantity', 'average_price', 'start_time', 'end_time']

# Step 7: Detailed Matching Pairs (Output 3)
matching_pairs = []
for group_id, group in df.groupby('group_id'):
    if group_id != -1:  # Ignore ungrouped transactions
        for (index1, transaction1), (index2, transaction2) in combinations(group.iterrows(), 2):
            if transaction1['O_buy_sell'] != transaction2['O_buy_sell']:
                matching_pairs.append({
                    'group_id': group_id,
                    'O_id_1': transaction1['O_id'],
                    'O_id_2': transaction2['O_id'],
                    'price_diff': abs(transaction1['O_price'] - transaction2['O_price']),
                    'quantity': transaction1['O_qty'],
                    'timestamp_diff': abs((transaction1['O_timestamp'] - transaction2['O_timestamp']).total_seconds())
                })

matching_pairs_df = pd.DataFrame(matching_pairs)

# Display all three DataFrames to the user
import ace_tools as tools; tools.display_dataframe_to_user(name="Grouped DataFrame with Group IDs", dataframe=df)
tools.display_dataframe_to_user(name="Summarized Aggregated Groups", dataframe=summarized_df)
tools.display_dataframe_to_user(name="Detailed Matching Pairs", dataframe=matching_pairs_df)
