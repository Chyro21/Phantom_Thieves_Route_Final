# Phantom Thieves Route

Phantom Thieves Route adalah proyek REST API berbasis Python yang dirancang untuk membantu pemain _Persona 5 Royal_ mengakses informasi permainan, termasuk aktivitas harian, Confidant, Persona, dan kalender dalam game.

Proyek ini dikembangkan sebagai proyek pembelajaran Backend Development dengan menggunakan Python, Flask, PostgreSQL, dan deployment melalui Vercel.

## 1. Informasi Proyek

- **Nama proyek:** Phantom Thieves Route
- **Bahasa pemrograman:** Python
- **Framework:** Flask
- **Database:** PostgreSQL
- **Database hosting:** Supabase
- **Deployment:** Vercel
- **Format respons API:** JSON
- **API testing:** Thunder Client

## 2. Deployment dan Repository

**Base URL API:**

https://phantom-thieves-route-final.vercel.app/

**Dokumentasi API:**

https://phantom-thieves-route-final.vercel.app/api/docs

**Repository GitHub:**

https://github.com/Chyro21/Phantom_Thieves_Route_Final

Aplikasi di-deploy melalui Vercel dan menggunakan PostgreSQL yang di-host melalui Supabase.

## 3. Fitur dan Dokumentasi API

### 3.1 Health Check

Endpoint ini digunakan untuk memeriksa status aplikasi dan koneksi database.

**Request:**

`GET /api/health`

**Contoh respons:**

```json
{
  "database": "postgres",
  "server_time": "2026-10-25T14:39:52.499537+00:00",
  "status": "ok"
}
```

Respons `status: ok` menunjukkan bahwa aplikasi berjalan dan koneksi database berhasil diperiksa.

### 3.2 Activities

Endpoint Activities digunakan untuk mengambil, menambahkan, memperbarui, dan menghapus data aktivitas.

| Method | Endpoint               | Fungsi                               |
| ------ | ---------------------- | ------------------------------------ |
| GET    | `/api/activities`      | Mengambil daftar aktivitas           |
| POST   | `/api/activities`      | Menambahkan aktivitas                |
| PATCH  | `/api/activities/{id}` | Memperbarui aktivitas berdasarkan ID |
| DELETE | `/api/activities/{id}` | Menghapus aktivitas berdasarkan ID   |

**Contoh request POST:**

```json
{
  "activity_name": "Study at Cafe",
  "category": "Social Stat",
  "description": "Aktivitas belajar."
}
```

Endpoint ini telah digunakan untuk menguji operasi CRUD, mulai dari menambahkan data, mengambil data, memperbarui data, hingga menghapus data.

### 3.3 Confidants

Endpoint ini digunakan untuk mengambil data karakter Confidant.

**Request:**

`GET /api/confidants`

Data yang dikembalikan mencakup informasi Confidant seperti ID, nama karakter, Arcana, dan catatan sesuai data yang tersedia di database.

### 3.4 Personas

Endpoint ini digunakan untuk mengambil data Persona.

**Request:**

`GET /api/personas`

Data yang dikembalikan mencakup informasi Persona seperti ID, nama, Arcana, level, dan catatan sesuai data yang tersedia di database.

### 3.5 Calendar

Endpoint Calendar digunakan untuk mengambil informasi aktivitas berdasarkan tanggal dalam game.

**Request:**

`GET /api/calendar?date=2026-04-11`

**Parameter:**

- `date`: tanggal dalam game dengan format `YYYY-MM-DD`.

Informasi yang dapat ditampilkan mencakup tanggal, hari, sesi aktivitas, nama aktivitas, kategori, dan nilai perubahan social stats.

Pada hari biasa, kalender menggunakan sesi After School dan Evening. Pada hari Minggu, sesi After School digantikan dengan Morning, sedangkan sesi Evening tetap digunakan.

### 3.6 QA dan Classroom Answers

Endpoint QA digunakan untuk mengambil data pertanyaan dan jawaban dalam game, termasuk pertanyaan kelas.

**Request:**

`GET /api/qa`

Secara default, jawaban dan penjelasan yang ditandai sebagai spoiler disembunyikan. Untuk membuka jawaban, gunakan parameter `reveal=true`.

**Menyembunyikan spoiler:**

`GET /api/qa`

**Membuka spoiler:**

`GET /api/qa?reveal=true`

Ketika spoiler disembunyikan, field `answer_text` dan `explanation` pada data yang dilindungi dikembalikan sebagai `null`. Ketika parameter `reveal=true` digunakan, jawaban dan penjelasan ditampilkan.

### 3.7 Confidant Interactions

Endpoint ini digunakan untuk mengambil informasi interaksi Confidant, termasuk pilihan dialog dan affection points.

**Request:**

`GET /api/confidant-interactions`

Secara default, informasi jawaban dan affection points yang ditandai sebagai spoiler disembunyikan.

**Menyembunyikan spoiler:**

`GET /api/confidant-interactions`

**Membuka spoiler:**

`GET /api/confidant-interactions?reveal=true`

Ketika spoiler disembunyikan, field `answer_text` dan `affection_points` pada data yang dilindungi dikembalikan sebagai `null`. Ketika parameter `reveal=true` digunakan, informasi tersebut ditampilkan.

## 4. Pengujian API

Pengujian API dilakukan menggunakan Thunder Client di Visual Studio Code terhadap aplikasi yang telah di-deploy melalui Vercel.

### 4.1 Health Check dan Data

| Pengujian                           | Hasil    |
| ----------------------------------- | -------- |
| GET `/api/health`                   | Berhasil |
| GET `/api/activities`               | Berhasil |
| GET `/api/confidants`               | Berhasil |
| GET `/api/personas`                 | Berhasil |
| GET `/api/calendar?date=2026-04-11` | Berhasil |
| GET `/api/calendar?date=2026-04-12` | Berhasil |

