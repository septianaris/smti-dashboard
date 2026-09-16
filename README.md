# Dashboard Monitoring Proyek & Kinerja Departemen SMTI
### PT Pupuk Kujang Cikampek

Aplikasi dashboard modern berbasis web untuk pemantauan proyek, kinerja karyawan, reminder deadline, dan alur progres kerja (workflow pipeline) Departemen Sistem Manajemen Terpadu & Inovasi (SMTI).

---

## 🚀 Fitur Utama

1. **Ringkasan Performa & KPI SMTI**:
   - Tingkat penyelesaian proyek, pencapaian target, dan evaluasi kinerja tim.
   - Status urgensi proyek: Prioritas Utama (Tinggi), Dalam Pengawalan (Sedang), dan Rutin & Monitoring.

2. **Proyek Berjalan & 3 Bidang SMTI**:
   - **MIKU** (Manajemen Inovasi & Kinerja Unggul)
   - **PMSMT** (Pengendalian Manajemen SMT)
   - **Pengembangan Sistem dan Prosedur**
   - Filter interaktif berdasarkan tingkat urgensi dan bidang kerja.

3. **Alur Progres & Interactive Step Builder**:
   - Visualisasi alur kerja 5 tahap (Pipeline Flow Stepper).
   - Builder tahapan kerja dinamis: Preset template alur kerja atau input manual bebas.
   - Checklist kegiatan per tahap yang dapat ditambah/diedit manual.
   - Catatan progres & komentar tim dengan timestamp otomatis.

4. **Layar Monitor TV (Live Board Kiosk Mode)**:
   - Tampilan khusus layar monitor TV / pengingat deadline.
   - Running ticker pengingat darurat (urgent alert).
   - Jam digital besar dan tema gelap/terang.
   - Filter interaktif kolom (Tinggi, Sedang, Rutin) dengan tata letak grid melebar responsif.
   - Dukungan tombol keyboard shortcut untuk operator TV (Angka 1-4, Esc, Fullscreen).

5. **Laporan & Manajemen Karyawan**:
   - Profil tim SMTI, sertifikasi keahlian, dan penugasan proyek.
   - Ekspor data proyek ke format CSV / Excel.

---

## 💻 Cara Menjalankan Secara Lokal

```bash
# Jalankan server lokal menggunakan Python
python -m http.server 8000
```
Buka browser di `http://localhost:8000` atau melalui IP lokal jaringan kantor: `http://192.168.53.41:8000`.

---

## 🌐 Deployment ke Vercel

Aplikasi ini siap dideploy langsung ke **Vercel**:
1. Login ke [vercel.com](https://vercel.com) dengan akun GitHub Anda.
2. Klik **Add New...** ➔ **Project**.
3. Pilih repositori `smti-dashboard`.
4. Klik **Deploy**.
