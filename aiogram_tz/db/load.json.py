import json
import psycopg2
from psycopg2.extras import execute_batch

conn = psycopg2.connect(
    dbname="video_analytics",
    user="analytics_user",
    password="analytics123",
    host="localhost",
    port=5432
)

cur = conn.cursor()

with open("videos.json", encoding="utf-8") as f:
    data = json.load(f)["videos"]

videos_rows = []
snapshots_rows = []

for v in data:
    videos_rows.append((
        v["id"],
        v["creator_id"],
        v["video_created_at"],
        v["views_count"],
        v["likes_count"],
        v["comments_count"],
        v["reports_count"],
        v["created_at"],
        v["updated_at"]
    ))

    for s in v["snapshots"]:
        snapshots_rows.append((
            s["id"],
            v["id"],
            s["views_count"],
            s["likes_count"],
            s["comments_count"],
            s["reports_count"],
            s["delta_views_count"],
            s["delta_likes_count"],
            s["delta_comments_count"],
            s["delta_reports_count"],
            s["created_at"],
            s["updated_at"]
        ))

execute_batch(cur, """
INSERT INTO videos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING
""", videos_rows)

execute_batch(cur, """
INSERT INTO video_snapshots VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING
""", snapshots_rows)

conn.commit()
print("Данные загружены")
