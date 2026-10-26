import json
import sys
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")  # backend tanpa jendela, aman untuk server
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from fitur import LABEL_KELAS, NAMA_FITUR, TARGET

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "train.csv"
MODEL_DIR = BASE_DIR / "models"
IMG_DIR = BASE_DIR / "public" / "img"
MODEL_PATH = MODEL_DIR / "model_pipeline.joblib"
LAPORAN_PATH = MODEL_DIR / "laporan.json"


def ke_python(nilai):
    """Ubah tipe numpy menjadi tipe Python biasa agar bisa disimpan ke JSON."""
    return nilai.item() if hasattr(nilai, "item") else nilai


def main():
    # ---------- 1. Muat dataset ----------
    if not DATA_PATH.exists():
        print(f"[GAGAL] File tidak ditemukan: {DATA_PATH}")
        print("Unduh train.csv dari Kaggle lalu letakkan di folder 'data'.")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    kolom_hilang = [k for k in NAMA_FITUR + [TARGET] if k not in df.columns]
    if kolom_hilang:
        print(f"[GAGAL] Kolom tidak ada di train.csv: {kolom_hilang}")
        sys.exit(1)

    MODEL_DIR.mkdir(exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    # ---------- 2. Analisis dataset ----------
    info_fitur = []
    for kolom in df.columns:
        info_fitur.append({
            "kolom": kolom,
            "tipe": str(df[kolom].dtype),
            "non_null": int(df[kolom].notna().sum()),
            "unik": int(df[kolom].nunique()),
            "min": ke_python(df[kolom].min()),
            "max": ke_python(df[kolom].max()),
        })

    distribusi = df[TARGET].value_counts().sort_index()
    statistik_fitur = {
        k: {
            "min": ke_python(df[k].min()),
            "max": ke_python(df[k].max()),
            "mean": round(float(df[k].mean()), 3),
        }
        for k in NAMA_FITUR
    }

    # Grafik distribusi kelas
    plt.figure(figsize=(6, 4))
    ax = sns.countplot(data=df, x=TARGET, hue=TARGET, palette="Blues", legend=False)
    for wadah in ax.containers:
        ax.bar_label(wadah)
    ax.set_title("Distribusi Kelas price_range")
    ax.set_xlabel("Kategori harga (0-3)")
    ax.set_ylabel("Jumlah data")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "distribusi_kelas.png", dpi=120)
    plt.close()

    # ---------- 3. Preprocessing ----------
    X = df[NAMA_FITUR]
    y = df[TARGET]

    # Pembagian data SEBELUM scaling -> scaler hanya belajar dari data latih
    X_latih, X_uji, y_latih, y_uji = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ---------- 4. Pipeline: StandardScaler + Logistic Regression ----------
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    model.fit(X_latih, y_latih)

    # ---------- 5. Evaluasi ----------
    y_pred = model.predict(X_uji)
    y_proba = model.predict_proba(X_uji)
    kelas = list(model.classes_)

    akurasi_uji = accuracy_score(y_uji, y_pred)
    akurasi_latih = accuracy_score(y_latih, model.predict(X_latih))
    prec, rec, f1, sup = precision_recall_fscore_support(
        y_uji, y_pred, labels=kelas, zero_division=0
    )
    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(
        y_uji, y_pred, average="macro", zero_division=0
    )
    auc = roc_auc_score(y_uji, y_proba, multi_class="ovr", average="macro")
    cm = confusion_matrix(y_uji, y_pred, labels=kelas)

    print("=== HASIL EVALUASI (data uji) ===")
    print(f"Akurasi data latih : {akurasi_latih:.4f}")
    print(f"Akurasi data uji   : {akurasi_uji:.4f}")
    print(f"ROC-AUC (OvR macro): {auc:.4f}")
    print(classification_report(y_uji, y_pred, digits=4, zero_division=0))

    # Grafik confusion matrix
    plt.figure(figsize=(5.5, 4.5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=kelas, yticklabels=kelas)
    plt.title("Confusion Matrix (Data Uji)")
    plt.xlabel("Prediksi")
    plt.ylabel("Aktual")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "confusion_matrix.png", dpi=120)
    plt.close()

    # ---------- 6. Simpan model & laporan ----------
    joblib.dump(model, MODEL_PATH)

    laporan = {
        "jumlah_baris": int(df.shape[0]),
        "jumlah_kolom": int(df.shape[1]),
        "head_html": df.head().to_html(classes="tabel", index=False, border=0),
        "info_fitur": info_fitur,
        "total_nilai_kosong": int(df.isnull().sum().sum()),
        "distribusi_target": [
            {"kelas": int(k), "label": LABEL_KELAS[int(k)], "jumlah": int(v)}
            for k, v in distribusi.items()
        ],
        "ukuran_latih": int(len(X_latih)),
        "ukuran_uji": int(len(X_uji)),
        "metrik": {
            "akurasi_latih": float(akurasi_latih),
            "akurasi_uji": float(akurasi_uji),
            "precision_macro": float(prec_m),
            "recall_macro": float(rec_m),
            "f1_macro": float(f1_m),
            "roc_auc_ovr_macro": float(auc),
        },
        "per_kelas": [
            {
                "kelas": int(k),
                "label": LABEL_KELAS[int(k)],
                "precision": float(prec[i]),
                "recall": float(rec[i]),
                "f1": float(f1[i]),
                "support": int(sup[i]),
            }
            for i, k in enumerate(kelas)
        ],
        "confusion_matrix": cm.tolist(),
        "statistik_fitur": statistik_fitur,
    }
    with open(LAPORAN_PATH, "w", encoding="utf-8") as berkas:
        json.dump(laporan, berkas, ensure_ascii=False, indent=2)

    print(f"\n[OK] Model disimpan di : {MODEL_PATH}")
    print(f"[OK] Laporan disimpan di: {LAPORAN_PATH}")


if __name__ == "__main__":
    main()