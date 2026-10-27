import pandas as pd
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_absolute_error

train = pd.read_csv("dataset/train.csv")
test = pd.read_csv("dataset/test.csv")

movies = pd.read_csv("dataset/movies.csv")
import os

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="movie_recommendation"
)

cursor = connection.cursor()

rating_matrix = train.pivot_table(
    index="user_id",
    columns="movie_id",
    values="rating"
).fillna(0)

user_similarity = cosine_similarity(rating_matrix)

user_means = train.groupby("user_id")["rating"].mean()


def predict_rating(user_id, movie_id):
    if user_id not in rating_matrix.index:
        return train["rating"].mean()

    if movie_id not in rating_matrix.columns:
        return train["rating"].mean()

    user_index = rating_matrix.index.get_loc(user_id)
    similarities = user_similarity[user_index]

    similar_users = similarities.argsort()[-20:][::-1]

    weighted_sum = 0
    similarity_sum = 0

    for index in similar_users:
        other_user = rating_matrix.index[index]

        if other_user == user_id:
            continue

        rating = rating_matrix.iloc[index][movie_id]

        if rating > 0:
            other_mean = user_means[other_user]
            deviation = rating - other_mean

            weighted_sum += similarities[index] * deviation
            similarity_sum += abs(similarities[index])

    user_mean = user_means[user_id]

    if similarity_sum == 0:
        return user_mean

    prediction = user_mean + (weighted_sum / similarity_sum)

    return max(1, min(5, prediction))


print("Predicted rating:", round(predict_rating(1, 50), 2))


actual = []
predicted = []

for _, row in test.iterrows():
    prediction = predict_rating(
        int(row["user_id"]),
        int(row["movie_id"])
    )

    actual.append(row["rating"])
    predicted.append(prediction)

mae = mean_absolute_error(actual, predicted)

print("\nModel Evaluation")
print("MAE:", round(mae, 4))


def recommend_movies(user_id, top_n=10):
    if user_id not in rating_matrix.index:
        return []

    rated_movies = set(
        train[train["user_id"] == user_id]["movie_id"]
    )

    predictions = []

    for movie_id in rating_matrix.columns:
        if movie_id not in rated_movies:
            prediction = predict_rating(user_id, movie_id)
            predictions.append((movie_id, prediction))

    predictions.sort(key=lambda x: x[1], reverse=True)

    return predictions[:top_n]


recommendations = recommend_movies(1)

print("\nTop 10 Recommendations for User 1:")

for movie_id, prediction in recommendations:
    movie = movies[movies["movie_id"] == movie_id]["title"].iloc[0]
    print(
        "Movie:",
        movie,
        "| Predicted Rating:",
        round(prediction, 2)
    )

cursor.execute(
    "DELETE FROM recommendations WHERE user_id = %s",
    (1,)
)

for movie_id, prediction in recommendations:
    cursor.execute(
        """
        INSERT INTO recommendations
        (user_id, movie_id, predicted_rating)
        VALUES (%s, %s, %s)
        """,
        (1, int(movie_id), round(float(prediction), 2))
    )

connection.commit()

cursor.close()
connection.close()

print("\nRecommendations saved to MySQL.")