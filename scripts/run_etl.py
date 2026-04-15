from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data.fetch_market import fetch_market_data
from app.data.fetch_news import fetch_news
from app.data.loader import save_data
from app.data.transform import clean_news


def main() -> int:
    output_dir = Path("scripts") / "outputs"

    market_data = fetch_market_data()
    raw_news = fetch_news()
    cleaned_news = clean_news(raw_news)

    market_saved = save_data(str(output_dir / "market_data.json"), market_data)
    news_saved = save_data(str(output_dir / "cleaned_news.json"), cleaned_news)

    if not (market_saved and news_saved):
        print("ETL pipeline failed while saving output files.")
        return 1

    print("ETL pipeline completed successfully.")
    print(f"Saved market data to: {output_dir / 'market_data.json'}")
    print(f"Saved cleaned news to: {output_dir / 'cleaned_news.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
