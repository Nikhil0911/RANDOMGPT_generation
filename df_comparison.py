
import pandas as pd
import numpy as np

# -----------------------------
# SAMPLE DATA
# -----------------------------
df1 = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["John", "Alice", "Bob"],
    "city": ["Delhi", "Mumbai", "Pune"],
    "amount": [100, 200, 300]
})

df2 = pd.DataFrame({
    "id": [11, 12, 13],
    "name": ["John", "Alicia", "Bob"],
    "city": ["Delhi", "Mumbai", "Pune"],
    "amount": [100, 250, 300]
})

# -----------------------------
# CONFIG
# -----------------------------
MATCH_THRESHOLD = 0.70     # 70%
COMPARE_COLUMNS = ["name", "city", "amount"]

# -----------------------------
# PREP
# -----------------------------
total_cols = len(COMPARE_COLUMNS)

results = []

# To ensure one row matches only once
used_df1 = set()
used_df2 = set()

# -----------------------------
# COMPARE ALL ROWS
# -----------------------------
all_matches = []

for i, row1 in df1.iterrows():

    for j, row2 in df2.iterrows():

        matched_cols = []
        unmatched_cols = []

        match_count = 0

        for col in COMPARE_COLUMNS:

            val1 = row1[col]
            val2 = row2[col]

            # Handle NaN comparison
            if pd.isna(val1) and pd.isna(val2):
                is_match = True
            else:
                is_match = val1 == val2

            if is_match:
                match_count += 1
                matched_cols.append(col)
            else:
                unmatched_cols.append(col)

        match_percent = match_count / total_cols

        # Keep only >=70% matches
        if match_percent >= MATCH_THRESHOLD:

            all_matches.append({
                "df1_index": i,
                "df2_index": j,
                "match_count": match_count,
                "total_columns": total_cols,
                "match_percent": round(match_percent * 100, 2),
                "matched_columns": matched_cols,
                "unmatched_columns": unmatched_cols
            })

# -----------------------------
# SORT BEST MATCHES FIRST
# -----------------------------
all_matches = sorted(
    all_matches,
    key=lambda x: x["match_count"],
    reverse=True
)

# -----------------------------
# UNIQUE MATCHING
# One row can match only once
# -----------------------------
final_matches = []

for match in all_matches:

    i = match["df1_index"]
    j = match["df2_index"]

    if i not in used_df1 and j not in used_df2:

        final_matches.append(match)

        used_df1.add(i)
        used_df2.add(j)

# -----------------------------
# FINAL OUTPUT
# -----------------------------
result_df = pd.DataFrame(final_matches)

print(result_df)


### Output Example

| df1_index | df2_index | match_count | total_columns | match_percent |
| --------- | --------- | ----------- | ------------- | ------------- |
| 0         | 0         | 3           | 3             | 100           |
| 2         | 2         | 3           | 3             | 100           |

---

### What This Code Does

* Compares every row of `df1` with every row of `df2`
* Counts how many columns match
* Keeps only rows with ≥ 70% match
* Ensures:

  * one row from `df1` matches only once
  * one row from `df2` matches only once
* Picks the best possible match first

---

### You Can Easily Extend This

You can add:

* fuzzy string matching
* tolerance for numeric values
* ignored columns
* weighted matching
* output unmatched rows separately
* very fast optimized version for large datasets

For reconciliation tasks like yours, fuzzy matching + tolerance-based matching becomes very useful.
