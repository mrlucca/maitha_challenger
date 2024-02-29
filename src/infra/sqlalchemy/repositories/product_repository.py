from datetime import datetime
from sqlalchemy import select, delete

from src.domain.contracts.repositories.product_repository import IProductRepository
from src.domain.entities.product import Product
from src.infra.sqlalchemy.models import (
    ProductModel,
    make_product_id_from_base,
)


class SQLAlchemyProductRepository(IProductRepository):
    def __init__(self, sqlalchemy_instance):
        self.sqlalchemy_instance = sqlalchemy_instance

    async def create(self, product: Product) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = ProductModel.from_entity(product)
            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)
            return product_model.to_entity()

    async def exists(self, product: Product) -> bool:
        return await self.exists_from(
            product.code, product.supplier, product.expiration_date
        )

    async def exists_from(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> bool:
        product_model = await self._get_product_by_code_supplier_expiration(
            code, supplier, expiration_date
        )
        if not product_model:
            return False

        return bool(product_model)

    async def update(self, product: Product) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = await self._get_product_by_code_supplier_expiration(
                product.code,
                product.supplier,
                product.expiration_date,
            )
            if not product_model:
                return None

            product_model.title = product.title
            product_model.description = product.description
            product_model.buy_price = product.buy_price
            product_model.sell_price = product.sell_price
            product_model.weight_in_kilograms = product.weight_in_kilograms
            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)
            return product_model.to_entity()

    async def remove(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> str | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_id = make_product_id_from_base(code, supplier, expiration_date)
            statement = delete(ProductModel).where(ProductModel.id == product_id)
            await session.execute(statement)
            await session.commit()
            return product_id

    async def add_inventory_to(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = await self._get_product_by_code_supplier_expiration(
                code, supplier, expiration_date
            )
            if not product_model:
                return None

            product_model.inventory_quantity += 1
            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)

    async def remove_inventory_from(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Product | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_model = await self._get_product_by_code_supplier_expiration(
                code, supplier, expiration_date
            )
            if not product_model and not (product_model.inventory_quantity > 0):
                return None

            product_model.inventory_quantity -= 1
            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)
            return product_model.to_entity()

    async def get_by_code_supplier_expiration(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> Product | None:
        product_model = await self._get_product_by_code_supplier_expiration(
            code, supplier, expiration_date
        )
        return None if not product_model else product_model.to_entity()

    async def _get_product_by_code_supplier_expiration(
        self, code: str, supplier: str, expiration_date: datetime
    ) -> ProductModel | None:
        async with self.sqlalchemy_instance.async_session() as session:
            product_id = make_product_id_from_base(code, supplier, expiration_date)
            statement = select(ProductModel).where(ProductModel.id == product_id)
            product_model = await session.execute(statement)
            return product_model.scalar_one_or_none()
