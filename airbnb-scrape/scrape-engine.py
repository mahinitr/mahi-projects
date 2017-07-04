# To scrape the data from website like AirBnb.com
# Urllib2, BeautifulSoup, mechanize, scrapemark, scrapy
import traceback
import urllib2
from util import HouseModel, log, isnumber, initialize
from bs4 import BeautifulSoup
import math
import re
import locale
import json
import datetime
import calendar
import  os

AIRBNB_ROOT_URL = "https://www.airbnb.co.in"
AIRBNB_S_URL = "https://www.airbnb.co.in/s"

HOME_PAGE_BODY_CLASS = "space-8 space-top-8"
DISPLAY_ADDRESS = "display-address"
HOME_PAGE_BODY_TITLE_CLASS = "space-4 text-center-sm"
BOOK_DIV_CLASS = "book-it__container js-book-it-container"
BOOK_PRICE_CLASS = "book-it__price-amount text-special"
RENTALS_CLASS = "crossfading-panel--vertically-centered h6 text-right pull-right"
HOME_PAGE_BODY_TITLE = "About this listing"
DATA_REACTID = "data-reactid"
LISTING_NAME = "listing_name"
#PF stands for Postfix
ACC_VAL_PF = "[$]Accommodates="
BATHROOMS_VAL_PF =  "[$]Bathrooms="
BEDROOMS_VAL_PF = "[$]Bedrooms="
BEDTYPE_VAL_PF = "[$]Bed type="
BEDS_VAL_PF = "[$]Beds="
COST_SPAN_CLASS = "h3 text-contrast price-amount"
WEEKLY_DIS_VAL_PF = "[$]Weekly discount="
MONTHLY_DIS_VAL_PF = "[$]Monthly discount="
MIN_STAY_VAL_PF = ".p.1.0.0"
CLEANING_FEE_VAL_PF = "[$]Cleaning Fee="
EXTRA_PPL_VAL_PF = "[$]Extra people="
SEC_DEPOSIT_VAL_PF = "[$]Security Deposit="

calendar_api = "/v2/calendar_months?key={}&currency={}&locale={}&listing_id={}&month={}&year={}&count={}&_format={}"
currency = "INR"
locale_str = "en-IN"
count = 12
MAX_NO = 20
_format = "with_conditions"

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
    log("Generating soup for url : " + url)
    home_page = call_api(url)
    soup = BeautifulSoup(home_page,"html.parser")
    return soup

def extract_cost(price):
    decimal_point_char = locale.localeconv()['decimal_point']
    clean = re.sub(r'[^0-9' + decimal_point_char + r']+', '', price)
    value = int(clean)
    return value

def populate_extra_prices(listing_div,div_id,cost_per_night,result):
    extra_price_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(EXTRA_PPL_VAL_PF)})
    for i in range(MAX_NO):
        result.PRICES_PER_ALL[i] = str(cost_per_night)
    if extra_price_tag != None and cost_per_night != None:
        if " / " in extra_price_tag.string:
            extra_price_arr = extra_price_tag.string.split("/")
            result.EXTRA_PRICE_NIGHT= extra_price_arr[0].strip()
            result.EXTRA_PRICE_NIGHT= extract_cost(result.EXTRA_PRICE_NIGHT)
            result.EXTRA_AFTER_PPL = (extra_price_arr[1].strip()).split(" ")[2]
            if(isnumber(result.EXTRA_AFTER_PPL)):
                no = int(result.EXTRA_AFTER_PPL)
            elif "first" in extra_price_arr[1].strip():
                no = 1
            elif "second" in extra_price_arr[1].strip():
                no = 2
            elif "third" in extra_price_arr[1].strip():
                no = 3
            elif "fourth" in extra_price_arr[1].strip():
                no = 4
            elif "fifth" in extra_price_arr[1].strip():
                no = 5
            elif "sixth" in extra_price_arr[1].strip():
                no = 6
            elif "seventh" in extra_price_arr[1].strip():
                no = 7
            result.EXTRA_AFTER_PPL = str(no)
            for i in range(1,MAX_NO+1):
                if i <= no:
                    price = cost_per_night
                else:
                    price = cost_per_night + ((i - no) * int(result.EXTRA_PRICE_NIGHT))
                result.PRICES_PER_ALL[i-1] = str(price)




