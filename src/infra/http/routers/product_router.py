from datetime import datetime
from typing import Self
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from src.domain.use_cases.product_create import (
    InputProductCreateDTO,
    ProductCreateUseCase,
    OutputProductCreateDTO,
)
from src.domain.use_cases.product_delete import (
    InputProductDeleteDTO,
    OutputProductDeleteDTO,
    ProductDeleteUseCase,
)
from src.domain.use_cases.product_get import (
    InputProductGetDTO,
    OutputProductGetDTO,
    ProductGetUseCase,
)
from src.domain.use_cases.product_send_inventory import (
    ProductSendInventoryUseCase,
    OutputProductSendInventoryDTO,
    InputProductSendInventoryDTO,
)
from src.domain.use_cases.product_update import (
    InputProductUpdateDTO,
    OutputProductUpdateDTO,
    ProductUpdateUseCase,
)
from src.infra.amqp.connection import SingletonAMQPConnection
from src.infra.amqp.repositories.inventory_repository import AmqpInventoryRepository
from src.infra.sqlalchemy.connection import SingletonSqlAlchemyConnection
from src.infra.sqlalchemy.repositories.product_repository import (
    SQLAlchemyProductRepository,
)


router = APIRouter(prefix="/api/product")


class BaseSingletonUseCase:
    _instance = None

    @classmethod
    def factory_instance(cls) -> Self:
        if cls._instance is None:
            connection_instance = SingletonSqlAlchemyConnection.get_instance()
            repo = SQLAlchemyProductRepository(connection_instance)
            cls._instance = cls(repo)

        return cls._instance


class InventorySingletonUseCase:
    _instance = None
    TOPIC_NAME = "inventory"

    def __init__(self, repo, broker_repo):
        self.repo = repo
        self.broker_repo = broker_repo
        self.use_case = ProductSendInventoryUseCase(self.broker_repo, self.repo)

    @classmethod
    async def factory_instance(cls) -> Self:
        if cls._instance is None:
            connection_instance = SingletonSqlAlchemyConnection.get_instance()
            repo = SQLAlchemyProductRepository(connection_instance)
            con = await SingletonAMQPConnection.get_instance()
            broker_repository = AmqpInventoryRepository(con, cls.TOPIC_NAME)
            cls._instance = cls(repo, broker_repository)

        return cls._instance


class AdaptCreateUseCase(ProductCreateUseCase, BaseSingletonUseCase): ...


class AdaptGetUseCase(ProductGetUseCase, BaseSingletonUseCase): ...


class AdaptUpdateUseCase(ProductUpdateUseCase, BaseSingletonUseCase): ...


class AdaptDeleteUseCase(ProductDeleteUseCase, BaseSingletonUseCase): ...


def factory_singleton_product_create_use_case() -> ProductCreateUseCase:
    return AdaptCreateUseCase.factory_instance()


def factory_singleton_product_get_use_case() -> ProductGetUseCase:
    return AdaptGetUseCase.factory_instance()


def factory_singleton_product_update_use_case() -> ProductUpdateUseCase:
    return AdaptUpdateUseCase.factory_instance()


def factory_singleton_product_delete_use_case() -> ProductDeleteUseCase:
    return AdaptDeleteUseCase.factory_instance()


async def factory_singleton_inventory_use_case() -> ProductSendInventoryUseCase:
    singleton_instance = await InventorySingletonUseCase.factory_instance()
    return singleton_instance.use_case


def return_200_if_success(res):
    return 200 if res.success else 400


@router.post("/", response_model=OutputProductCreateDTO)
async def create_product(
    input_dto: InputProductCreateDTO,
    use_case: ProductCreateUseCase = Depends(factory_singleton_product_create_use_case),
) -> ORJSONResponse:
    res = await use_case.execute(input_dto)
    return ORJSONResponse(
        content=res.model_dump_json(), status_code=return_200_if_success(res)
    )


@router.get("/", response_model=OutputProductGetDTO)
async def get_product(
    code: str,
    supplier: str,
    expiration_date: datetime,
    use_case: ProductGetUseCase = Depends(factory_singleton_product_get_use_case),
) -> ORJSONResponse:
    input_dto = InputProductGetDTO(
        code=code, supplier=supplier, expiration_date=expiration_date
    )
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))


@router.put("/", response_model=OutputProductUpdateDTO)
async def update_product(
    input_dto: InputProductUpdateDTO,
    use_case: ProductUpdateUseCase = Depends(factory_singleton_product_update_use_case),
) -> ORJSONResponse:
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))


@router.delete("/", response_model=OutputProductDeleteDTO)
async def delete_product(
    input_dto: InputProductDeleteDTO,
    use_case: ProductDeleteUseCase = Depends(factory_singleton_product_delete_use_case),
) -> ORJSONResponse:
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))


@router.post("/send/inventory", response_model=OutputProductSendInventoryDTO)
async def delete_product(
    input_dto: InputProductSendInventoryDTO,
    use_case: ProductSendInventoryUseCase = Depends(
        factory_singleton_inventory_use_case
    ),
) -> ORJSONResponse:
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))
