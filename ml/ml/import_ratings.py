import pandas as pd
import mysql.connector

df = pd.read_csv("../../dataset/ratings.csv")
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SQLpassword",
    database="movie_recommendation"
)

cursor = connection.cursor()

data = list(df[["user_id", "movie_id", "rating", "rated_at"]].itertuples(index=False, name=None))

query = """
INSERT INTO ratings (user_id, movie_id, rating, rated_at)
VALUES (%s, %s, %s, %s)
"""

for i in range(0, len(data), 5000):
    batch = data[i:i+5000]
    cursor.executemany(query, batch)
    connection.commit()
    print(f"Imported {min(i + 5000, len(data))} / {len(data)} ratings")

cursor.close()
connection.close()

print("All ratings imported successfully.")