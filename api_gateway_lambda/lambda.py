import json
import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context) -> dict:
    """
    Function take the website url from aws rest api gateway.
    Parse the website with beautifulsoup, format the necessary data and return it in body response.
    """
    # getting URL from event. example URL: "https://excheck.pro/company/4205160147-resurs"
    url = event['body']
    url = url.split(":", 1)[-1].strip('"} ')

    # define user-agent
    ua = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/112.0.0.0 Safari/537.36"}

    # translate months
    months = {
        "янв": "jan",
        "фев": "feb",
        "мар": "mar",
        "апр": "apr",
        "мая": "may",
        "июн": "jun",
        "июл": "jul",
        "авг": "aug",
        "сен": "sep",
        "окт": "oct",
        "ноя": "nov",
        "дек": "dec",
    }

    # make request
    response = requests.get(url=url, headers=ua)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html5lib")

    # retrieve company_name
    company_name = soup.find(class_="fst-normal d-block pb-2").text
    company_name = company_name[company_name.find("\""):].strip("\"").title()

    # retrieve company_form
    company_form = soup.find("h1", class_="mb-2").text
    company_form = company_form[:company_form.find("\"")].strip()

    # retrieve INN
    inn = soup.find(id="copy-inn").text

    # retrieve date and format it to dd/mon/yyyy
    data = soup.find("section", class_="info-columns").find("div").find_all("div")
    data = data[1].text.split()
    data.pop()
    data[1] = months[data[1][:3]]

    # get post index
    post_index = soup.find("section", id="contacts-section").find_all("div")[-1].text[:6]

    # get phone number
    phone_number = soup.find("section", id="contacts-section").find_all("a")[2]['href'][4:]
    if not phone_number.startswith("+"):
        phone_number = "-----"

    # get company website
    website = soup.find("section", id="contacts-section").find_all("div", class_="col")[1].find_all('a')[-1]['href']
    if "http" not in website:
        website = "-----"

    # forming a result with company data
    result = {
        'company_name': company_name,
        'company_form': company_form,
        'inn': inn,
        'date': "/".join(data),
        'post_index': post_index,
        'phone_number': phone_number,
        'website': website
    }

    response = {
        "isBase64Encoded": "false",
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
        'body': json.dumps(result, ensure_ascii=False)
    }

    # returning the function response
    return response
