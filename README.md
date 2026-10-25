# Phantom Thieves Route — REST API

REST API backend untuk proyek Persona 5 Royal **Phantom Thieves Route**. Dibangun dengan Python Flask dan PostgreSQL (Supabase/Neon). API berfokus pada modul kalender aktivitas, Confidant, Persona, profil pemain, dan database boss dengan penanda spoiler.

> **Status deployment:** paket ini sudah dikonfigurasi untuk Vercel, tetapi URL publik belum tersedia karena deployment membutuhkan akun GitHub/Vercel dan connection string database milik pemilik proyek. Jangan mencantumkan URL palsu sebagai deployment yang sudah live.

## Teknologi
- Python + Flask
- PostgreSQL melalui `psycopg2`
- Vercel Serverless Functions
- Supabase atau Neon sebagai database online
- Postman / Thunder Client untuk pengujian

## Struktur berkas
- `app.py` — endpoint REST API.
- `api/index.py`, `vercel.json` — entrypoint dan routing Vercel.
- `sql/schema.sql` — 15 tabel relasional.
- `sql/dummy_data.sql` — data contoh untuk pengujian.
- `ERD_Phantom_Thieves_Route.png` — gambar ringkasan ERD untuk dokumentasi.
- `sql/schema.dbml` — definisi ERD yang bisa diimpor ke dbdiagram.io untuk tampilan detail.
- `postman_collection.json` — koleksi request untuk diimpor ke Postman.
- `.env.example` — contoh environment variable, bukan credential asli.

## Database dan ERD
1. Buat database PostgreSQL pada Supabase atau Neon.
2. Jalankan seluruh isi `sql/schema.sql` di SQL Editor. Script membuat schema `phantom_route` dan 15 tabel dengan primary key, foreign key, constraint, dan indeks.
3. Jalankan `sql/dummy_data.sql` untuk memasukkan data uji. Data ini hanya contoh dan **bukan** kumpulan data lengkap Persona 5 Royal.
4. Gambar ringkasan ERD sudah disertakan sebagai `ERD_Phantom_Thieves_Route.png`. Untuk diagram detail yang dapat diedit, buka https://dbdiagram.io, buat diagram baru, lalu tempel isi `sql/schema.dbml`.

Relasi utama:
- `game_dates` 1:N `calendar_activities`.
- `activities` 1:N `calendar_activities`.
- `player_profiles` N:N `confidants` melalui `player_confidant_ranks`.
- `confidants` 1:N `confidant_interactions`.
- `personas` 1:N `fusion_recipes` sebagai Persona target.
- `fusion_recipes` N:N `personas` melalui `fusion_recipe_materials`.
- `bosses` 1:N `boss_affinities`.
- `bosses` N:N `party_members` melalui `recommended_party_members`.

## Menjalankan secara lokal
1. Gunakan Python 3.10 atau lebih baru.
2. Buat virtual environment dan instal paket:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Atur `DATABASE_URL` dari database PostgreSQL. Jangan masukkan password asli ke GitHub.
   - Windows PowerShell: `$env:DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require"`
   - macOS/Linux: `export DATABASE_URL='postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require'`
4. Jalankan API:
   ```bash
   python app.py
   ```
5. Buka `http://127.0.0.1:5000/` atau `/api/health`.

## Deployment Vercel
1. Push folder proyek ini ke repository GitHub baru. Pastikan `.env` tidak ikut di-commit.
2. Di Vercel, pilih **Add New → Project** lalu impor repository tersebut.
3. Di Project Settings → Environment Variables, tambahkan `DATABASE_URL` berisi connection string PostgreSQL online. Gunakan connection string dengan SSL sesuai penyedia database.
4. Deploy. Jika mengubah environment variable, lakukan redeploy.
5. Uji `https://<nama-proyek>.vercel.app/api/health`. Deployment baru dapat dianggap selesai setelah URL tersebut merespons `{"status":"ok", ...}`.
6. Ganti variabel `baseUrl` dalam koleksi Postman dari `http://localhost:5000` ke URL Vercel.

## Endpoint API
Semua response menggunakan JSON. Header untuk request dengan body: `Content-Type: application/json`.

### 1. Health check
- Method: `GET`
- URL: `/api/health`
- Deskripsi: memeriksa koneksi database.
- Response sukses (200): `{"status":"ok","database":"...","server_time":"..."}`
- Response error (503): `{"error":"Database tidak dapat dihubungi..."}`

### 2. Daftar aktivitas
- Method: `GET`
- URL: `/api/activities`
- Deskripsi: mengambil semua aktivitas. Filter opsional `?category=Study`.
- Response sukses (200): `{"data":[{"activity_id":1,"activity_name":"Study","category":"Study","description":"..."}],"count":1}`

### 3. Detail aktivitas
- Method: `GET`
- URL: `/api/activities/1`
- Deskripsi: mengambil satu aktivitas.
- Response sukses (200): `{"data":{"activity_id":1,"activity_name":"Study","category":"Study","description":"..."}}`
- Response error (404): `{"error":"Aktivitas tidak ditemukan."}`

