# mail_scraper

This is a Python project that uses Scrapy to scrape email addresses from a website and save them to a CSV file.

## Installation

1. Clone the repository

2. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Navigate to the project directory:
```
cd mail_scraper/
```

2. Run the spider:
```
scrapy crawl mail_spider -a domain=example.com -o data/emails.csv
```
Replace `example.com` with the domain you want to scrape email addresses from.

3. The spider will scrape the website and save the email addresses to a CSV file named `emails.csv` inside the `data` directory.
