import pandas as pd

ratings = pd.read_csv("../../dataset/ratings.csv")

rating_matrix = ratings.pivot_table(
    index="user_id",
    columns="movie_id",
    values="rating"
)

print("Rating matrix shape:", rating_matrix.shape)

print("\nFirst 5 rows:")
print(rating_matrix.head())

print("\nMissing values in matrix:", rating_matrix.isnull().sum().sum())

rating_matrix.to_csv("../../dataset/rating_matrix.csv")

print("\nRating matrix saved successfully.")