import csv
from io import StringIO
import re

from sqlalchemy.orm import Session

from app.repositories.product_repository import (
    CategoryRepository,
    ProductRepository,
)
from app.services.myntra_service import MyntraService


class ImportService:

    @staticmethod
    def is_valid_product_id(product_id: str) -> bool:
        '''
        Check if the product ID is valid.
        Args:
            product_id: Product ID
        Returns:
            True if the product ID is valid, False otherwise
        '''
        if not product_id:
            return False

        # must be digits only
        if not re.match(r"^\d+$", product_id):
            return False

        # optional: length check (Myntra IDs usually 6–10 digits)
        if not (5 <= len(product_id) <= 12):
            return False

        return True

    @staticmethod
    def import_products(file, db: Session):

        '''
        Import products from a CSV file.
        Args:
            file: CSV file
            db: SQLAlchemy session
        Returns:
            Dictionary containing the import results
        '''
        content = file.file.read().decode("utf-8")
        csv_reader = csv.DictReader(StringIO(content))

        total_products = 0
        imported_products = 0
        failed_products = 0
        errors = []

        for row in csv_reader:

            total_products += 1

            product_id = row.get("product_id")
            if not ImportService.is_valid_product_id(product_id):
                failed_products += 1
                errors.append(f"{product_id}: Invalid product_id format")
                continue

            try:

                # Skip if product already exists
                existing_product = ProductRepository.get_by_product_id(
                    db,
                    product_id
                )

                if existing_product:
                    continue

                # Fetch product details
                product = MyntraService.get_product_details(product_id)

                if not product.get("title"):
                    failed_products += 1
                    errors.append(f"{product_id}: Product not found")
                    continue

                category_name = product["category"]

                if not product.get("category"):
                    failed_products += 1
                    errors.append(f"{product_id}: Category not found")
                    continue
                
                # Check category
                category = CategoryRepository.get_by_name(
                    db,
                    category_name
                )

                # Create category if not exists
                if not category:

                    sponsored_ads = (
                        MyntraService.get_sponsored_products(
                            category_name
                        )
                    )

                    category = CategoryRepository.create(
                        db=db,
                        name=category_name,
                        sponsored_products=sponsored_ads
                    )

                # Store product
                ProductRepository.create(
                    db=db,
                    product_data=product,
                    category_id=category.id
                )

                imported_products += 1

            except Exception as e:

                failed_products += 1

                errors.append(
                    f"{product_id}: {str(e)}"
                )

        return {
            "total_products": total_products,
            "imported_products": imported_products,
            "failed_products": failed_products,
            "errors": errors
        }