# 🛒 E-commerce Web Scraper (Task 5)

This project is part of **Prodigy ML Internship**.  
It is a Python-based **web scraper** that extracts product details (tested on [BooksToScrape](https://books.toscrape.com)).

## 🚀 Features
- Scrapes:
  - Product Name
  - Price
  - Rating
  - Category
  - Image URL
  - UPC
  - Product URL
- Saves data to **CSV/Excel**
- Built with `requests`, `BeautifulSoup`, `pandas`

## 📂 Files
- `scraper.py` → Main scraper script  
- `scraped_products.csv` → Sample output  

## 🖥️ Usage
```bash
python scraper.py
Enter website URL (default: https://books.toscrape.com) and max products to scrape.

📦 Requirements
bash
Copy
Edit
pip install requests beautifulsoup4 pandas
📜 Example Output
Name	Price	Category	Rating	UPC
A Light in the Attic	£51.77	Poetry	Three	a897fe39b10563

