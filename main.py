import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from admin.product import router as product_router

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

router = APIRouter(prefix="/api/v1")
router.include_router(router=product_router, prefix="/products")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True, env_file=".env")
