-- Phantom Thieves Route | contoh data dummy untuk uji relasi
-- Jalankan setelah 01_schema.sql / 04_supabase_setup.sql.
BEGIN;
SET search_path TO phantom_route, public;

INSERT INTO game_dates (game_date, weekday, notes) VALUES
('2026-04-11','Saturday','Contoh tanggal untuk pengujian; bukan klaim kalender game lengkap.'),
('2026-04-12','Sunday','Contoh hari Minggu; sesi kalender menggunakan Morning dan Evening.'),
('2026-04-13','Monday','Contoh tanggal untuk pengujian.')
ON CONFLICT (game_date) DO NOTHING;

INSERT INTO activities (activity_name, category, description) VALUES
('Study at Cafe','Social Stat','Contoh aktivitas belajar.'),
('Read a Book','Social Stat','Contoh aktivitas membaca.'),
('Spend Time with Confidant','Confidant','Contoh aktivitas perkembangan Confidant.'),
('Work Part-time','Job','Contoh aktivitas kerja paruh waktu.'),
('Solve Crossword','Question','Contoh teka-teki silang.')
ON CONFLICT (activity_name) DO NOTHING;

INSERT INTO calendar_activities (game_date_id, activity_id, session, condition_name, knowledge_gain, proficiency_gain, guts_gain, kindness_gain, charm_gain, notes)
SELECT gd.game_date_id, a.activity_id, x.session, x.condition_name, x.knowledge_gain, x.proficiency_gain, x.guts_gain, x.kindness_gain, x.charm_gain, x.notes
FROM (VALUES
 ('2026-04-11'::date,'Study at Cafe','After School','Normal',2,0,0,0,0,'Nilai stat hanya contoh dummy.'),
 ('2026-04-11'::date,'Read a Book','Evening','Normal',1,0,0,0,0,'Nilai stat hanya contoh dummy.'),
 ('2026-04-12'::date,'Work Part-time','Morning','Normal',0,1,0,1,0,'Hari Minggu memakai sesi Morning.'),
 ('2026-04-12'::date,'Solve Crossword','Evening','Normal',0,0,0,0,0,'Jawaban disimpan terpisah dan ditandai spoiler.'),
 ('2026-04-13'::date,'Spend Time with Confidant','After School','Available',0,0,0,0,0,'Periksa rank tracker untuk menentukan event berikutnya.')
) AS x(game_date, activity_name, session, condition_name, knowledge_gain, proficiency_gain, guts_gain, kindness_gain, charm_gain, notes)
JOIN game_dates gd ON gd.game_date=x.game_date
JOIN activities a ON a.activity_name=x.activity_name
ON CONFLICT (game_date_id, activity_id, session, condition_name) DO NOTHING;

INSERT INTO player_profiles (player_name, current_game_date_id, knowledge, proficiency, guts, kindness, charm)
SELECT 'Player Demo', gd.game_date_id, 2, 1, 1, 2, 1 FROM game_dates gd WHERE gd.game_date='2026-04-11'
AND NOT EXISTS (SELECT 1 FROM player_profiles WHERE player_name='Player Demo');

INSERT INTO confidants (confidant_name, arcana, notes) VALUES
('Ryuji Sakamoto','Chariot','Data contoh untuk uji tracker.'),
('Ann Takamaki','Lovers','Data contoh untuk uji tracker.'),
('Sojiro Sakura','Hierophant','Data contoh untuk uji tracker.')
ON CONFLICT (confidant_name) DO NOTHING;

INSERT INTO player_confidant_ranks (player_id, confidant_id, current_rank)
SELECT p.player_id, c.confidant_id, x.current_rank
FROM (VALUES ('Ryuji Sakamoto',3),('Ann Takamaki',1),('Sojiro Sakura',2)) AS x(confidant_name,current_rank)
JOIN player_profiles p ON p.player_name='Player Demo'
JOIN confidants c ON c.confidant_name=x.confidant_name
ON CONFLICT (player_id, confidant_id) DO NOTHING;

