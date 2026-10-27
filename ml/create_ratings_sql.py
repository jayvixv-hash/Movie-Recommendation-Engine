import pandas as pd

df = pd.read_csv(
    "../dataset/u.data",
    sep="\t",
    names=["user_id", "movie_id", "rating", "timestamp"]
)

with open("../dataset/ratings_insert.sql", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        user_id = int(row["user_id"])
        movie_id = int(row["movie_id"])
        rating = int(row["rating"])

        rated_at = pd.to_datetime(
            row["timestamp"], unit="s"
        ).strftime("%Y-%m-%d %H:%M:%S")

        f.write(
            f"INSERT INTO ratings (user_id, movie_id, rating, rated_at) "
            f"VALUES ({user_id}, {movie_id}, {rating}, '{rated_at}');\n"
        )