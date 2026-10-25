# Phantom Thieves Route

Phantom Thieves Route adalah proyek REST API berbasis Python yang dirancang untuk membantu pemain _Persona 5 Royal_ mengakses informasi permainan, termasuk aktivitas harian, Confidant, Persona, dan kalender dalam game.

Proyek ini dikembangkan sebagai proyek pembelajaran Backend Development dengan menggunakan Python, Flask, PostgreSQL, dan deployment melalui Vercel.

## Informasi Proyek

- **Nama:** Phantom Thieves Route
- **Bahasa pemrograman:** Python
- **Framework:** Flask
- **Database:** PostgreSQL
- **Database hosting:** Supabase
- **Deployment:** Vercel
- **Format respons:** JSON

## Deployment

Base URL API:

https://phantom-thieves-route-final.vercel.app/

Dokumentasi API:

https://phantom-thieves-route-final.vercel.app/api/docs

## Fitur API

### 1. Health Check

Memeriksa status aplikasi dan koneksi database.

**Request**

`GET /api/health`

**Contoh respons**

```json
{
  "database": "postgres",
  "server_time": "2026-10-25T14:39:52.499537+00:00",
  "status": "ok"
}
```

### 2. Activities

Mengambil dan mengelola data aktivitas.

| Method | Endpoint               | Fungsi                     |
| ------ | ---------------------- | -------------------------- |
| GET    | `/api/activities`      | Mengambil daftar aktivitas |
| POST   | `/api/activities`      | Menambahkan aktivitas      |
| PATCH  | `/api/activities/{id}` | Memperbarui aktivitas      |
| DELETE | `/api/activities/{id}` | Menghapus aktivitas        |

Contoh request POST:

```json
{
  "activity_name": "Study at Cafe",
  "category": "Social Stat",
  "description": "Aktivitas belajar."
}
```

### 3. Confidants

Mengambil data karakter Confidant.

`GET /api/confidants`

Data yang dikembalikan mencakup ID Confidant, nama karakter, Arcana, dan catatan.

### 4. Personas

Mengambil data Persona.

`GET /api/personas`

Data yang dikembalikan mencakup ID Persona, nama, Arcana, level, dan catatan.

### 5. Calendar

Mengambil informasi aktivitas berdasarkan tanggal dalam game.

`GET /api/calendar?date=2026-04-11`

Parameter:

- `date`: tanggal dalam format `YYYY-MM-DD`.

Informasi yang dapat ditampilkan mencakup tanggal, hari, sesi aktivitas, nama aktivitas, kategori, serta nilai perubahan social stats.

Pada hari Minggu, sesi kalender menggunakan Morning dan Evening, sesuai hasil pengujian yang dilakukan.

## Pengujian API

Pengujian dilakukan menggunakan Thunder Client di Visual Studio Code terhadap URL deployment Vercel.

| Pengujian                              | Hasil                  |
| -------------------------------------- | ---------------------- |
| GET `/api/health`                      | Berhasil               |
| GET `/api/activities`                  | Berhasil               |
| POST `/api/activities`                 | Berhasil               |
| GET `/api/activities` setelah POST     | Berhasil               |
| PATCH `/api/activities/7`              | Berhasil               |
| DELETE `/api/activities/7`             | Berhasil               |
| GET `/api/activities/7` setelah DELETE | Mengembalikan HTTP 404 |
| GET `/api/confidants`                  | Berhasil               |
| GET `/api/personas`                    | Berhasil               |
| GET `/api/calendar?date=2026-04-11`    | Berhasil               |
| GET `/api/calendar?date=2026-04-12`    | Berhasil               |

## Menjalankan Proyek Secara Lokal

### Prasyarat

- Python
- pip
- Git
- Akun Supabase dengan database PostgreSQL
- Visual Studio Code atau editor kode lainnya

### Instalasi

1. Clone repository:

   ```bash
   git clone https://github.com/Chyro21/Phantom_Thieves_Route_Final.git
   ```

2. Masuk ke folder proyek:

   ```bash
   cd Phantom_Thieves_Route_Final
   ```

3. Buat virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Aktifkan virtual environment di Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Instal dependensi:

   ```bash
   pip install -r requirements.txt
   ```

6. Siapkan variabel lingkungan `DATABASE_URL` menggunakan connection string PostgreSQL milikmu. Jangan mengunggah file `.env` atau membagikan password database.

7. Jalankan aplikasi sesuai entry point lokal yang tersedia di repository.

## Teknologi

- Python
- Flask
- PostgreSQL
- Supabase
- Vercel
- Thunder Client

## Catatan Pengembangan

Sebagian data yang digunakan dalam pengujian masih berupa data contoh (_dummy_). Pengembangan berikutnya mencakup penyempurnaan data game, integrasi tracker, kalkulator fusion Persona, serta database boss dengan perlindungan spoiler.

## Repository

https://github.com/Chyro21/Phantom_Thieves_Route_Final
