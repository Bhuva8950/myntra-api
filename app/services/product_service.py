from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.repositories.product_repository import CategoryRepository
from app.services.myntra_service import MyntraService


class ProductService:

    @staticmethod
    def get_or_create_product(db: Session, product_id: str):

        # 1. CHECK DB FIRST
        product = ProductRepository.get_by_product_id(db, product_id)

        if product:
            category = product.category

            return {
                "source": "db",
                "product_id": product.product_id,
                "title": product.title,
                "description": product.description,
                "image_urls": product.image_urls,
                "rating": product.rating,
                "rating_count": product.rating_count,
                "brand": product.brand,
                "price": product.price,
                "currency": product.currency,
                "category": {
                    "id": category.id,
                    "name": category.name,
                    "sponsored_products": (
                        category.sponsored_products[:3]
                        if category.sponsored_products else []
                    )
                }
            }

        # 2. FETCH FROM EXTERNAL API
        product_data = MyntraService.get_product_details(product_id)

        category_name = product_data["category"]
        print("category_name", category_name)

        # 3. GET OR CREATE CATEGORY
        category = CategoryRepository.get_by_name(db, category_name)

        if not category:

            sponsored_ads = MyntraService.get_sponsored_products(category_name)

            category = CategoryRepository.create(
                db=db,
                name=category_name,
                sponsored_products=sponsored_ads
            )

        # 4. STORE PRODUCT IN DB
        product = ProductRepository.create(
            db=db,
            product_data=product_data,
            category_id=category.id
        )

        # 5. RETURN RESPONSE
        return {
            "source": "api",
            "product_id": product.product_id,
            "title": product.title,
            "description": product.description,
            "image_urls": product.image_urls,
            "rating": product.rating,
            "rating_count": product.rating_count,
            "brand": product.brand,
            "price": product.price,
            "currency": product.currency,
            "category": {
                "id": category.id,
                "name": category.name,
                "sponsored_products": (
                    category.sponsored_products[:3]
                    if category.sponsored_products else []
                )
            }
        }