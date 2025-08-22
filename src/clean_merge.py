import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_stat(filepath: Path, stat_name: str) -> pd.DataFrame:
    """Load a PGA stat CSV and keep only PLAYER + (AVG or %) column, renaming it to stat_name."""
    df = pd.read_csv(filepath)

    # Identify correct column name
    value_col = "AVG" if "AVG" in df.columns else "%"
    
    df = df[["PLAYER", value_col]].rename(columns={"PLAYER": "Player", value_col: stat_name})

    return df

if __name__ == "__main__":
    acc = load_stat(RAW_DATA_DIR / "driving_accuracy.csv", "DrivingAccuracy")
    dist = load_stat(RAW_DATA_DIR / "driving_distance.csv", "DrivingDistance")
    gir = load_stat(RAW_DATA_DIR / "gir.csv", "GIR")
    score = load_stat(RAW_DATA_DIR / "scoring_average.csv", "ScoringAverage")

    # Merge on Player
    df = acc.merge(dist, on="Player").merge(gir, on="Player").merge(score, on="Player")

    out_file = PROCESSED_DATA_DIR / "pga_stats_merged.csv"
    df.to_csv(out_file, index=False)

    print(f"\n✅ Saved merged dataset to {out_file}")
    print(df.head())
