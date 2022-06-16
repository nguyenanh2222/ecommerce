from enum import Enum

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from admin.order import router as order_router
from admin.product import router as product_admin_router

from customer.product import router as product_customer_router
from customer.cart import router as cart_router
from customer.order import router as customer_order_router
from customer.order_items import router as customer_order_items_router
from customer.customer import router as customers_router
app = FastAPI(
    title="ecommerce",
    description="ecommerce description",
    debug=True,
    version="0.0.1",
    docs_url="/",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["POST", "GET"],
)


class Tags(str, Enum):
    customer = "[Customer]"
    admin = "[Admin]"


router = APIRouter(prefix="/api/v1")
router.include_router(router=product_admin_router, prefix="/products", tags=[Tags.admin])
router.include_router(router=order_router, prefix="/orders", tags=[Tags.admin])

router.include_router(router=product_customer_router, prefix="/customer/products", tags=[Tags.customer])
router.include_router(router=customer_order_router, prefix="/customers/orders", tags=[Tags.customer])
router.include_router(router=cart_router, prefix="/customers/cart", tags=[Tags.customer])
router.include_router(router=customer_order_items_router, prefix="/customers/orders", tags=[Tags.customer])
router.include_router(router=customers_router, prefix="/customers", tags=[Tags.customer])


app.include_router(router)
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8001, reload=True, env_file=".env")
