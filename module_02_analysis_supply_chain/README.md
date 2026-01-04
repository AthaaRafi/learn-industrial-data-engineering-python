# Analisis Bottleneck Logistik & Cost of Poor Quality (Olist E-Commerce)

## 1. Masalah Bisnis
Perusahaan logistik mengalami keluhan keterlambatan pengiriman dan ingin mengetahui:
1. Akar masalah keterlambatan (Lokasi/Rute).
2. Biaya yang terbuang akibat pembatalan pesanan (*Cost of Poor Quality*).

## 2. Metodologi yang digunakan
* **Data Cleaning:** Melalukan Data Cleaning dengan memisahkan data yang kurang lengkap (tanggal delivernya tidak tercatat) dengan data yang sudah lengkap. Selanjutnya juga memisahkan order status yang delivered dengan yang unavailable serta cancelled
* **Melakukan Perhitungan:** Menghitung *Lead Time* aktual vs estimasi tanpa menggunakan Loop (Vectorized Operation).
* **Integrity Check:** Menggunakan `pd.merge` (Inner Join) dengan tujuan agar saat di merge sesuai dengan order id dan tidak acak.

## 3. Temuan Utama (Key Insights)
* **Pareto Analysis:** Ditemukan bahwa **Sao Paulo (SP)** dan **Rio de Janeiro (RJ)** secara kumulatif menyumbang lebih dari **50%** total kasus keterlambatan. Perbaikan operasional harus diprioritaskan di dua hub ini.
* **Financial Leakage:** Teridentifikasi kerugian sebesar **10,783** pada *Freight Value* untuk pesanan yang statusnya *canceled* atau *unavailable*.

## 4. Rekomendasi
1. Lakukan audit proses serah terima barang di Hub SP & RJ.
2. Cegah input status 'delivered' jika tanggal kosong.