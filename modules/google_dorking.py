def generate_dorks(number):
    dorks = [
        f'intext:"{number}" site:facebook.com',
        f'intext:"{number}" site:instagram.com',
        f'intext:"{number}" site:linkedin.com',
        f'intext:"{number}" site:twitter.com',
        f'intext:"{number}" site:pinterest.com',
        f'intext:"{number}" site:pastebin.com',
        f'intext:"{number}" ext:pdf OR ext:doc',
        f'"{number}"'
    ]
    return [f"https://www.google.com/search?q={dork}" for dork in dorks]
