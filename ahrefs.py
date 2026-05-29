#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import sys
import re
import time
import json

BANNER = r"""
  _    _    _    _    _    _    _    _    _    _  
 / \  / \  / \  / \  / \  / \  / \  / \  / \  / \ 
( A )( h )( r )( e )( f )( s ) ( B )( u )( l )( k )
 \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/ 
            Domain & URL Rating Checker
"""
print(BANNER)

API_TOKEN = "PUT UR TOKEN HERE"
HEADERS = {
    "Authorization": "Bearer " + API_TOKEN,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def extract_domain_from_url(url):
    url = url.strip()
    url = re.sub(r'^(https?://)?(www\.)?', '', url)
    url = re.sub(r'/.*$', '', url)
    return url.rstrip('/')

def is_valid_line(line):
    line = line.strip()
    if not line:
        return False
    if '|' in line or 'domain:' in line or 'dr :' in line:
        return False
    return True

def clean_target(raw):
    return extract_domain_from_url(raw)

def get_metrics(target, retries=2):
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target

    url = "https://api.ahrefs.com/v3/batch-analysis/batch-analysis"
    payload = {
        "select": ["domain_rating", "url_rating"],
        "targets": [{
            "url": target,
            "mode": "exact",
            "protocol": "https"
        }]
    }

    for attempt in range(retries):
        try:
            response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
            print("  API status: {}".format(response.status_code))

            if response.status_code == 200:
                data = response.json()
                if data.get('targets') and len(data['targets']) > 0:
                    res = data['targets'][0]
                    dr = float(res.get('domain_rating', 0))
                    ur = float(res.get('url_rating', 0))
                    return {'dr': dr, 'ur': ur}
                else:
                    print("  No targets in response")
                    return {'dr': 0.0, 'ur': 0.0}
            elif response.status_code == 500:
                print("  Server error (500), retrying in 3s...")
                time.sleep(3)
                continue
            else:
                print("  API error: {}".format(response.text[:200]))
                return {'dr': 0.0, 'ur': 0.0}
        except Exception as e:
            print("  Request failed: {}".format(str(e)))
            if attempt < retries - 1:
                time.sleep(3)
            else:
                return {'dr': 0.0, 'ur': 0.0}
    return {'dr': 0.0, 'ur': 0.0}

def main():
    if len(sys.argv) < 2:
        print("Usage: python2 ahrefs.py list.txt")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except IOError:
        print("File {} not found.".format(filename))
        sys.exit(1)

    domains = []
    for line in lines:
        raw = line.strip()
        if not is_valid_line(raw):
            continue
        domain = clean_target(raw)
        if domain:
            domains.append(domain)

    if not domains:
        print("No valid domains found. Make sure the file contains one URL/domain per line.")
        sys.exit(1)

    print("Processing {} domains...".format(len(domains)))

    for domain in domains:
        print("\nChecking: {}".format(domain))
        metrics = get_metrics(domain)
        dr = metrics['dr']
        ur = metrics['ur']

        result_line = "domain: {} | dr : {} | ur : {}".format(domain, dr, ur)
        print("  Result: {}".format(result_line))

        if dr > 5 or ur > 5:
            with open('res.txt', 'a') as out_file:
                out_file.write(result_line + "\n")
            print("  >> Saved to res.txt")
        else:
            print("  >> Does not meet criteria (DR <= 5 and UR <= 5)")

        time.sleep(1.5)

    print("\nDone. Results saved in res.txt")

if __name__ == "__main__":
    main()