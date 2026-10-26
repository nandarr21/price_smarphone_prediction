# Pembelajaran Mesin: Prediksi Kategori Harga Smartphone (Logistic Regression)

Aplikasi web Flask untuk memprediksi kategori harga smartphone (0-3) dari spesifikasinya,
memakai Logistic Regression multikelas dalam satu `Pipeline` (StandardScaler + LogisticRegression).

Dataset: [Mobile Price Classification (Kaggle)](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification), file `train.csv`.

## Persiapan (Windows)

1. Pasang **Python 3.10+** dari python.org. Saat instalasi, centang **"Add python.exe to PATH"**.
2. Pasang **Visual Studio Code** dan ekstensi **Python** (Microsoft).
3. Unduh `train.csv` dari halaman Kaggle di atas (butuh akun Kaggle gratis).

## Langkah Menjalankan

1. Ekstrak/salin folder proyek, lalu di VS Code pilih **File > Open Folder** dan buka folder `ta03-harga-smartphone`.
2. Letakkan `train.csv` di folder `data/` (buat folder `data` jika belum ada).
3. Buka terminal: menu **Terminal > New Terminal**.
4. Buat virtual environment:
   ```
   python -m venv venv
   ```
5. Aktifkan virtual environment:
   ```
   venv\Scripts\activate
   ```
   Jika muncul galat *"running scripts is disabled"* di PowerShell, jalankan:
   ```
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
   lalu ulangi perintah aktivasi. Atau ganti terminal ke **Command Prompt**.
   Tanda berhasil: muncul `(venv)` di awal baris terminal.
6. (Disarankan) Pilih interpreter: tekan `Ctrl+Shift+P`, ketik **Python: Select Interpreter**, pilih yang berada di `.\venv\`.
7. Pasang pustaka:
   ```
   pip install -r requirements.txt
   ```
8. Latih model (hasil evaluasi dihitung dari dataset Anda):
   ```
   python train_model.py
   ```
   Terminal menampilkan akurasi, classification report, dan ROC-AUC.
   File `models/model_pipeline.joblib`, `models/laporan.json`, dan gambar di `static/img/` akan dibuat.
9. Jalankan aplikasi web:
   ```
   python app.py
   ```
10. Buka browser ke **http://127.0.0.1:5000**. Hentikan server dengan `Ctrl+C`.

## Halaman Aplikasi

| Halaman | Isi |
|---|---|
| Beranda | Ringkasan proyek |
| Dataset | 5 data pertama, ukuran data, info fitur, nilai kosong, distribusi target |
| Evaluasi | Accuracy, Precision, Recall, F1, ROC-AUC, confusion matrix, grafik distribusi kelas |
| Prediksi | Formulir spesifikasi, hasil kategori 0-3, dan probabilitas tiap kelas |

## Mencegah Data Leakage

Data dibagi menjadi latih dan uji **sebelum** scaling. `StandardScaler` berada di dalam `Pipeline`,
sehingga hanya belajar rata-rata dan simpangan baku dari data latih. Saat prediksi, data baru
otomatis melewati scaler yang sama.

## Pemecahan Masalah

- **`'python' is not recognized`**: Python belum masuk PATH. Pasang ulang dan centang "Add to PATH".
- **File train.csv tidak ditemukan**: pastikan letaknya `data/train.csv`.
- **Halaman menampilkan "Model belum tersedia"**: jalankan `python train_model.py`, lalu jalankan ulang `python app.py`.
- **Galat versi scikit-learn saat memuat model**: latih ulang dengan `python train_model.py` di lingkungan yang sama.
- **Port 5000 dipakai**: ubah ke `app.run(debug=True, port=5001)` di `app.py`.