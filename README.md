# 🌊 WaveSend

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

**WaveSend** adalah *Command Line Interface* (CLI) tool berbasis Python dan Selenium WebDriver untuk otomatisasi pengiriman pesan WhatsApp Web. Dibangun dengan arsitektur berorientasi objek (OOP), dilengkapi algoritma *Humanized Delay* dan clipboard injection untuk pengiriman teks yang stabil.

Dibuat untuk kebutuhan personal — reminder ke channel/grup sendiri, broadcast ke kontak yang sudah opt-in, atau eksperimen belajar browser automation dengan Selenium.

---

## ⚠️ Batasan Penggunaan

> Tool ini **hanya untuk digunakan pada nomor/kontak milik sendiri atau kontak yang sudah memberi izin eksplisit** untuk menerima pesan berulang (misalnya reminder komunitas opt-in, broadcast ke grup kerja yang sudah setuju).
>
> **Dilarang digunakan untuk** mengirim pesan tanpa izin ke pihak lain, harassment, atau pelanggaran Terms of Service WhatsApp/Meta. Fitur pengiriman berulang di tool ini dibuat untuk kasus seperti reminder ke channel sendiri — bukan untuk membanjiri chat orang lain. Penggunaan di luar itu sepenuhnya tanggung jawab pengguna dan tidak didukung oleh developer.

---

## ✨ Arsitektur & Fitur Utama

| Fitur | Deskripsi |
|---|---|
| 🛡️ **Humanized Delay** | Jeda antar pesan diacak (1.5–3.5 detik) agar ritme pengiriman lebih wajar dan tidak membebani sistem WhatsApp |
| 💾 **Persistent Session** | Sesi login tersimpan lokal di folder `chrome_profile`, cukup scan QR sekali |
| 📋 **Clipboard Injection** | Menggunakan `pyperclip` untuk menyalin teks panjang/kompleks langsung ke clipboard OS, menghindari masalah rendering saat mengetik manual |
| 💻 **Interactive CLI** | Antarmuka terminal berbasis `rich` dan `pyfiglet`, rapi dan informatif |
| 📄 **3 Mode Pengiriman** | Manual (terminal), File (`.txt`), dan Interactive (ketik langsung di WhatsApp Web) |

---

## 🚀 Instalasi

Pastikan sudah terinstal [Python](https://www.python.org/downloads/) 3.10+ dan **Google Chrome**.

**1. Clone repositori:**
```bash
git clone https://github.com/nezmajesty-dev/WaveSend.git
cd WaveSend
```

**2. Instal dependensi:**
```bash
pip install -r requirements.txt
```

**3. Jalankan:**
```bash
python main.py
```

---

## ⚙️ Panduan Mode Operasi

Saat pertama kali dijalankan, Chrome akan terbuka otomatis. Pindai QR Code dengan WhatsApp di ponsel. Setelah terminal menampilkan `auth --success`, pilih salah satu mode:

**`[1] send --manual`**
Mode standar. Masukkan nomor target (format `628...`), isi pesan, dan jumlah pengulangan langsung di terminal.

**`[2] send --file`**
Untuk pesan berukuran besar. Siapkan file `.txt` (misal `pesan.txt`) di folder project, lalu masukkan nama filenya saat diminta.

**`[3] send --interactive`**
Ketik pesan langsung di kolom WhatsApp Web (mendukung emoji native), lalu tekan Enter di terminal untuk memproses dan mengirim.

---

## 🤝 Kontribusi

Pull Request dipersilakan. Untuk perubahan besar (misal migrasi ke arsitektur WebSocket/API resmi), buka issue terlebih dahulu untuk didiskusikan.

---

**Developed with ☕ by [nez](https://github.com/nezmajesty-dev)**