### 4. Tambah aktivitas
- Method: `POST`
- URL: `/api/activities`
- Deskripsi: membuat aktivitas baru.
- Request body:
  ```json
  {"activity_name":"Study at Library","category":"Study","description":"Belajar untuk meningkatkan Knowledge"}
  ```
- Response sukses (201): `{"message":"Aktivitas berhasil ditambahkan.","data":{"activity_id":1,"activity_name":"Study at Library","category":"Study","description":"..."}}`
- Response error (400): `{"error":"Field activity_name wajib diisi dengan teks."}`
- Response error (409): nama aktivitas duplikat.

### 5. Ganti aktivitas
- Method: `PUT`
- URL: `/api/activities/1`
- Deskripsi: mengganti field utama aktivitas; `activity_name` dan `category` wajib disertakan.
- Request body:
  ```json
  {"activity_name":"Study at School","category":"Study","description":"Belajar di sekolah"}
  ```
- Response sukses (200): `{"message":"Aktivitas berhasil diperbarui.","data":{...}}`
- Response error (400/404): body tidak valid atau aktivitas tidak ditemukan.

### 6. Ubah sebagian aktivitas
- Method: `PATCH`
- URL: `/api/activities/1`
- Deskripsi: memperbarui satu atau beberapa field aktivitas.
- Request body: `{"description":"Belajar saat hujan"}`
- Response sukses (200): `{"message":"Aktivitas berhasil diperbarui.","data":{...}}`
- Response error (404): aktivitas tidak ditemukan.

### 7. Hapus aktivitas
- Method: `DELETE`
- URL: `/api/activities/1`
- Deskripsi: menghapus aktivitas yang tidak sedang digunakan kalender.
- Response sukses (200): `{"message":"Aktivitas berhasil dihapus.","data":{"activity_id":1,"activity_name":"..."}}`
- Response error (404): aktivitas tidak ditemukan.
- Response error (409): aktivitas masih direferensikan kalender.

### 8. Kalender berdasarkan tanggal
- Method: `GET`
- URL: `/api/calendar?date=2026-04-11`
- Deskripsi: mengambil sesi dan aktivitas untuk tanggal tertentu.
- Response sukses (200): objek berisi `date`, `weekday`, dan `data` aktivitas.
- Response error (400): tanggal tidak diisi atau format salah.
- Response error (404): tanggal belum tersedia di data kalender.

### 9. Daftar Confidant
- Method: `GET`
- URL: `/api/confidants`
- Deskripsi: mengambil daftar Confidant.
- Response sukses (200): `{"data":[...],"count":0}`

### 10. Daftar Persona
- Method: `GET`
- URL: `/api/personas`
- Deskripsi: mengambil daftar Persona untuk mendukung modul fusion.
- Response sukses (200): `{"data":[...],"count":0}`

### 11. Daftar boss
- Method: `GET`
- URL: `/api/bosses?date=2026-04-11`
- Deskripsi: mengambil boss yang rentang tanggal ketersediaannya mencakup tanggal yang diminta. Deskripsi bertanda spoiler disembunyikan secara default.
- Untuk mengungkap deskripsi setelah meminta konfirmasi pengguna, gunakan `/api/bosses?date=2026-04-11&reveal=true`.
- Response sukses (200): `{"date":"2026-04-11","data":[...],"count":0,"spoilers_revealed":false}`
- Response error (400): parameter `date` wajib diisi; response 404 jika tanggal tidak ada di tabel kalender. Boss yang belum diisi tanggal ketersediaannya tetap dapat muncul, jadi data tanggal harus diisi dengan benar untuk mengaktifkan pembatasan progres.

### 12. Daftar profil pemain
- Method: `GET`
- URL: `/api/profiles`
- Deskripsi: mengambil profil dan statistik pemain.
- Response sukses (200): `{"data":[...],"count":0}`

## Pengujian Postman / Thunder Client
Impor `postman_collection.json` ke Postman. Mulai dari health check, kemudian uji endpoint aktivitas dengan GET, POST, PUT, PATCH, dan DELETE. Untuk request yang mengubah data, pastikan database uji telah disiapkan. Setelah deployment, ganti `baseUrl` ke URL Vercel dan lakukan ulang semua tes. Simpan screenshot atau ekspor hasil pengujian setelah endpoint diuji pada URL publik.

## Batasan yang perlu diketahui
- Data dummy hanya digunakan untuk pengujian struktur dan endpoint.
- Aplikasi tidak mengklaim telah live sampai dideploy ke akun Vercel pemilik proyek.
- `reveal=true` adalah parameter untuk mengungkap data bertanda spoiler; frontend idealnya menampilkan konfirmasi terlebih dahulu. Penegakan progres tanggal untuk boss dan kelengkapan data game adalah pengembangan lanjutan.
