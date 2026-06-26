from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.import_service import ImportService
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/import")
def import_products(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return ImportService.import_products(file, db)



@router.get("/{product_id}")
def get_product(product_id: str, db: Session = Depends(get_db)):

    result = ProductService.get_or_create_product(db, product_id)

    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    return result