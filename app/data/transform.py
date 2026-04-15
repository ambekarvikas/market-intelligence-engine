def clean_news(articles: list) -> list[dict]:
    cleaned_articles = []

    for article in articles or []:
        if not isinstance(article, dict):
            cleaned_articles.append({"text": "", "timestamp": ""})
            continue

        title = str(article.get("title") or "").strip()
        summary = str(article.get("summary") or "").strip()
        text = " - ".join(part for part in [title, summary] if part).strip()
        timestamp = str(article.get("published") or article.get("timestamp") or "").strip()

        cleaned_articles.append(
            {
                "text": text,
                "timestamp": timestamp,
            }
        )

    return cleaned_articles
