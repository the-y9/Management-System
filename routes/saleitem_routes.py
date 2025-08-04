from fastapi import APIRouter, HTTPException, status, Request
from dao.saleitem_dao import SaleItemDAO

router = APIRouter(prefix="/saleitem")
sale_item_dao = SaleItemDAO()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_sale_item(request: Request):
    data = await request.json()
    sale_id = data.get("sale_id")
    item = data.get("item")

    if not sale_id or not item:
        raise HTTPException(status_code=400, detail="Missing sale_id or item data")

    success = sale_item_dao.create(sale_id, item)
    if success:
        return {"message": "SaleItem created"}
    raise HTTPException(status_code=500, detail="Failed to create SaleItem")

@router.get("/{sale_item_id}")
async def get_sale_item(sale_item_id: int):
    item = sale_item_dao.get_by_id(sale_item_id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="SaleItem not found")

@router.get("/sale/{sale_id}")
async def get_sale_items_by_sale(sale_id: str):
    items = sale_item_dao.get_all_by_sale(sale_id)
    return items

@router.put("/{sale_item_id}")
async def update_sale_item(sale_item_id: int, request: Request):
    data = await request.json()
    if not data:
        raise HTTPException(status_code=400, detail="Missing data for update")

    success = sale_item_dao.update(sale_item_id, data)
    if success:
        return {"message": "SaleItem updated"}
    raise HTTPException(status_code=404, detail="SaleItem not found or update failed")

@router.delete("/{sale_item_id}")
async def delete_sale_item(sale_item_id: int):
    success = sale_item_dao.delete(sale_item_id)
    if success:
        return {"message": "SaleItem deleted"}
    raise HTTPException(status_code=404, detail="SaleItem not found")
