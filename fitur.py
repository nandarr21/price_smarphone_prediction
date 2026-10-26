# tipe: "int" = bilangan bulat, "float" = desimal, "biner" = 0/1 (Tidak/Ya)
FITUR = [
    {"nama": "battery_power", "label": "Daya baterai (mAh)", "tipe": "int"},
    {"nama": "blue", "label": "Bluetooth", "tipe": "biner"},
    {"nama": "clock_speed", "label": "Kecepatan prosesor (GHz)", "tipe": "float"},
    {"nama": "dual_sim", "label": "Dual SIM", "tipe": "biner"},
    {"nama": "fc", "label": "Kamera depan (MP)", "tipe": "int"},
    {"nama": "four_g", "label": "Dukungan 4G", "tipe": "biner"},
    {"nama": "int_memory", "label": "Memori internal (GB)", "tipe": "int"},
    {"nama": "m_dep", "label": "Ketebalan (cm)", "tipe": "float"},
    {"nama": "mobile_wt", "label": "Berat (gram)", "tipe": "int"},
    {"nama": "n_cores", "label": "Jumlah inti prosesor", "tipe": "int"},
    {"nama": "pc", "label": "Kamera utama (MP)", "tipe": "int"},
    {"nama": "px_height", "label": "Tinggi resolusi (piksel)", "tipe": "int"},
    {"nama": "px_width", "label": "Lebar resolusi (piksel)", "tipe": "int"},
    {"nama": "ram", "label": "RAM (MB)", "tipe": "int"},
    {"nama": "sc_h", "label": "Tinggi layar (cm)", "tipe": "int"},
    {"nama": "sc_w", "label": "Lebar layar (cm)", "tipe": "int"},
    {"nama": "talk_time", "label": "Waktu bicara maksimal (jam)", "tipe": "int"},
    {"nama": "three_g", "label": "Dukungan 3G", "tipe": "biner"},
    {"nama": "touch_screen", "label": "Layar sentuh", "tipe": "biner"},
    {"nama": "wifi", "label": "Wi-Fi", "tipe": "biner"},
]

NAMA_FITUR = [f["nama"] for f in FITUR]
TARGET = "price_range"

LABEL_KELAS = {
    0: "Murah",
    1: "Menengah",
    2: "Tinggi",
    3: "Sangat Tinggi",
}