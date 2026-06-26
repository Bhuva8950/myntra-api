from fastapi import FastAPI

from app.api.product_routers import router as product_router
from app.db.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.product import Category, Product


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Myntra Product API",
    version="1.0.0"
)

app.include_router(product_router)


@app.get("/")
def health_check():
    return {
        "message": "Myntra Product API is running."
    }