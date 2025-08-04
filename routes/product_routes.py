from fastapi import APIRouter, HTTPException, status
from fastapi.requests import Request
from dao.product_dao import ProductDAO

router = APIRouter()
product_dao = ProductDAO()

@router.get("/products")
async def get_all_products():
    return product_dao.list_all()

@router.get("/product/{stock_no}")
async def get_product(stock_no: str):
    product = product_dao.get(stock_no)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/product", status_code=status.HTTP_201_CREATED)
async def create_product(request: Request):
    data = await request.json()
    if product_dao.create(data):
        return {"message": "Product created successfully"}
    raise HTTPException(status_code=400, detail="Failed to create product")

@router.put("/product/{stock_no}")
async def update_product(stock_no: str, request: Request):
    data = await request.json()
    if product_dao.update(stock_no, data):
        return {"message": "Product updated"}
    raise HTTPException(status_code=400, detail="Update failed or product not found")

@router.delete("/product/{stock_no}")
async def delete_product(stock_no: str):
    if product_dao.delete(stock_no):
        return {"message": "Product deleted"}
    raise HTTPException(status_code=400, detail="Delete failed or product not found")