def populate_reserved_dates(home_url, soup, result):
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
        calendar_url = (baseURL + calendar_api).format(key,currency,locale_str,listing_id,month,year,count,_format)
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
            traceback.print_exc()
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
    result.RESERVED_DAYS_12_MONTHS = ",".join(reserved_days)

def extract_data_from_house_page(home_url,line):
    soup = generate_soup(home_url)
    divs_list = soup.find_all("div",class_=HOME_PAGE_BODY_CLASS)
    listing_div = None
    for div in divs_list:
        h4_tag = div.find('h4',class_=HOME_PAGE_BODY_TITLE_CLASS)
        if h4_tag.string == HOME_PAGE_BODY_TITLE:
            listing_div = div
            break
    if listing_div is None:
        log("Not found required div, exiting...")
        return

    result = HouseModel()
    if "sw_lat" in line and "sw_lng" in line:
        query_splits = line.split("&")
        for split in query_splits:
            if "sw_lat" in split:
                result.SW_LATT = split.split("=")[1]
            elif "sw_lng" in split:
                result.SW_LNG = split.split("=")[1]
            elif "ne_lat" in split:
                result.NE_LATT = split.split("=")[1]
            elif "ne_lng" in split:
                result.NE_LNG = split.split("=")[1]

    div_id = listing_div.get(DATA_REACTID)
    address_div = soup.find("div", attrs={"id":DISPLAY_ADDRESS})
    address = address_div.find("a").string

    addr_split = address.split(",")
    if len(addr_split) == 3:
        result.CITY = addr_split[0].strip()
        result.STATE = addr_split[1].strip()
        result.COUNTRY = addr_split[2].strip()
    result.PROP_NAME = soup.find("h1", attrs={"id": LISTING_NAME}).string
    result.PROP_URL = home_url
    max_ppl_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(ACC_VAL_PF)})
    if max_ppl_tag != None:
        result.MAX_PPL = max_ppl_tag.string

    bedrooms_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(BEDROOMS_VAL_PF)})
    if bedrooms_tag != None:
        result.BEDROOMS = bedrooms_tag.string

    beds_tag  = listing_div.find("strong", attrs={DATA_REACTID: re.compile(BEDS_VAL_PF)})
    if beds_tag != None:
        result.BEDS = beds_tag.string

    bathrooms_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(BATHROOMS_VAL_PF)})
    if bathrooms_tag != None:
        result.BATHROOMS = bathrooms_tag.string

    min_stay_tags = soup.find_all(text=re.compile('minimum stay'))
    for tag in min_stay_tags:
        parent = tag.parent
        class_ = parent.get("class")
        if class_ == None:
            continue
        if class_[0] != "col-md-6":
            continue
        avl_tags = parent.find_all("strong")
        for avl_tag in avl_tags:
            if "night" in avl_tag.string:
                splits = avl_tag.string.split(" ")
                if isnumber(splits[0]):
                    result.NIGHTS_MIN_STAY = splits[0]
                    break

    price_span = soup.find("span", class_ = COST_SPAN_CLASS)
    price = price_span.find("span").string
    cost_per_night = extract_cost(price)

    security_deposit_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(SEC_DEPOSIT_VAL_PF)})
    if security_deposit_tag != None:
        result.SECURITY_DEPOSIT = security_deposit_tag.string
        result.SECURITY_DEPOSIT = extract_cost(result.SECURITY_DEPOSIT)

    cleaning_fee_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(CLEANING_FEE_VAL_PF)})
    if cleaning_fee_tag != None:
        result.CLEANING_FEE = cleaning_fee_tag.string
        result.CLEANING_FEE = extract_cost(result.CLEANING_FEE)

    weekly_dis_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(WEEKLY_DIS_VAL_PF)})
    if weekly_dis_tag != None:
        result.WEEKLY_DIS = weekly_dis_tag.string

    monthly_dis_tag = listing_div.find("strong", attrs={DATA_REACTID: re.compile(MONTHLY_DIS_VAL_PF)})
    if monthly_dis_tag != None:
        result.MONTHLY_DIS = monthly_dis_tag.string

    populate_extra_prices(listing_div,div_id,cost_per_night,result)

    populate_reserved_dates(home_url,soup,result)

    return result


