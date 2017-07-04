from bs4 import BeautifulSoup
import urllib2
import json
import traceback
import datetime
import calendar
import re

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}

def call_api(url):
    req = urllib2.Request(url, headers=header)
    try:
        response = urllib2.urlopen(req)
        return response
    except urllib2.HTTPError, e:
        log("Error: " + str(e))
        return ""

def generate_soup(url):
    home_page = call_api(url)
    soup = BeautifulSoup(home_page,"html.parser")
    return soup

def log(msg):
    print msg

calendar_api = "/v2/calendar_months?key={}&currency={}&locale={}&listing_id={}&month={}&year={}&count={}&_format={}"
currency = "INR"
locale = "en-IN"
count = 12
_format = "with_conditions"

if __name__ == "__main__":
    home_url = "https://www.airbnb.co.in/rooms/14780765"
    soup = generate_soup(home_url)
    tags = soup.find_all(text=re.compile('minimum stay'))
    for tag in tags:
        parent = tag.parent
        class_ = parent.get("class")
        if class_ == None:
            continue
        if class_[0] != "col-md-6":
            continue
        avl_tag = parent.find("strong")
        if avl_tag == None:
            continue
        avl = avl_tag.string.split(" ")[0]


    baseURL = ""
    key = ""
    listing_id = ""
    month = ""
    year = ""
    listing_id = home_url[(home_url.rfind("/") + 1) : ]
    now  = datetime.datetime.now()
    year = now.year
    month = now.month + 1
    if(month > 12):
        month = 1
        year = year + 1

    reserved_dates = []

    meta_tags = soup.find_all("meta")
    for meta_tag in meta_tags:
        content = meta_tag.get("content")
        if content != None and content != "":
            if "api_config" in content:
                try:
                    json_obj = json.loads(content)
                    api_config = json_obj["api_config"]
                    baseURL = api_config["baseUrl"]
                    key = api_config["key"]
                except KeyError as e:
                    traceback.print_exc()
    if baseURL != None and baseURL != "" and key != None and key != "":
        calendar_url = (baseURL + calendar_api).format(key,currency,locale,listing_id,month,year,count,_format)
        response = call_api(calendar_url)
        try:
            calendar_json = json.load(response)
            for month_ in calendar_json["calendar_months"]:
                for day in month_["days"]:
                    avl = day["available"]
                    date = day["date"]
                    if avl == False or str(avl).lower() == "false":
                        if date not in reserved_dates:
                            reserved_dates.append(date)
        except Exception as e:
            log("Error: " + str(e))

    reserved_days = []
    for date in reserved_dates:
        splits = date.split("-")
        year_no = int(splits[0])
        month_no = int(splits[1])
        if (year_no == year and month_no >= month) or (year_no > year):
            date = int(splits[2])
            reserved_days.append(calendar.month_abbr[month_no] + " " + str(date))
    if len(reserved_days) == 0:
        reserved_days.append("NA")
    log(",".join(reserved_days))
