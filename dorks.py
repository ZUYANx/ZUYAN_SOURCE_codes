import requests
from bs4 import BeautifulSoup
import time
import re

def logger(filename, data):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(data + "\n")

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_]', '_', text)

def bing_search(query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.bing.com/search?q={query}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("li", {"class": "b_algo"})
        found = False
        for li in links:
            a = li.find("a")
            if a and "http" in a['href']:
                print(f"[BING] [+] {a['href']}")
                logger("dorks_results.txt", a['href'])
                found = True
        if not found:
            print(f"[BING] [-] No results for: {query}")
    except Exception as e:
        print(f"[BING] [!] Error on {query}: {e}")

def duckduckgo_search(query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://html.duckduckgo.com/html/?q={query}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", class_="result__a")
        found = False
        for link in links:
            href = link.get("href")
            if href:
                print(f"[DUCK] [+] {href}")
                logger("dorks_results.txt", href)
                found = True
        if not found:
            print(f"[DUCK] [-] No results for: {query}")
    except Exception as e:
        print(f"[DUCK] [!] Error on {query}: {e}")

def auto_dork_scan():
    dorks = [
        'inurl:/upload.php',
        'inurl:/admin/upload/',
        'inurl:php?file=',
        'inurl:view.php?page=',
        'intitle:"index of" "shell.php"',
        'inurl:cmd.php',
        'inurl:login.php site:.gov',
        'inurl:config.php',
        'inurl:admin/login.php',
        'inurl:wp-content/plugins/',
    ]

    for dork in dorks:
        print(f"\n[>] Searching Dork: {dork}")
        bing_search(dork)
        time.sleep(1)
        duckduckgo_search(dork)
        time.sleep(1)

if __name__ == "__main__":
    print("=== Auto Dork Scanner (BING + DUCK) by MR ZUYAN ===\n")
    auto_dork_scan()