import pandas as pd
from sklearn.model_selection import train_test_split

ratings = pd.read_csv("../../dataset/ratings.csv")

train, test = train_test_split(
    ratings,
    test_size=0.2,
    random_state=42
)

train.to_csv("../../dataset/train.csv", index=False)
test.to_csv("../../dataset/test.csv", index=False)

print("Training ratings:", len(train))
print("Testing ratings:", len(test))
print("Total ratings:", len(train) + len(test))