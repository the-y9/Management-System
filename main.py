from fastapi import FastAPI
from routes.product_routes import router as product_router
from routes.customer_routes import router as customer_router
from routes.sale_routes import router as sale_router
from routes.saleitem_routes import router as saleitem_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# 👇 Add this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product_router)
app.include_router(customer_router)
app.include_router(sale_router)
app.include_router(saleitem_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
