import requests
from bs4 import BeautifulSoup
from datetime import datetime
import dateparser
import time

BASE = "https://www.fiverr.com"
CATEGORY = "/categories/programming-tech/buy/website-development/landing-page"
HEADERS = {"User-Agent": "Mozilla/5.0"}

CUTOFF = datetime.now() - dateparser.parse("3 months ago")

def fetch_gig_urls(page=1):
    url = BASE + CATEGORY + f"?page={page}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, 'html.parser')
    urls = []
    for p in soup.select('p[role="heading"][aria-level="3"]'):
        a = p.find_parent('a', href=True)
        if a:
            link = a['href']
            if link.startswith('/'):
                link = BASE + link
            urls.append(link)
    return urls

def has_recent_review(gig_url):
    soup = BeautifulSoup(requests.get(gig_url, headers=HEADERS).text, 'html.parser')
    tags = soup.select('p[class*="_5plgh7k"] time')
    for t in tags:
        dt = dateparser.parse(t.get_text(strip=True))
        if dt and dt >= CUTOFF:
            return True
    return False

def analyze(pages=3, limit=200):
    urls = []
    for p in range(1, pages+1):
        print(f"Страница {p}…")
        urls += fetch_gig_urls(p)
        time.sleep(0.5)
    urls = urls[:limit]
    print(f"Гигов на проверку: {len(urls)}")

    count = 0
    for i, u in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}]")
        if has_recent_review(u): count += 1
        time.sleep(0.5)

    ratio = count / len(urls) if urls else 0
    estimate = round(ratio * 22000)
    print(f"\nВсего гигов: {len(urls)}")
    print(f"С отзывами ≤ 3 мес: {count}")
    print(f"Доля: {ratio:.1%}, Примерно: {estimate} фрилансеров")

if __name__ == "__main__":
    analyze()
