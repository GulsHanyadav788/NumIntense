def spam_check(number):
    print(f"\n[🚫] Spam Report Lookup for: {number}")
    spam_sources = [
        f"https://www.google.com/search?q=spam report {number}",
        f"https://www.tellows.com/search?num={number}",
        f"https://www.shouldianswer.com/phone-number/{number.replace('+', '')}"
    ]
    for url in spam_sources:
        print(f"[Link] {url}")
