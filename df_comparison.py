import pandas as pd
import numpy as np

# ---------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------
df1 = pd.DataFrame({
    "name": ["John", "Alice", "Bob", "David"],
    "city": ["Delhi", "Mumbai", "Pune", "Chennai"],
    "amount": [100, 200, 300, 400]
})

df2 = pd.DataFrame({
    "name": ["John", "Alicia", "Bob", "David"],
    "city": ["Delhi", "Mumbai", "Pune", "Chennai"],
    "amount": [100, 250, 300, 450]
})

COMPARE_COLUMNS = ["name", "city", "amount"]
THRESHOLD = 0.7

# ---------------------------------------------------
# STEP 1: CREATE BLOCKING KEY
# Reduce comparisons drastically
# ---------------------------------------------------
# Example:
# Compare only rows having same city

df1["block_key"] = df1["city"].astype(str).str.lower()
df2["block_key"] = df2["city"].astype(str).str.lower()

# ---------------------------------------------------
# STEP 2: GROUP SECOND DF
# Fast lookup
# ---------------------------------------------------
df2_groups = {
    key: grp.reset_index()
    for key, grp in df2.groupby("block_key")
}

# ---------------------------------------------------
# STEP 3: MATCH
# ---------------------------------------------------
used_df2 = set()
results = []

total_cols = len(COMPARE_COLUMNS)

for idx1, row1 in df1.iterrows():

    block = row1["block_key"]

    # Skip if no candidate exists
    if block not in df2_groups:
        continue

    candidates = df2_groups[block]

    best_match = None
    best_score = -1

    # Compare only small subset
    for _, row2 in candidates.iterrows():

        idx2 = row2["index"]

        # ensure unique matching
        if idx2 in used_df2:
            continue

        match_count = 0
        matched_cols = []

        for col in COMPARE_COLUMNS:

            v1 = row1[col]
            v2 = row2[col]

            if pd.isna(v1) and pd.isna(v2):
                is_match = True
            else:
                is_match = v1 == v2

            if is_match:
                match_count += 1
                matched_cols.append(col)

        score = match_count / total_cols

        if score > best_score:
            best_score = score

            best_match = {
                "df1_index": idx1,
                "df2_index": idx2,
                "match_percent": round(score * 100, 2),
                "match_count": match_count,
                "matched_columns": matched_cols
            }

    # Keep only threshold matches
    if best_match and best_score >= THRESHOLD:

        results.append(best_match)
        used_df2.add(best_match["df2_index"])

# ---------------------------------------------------
# FINAL OUTPUT
# ---------------------------------------------------
result_df = pd.DataFrame(results)

print(result_df)