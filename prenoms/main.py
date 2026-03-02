import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib


def train():
    print("Training model...")
    cols = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "special",
    ]
    df = pd.read_csv("prenoms.csv")
    X, Y = df[cols].values, df["sex"].values

    model = LogisticRegression()
    model.fit(X, Y)
    print("Model trained successfully.")

    return model


letters = "abcdefghijklmnopqrstuvwxyz-"


def predict(model, name):
    print("Predicting...")
    encoded = []
    for letter in letters:
        if letter in name.lower():
            encoded.append(name.count(letter))
        else:
            encoded.append(0)
    print("Predicted successfully.")
    return model.predict([encoded])


if __name__ == "__main__":
    model = train()
    joblib.dump(model, "model.joblib")
