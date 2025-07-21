import requests

def truecaller_lookup(number):
    print(f"\n[📞] Truecaller Lookup for: {number}")
    try:
        dork = f'intext:"{number}" site:truecaller.com'
        print(f"[🔍] Google Dork: https://www.google.com/search?q={dork}")

        url = f"https://api.numspy.io/v1/lookup?number={number}"
        headers = {"User-Agent": "NumIntensePro"}
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            data = r.json()
            name = data.get("name")
            if name:
                print(f"[🧠] Name: {name}")
            else:
                print("[ℹ️] No name found.")
        else:
            print("[!] Could not fetch Truecaller data.")
    except Exception as e:
        print(f"[x] Error during lookup: {e}")