INSERT INTO confidant_interactions (confidant_id, rank_target, interaction_description, answer_text, affection_points, is_spoiler)
SELECT confidant_id, 4, 'Contoh pilihan dialog untuk rank target 4.', 'Contoh jawaban terbaik (dummy).', 3, TRUE
FROM confidants WHERE confidant_name='Ryuji Sakamoto'
AND NOT EXISTS (SELECT 1 FROM confidant_interactions ci WHERE ci.confidant_id=confidants.confidant_id AND ci.rank_target=4);

INSERT INTO qa_entries (game_date_id, question_type, question_text, answer_text, explanation, is_spoiler)
SELECT game_date_id, 'Class', 'Contoh pertanyaan kelas (dummy)', 'Contoh jawaban (dummy)', 'Ganti dengan data terverifikasi dari panduan game.', TRUE
FROM game_dates WHERE game_date='2026-04-13'
AND NOT EXISTS (SELECT 1 FROM qa_entries WHERE question_text='Contoh pertanyaan kelas (dummy)');

INSERT INTO personas (persona_name, level, arcana, notes) VALUES
('Arsene',1,'Fool','Contoh data Persona untuk pengujian.'),
('Pixie',2,'Lovers','Contoh data Persona untuk pengujian.'),
('Agathion',3,'Chariot','Contoh data Persona untuk pengujian.'),
('Jack-o-Lantern',2,'Magician','Contoh data Persona untuk pengujian.')
ON CONFLICT (persona_name) DO NOTHING;

INSERT INTO fusion_recipes (target_persona_id, recipe_name, source_name, notes)
SELECT p.persona_id, 'Contoh resep Arsene', 'Dummy', 'Resep ilustratif saja; verifikasi kombinasi asli sebelum dipakai.'
FROM personas p WHERE p.persona_name='Arsene'
AND NOT EXISTS (SELECT 1 FROM fusion_recipes fr WHERE fr.target_persona_id=p.persona_id AND fr.recipe_name='Contoh resep Arsene');

INSERT INTO fusion_recipe_materials (recipe_id, material_slot, persona_id)
SELECT fr.recipe_id, v.slot, p.persona_id
FROM fusion_recipes fr
JOIN personas target ON target.persona_id=fr.target_persona_id AND target.persona_name='Arsene' AND fr.recipe_name='Contoh resep Arsene'
JOIN (VALUES (1,'Pixie'),(2,'Agathion')) AS v(slot, persona_name) ON TRUE
JOIN personas p ON p.persona_name=v.persona_name
ON CONFLICT (recipe_id, material_slot) DO NOTHING;

INSERT INTO bosses (boss_name, first_available_date_id, last_available_date_id, is_optional, description, is_spoiler)
SELECT 'Contoh Boss (Dummy)', gd1.game_date_id, gd2.game_date_id, TRUE, 'Baris contoh untuk pengujian database, bukan boss kanonis.', TRUE
FROM game_dates gd1 CROSS JOIN game_dates gd2
WHERE gd1.game_date='2026-04-11' AND gd2.game_date='2026-04-13'
AND NOT EXISTS (SELECT 1 FROM bosses WHERE boss_name='Contoh Boss (Dummy)');

INSERT INTO boss_affinities (boss_id, element, affinity_type, notes)
SELECT boss_id, v.element, v.affinity_type, 'Nilai dummy; bukan informasi boss game.'
FROM bosses b CROSS JOIN (VALUES ('Fire','Weak'),('Ice','Resist'),('Electric','Normal')) AS v(element, affinity_type)
WHERE b.boss_name='Contoh Boss (Dummy)'
ON CONFLICT (boss_id, element) DO NOTHING;

INSERT INTO party_members (member_name) VALUES ('Joker'),('Ryuji'),('Ann'),('Morgana')
ON CONFLICT (member_name) DO NOTHING;

INSERT INTO recommended_party_members (boss_id, party_member_id, recommendation_notes)
SELECT b.boss_id, pm.party_member_id, 'Rekomendasi dummy untuk menguji relasi.'
FROM bosses b CROSS JOIN party_members pm
WHERE b.boss_name='Contoh Boss (Dummy)' AND pm.member_name IN ('Joker','Ann')
ON CONFLICT (boss_id, party_member_id) DO NOTHING;

COMMIT;
