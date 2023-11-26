### NS&I Premium Bond Prize Checker

Scrapy spider to reproduce NS&I prize check POST request.

---

Process:

1. Holder names and numbers strings are loaded in from .env file with python-dotenv.
2. Holder names and numbers strings are split into lists.
3. Holder names and numbers lists are zipped together to get list of (name, number) tuples.
4. The spider performs a prize check POST request for each holder tuple, and writes result to a holder-unique txt file.

---

Next steps:

Run check on results day, email results to account holders.