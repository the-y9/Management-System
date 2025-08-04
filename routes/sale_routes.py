from fastapi import APIRouter, HTTPException, status, Request
from dao.sale_dao import SaleDAO

router = APIRouter()
sale_dao = SaleDAO()

@router.post("/sale", status_code=status.HTTP_201_CREATED)
async def create_sale(request: Request):
    data = await request.json()
    sale = data.get("sale")
    items = data.get("items", [])
    if not sale or not items:
        raise HTTPException(status_code=400, detail="Missing sale or items")

    success = sale_dao.create(sale, items)
    if success:
        return {"message": "Sale created"}
    raise HTTPException(status_code=500, detail="Failed to create sale")

@router.get("/sale/{sale_id}")
async def get_sale(sale_id: str):
    result = sale_dao.get(sale_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Sale not found")

@router.delete("/sale/{sale_id}")
async def delete_sale(sale_id: str):
    success = sale_dao.delete(sale_id)
    if success:
        return {"message": "Sale deleted"}
    raise HTTPException(status_code=404, detail="Sale not found")

# You can similarly add list and update endpoints using APIRouter syntax
