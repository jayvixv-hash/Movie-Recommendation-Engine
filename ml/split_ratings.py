import pandas as pd

df = pd.read_csv("../dataset/ratings.csv")

for i in range(0, len(df), 10000):
    chunk = df.iloc[i:i+10000]
    chunk.to_csv(f"../dataset/ratings_{i//10000 + 1}.csv", index=False)

print("Created 10 rating files.")