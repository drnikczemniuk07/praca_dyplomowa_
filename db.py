import sqlite3
from pathlib import Path 

DB_PATH = Path("data")/"library.db"



def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracks (
                    id INTEGER PRIMARY KEY,
                    path TEXT NOT NULL UNIQUE,
                    duration_sec REAL NOT NULL,
                    rms_mean REAL NOT NULL,
                    spectral_centroid_mean_hz REAL NOT NULL,
                    spectral_rolloff_mean_hz REAL NOT NULL,
                    tempo_bpm REAL NOT NULL,
                    key TEXT NOT NULL 
                    
                );
     """)   
    cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tracks_bpm_tempo
                ON tracks(tempo_bpm);
                  """)
    cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tracks_key 
                ON tracks(key);
                   """)    
        
    # cursor.execute("PRAGMA table_info(tracks);")
    # print("COLUMNS:", cursor.fetchall())
    # cursor.execute("PRAGMA index_list(tracks);")
    # print("INDEXES:", cursor.fetchall())
    
        
    conn.commit()
    conn.close()
    
def insert_tracks(path: str, features: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    #cursor.execute("PRAGMA database_list;")
    #print("DB LIST (inside insert):", cursor.fetchall())
    cursor.execute("""
                INSERT INTO tracks (path, duration_sec, rms_mean, spectral_centroid_mean_hz, spectral_rolloff_mean_hz, tempo_bpm, key)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                duration_sec = excluded.duration_sec,
                rms_mean = excluded.rms_mean,
                spectral_centroid_mean_hz = excluded.spectral_centroid_mean_hz,
                spectral_rolloff_mean_hz = excluded.spectral_rolloff_mean_hz,
                tempo_bpm = excluded.tempo_bpm,
                key = excluded.key
                    """, (
                        path,
                        features["duration_sec"],
                        features["rms_mean"],
                        features["spectral_centroid_mean_hz"],
                        features["spectral_rolloff_mean_hz"],
                        features["tempo_bpm"],
                        features["key"]
                        
    ))
    
    #print("lastrowid:", cursor.lastrowid) 
    conn.commit()
    conn.close()
    
def get_all_tracks():
    tracks = []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks") 
    rows =  cursor.fetchall()
    column_names = [col[0] for col in cursor.description]
    for row in rows:
        track = dict(zip(column_names, row))
        tracks.append(track)
    conn.close()
    return tracks

def delete_track(path: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tracks WHERE path = ?", (path,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    # insert_tracks(
    #     "test.wav",
    #     {
    #         "duration_sec": 10.0,
    #         "rms_mean": 0.05,
    #         "spectral_centroid_mean_hz": 2500.0,
    #         "spectral_rolloff_mean_hz": 5000.0,
    #         "tempo_bpm": 128.0,
    #         "key": "Am"
    #     }
    # )
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, path, tempo_bpm, key FROM tracks ORDER BY id;")
    print("ROWS:", cursor.fetchall())
    conn.close()
    
