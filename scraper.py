# Python Web Scraper Example - books.toscrape.com
# Extracts book title, price, and rating from the first page
# Saves results to a CSV file

import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Target URL (practice site - safe for learning)
base_url = "https://books.toscrape.com/"
url = base_url + "catalogue/page-1.html"  # first page

# Headers to mimic a real browser (helps avoid basic blocks)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Fetching page:", url)

try:
    # Send GET request
    response = requests.get(url, headers=headers, timeout=30)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        exit()

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all book articles
    books = soup.find_all("article", class_="product_pod")

    if not books:
        print("No books found on the page.")
        exit()

    # List to store extracted data
    data = []

    print(f"Found {len(books)} books. Extracting data...")

    for book in books:
        # Extract title
        title_tag = book.h3.a
        title = title_tag["title"].strip() if title_tag else "N/A"

        # Extract price
        price_tag = book.find("p", class_="price_color")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        # Extract rating (star rating class)
        rating_tag = book.find("p", class_="star-rating")
        rating = rating_tag["class"][1] if rating_tag and len(rating_tag["class"]) > 1 else "N/A"

        # Clean up rating (e.g., "Three" → "3/5")
        rating_map = {
            "One": "1/5", "Two": "2/5", "Three": "3/5",
            "Four": "4/5", "Five": "5/5"
        }
        rating = rating_map.get(rating, rating)

        data.append({
            "Title": title,
            "Price": price,
            "Rating": rating
        })

    # Print preview
    print("\nSample extracted books (first 3):")
    for item in data[:3]:
        print(f"• {item['Title']} | {item['Price']} | {item['Rating']}")

    # Save to CSV
    csv_filename = "books_data.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Rating"])
        writer.writeheader()
        writer.writerows(data)

    print(f"\nSuccess! Data saved to '{csv_filename}' ({len(data)} rows)")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")