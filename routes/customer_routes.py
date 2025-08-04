from fastapi import APIRouter, HTTPException, status
from fastapi.requests import Request
from dao.customer_dao import CustomerDAO

router = APIRouter()
customer_dao = CustomerDAO()

@router.get("/customers")
async def list_customers():
    return customer_dao.list_all()

@router.get("/customer/{customer_id}")
async def get_customer(customer_id: str):
    customer = customer_dao.get(customer_id)
    if customer:
        return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@router.post("/customer", status_code=status.HTTP_201_CREATED)
async def create_customer(request: Request):
    data = await request.json()
    if customer_dao.create(data):
        return {"message": "Customer created"}
    raise HTTPException(status_code=400, detail="Failed to create customer")

@router.put("/customer/{customer_id}")
async def update_customer(customer_id: str, request: Request):
    data = await request.json()
    if customer_dao.update(customer_id, data):
        return {"message": "Customer updated"}
    raise HTTPException(status_code=400, detail="Update failed or customer not found")

@router.delete("/customer/{customer_id}")
async def delete_customer(customer_id: str):
    if customer_dao.delete(customer_id):
        return {"message": "Customer deleted"}
    raise HTTPException(status_code=400, detail="Delete failed or customer not found")
