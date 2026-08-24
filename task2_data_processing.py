import pandas as pd

input_file="data/trends_20260823.json"

df = pd.read_json(input_file)

print(f"Loaded {len(df)} stories from {input_file}")

df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")

df = df.dropna(
    subset=["post_id","title","score"]
)

print(f"After removing nulls: {len(df)}")

df["score"] = pd.to_numeric(df["score"], errors="coerce")

df["num_comments"]=pd.to_numeric(df["num_comments"], errors="coerce")

df = df.dropna(
    subset=["score","num_comments"]
)

df["score"] = df["score"].astype(int) 
df["num_comments"] = df["num_comments"].astype(int)

df = df[df["score"]>=5]

print(f"After removing low scores: {len(df)}")

df["title"] = df["title"].str.strip()

output_file = "data/trends_clean.csv"

df.to_csv(output_file,index=False)

print(f"\nStories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
  print(f" {category:<15} {count}")
