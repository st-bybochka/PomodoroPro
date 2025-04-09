from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from schemas import CategorySchema, CategoryUpdateSchema
from repository import CategoryRepository
from dependencies import get_category_repository

router = APIRouter(
    prefix="/category",
    tags=["categories"]
)


@router.get("/", response_model=List[CategorySchema])
async def get_categories(
        repo: CategoryRepository = Depends(get_category_repository)
):
    return await repo.get_all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
        category: CategorySchema,
        repo: CategoryRepository = Depends(get_category_repository)
):
    await repo.add(**category.dict())


@router.patch("/{Category_id}")
async def update_category(
        category_id: int,
        update_data: CategoryUpdateSchema,
        repo: CategoryRepository = Depends(get_category_repository)
):
    if not update_data.dict(exclude_unset=True):
        raise HTTPException(
            status_code=400,
            detail="No data to update")

    Category = await repo.get_by_id(category_id)
    if not Category:
        raise HTTPException(
            status_code=404,
            detail=f"Category withid {category_id} not found")

    await repo.update(category_id, **update_data.dict(exclude_unset=True))
    return {"messsage": f"Category updated successfully, Category_id {category_id}"}


@router.delete("/{Category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        repo: CategoryRepository = Depends(get_category_repository)
):
    category = await repo.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found")

    await repo.delete(category_id)