def scrape_web(url,line,output_path,db,latest_num):
    page_url = url
    soup = generate_soup(page_url)
    rentals_tag = soup.find("h1", class_=RENTALS_CLASS)
    span_tag_splits = rentals_tag.find("span").string.split(" ")
    no_of_results = span_tag_splits[0]
    if no_of_results.isdigit():
        no_of_results = int(no_of_results)
    elif no_of_results.endswith("+"):
        no_of_results = no_of_results[:-1]
        no_of_results = int(no_of_results)
    else:
        log("Error: Unable to scrape the no of results from the page " + url)
        no_of_results = 1
    no_pages = int(math.ceil(no_of_results/18.0))
    pages = range(1,no_pages + 1)
    all_homes_urls = []
    for i in pages:
        if i != 1:
            page_url = url + "?page=" + str(i)
            soup = generate_soup(page_url)
        results_div = soup.find("div", class_="search-results")
        if results_div is None:
            log("No records found at URL " + page_url)
            return
        anchor_tags = results_div.find_all("a",class_="media-photo media-cover")
        for a in anchor_tags:
            home_url = AIRBNB_ROOT_URL + a.get("href")
            if home_url not in all_homes_urls:
                all_homes_urls.append(home_url)
    log("\nNow scraping the content from each home page..., found {} results for input {}".format(len(all_homes_urls),line))
    try:
        for home_url in all_homes_urls:
            result = extract_data_from_house_page(home_url,line)
            try:
                db.write_to_db(result)
            except:
                traceback.print_exc()
        log("Successfully process scraping and stored results to DB.")
        log("Now reading the results with Number > {} and writing to CSV file...".format((latest_num)))
        db.retrieve_and_wrtie_to_csv(output_path, latest_num)
        db.close()
    except Exception as e:
        log("Error: " + str(e))
        traceback.print_exc()
        log("The results of now are stored into mysqlDB, from the NUMBER " + str(latest_num + 1))



def generate_address(address, char):
    address_str = ""
    splits = address.split(char)
    for elem in splits:
        if elem.strip() != "":
            address_str = address_str + "--" + elem.strip()
    address_str = address_str.strip("-")
    address_str = address_str.strip(" ")
    return address_str

def generate_url(input):
    if "sw_lat" in input and "sw_lng" in input:
        return AIRBNB_S_URL + "?" + input
    address = input
    if "," in address:
        address = generate_address(address, ",")
    if " " in address:
        address = generate_address(address, " ")
    url = AIRBNB_S_URL + "/" + address
    return url

def read_input(file):
    try:
        lines = []
        with open(file) as fp:
            lines = fp.readlines()
        return lines
    except Exception as e:
        traceback.print_exc()
        log("Error: Error occured while reading input file")


def process_engine(file_path,output_path,db,latest_num):
    lines = read_input(file_path)
    for line in lines:
        line = line.strip()
        try:
            log("Processing input : " + line)
            url = generate_url(line)
            scrape_web(url,line,output_path,db,latest_num)
        except Exception as e:
            log("Error: " +  str(e))
            traceback.print_exc()
            log("Error: Something went wrong with input:" + line)

if __name__ == "__main__":
    log("...Welcome to Scraping Tool..")
    log("Please read file README, before running...")
    config = initialize("config.json")
    if config is None:
        log("Error: Some thing went wrong, exiting...")
    else:
        input_file, output_file, db = config
        if input_file == None or input_file.strip() == "":
            log("Error: No input file provided")
        if output_file == None or output_file.strip() == "":
            log("Error: No output file provided")
        if db == None:
            log("Error: Failed to initialize DB")
            os._exit(0)
        log("input_file : " + input_file)
        log("output_file : " + output_file)
        log("Initialized Database")
        latest_num = db.get_latest_num()
        if latest_num == None:
            log("Error while reading the latest num from DB.")
            os._exit(0)
        process_engine(input_file,output_file,db, latest_num)