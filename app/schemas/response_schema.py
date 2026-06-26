from typing import List, Optional

from pydantic import BaseModel


class SponsoredProductResponse(BaseModel):
    title: str
    price: Optional[float] = None
    rating: Optional[float] = None


class ProductResponse(BaseModel):
    product_id: str

    title: Optional[str] = None
    description: Optional[str] = None

    image_urls: List[str] = []

    rating: Optional[float] = None
    rating_count: Optional[int] = None

    brand: Optional[str] = None

    price: Optional[float] = None
    currency: Optional[str] = None

    category: Optional[str] = None

    sponsored_ads: List[SponsoredProductResponse] = []


class ImportResponse(BaseModel):
    total_products: int
    imported_products: int
    failed_products: int

    errors: List[str] = []