import pandas as pd

df = pd.read_csv("../dataset/movies.csv")

with open("../dataset/movies_insert.sql", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        movie_id = int(row["movie_id"])
        title = str(row["title"]).replace("'", "''")

        if pd.isna(row["release_date"]):
            release_date = "NULL"
        else:
            date = pd.to_datetime(row["release_date"], format="%d-%b-%Y")
            release_date = f"'{date.strftime('%Y-%m-%d')}'"

        f.write(
            f"INSERT INTO movies (movie_id, title, release_date) "
            f"VALUES ({movie_id}, '{title}', {release_date});\n"
        )