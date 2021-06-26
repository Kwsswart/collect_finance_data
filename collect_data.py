import re
import json
import requests
from bs4 import BeautifulSoup as bs


def collect_data(ticker):
    main_url = f"https://finance.yahoo.com/quote/{ticker.upper().strip()}"
    res = requests.get(main_url)
    soup = bs(res.text, "lxml")

    try: ticker_name = soup.find("h1").text
    except: ticker_name = ticker

    try: price = soup.find("div", {"id": "quote-market-notice"}).parent.find("span").text
    except: price = None

    try: market_cap = soup.find("td", text="Market Cap").parent.find_all("td")[-1].text
    except: market_cap = None

    try: beta = soup.find("td", text=re.compile("Beta")).parent.find_all("td")[-1].text
    except: beta = None

    try: pe_ratio = soup.find("td", text=re.compile("PE Ratio")).parent.find_all("td")[-1].text
    except: pe_ratio = None

    try: eps = soup.find("td", text=re.compile("EPS")).parent.find_all("td")[-1].text
    except: eps = None

    try: target_est = soup.find("td", text=re.compile("Target Est")).parent.find_all("td")[-1].text
    except: target_est = None

    analysis_url = f"https://finance.yahoo.com/quote/{ticker.upper().strip()}/analysis?p={ticker.upper().strip()}"
    res = requests.get(analysis_url)
    soup = bs(res.text, "lxml")

    try: sales_growth = soup.find("span", text=re.compile("Sales Growth")).parent.findNext('td').text
    except: sales_growth = None

    try: current_year_growth_estimate = soup.find("th", text=re.compile("Growth Estimates")).parent.parent.parent \
        .find("span", text=re.compile("Current Year")).parent.findNext("td").text
    except: current_year_growth_estimate = None

    try: next_5_years_growth_estimate = soup.find("th", text=re.compile("Growth Estimates")).parent.parent.parent \
        .find("span", text=re.compile("Next 5 Years")).parent.findNext("td").text
    except: next_5_years_growth_estimate = None

    try: past_5_years_growth_estimate = soup.find("th", text=re.compile("Growth Estimates")).parent.parent.parent \
        .find("span", text=re.compile("Past 5 Years")).parent.findNext("td").text
    except: past_5_years_growth_estimate = None

    data = dict()
    data["TICKER_NAME"] = ticker_name
    data["PRICE"] = price
    data["MARKET_CAP"] = market_cap
    data["BETA"] = beta
    data["PE_RATIO"] = pe_ratio
    data["EPS"] = eps
    data["TARGET_EST"] = target_est
    data["SALES_GROWTH"] = sales_growth
    data["CURRENT_YEAR_GROWTH_RATIO"] = current_year_growth_estimate
    data["NEXT_5_YEARS_GROWTH_RATIO"] = next_5_years_growth_estimate
    data["PAST_5_YEARS_GROWTH_RATIO"] = past_5_years_growth_estimate

    for key in data.keys():
        try: data[key] = data[key].strip()
        except: pass
        if data[key] == "N/A":
            data[key] = None

    with open("data.jsonlines", "a") as dest:
        dest.write(json.dumps(data))
        dest.write("\n")