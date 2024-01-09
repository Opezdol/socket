from fastapi import APIRouter
from fake import deal as service
from model.deal import Deal

router = APIRouter(prefix="/deals")


@router.get("/")
async def get_all() -> list[Deal]:
    return await service.get_all()


@router.get("/{name}")
async def get_one(name: int) -> Deal | None:
    return await service.get_one(name)


@router.post("/")
async def create(d: Deal) -> Deal:
    return await service.create(d)


@router.patch("/")
async def modify(d: Deal) -> Deal:
    return await service.modify(d)


@router.put("/")
async def replace(d: Deal) -> Deal:
    return await service.replace(d)


@router.delete("/")
async def delete(id) -> bool:
    return await service.delete(id)
