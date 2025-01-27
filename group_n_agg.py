import pandas as pd

# Sample dummy data for testing
data = {
    'O_id': [1, 2, 3, 4, 5, 6],
    'O_book_id': ['Book1', 'Book1', 'Book2', 'Book2', 'Book1', 'Book1'],
    'O_buy_sell': ['B', 'S', 'B', 'S', 'B', 'S'],
    'O_isin_code': ['ABC', 'ABC', 'XYZ', 'XYZ', 'ABC', 'ABC'],
    'O_qty': [100, 100, 200, 200, 100, 100],
    'O_price': [50, 50.5, 30, 30.8, 49.5, 50.4],
    'O_timestamp': [
        '2025-01-01 10:00:00',
        '2025-01-01 10:00:30',
        '2025-01-01 10:01:00',
        '2025-01-01 10:01:30',
        '2025-01-01 10:02:00',
        '2025-01-01 10:02:30',
    ],
}

# Step 1: Create DataFrame and preprocess
df = pd.DataFrame(data)
df['O_timestamp'] = pd.to_datetime(df['O_timestamp'])
df = df.sort_values(by='O_timestamp')

# Step 2: Create potential matches using a self-join on rolling 1-minute windows
df['time_group'] = df['O_timestamp'].dt.floor('1min')
merged = df.merge(
    df,
    on=['O_book_id', 'O_isin_code', 'O_buy_sell', 'time_group'],  # Include O_buy_sell
    suffixes=('_1', '_2'),
).query(
    "O_id_1 < O_id_2"  # Avoid self-matches and duplicates
)

# Step 3: Filter matches based on conditions
filtered = merged[
    (abs(merged['O_price_1'] - merged['O_price_2']) <= 1) &  # Price difference
    (merged['O_qty_1'] == merged['O_qty_2']) &              # Quantity match
    (merged['O_buy_sell_1'] != merged['O_buy_sell_2'])      # Opposite buy/sell
]

# Step 4: Assign group_id to matched pairs
filtered['group_id'] = (
    filtered.groupby(['O_book_id', 'O_isin_code', 'O_buy_sell']).cumcount() + 1
)

# Step 5: Create the grouped DataFrame
grouped_df = df.copy()
grouped_df = grouped_df.merge(
    filtered[['O_id_1', 'group_id']].rename(columns={'O_id_1': 'O_id'}),
    on='O_id',
    how='left'
)

# Step 6: Create summarized DataFrame
summarized_df = grouped_df.groupby('group_id').agg(
    total_quantity=('O_qty', 'sum'),
    average_price=('O_price', 'mean'),
    start_time=('O_timestamp', 'min'),
    end_time=('O_timestamp', 'max')
).reset_index()

# Step 7: Create detailed matching pairs DataFrame
detailed_matches = filtered[
    [
        'group_id', 'O_id_1', 'O_book_id_1', 'O_isin_code_1', 'O_buy_sell_1',
        'O_qty_1', 'O_price_1', 'O_timestamp_1',
        'O_id_2', 'O_book_id_2', 'O_isin_code_2', 'O_buy_sell_2',
        'O_qty_2', 'O_price_2', 'O_timestamp_2'
    ]
].copy()
detailed_matches['price_diff'] = abs(detailed_matches['O_price_1'] - detailed_matches['O_price_2'])
detailed_matches['timestamp_diff'] = (
    detailed_matches['O_timestamp_1'] - detailed_matches['O_timestamp_2']
).abs().dt.total_seconds()

# Display all three DataFrames
import ace_tools as tools
tools.display_dataframe_to_user(name="Grouped DataFrame with Group IDs", dataframe=grouped_df)
tools.display_dataframe_to_user(name="Summarized Aggregated Groups", dataframe=summarized_df)
tools.display_dataframe_to_user(name="Detailed Matching Pairs", dataframe=detailed_matches)
