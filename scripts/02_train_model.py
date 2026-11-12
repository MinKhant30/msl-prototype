from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
MODEL_OUT_PATH = ROOT_DIR / "models" / "msl_classifier.joblib"


def main():
    csv_files = sorted(RAW_DATA_DIR.glob("landmarks*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DATA_DIR}. Run 01_collect_data.py first.")

    df_list = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(df_list, ignore_index=True)

    print(f"Merged {len(csv_files)} file(s) -> {len(df)} total samples:")
    print(df["label"].value_counts(), "\n")

   # Drop metadata columns if present so X contains only the 63 landmark features
    feature_cols = [c for c in df.columns if c not in ("label", "member_key", "collector", "timestamp")]
    X = df[feature_cols].values
    y = df["label"].values

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