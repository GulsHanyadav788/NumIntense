import requests

def email_breach_check(email):
    print(f"\n[🛡️] Breach check for email: {email}")
    try:
        url = f"https://haveibeenpwned.com/unifiedsearch/{email}"
        headers = {"User-Agent": "NumIntensePro"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print("[⚠️] Found breaches!")
        elif r.status_code == 404:
            print("[✓] No breaches found.")
        else:
            print("[!] Could not perform breach check.")
    except Exception as e:
        print(f"[x] Error: {e}")
