import requests
import re

# List of popular ad-block hosts sources
HOSTS_SOURCES = [
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt",
    "https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt",
    "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt"
]

HOSTS_FILE = "hosts"

def fetch_hosts(url):
    print(f"Fetching: {url}")
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

def extract_domains(hosts_content):
    domains = set()
    for line in hosts_content.splitlines():
        line = line.strip()
        # Match: 0.0.0.0 domain or 127.0.0.1 domain
        m = re.match(r"^(0\.0\.0\.0|127\.0\.0\.1)\s+([^\s#]+)", line)
        if m:
            domains.add(m.group(2))
    return domains

def main():
    all_domains = set()
    for url in HOSTS_SOURCES:
        hosts_raw = fetch_hosts(url)
        all_domains.update(extract_domains(hosts_raw))
    
    with open(HOSTS_FILE, "w") as f:
        f.write("# Unified ad-block hosts file for Android games\n")
        f.write("# Generated automatically\n\n")
        for domain in sorted(all_domains):
            f.write(f"0.0.0.0 {domain}\n")

if __name__ == "__main__":
    main()