"""Phantom Thieves Route REST API — Flask + PostgreSQL (Supabase/Neon)."""

import os
from datetime import date
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import IntegrityError, Error

load_dotenv()

app = Flask(__name__)
SCHEMA = "phantom_route"


def db_connect():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL belum diatur. Tambahkan connection string PostgreSQL pada environment variables.")
    conn = psycopg2.connect(url, cursor_factory=RealDictCursor, connect_timeout=10)
    with conn.cursor() as cur:
        cur.execute("SET search_path TO phantom_route, public")
    return conn


def error(message, status):
    return jsonify({"error": message}), status


def fetch_all(sql, params=()):
    conn = db_connect()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


def execute_returning(sql, params=()):
    conn = db_connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                row = cur.fetchone()
                return dict(row) if row else None
    finally:
        conn.close()


def json_body():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return None
    return body


@app.get("/")
def home():
    return jsonify({
        "project": "Phantom Thieves Route",
        "message": "REST API is running",
        "version": "1.0.0",
        "documentation": "/api/docs",
        "health": "/api/health"
    })


@app.get("/api/health")
def health():
    try:
        row = fetch_one("SELECT current_database() AS database, NOW() AS server_time")
        return jsonify({"status": "ok", "database": row["database"], "server_time": row["server_time"].isoformat()}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Database health check failed")
        return error("Database tidak dapat dihubungi. Periksa DATABASE_URL dan status database.", 503)



@app.get("/api/docs")
def api_docs():
    return jsonify({
        "base_url": request.host_url.rstrip("/"),
        "endpoints": [
            {
                "method": "GET",
                "path": "/api/health",
                "description": "Memeriksa koneksi database"
            },
            {
                "method": "GET",
                "path": "/api/activities",
                "description": "Daftar aktivitas; query ?category=Study opsional"
            },
            {
                "method": "GET",
                "path": "/api/activities/<id>",
                "description": "Detail aktivitas"
            },
            {
                "method": "POST",
                "path": "/api/activities",
                "description": "Tambah aktivitas"
            },
            {
                "method": "PUT/PATCH",
                "path": "/api/activities/<id>",
                "description": "Ubah aktivitas"
            },
            {
                "method": "DELETE",
                "path": "/api/activities/<id>",
                "description": "Hapus aktivitas"
            },
            {
                "method": "GET",
                "path": "/api/calendar?date=YYYY-MM-DD",
                "description": "Aktivitas kalender berdasarkan tanggal"
            },
            {
                "method": "GET",
                "path": "/api/confidants",
                "description": "Daftar Confidant"
            },
            {
                "method": "GET",
                "path": "/api/personas",
                "description": "Daftar Persona"
            },
            {
                "method": "GET",
                "path": "/api/bosses?date=YYYY-MM-DD",
                "description": "Daftar boss berdasarkan tanggal; spoiler tersembunyi secara default"
            },
            {
                "method": "GET",
                "path": "/api/profiles",
                "description": "Daftar profil pemain"
            },
            {
                "method": "GET",
                "path": "/api/qa",
                "description": "Daftar pertanyaan dan jawaban; spoiler tersembunyi secara default. Gunakan ?reveal=true untuk menampilkan jawaban"
            },
            {
                "method": "GET",
                "path": "/api/confidant-interactions",
                "description": "Daftar interaksi Confidant; spoiler tersembunyi secara default. Gunakan ?reveal=true untuk menampilkan jawaban"
            }
        ]
    })



@app.get("/api/activities")
def activities_list():
    try:
        category = request.args.get("category")
        if category:
            rows = fetch_all("SELECT activity_id, activity_name, category, description FROM activities WHERE category = %s ORDER BY activity_name", (category,))
        else:
            rows = fetch_all("SELECT activity_id, activity_name, category, description FROM activities ORDER BY activity_id")
        return jsonify({"data": rows, "count": len(rows)}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not list activities")
        return error("Gagal mengambil data aktivitas.", 500)



@app.get("/api/activities/<int:activity_id>")
def activity_detail(activity_id):
    try:
        row = fetch_one(
            "SELECT activity_id, activity_name, category, description "
            "FROM activities WHERE activity_id = %s",
            (activity_id,)
        )

        if not row:
            return error("Aktivitas tidak ditemukan.", 404)

        return jsonify({"data": row}), 200

    except RuntimeError as exc:
        return error(str(exc), 503)

    except Error:
        app.logger.exception("Could not fetch activity")
        return error("Gagal mengambil detail aktivitas.", 500)


@app.post("/api/activities")
def activity_create():
    body = json_body()
    if body is None:
        return error("Request body harus berupa JSON object.", 400)
    name = body.get("activity_name")
    category = body.get("category")
    description = body.get("description")
    if not isinstance(name, str) or not name.strip():
        return error("Field activity_name wajib diisi dengan teks.", 400)
    if not isinstance(category, str) or not category.strip():
        return error("Field category wajib diisi dengan teks.", 400)
    if len(name.strip()) > 100 or len(category.strip()) > 50:
        return error("activity_name maksimal 100 karakter dan category maksimal 50 karakter.", 400)
    try:
        row = execute_returning(
            "INSERT INTO activities (activity_name, category, description) VALUES (%s, %s, %s) RETURNING activity_id, activity_name, category, description",
            (name.strip(), category.strip(), description)
        )
        return jsonify({"message": "Aktivitas berhasil ditambahkan.", "data": row}), 201
    except RuntimeError as exc:
        return error(str(exc), 503)
    except IntegrityError:
        return error("Nama aktivitas sudah terdaftar.", 409)
    except Error:
        app.logger.exception("Could not create activity")
        return error("Gagal menambahkan aktivitas.", 500)


def update_activity(activity_id, partial):
    body = json_body()
    if body is None:
        return error("Request body harus berupa JSON object.", 400)
    allowed = {"activity_name", "category", "description"}
    if not body or set(body) - allowed:
        return error("Body harus berisi field yang valid: activity_name, category, description.", 400)
    if not partial and not {"activity_name", "category"}.issubset(body):
        return error("PUT wajib menyertakan activity_name dan category.", 400)
    for key in ("activity_name", "category"):
        if key in body and (not isinstance(body[key], str) or not body[key].strip()):
            return error(f"Field {key} harus berupa teks yang tidak kosong.", 400)
    if "activity_name" in body and len(body["activity_name"].strip()) > 100:
        return error("activity_name maksimal 100 karakter.", 400)
    if "category" in body and len(body["category"].strip()) > 50:
        return error("category maksimal 50 karakter.", 400)
    fields, values = [], []
    for key in ("activity_name", "category", "description"):
        if key in body:
            fields.append(f"{key} = %s")
            values.append(body[key].strip() if key in ("activity_name", "category") else body[key])
    values.append(activity_id)
    try:
        row = execute_returning(
            f"UPDATE activities SET {', '.join(fields)} WHERE activity_id = %s RETURNING activity_id, activity_name, category, description",
            tuple(values)
        )
        if not row:
            return error("Aktivitas tidak ditemukan.", 404)
        return jsonify({"message": "Aktivitas berhasil diperbarui.", "data": row}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except IntegrityError:
        return error("Nama aktivitas sudah digunakan.", 409)
    except Error:
        app.logger.exception("Could not update activity")
        return error("Gagal memperbarui aktivitas.", 500)


@app.put("/api/activities/<int:activity_id>")
def activity_replace(activity_id):
    return update_activity(activity_id, partial=False)


@app.patch("/api/activities/<int:activity_id>")
def activity_patch(activity_id):
    return update_activity(activity_id, partial=True)


@app.delete("/api/activities/<int:activity_id>")
def activity_delete(activity_id):
    try:
        row = execute_returning("DELETE FROM activities WHERE activity_id = %s RETURNING activity_id, activity_name", (activity_id,))
        if not row:
            return error("Aktivitas tidak ditemukan.", 404)
        return jsonify({"message": "Aktivitas berhasil dihapus.", "data": row}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error as exc:
        app.logger.exception("Could not delete activity")
        if getattr(exc, "pgcode", None) == "23503":
            return error("Aktivitas masih digunakan pada kalender sehingga tidak dapat dihapus.", 409)
        return error("Gagal menghapus aktivitas.", 500)


@app.get("/api/calendar")
def calendar_for_date():
    raw_date = request.args.get("date")
    if not raw_date:
        return error("Query parameter date wajib diisi dengan format YYYY-MM-DD.", 400)
    try:
        selected = date.fromisoformat(raw_date)
    except ValueError:
        return error("Format date tidak valid. Gunakan YYYY-MM-DD.", 400)
    try:
        rows = fetch_all("""
            SELECT gd.game_date, gd.weekday, ca.session, a.activity_id, a.activity_name,
                   a.category, a.description, ca.condition_name, ca.knowledge_gain,
                   ca.proficiency_gain, ca.guts_gain, ca.kindness_gain, ca.charm_gain, ca.notes
            FROM game_dates gd
            LEFT JOIN calendar_activities ca ON ca.game_date_id = gd.game_date_id
            LEFT JOIN activities a ON a.activity_id = ca.activity_id
            WHERE gd.game_date = %s
            ORDER BY CASE ca.session WHEN 'Morning' THEN 1 WHEN 'After School' THEN 2 WHEN 'Evening' THEN 3 ELSE 4 END, a.activity_name
        """, (selected,))
        if not rows:
            return error("Tanggal tersebut belum tersedia pada data kalender.", 404)
        return jsonify({"date": selected.isoformat(), "weekday": rows[0]["weekday"], "data": rows}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not load calendar")
        return error("Gagal mengambil data kalender.", 500)


@app.get("/api/confidants")
def confidants_list():
    try:
        rows = fetch_all("SELECT confidant_id, confidant_name, arcana, notes FROM confidants ORDER BY confidant_name")
        return jsonify({"data": rows, "count": len(rows)}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not list confidants")
        return error("Gagal mengambil data Confidant.", 500)


@app.get("/api/personas")
def personas_list():
    try:
        rows = fetch_all("SELECT persona_id, persona_name, level, arcana, notes FROM personas ORDER BY level, persona_name")
        return jsonify({"data": rows, "count": len(rows)}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not list personas")
        return error("Gagal mengambil data Persona.", 500)


@app.get("/api/bosses")
def bosses_list():
    raw_date = request.args.get("date")
    reveal = request.args.get("reveal", "false").lower() == "true"
    if not raw_date:
        return error("Query parameter date wajib diisi (YYYY-MM-DD) agar boss difilter berdasarkan progres kalender.", 400)
    try:
        selected = date.fromisoformat(raw_date)
    except ValueError:
        return error("Format date tidak valid. Gunakan YYYY-MM-DD.", 400)
    try:
        date_row = fetch_one("SELECT game_date_id FROM game_dates WHERE game_date = %s", (selected,))
        if not date_row:
            return error("Tanggal tersebut belum tersedia pada data kalender.", 404)
        rows = fetch_all("""
            SELECT b.boss_id, b.boss_name, b.first_available_date_id, b.last_available_date_id,
                   b.is_optional, b.is_spoiler,
                   CASE WHEN %s OR NOT b.is_spoiler THEN b.description ELSE NULL END AS description,
                   first_date.game_date AS first_available_date,
                   last_date.game_date AS last_available_date
            FROM bosses b
            LEFT JOIN game_dates first_date ON first_date.game_date_id = b.first_available_date_id
            LEFT JOIN game_dates last_date ON last_date.game_date_id = b.last_available_date_id
            WHERE (b.first_available_date_id IS NULL OR first_date.game_date <= %s)
              AND (b.last_available_date_id IS NULL OR last_date.game_date >= %s)
            ORDER BY b.boss_id
        """, (reveal, selected, selected))
        return jsonify({"date": selected.isoformat(), "data": rows, "count": len(rows), "spoilers_revealed": reveal}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not list bosses")
        return error("Gagal mengambil data boss.", 500)


@app.get("/api/profiles")
def profiles_list():
    try:
        rows = fetch_all("""
            SELECT player_id, player_name, current_game_date_id, knowledge, proficiency,
                   guts, kindness, charm, created_at, updated_at
            FROM player_profiles ORDER BY player_id
        """)
        return jsonify({"data": rows, "count": len(rows)}), 200
    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not list profiles")
        return error("Gagal mengambil data profil pemain.", 500)


@app.get("/api/qa")
def qa_list():
    reveal = request.args.get("reveal", "false").lower() == "true"

    try:
        rows = fetch_all("""
            SELECT
                q.qa_id,
                q.game_date_id,
                q.question_type,
                q.question_text,
                CASE
                    WHEN %s OR NOT q.is_spoiler
                    THEN q.answer_text
                    ELSE NULL
                END AS answer_text,
                CASE
                    WHEN %s OR NOT q.is_spoiler
                    THEN q.explanation
                    ELSE NULL
                END AS explanation,
                q.is_spoiler
            FROM qa_entries q
            ORDER BY q.game_date_id, q.qa_id
        """, (reveal, reveal))

        return jsonify({
            "data": rows,
            "count": len(rows),
            "spoilers_revealed": reveal
        }), 200

    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not list Q&A entries")
        return error("Gagal mengambil data pertanyaan dan jawaban.", 500)


@app.get("/api/confidant-interactions")
def confidant_interactions_list():
    reveal = request.args.get("reveal", "false").lower() == "true"

    try:
        rows = fetch_all("""
            SELECT
                ci.interaction_id,
                ci.confidant_id,
                c.confidant_name,
                ci.rank_target,
                ci.interaction_description,
                CASE
                    WHEN %s OR NOT ci.is_spoiler
                    THEN ci.answer_text
                    ELSE NULL
                END AS answer_text,
                CASE
                    WHEN %s OR NOT ci.is_spoiler
                    THEN ci.affection_points
                    ELSE NULL
                END AS affection_points,
                ci.is_spoiler
            FROM confidant_interactions ci
            JOIN confidants c ON c.confidant_id = ci.confidant_id
            ORDER BY c.confidant_name, ci.rank_target, ci.interaction_id
        """, (reveal, reveal))

        return jsonify({
            "data": rows,
            "count": len(rows),
            "spoilers_revealed": reveal
        }), 200

    except RuntimeError as exc:
        return error(str(exc), 503)
    except Error:
        app.logger.exception("Could not list Confidant interactions")
        return error("Gagal mengambil data interaksi Confidant.", 500)


@app.errorhandler(404)
def not_found(_exc):
    return error("Endpoint tidak ditemukan.", 404)


@app.errorhandler(405)
def method_not_allowed(_exc):
    return error("HTTP method tidak diizinkan untuk endpoint ini.", 405)


@app.errorhandler(500)
def server_error(_exc):
    return error("Terjadi kesalahan internal server.", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
