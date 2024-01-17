import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
import gspread
from google.oauth2 import service_account


key_path = '' #actual path to your service account key file
credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(credentials)
sh = gc.open_by_key('') #Google Sheets API key
current_sheet = sh.sheet1

URL = "https://www.cse.iitb.ac.in"

base_url = URL
if base_url.endswith("/"):
    base_url = base_url[:-1]

scanned = []


def parse_a_tags(a_tags):
    links = []

    for a in a_tags:
        # print(a_tags)
        link = a["href"]
        # links.clear()
        # print(a)
        # b= re.findall(r'share',a)
        # print(b)
        # if b:
        #     a_tags.remove(a)
        # else:
        #     continue
        # url = "https://dampmemsiitb.wordpress.com/2020/07/22/mm201-structure-of-materials/?share=twitter"
        pattern = r'\bshare=\b'

        match = re.search(pattern, link)

        if match:
            continue
        else:
            # Skip certain links
            if link.startswith("#") or link.startswith("mailto:") or link == "/":
                continue

            if link.startswith("/"):
                link = "{}{}".format(base_url, link)

            if not link.startswith("http://") and not link.startswith("https://"):
                link = "{}/{}".format(base_url, link)

            if not link.startswith(base_url):
                continue
            
            # if link.contains
            if link not in links:
                links.append(link)
    result_list = [[link] for link in links]
    current_sheet.update([result_list])
    return links


def scan(url):
    scanned.append(url)

    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")
    a_tags = soup.find_all("a", href=True)
    # print(a_tags)
    links = parse_a_tags(a_tags)
    links = links[1:]
    scanned.append(links)

    next_scan_urls = [link for link in links if link not in scanned]
    # print(next_scan_urls)

    if len(next_scan_urls) != 0:
        for link in next_scan_urls:
            scan(link)
    return scanned 


if __name__ == "__main__":
    links = scan(base_url)



    # df=pd.DataFrame(links)
    # df.to_csv('csedepartment.csv', index=True)
