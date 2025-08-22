import requests
import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def scrape_stat(stat_id: int, stat_name: str, season: int = 2024) -> pd.DataFrame:
    """
    Scrape a PGA Tour stat leaderboard given its stat_id and season.
    Example stat IDs:
        101 = Driving Distance
        102 = Driving Accuracy
        103 = GIR%
        120 = Scoring Average
    """
    url = f"https://statdata.pgatour.com/r/{stat_id}/{season}.json"
    print(f"Fetching {stat_name} from {url} ...")

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Data is under "tours" -> "years" -> "stats" -> "details"
    players = data["tours"][0]["years"][0]["stats"][0]["details"]

    rows = []
    for p in players:
        rank = p.get("rank", "")
        player_name = p.get("playerName", "")
        value = p.get("value", "")
        rows.append([rank, player_name, value])

    df = pd.DataFrame(rows, columns=["Rank", "Player", stat_name])
    return df


if __name__ == "__main__":
    df = scrape_stat(101, "DrivingDistance", 2024)
    print(df.head())

    out_file = RAW_DATA_DIR / "driving_distance.csv"
    df.to_csv(out_file, index=False)
    print(f"Saved {out_file}")

