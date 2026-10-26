"""Aplikasi web Flask: prediksi kategori harga smartphone."""
import json
import math
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, render_template, request

from fitur import FITUR, LABEL_KELAS, NAMA_FITUR

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "model_pipeline.joblib"
LAPORAN_PATH = BASE_DIR / "models" / "laporan.json"

# Folder statis = "public" (wajib agar sama dengan Vercel). Alamat tetap /css/..., /img/...
app = Flask(__name__, static_folder="public", static_url_path="")

# Muat model & laporan sekali saat aplikasi dijalankan
model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
laporan = None
if LAPORAN_PATH.exists():
    with open(LAPORAN_PATH, encoding="utf-8") as berkas:
        laporan = json.load(berkas)

SIAP = model is not None and laporan is not None

# Gabungkan definisi fitur dengan rentang min/max dari dataset
DAFTAR_FITUR = []
if SIAP:
    for f in FITUR:
        stat = laporan["statistik_fitur"][f["nama"]]
        DAFTAR_FITUR.append({**f, "min": stat["min"], "max": stat["max"]})


def validasi_input(form):
    """Periksa setiap isian. Mengembalikan (nilai_valid, pesan_galat)."""
    nilai, galat = {}, {}
    for f in DAFTAR_FITUR:
        nama = f["nama"]
        mentah = form.get(nama, "").strip().replace(",", ".")

        if mentah == "":
            galat[nama] = "Wajib diisi."
            continue
        try:
            angka = float(mentah)
        except ValueError:
            galat[nama] = "Harus berupa angka."
            continue
        if not math.isfinite(angka):
            galat[nama] = "Angka tidak valid."
            continue

        if f["tipe"] == "biner":
            if angka not in (0.0, 1.0):
                galat[nama] = "Pilih Ya atau Tidak."
                continue
        else:
            if f["tipe"] == "int" and not angka.is_integer():
                galat[nama] = "Harus bilangan bulat."
                continue
            if not f["min"] <= angka <= f["max"]:
                galat[nama] = f"Harus di antara {f['min']} dan {f['max']}."
                continue

        nilai[nama] = int(angka) if f["tipe"] in ("int", "biner") else angka
    return nilai, galat


@app.route("/")
def beranda():
    return render_template("beranda.html", siap=SIAP, laporan=laporan)


@app.route("/dataset")
def dataset():
    if not SIAP:
        return render_template("belum_siap.html")
    return render_template("dataset.html", laporan=laporan)


@app.route("/evaluasi")
def evaluasi():
    if not SIAP:
        return render_template("belum_siap.html")
    return render_template("evaluasi.html", laporan=laporan)


@app.route("/prediksi", methods=["GET", "POST"])
def prediksi():
    if not SIAP:
        return render_template("belum_siap.html")

    nilai_form, galat, hasil = {}, {}, None

    if request.method == "POST":
        nilai_form = request.form.to_dict()
        nilai, galat = validasi_input(request.form)

        if not galat:
            # Urutan kolom harus sama dengan saat training
            X_baru = pd.DataFrame([nilai], columns=NAMA_FITUR)
            kelas_prediksi = int(model.predict(X_baru)[0])
            proba = model.predict_proba(X_baru)[0]
            hasil = {
                "kelas": kelas_prediksi,
                "label": LABEL_KELAS[kelas_prediksi],
                "probabilitas": [
                    {
                        "kelas": int(k),
                        "label": LABEL_KELAS[int(k)],
                        "persen": round(float(p) * 100, 2),
                    }
                    for k, p in zip(model.classes_, proba)
                ],
            }

    return render_template(
        "prediksi.html",
        fitur=DAFTAR_FITUR,
        nilai_form=nilai_form,
        galat=galat,
        hasil=hasil,
    )


if __name__ == "__main__":
    app.run(debug=True)