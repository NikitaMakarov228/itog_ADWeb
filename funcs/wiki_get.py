import wikipediaapi
from funcs.translation import translate_word
import string


def fetch_wikipedia_article(title):
    title = translate_word(title)
    user_agent = "Studies (nikita228makar228@gmail.com)"
    wiki = wikipediaapi.Wikipedia(
        user_agent=user_agent, extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    page = wiki.page(title)

    if not page.exists():
        return f"Статья с названием '{title}' не найдена."
    return {
        "title": page.title,
        "text": page.text.split("\nSee also\n")[0],
        "link": page.fullurl,
    }
