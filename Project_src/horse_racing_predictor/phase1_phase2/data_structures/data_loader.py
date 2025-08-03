import pandas as pd

def load_horses_from_excel(filepath, db):
    # Loads horse data from an Excel
    # Excel columns: horse_id, name, avg_speed, win_ratio
    df = pd.read_excel(filepath)
    for _, row in df.iterrows():
        db.add_horse(
            row['horse_id'],
            {
                "name": row['name'],
                "avg_speed": float(row['avg_speed']),
                "win_ratio": float(row['win_ratio'])
            }
        )