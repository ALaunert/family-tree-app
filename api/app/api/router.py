from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.people import router as people_router
from app.api.routes.relationships import router as relationships_router
from app.api.routes.tree import router as tree_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(health_router)
api_router.include_router(people_router)
api_router.include_router(relationships_router)
api_router.include_router(tree_router)
