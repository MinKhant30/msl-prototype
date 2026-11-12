from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "raw" / "landmarks.csv"
CLEAN_PATH = ROOT_DIR / "data" / "raw" / "landmarks_clean.csv"


def main():
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["label"]).values
    y = df["label"].values

    # 5-fold out-of-sample probability prediction:
    # Each row is predicted by models that NEVER saw that row during training
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof_probs = cross_val_predict(clf, X, y, cv=cv, method="predict_proba")

    classes = np.unique(y)
    class_to_idx = {c: i for i, c in enumerate(classes)}

    # Check the model's predicted probability for the GIVEN (human-assigned) label
    given_label_probs = np.array([oof_probs[i, class_to_idx[label]] for i, label in enumerate(y)])
    predicted_labels = classes[np.argmax(oof_probs, axis=1)]

    # Flag rows where the model strongly disagrees with the recorded label (< 30% confidence)
    suspect_mask = given_label_probs < 0.30
    suspects = df[suspect_mask].copy()
    suspects["recorded_label"] = y[suspect_mask]
    suspects["model_thinks_it_is"] = predicted_labels[suspect_mask]
    suspects["given_label_confidence"] = np.round(given_label_probs[suspect_mask], 3)

    print(f"Total rows scanned: {len(df)}")
    print(f"Suspected mislabeled rows found: {len(suspects)}\n")

    if len(suspects) > 0:
        print(suspects[["recorded_label", "model_thinks_it_is", "given_label_confidence"]].head(20))

    # Save cleaned dataset with suspected mistakes removed
    clean_df = df[~suspect_mask]
    clean_df.to_csv(CLEAN_PATH, index=False)
    print(f"\nSaved {len(clean_df)} clean rows to {CLEAN_PATH}")


if __name__ == "__main__":
    main()