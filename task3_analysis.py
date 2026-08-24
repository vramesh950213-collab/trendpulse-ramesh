import pandas as pd
import numpy as np

input_file="data/trends_clean.csv"
output_file="data/trends_analysed.csv"

df=pd.read_csv(input_file)

print(f"Loaded data: {df.shape}")

print("\nFirst 5 rows:")
print(df.head())

average_score=df["score"].mean()
average_comments=df["num_comments"].mean()

print(f"\nAverage score : {average_score:,.2f}")
print(f"Average comments: {average_comments:,.2f}")

scores=df["score"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n---Numpy Stats---")
print(f"Mean score    : {mean_score:,.2f}")
print(f"Median score  : {median_score:,.2f}")
print(f"Std deviation : {std_score:,.2f}")
print(f"Max score     : {max_score:,.2f}")
print(f"Min score     : {min_score:,.2f}")

category_counts = df["category"].value_counts()

most_category = category_counts.idxmax()
most_category_count = category_counts.max()

print(
    f"\nMost stories in:"
    f"{most_category} ({most_category_count} stories)"
)

most_commented_index = df["num_comments"].idxmax()

most_commented_title = df.loc[most_commented_index,"title"]
most_commented_count = df.loc[most_commented_index,"num_comments"]

print(
    f"Most commented story:"
    f'"{most_commented_title}" - {most_commented_count:,} comments'
)

df["engagement"] = df["num_comments"] / (df["score"]+1)
df["is_popular"] = df["score"]>average_score

df.to_csv(output_file,index=False)
print(f"\nSaved to {output_file}")
