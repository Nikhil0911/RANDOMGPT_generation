import pandas as pd

# Example DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3, 1],
    'B': [4, 5, 6, 4],
    'C': [7, 8, 9, 7],
    'D': [10, 11, 12, 10],
    'E': [13, 14, 15, 16],
    'F': [17, 18, 19, 20]
})

# Function to handle merging in chunks
def merge_in_chunks(df, chunk_size=10000):
    # Generator to yield chunks of the DataFrame
    def chunk_generator(df, chunk_size):
        for start in range(0, len(df), chunk_size):
            yield df[start:start + chunk_size]

    chunks = chunk_generator(df, chunk_size)
    merged_chunks = []

    for chunk in chunks:
        merged_chunk = pd.merge(df, chunk, on=['A', 'B', 'C', 'D'], suffixes=('_left', '_right'))
        filtered_chunk = merged_chunk[(merged_chunk['E_left'] != merged_chunk['E_right']) & 
                                      (merged_chunk['F_left'] != merged_chunk['F_right'])]
        merged_chunks.append(filtered_chunk)

    return pd.concat(merged_chunks, ignore_index=True)

# Perform the memory-efficient merge and filter
result_df = merge_in_chunks(df)

# Display the result
print(result_df)
