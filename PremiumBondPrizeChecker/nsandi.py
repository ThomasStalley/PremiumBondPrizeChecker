import json
import os

import scrapy
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser

# Load holder name, number pairs from env file:
load_dotenv()
holder_names = os.getenv('NAMES').split(",")
holder_numbers = os.getenv('NUMBERS').split(",")
holder_number_name_pairs = zip(holder_names, holder_numbers)


class PremiumBondSpider(scrapy.Spider):
    name = "premium_bond"
    allowed_domains = ["nsandi.com"]
    start_urls = ["https://www.nsandi.com/premium-bonds-have-i-won-ajax"]

    def start_requests(self):
        url = "https://www.nsandi.com/premium-bonds-have-i-won-ajax"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.nsandi.com/prize-checker",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.nsandi.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

        # Post request to prize check page for each holder:
        for holder_number_name_pair in holder_number_name_pairs:
            number = holder_number_name_pair[0]
            name = holder_number_name_pair[1]

            cb_kwargs = {"name": name, "number": number}
            body = f"field_premium_bond_period=this_month&field_premium_bond_number={number}"
            yield scrapy.Request(
                url=url,
                method="POST",
                headers=headers,
                body=body,
                callback=self.parse,
                cb_kwargs=cb_kwargs,
                dont_filter=True
            )

    def parse(self, response, name, number):
        response_data = json.loads(response.body)

        # Detail of account holder, and overall win:
        display_name = name.replace("_", " ").title()
        header = response_data["header"]
        tagline = response_data["tagline"]
        history = response_data["history"]
        formatted_text = f"Holder: {display_name} ({number})\n\n"
        formatted_text += f"{header}\n"
        formatted_text += f"{tagline}\n\n"

        # Detail of each prize:
        formatted_text += "Prize History:\n"
        for entry in history:
            date = entry["date"]
            bond_number = entry["bond_number"]
            prize = entry["prize"]
            formatted_text += f"\tDate: {date}, Bond Number: {bond_number}, Prize: £{prize}\n"

        # Saving the formatted text to a txt file:
        file_name = name.lower()
        file = f"Results/{file_name}_results.txt"
        with open(file=file, mode="w") as file:
            file.write(formatted_text)


# Initialise crawler, with custom settings:
process = CrawlerProcess(settings={
    "DOWNLOAD_DELAY": 3,
    "AUTOTHROTTLE_ENABLED": True,
    "AUTOTHROTTLE_START_DELAY": 5,
    "AUTOTHROTTLE_MAX_DELAY": 60,
    "RANDOMIZE_DOWNLOAD_DELAY": True,
    "ROBOTSTXT_OBEY": True,
    "CONCURRENT_REQUESTS": 16
})
process.crawl(PremiumBondSpider)
process.start()
