import json
import re

import requests
from bs4 import BeautifulSoup

from app.config.settings import (
    HEADERS,
    MYNTRA_BASE_URL,
    REQUEST_TIMEOUT,
)


class MyntraService:

    @staticmethod
    def get_product_details(product_id: str):

        url = f"{MYNTRA_BASE_URL}/{product_id}"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        product_script = ""
        breadcrumb = None

        for script in soup.find_all("script", type="application/ld+json"):

            text = script.get_text()

            if '"@type":"Product"' in text or '"@type" : "Product"' in text:
                product_script = text

            elif '"@type":"BreadcrumbList"' in text or '"@type" : "BreadcrumbList"' in text:
                breadcrumb = json.loads(text)

        def extract(pattern):
            match = re.search(pattern, product_script, re.DOTALL)
            return match.group(1) if match else None

        brand = extract(
            r'"brand"\s*:\s*{.*?"name"\s*:\s*"([^"]+)"'
        )

        category = None

        if breadcrumb:

            for item in breadcrumb.get("itemListElement", []):

                name = item["item"]["name"]

                if name == brand:
                    break

                if name.startswith("More by"):
                    continue

                category = name

        image = extract(r'"image"\s*:\s*"([^"]+)"')

        image_urls = []

        if image:
            image_urls.append(image)

        return {
            "product_id": product_id,
            "title": extract(r'"name"\s*:\s*"([^"]+)"'),
            "description": extract(r'"description"\s*:\s*"([^"]+)"'),
            "image_urls": image_urls,
            "brand": brand,
            "price": extract(r'"price"\s*:\s*"([^"]+)"'),
            "currency": extract(r'"priceCurrency"\s*:\s*"([^"]+)"'),
            "rating": extract(r'"ratingValue"\s*:\s*"([^"]+)"'),
            "rating_count": extract(r'"ratingCount"\s*:\s*"([^"]+)"'),
            "category": category,
        }

    @staticmethod
    def get_sponsored_products(category: str):
        url = f"{MYNTRA_BASE_URL}/{category.lower()}"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        ads = []

        pattern = re.compile(
            r'\{"landingPageUrl":.*?"source":"monet".*?\}',
            re.DOTALL
        )

        matches = pattern.findall(response.text)

        for item in matches:

            try:
                product = json.loads(item)

                meta = product.get("productMetaData", {})

                if not meta.get("plaSlot"):
                    continue

                ads.append({
                    "title": product.get("productName"),
                    "price": product.get("price"),
                    "rating": product.get("rating"),
                })

                if len(ads) == 3:
                    break

            except Exception:
                continue

        return ads