### 4.2 Pengujian CRUD Activities

| Pengujian                              | Hasil                                  |
| -------------------------------------- | -------------------------------------- |
| POST `/api/activities`                 | Berhasil menambahkan aktivitas         |
| GET `/api/activities` setelah POST     | Data aktivitas baru berhasil ditemukan |
| PATCH `/api/activities/7`              | Berhasil memperbarui aktivitas         |
| DELETE `/api/activities/7`             | Berhasil menghapus aktivitas           |
| GET `/api/activities/7` setelah DELETE | Mengembalikan HTTP 404                 |

Hasil tersebut menunjukkan bahwa operasi Create, Read, Update, dan Delete pada endpoint Activities telah berhasil diuji.

### 4.3 Pengujian Perlindungan Spoiler

| Method | Endpoint                                  | Hasil                                                  |
| ------ | ----------------------------------------- | ------------------------------------------------------ |
| GET    | `/api/qa`                                 | Berhasil; jawaban dan penjelasan spoiler disembunyikan |
| GET    | `/api/qa?reveal=true`                     | Berhasil; jawaban dan penjelasan ditampilkan           |
| GET    | `/api/confidant-interactions`             | Berhasil; jawaban dan affection points disembunyikan   |
| GET    | `/api/confidant-interactions?reveal=true` | Berhasil; jawaban dan affection points ditampilkan     |

Pada mode default, data yang ditandai sebagai spoiler memiliki nilai `null` pada field jawaban yang dilindungi. Ketika parameter `reveal=true` digunakan, field tersebut ditampilkan dan respons mengindikasikan bahwa spoiler telah dibuka.

Pengujian ini menunjukkan bahwa mekanisme penyembunyian dan pengungkapan spoiler berjalan sesuai rancangan berdasarkan respons API yang diperoleh.

### 4.4 Dokumentasi Endpoint

Dokumentasi endpoint dapat diakses melalui:

https://phantom-thieves-route-final.vercel.app/api/docs

Dokumentasi tersebut menyediakan daftar endpoint API beserta metode dan deskripsi penggunaannya. Pada pemeriksaan terakhir, dokumentasi menampilkan 13 endpoint.

## 5. Menjalankan Proyek Secara Lokal

### 5.1 Prasyarat

Perangkat yang digunakan perlu memiliki:

- Python
- pip
- Git
- Visual Studio Code atau editor kode lainnya
- Akun Supabase dengan database PostgreSQL

### 5.2 Clone Repository

Jalankan perintah berikut pada terminal:

```bash
git clone https://github.com/Chyro21/Phantom_Thieves_Route_Final.git
```

### 5.3 Masuk ke Folder Proyek

```bash
cd Phantom_Thieves_Route_Final
```

### 5.4 Membuat Virtual Environment

```bash
python -m venv .venv
```

### 5.5 Mengaktifkan Virtual Environment

Untuk Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5.6 Menginstal Dependensi

```bash
pip install -r requirements.txt
```

### 5.7 Menyiapkan Database

Siapkan variabel lingkungan `DATABASE_URL` menggunakan connection string PostgreSQL milik sendiri.

Jika proyek menggunakan file `.env`, isi file tersebut dengan konfigurasi database lokal yang sesuai. Jangan mengunggah file `.env` atau membagikan password dan kredensial database ke repository publik.

### 5.8 Menjalankan Aplikasi

Jalankan aplikasi sesuai entry point lokal dan konfigurasi yang tersedia di repository.

## 6. Teknologi yang Digunakan

- **Python:** bahasa pemrograman untuk implementasi backend.
- **Flask:** framework untuk membangun REST API.
- **PostgreSQL:** sistem manajemen database relasional.
- **Supabase:** layanan hosting PostgreSQL.
- **Vercel:** platform deployment aplikasi.
- **Thunder Client:** alat untuk menguji endpoint HTTP dan memeriksa respons API.
- **Git dan GitHub:** digunakan untuk pengelolaan versi dan penyimpanan source code.

## 7. Catatan Pengembangan

Sebagian data yang digunakan dalam pengujian masih berupa data contoh (_dummy_). Data tersebut digunakan untuk menguji struktur respons API, operasi CRUD, serta mekanisme perlindungan spoiler.

Pengembangan selanjutnya direncanakan mencakup:

1. Penyempurnaan data game Persona 5 Royal.
2. Integrasi kalender dengan Manual Tracker.
3. Pengembangan Persona Fusion Calculator.
4. Pengembangan database boss beserta informasi kelemahan dan perlindungan spoiler.
5. Penyempurnaan dokumentasi dan pengujian seluruh endpoint.

## 8. Kesimpulan

Phantom Thieves Route merupakan proyek backend berbasis Python yang menyediakan REST API dengan database PostgreSQL. Aplikasi telah di-deploy melalui Vercel dan menyediakan endpoint untuk aktivitas, Confidant, Persona, kalender, QA, serta interaksi Confidant.

Berdasarkan pengujian yang telah dilakukan, endpoint health check, operasi CRUD aktivitas, pengambilan data, dan mekanisme perlindungan spoiler telah berhasil diuji pada deployment produksi. Data yang digunakan sebagian masih berupa data contoh sehingga penyempurnaan isi data game dapat dilakukan pada tahap pengembangan berikutnya.

## 9. Tautan Proyek

- **GitHub Repository:** https://github.com/Chyro21/Phantom_Thieves_Route_Final
- **Base URL API:** https://phantom-thieves-route-final.vercel.app/
- **Dokumentasi API:** https://phantom-thieves-route-final.vercel.app/api/docs
