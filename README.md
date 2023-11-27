### NS&I Premium Bond Prize Checker

Scrapy spider to reproduce NS&I prize check POST request.

---

_**Process:**_

1. Holder names and numbers strings are loaded in from .env file with python-dotenv.
2. Holder names and numbers strings are split into lists.
3. Holder names and numbers lists are zipped together to get list of (name, number) tuples.
4. The spider performs a prize check POST request for each holder tuple, and writes result to a holder-unique txt file.

---

_**example_results.txt:**_

Holder: Example Account (XXXXXXXXX)

Congratulations!\
You've won £200 in November 2023's draw

Prize History:\
	Date: November 2023, Bond Number: XXXXXXXXXXX, Prize: £100\
	Date: November 2023, Bond Number: XXXXXXXXXXX, Prize: £100

---

_**Next steps:**_

Run check on results day, email results to account holders.
