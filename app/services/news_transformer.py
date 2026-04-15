def clean_news(articles: list) -> list[dict]:
    cleaned_articles = []

    for article in articles or []:
        if not isinstance(article, dict):
            cleaned_articles.append({"text": "", "timestamp": ""})
            continue

        text = article.get("text")
        if not text:
            title = article.get("title") or ""
            summary = article.get("summary") or ""
            text = " - ".join(part for part in [title, summary] if part).strip()

        timestamp = article.get("timestamp")
        if not timestamp:
            timestamp = article.get("published_date") or article.get("published") or ""

        cleaned_articles.append(
            {
                "text": str(text or "").strip(),
                "timestamp": str(timestamp or "").strip(),
            }
        )

    return cleaned_articles
