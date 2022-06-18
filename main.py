from enum import Enum

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from admin.order import router as order_router
from admin.product import router as product_admin_router
from admin.analysis import router as analysis_admin_router

from customer.product import router as product_customer_router
from customer.cart import router as cart_router
from customer.order import router as customer_order_router
from customer.order_items import router as customer_order_items_router
from customer.customer import router as customers_router


from orm.customer import product as orm_product_router
from orm.customer import customer as orm_customer_router
from orm.customer import order as orm_order_router
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
    customer_orm = "[Customer][ORM]"
    admin_orm = "[Admin][ORM]"


router = APIRouter(prefix="/api/v1")
router.include_router(router=product_admin_router, prefix="/products", tags=[Tags.admin])
router.include_router(router=order_router, prefix="/orders", tags=[Tags.admin])

router.include_router(router=product_customer_router, prefix="/customer/products", tags=[Tags.customer])
router.include_router(router=customer_order_router, prefix="/customers/orders", tags=[Tags.customer])
router.include_router(router=cart_router, prefix="/customers/cart", tags=[Tags.customer])
router.include_router(router=customer_order_items_router, prefix="/customers/orders", tags=[Tags.customer])
router.include_router(router=customers_router, prefix="/customers", tags=[Tags.customer])
router.include_router(router=analysis_admin_router, prefix="/admin/analysis", tags=[Tags.admin])

router_orm = APIRouter(prefix="/api/v2")
router_orm.include_router(router=orm_customer_router.router, prefix="/customer",
                          tags=[Tags.customer_orm])
router_orm.include_router(router=orm_product_router.router, prefix="/customer/products",
                          tags=[Tags.customer_orm])
router_orm.include_router(router=orm_order_router.router, prefix="/customer/order",
                          tags=[Tags.customer_orm])
app.include_router(router)
app.include_router(router_orm)
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8001, reload=True, env_file=".env")
