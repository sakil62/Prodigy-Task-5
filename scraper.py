import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)

class BookScraper:
    def __init__(self, base_url, delay=1):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()

    def fetch_page(self, url):
        """Fetch HTML content with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return None

    def scrape_products(self, max_products=20):
        """Scrape products from the main catalog"""
        results = []
        url = self.base_url
        scraped = 0

        while url and scraped < max_products:
            html = self.fetch_page(url)
            if not html:
                break

            soup = BeautifulSoup(html, "html.parser")
            containers = soup.select("article.product_pod")

            for product in containers:
                if scraped >= max_products:
                    break

                # Extract basic fields
                name = product.h3.a["title"].strip()
                price = product.select_one(".price_color").text.strip()
                rating = product.p["class"][1] if product.p.has_attr("class") else ""
                product_url = urljoin(self.base_url, product.h3.a["href"])

                # Fetch extra details from product page
                category, image_url, upc = self.scrape_product_page(product_url)

                results.append({
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "category": category,
                    "image_url": image_url,
                    "upc": upc,
                    "url": product_url,
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                })

                scraped += 1
                logging.info(f"Scraped {scraped}: {name}")
                time.sleep(self.delay)

            # Find next page link
            next_page = soup.select_one("li.next a")
            url = urljoin(url, next_page["href"]) if next_page else None

        return results

    def scrape_product_page(self, product_url):
        """Scrape category, image URL, and UPC from product detail page"""
        html = self.fetch_page(product_url)
        if not html:
            return "", "", ""

        soup = BeautifulSoup(html, "html.parser")

        # Category (breadcrumb navigation)
        breadcrumb = soup.select("ul.breadcrumb li a")
        category = breadcrumb[-1].text.strip() if breadcrumb else ""

        # Image URL
        image_tag = soup.select_one("div.item.active img")
        image_url = urljoin(self.base_url, image_tag["src"]) if image_tag else ""

        # UPC (in product info table)
        upc = ""
        table = soup.select_one("table.table.table-striped")
        if table:
            rows = table.find_all("tr")
            for row in rows:
                if row.th.text.strip() == "UPC":
                    upc = row.td.text.strip()
                    break

        return category, image_url, upc


def save_data(data, filename="products", filetype="csv"):
    """Save scraped data to CSV or Excel"""
    df = pd.DataFrame(data)
    if filetype == "csv":
        df.to_csv(f"{filename}.csv", index=False)
        logging.info(f"Data saved to {filename}.csv")
    elif filetype == "excel":
        df.to_excel(f"{filename}.xlsx", index=False)
        logging.info(f"Data saved to {filename}.xlsx")
    else:
        logging.error("Unsupported file type")


if __name__ == "__main__":
    print("E-commerce Web Scraper")
    print("=" * 50)

    base_url = input("Enter the e-commerce website URL: ").strip() or "https://books.toscrape.com/"
    max_products = int(input("Enter max products to scrape (default 20): ") or "20")

    scraper = BookScraper(base_url)
    products = scraper.scrape_products(max_products=max_products)

    if products:
        print(f"\nScraped {len(products)} products:")
        for i, p in enumerate(products, 1):
            print(f"{i}. {p['name']} - {p['price']} - {p['category']}")

        filetype = input("\nSave as (csv/excel): ").strip().lower() or "csv"
        filename = input("Enter filename (without extension): ").strip() or "scraped_products"
        save_data(products, filename, filetype)
    else:
        print("No products scraped.")
