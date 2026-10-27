import pandas as pd

ratings = pd.read_csv(
    "../dataset/u.data",
    sep="\t",
    names=["user_id", "movie_id", "rating", "timestamp"]
)

movies = pd.read_csv(
    "../dataset/u.item",
    sep="|",
    encoding="latin-1",
    header=None
)

print("First 5 ratings:")
print(ratings.head())

print("\nTotal ratings:", len(ratings))
print("Total users:", ratings["user_id"].nunique())
print("Total movies:", ratings["movie_id"].nunique())

print("\nMissing values:")
print(ratings.isnull().sum())