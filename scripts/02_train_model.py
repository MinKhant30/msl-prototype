import sys
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "raw" / "landmarks.csv"
MODEL_OUT_PATH = ROOT_DIR / "models" / "msl_classifier.joblib"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run 01_collect_data.py first.")

    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} total samples:")
    print(df["label"].value_counts(), "\n")

    X = df.drop(columns=["label"]).values
    y = df["label"].values

    # Stratified 80/20 split keeps class proportions equal in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    MODEL_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_OUT_PATH)
    print(f"Saved trained classifier to {MODEL_OUT_PATH}")


if __name__ == "__main__":
    main()