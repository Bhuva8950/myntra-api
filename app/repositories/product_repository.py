from sqlalchemy.orm import Session

from app.models.product import Category, Product


class CategoryRepository:

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Category).filter(Category.name == name).first()

    @staticmethod
    def create(
        db: Session,
        name: str,
        sponsored_products: list   
    ):
        category = Category(
            name=name,
            sponsored_products=sponsored_products
        )

        db.add(category)
        db.commit()
        db.refresh(category)

        return category


class ProductRepository:

    @staticmethod
    def get_by_product_id(
        db: Session,
        product_id: str
    ):
        return (
            db.query(Product)
            .filter(Product.product_id == product_id)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        product_data: dict,
        category_id: int
    ):
        product = Product(
            product_id=product_data["product_id"],
            title=product_data.get("title"),
            description=product_data.get("description"),
            image_urls=product_data.get("image_urls"),
            rating=product_data.get("rating"),
            rating_count=product_data.get("rating_count"),
            brand=product_data.get("brand"),
            price=product_data.get("price"),
            currency=product_data.get("currency"),
            category_id=category_id
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product