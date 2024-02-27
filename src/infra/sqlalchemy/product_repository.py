from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product
from src.infra.sqlalchemy.models import ProductModel, make_product_id_from


class SQLAlchemyProductRepository(IProductRepository):
    def __init__(self, sqlalchemy_instance):
        self.sqlalchemy_instance = sqlalchemy_instance

    async def create(self, product: Product) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = ProductModel.from_entity(product)
            try:
                async with session.begin():
                    session.add(product_model)
                    await session.flush()
                    await session.refresh(product_model)
            except SQLAlchemyError as e:
                await session.rollback()
            finally:
                await session.close()
            await session.commit()
            return product_model.to_entity()

    async def exists(self, product: Product) -> bool:
        id = make_product_id_from(product)
        async with self.sqlalchemy_instance.async_session() as session:

            statement = select(ProductModel).where(ProductModel.id == id)
            result = await session.execute(statement)
            if not result:
                return False

            return bool(result)

    async def update(self, product: Product) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = await self._get_product_by_code_supplier_expiration(
                product.code,
                product.supplier,
                product.expiration_date.replace(tzinfo=timezone.utc),
            )
            if product_model:
                product_model.title = product.title
                product_model.description = product.description
                product_model.buy_price = product.buy_price
                product_model.sell_price = product.sell_price
                product_model.weight_in_kilograms = product.weight_in_kilograms
                await session.commit()
                return product_model.to_entity()
            return None

    async def add_inventory_to(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = await self._get_product_by_code_supplier_expiration(
                code, supplier, expiration_date.replace(tzinfo=timezone.utc)
            )
            if product_model:
                product_model.inventory_quantity += 1
                await session.commit()
                return product_model.to_entity()
            return None

    async def remove_inventory_from(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = await self._get_product_by_code_supplier_expiration(
                code, supplier, expiration_date.replace(tzinfo=timezone.utc)
            )
            if product_model and product_model.inventory_quantity > 0:
                product_model.inventory_quantity -= 1
                await session.commit()
                return product_model.to_entity()
            return None

    async def get_by_code_supplier_expiration(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Optional[Product]:
        product_model = await self._get_product_by_code_supplier_expiration(
            code, supplier, expiration_date.replace(tzinfo=timezone.utc)
        )
        if product_model:
            return product_model.to_entity()
        return None

    async def _get_product_by_code_supplier_expiration(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Optional[ProductModel]:
        async with self.sqlalchemy_instance.async_session() as session:
            query = await session.execute(
                select(ProductModel)
                .filter_by(
                    code=code, supplier=supplier, expiration_date=expiration_date
                )
                .first()
            )
            return query.scalar()
