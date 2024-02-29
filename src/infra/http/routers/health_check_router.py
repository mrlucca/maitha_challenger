from typing import Self
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from src.domain.use_cases.health_check import HealthCheckUseCase, OutputHealthCheckDTO
from src.infra.sqlalchemy.repositories.health_check_repository import (
    SqlAlchemyHealthCheckRepository,
)

from src.infra.sqlalchemy.connection import SingletonSqlAlchemyConnection


router = APIRouter(prefix="/api/health")


class SingletonHealthCheckUseCaseFactory:
    _instance = None

    @classmethod
    def factory(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self.db_instance = SingletonSqlAlchemyConnection.get_instance()
        self.repository_instance = SqlAlchemyHealthCheckRepository(self.db_instance)
        self.use_case_instance = HealthCheckUseCase(self.repository_instance)


async def get_health_check_use_case() -> HealthCheckUseCase:
    return SingletonHealthCheckUseCaseFactory.factory().use_case_instance


@router.get(
    "/check",
    tags=["Health Check"],
    summary="Verificar o estado de saúde da aplicação",
    response_model=OutputHealthCheckDTO,
)
async def health_check(
    singleton_use_case: HealthCheckUseCase = Depends(get_health_check_use_case),
) -> ORJSONResponse:
    """
    Verifica o estado de saúde da aplicação.

    Retorna informações sobre o estado atual da aplicação, incluindo status do banco de dados, conexão com serviços externos,
    e outros indicadores importantes.

    ## Respostas:
    - **200 OK**: A aplicação está em um estado saudável.
    - **500 Internal Server Error**: Ocorreu um erro ao verificar o estado da aplicação.

    ## Modelos de Resposta:
    - **OutputHealthCheckDTO**: Contém informações sobre o estado da aplicação.

    ### Notas:
    - Certifique-se de que a aplicação esteja em execução antes de acessar esta rota.

    ### Exemplo:
    ```json
    {
        "available": true,
    }
    ```
    """
    res = await singleton_use_case.execute()
    return ORJSONResponse(
        content=res.model_dump_json(), status_code=200 if res.available else 500
    )
