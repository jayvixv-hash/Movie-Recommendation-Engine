import pandas as pd

df = pd.read_csv(
    "../dataset/u.data",
    sep="\t",
    names=["user_id", "movie_id", "rating", "timestamp"]
)

df["rated_at"] = pd.to_datetime(df["timestamp"], unit="s")

df = df[["user_id", "movie_id", "rating", "rated_at"]]

df.to_csv("../dataset/ratings.csv", index=False)