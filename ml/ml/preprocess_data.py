import pandas as pd

ratings = pd.read_csv("../../dataset/ratings.csv")

print("First 5 ratings:")
print(ratings.head())

print("\nTotal ratings:", len(ratings))
print("Total users:", ratings["user_id"].nunique())
print("Total movies:", ratings["movie_id"].nunique())

print("\nMissing values:")
print(ratings.isnull().sum())