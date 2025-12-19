# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extras import RealDictCursor

# ⚠️ лучше вынести в config.py
DB_CONFIG = {
    "dbname": "video_analytics",
    "user": "analytics_user",
    "password": "analytics123",
    "host": "localhost",
    "port": 5432
}
for k, v in DB_CONFIG.items():
    print(k, repr(v))

def fetch_value(sql, params):
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cur = conn.cursor()
    cur.execute(sql, params)
    result = cur.fetchone()[0]
    conn.close()
    return result
