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


router = APIRouter(prefix="/api/product", tags=["Product"])


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


@router.post(
    "/",
    response_model=OutputProductCreateDTO,
    summary="Criar um novo produto"
)
async def create_product(
    input_dto: InputProductCreateDTO,
    use_case: ProductCreateUseCase = Depends(factory_singleton_product_create_use_case),
) -> ORJSONResponse:
    """
    Cria um novo produto com base nos dados fornecidos.

    ## Parâmetros:
    - **input_dto**: Dados de entrada para criar o produto.

    ## Respostas:
    - **200 OK**: Produto criado com sucesso. Retorna um objeto `OutputProductCreateDTO` com detalhes do produto criado.
    - **404 Not Found**: Produto já existente com o mesmo código.

    ## Modelo de Dados de Entrada:
    - **InputProductCreateDTO**: Contém os dados necessários para criar um novo produto.

    ## Modelo de Dados de Saída:
    - **OutputProductCreateDTO**: Contém detalhes sobre o resultado da criação do produto.

    ### Exemplo de Dados de Entrada:
    ```json
    {
        "title": "Produto Exemplo",
        "description": "Descrição do produto",
        "code": "123456",
        "supplier": "Fornecedor A",
        "inventory_quantity": 100,
        "buy_price": 10.5,
        "sell_price": 15.0,
        "weight_in_kilograms": 2.5,
        "expiration_date": "2024-12-31T23:59:59"
    }
    ```

    ### Exemplo de Dados de Saída (Sucesso):
    ```json
    {
        "success": true,
        "product": {
            "title": "Produto Exemplo",
            "description": "Descrição do produto",
            "code": "123456",
            "supplier": "Fornecedor A",
            "inventory_quantity": 100,
            "buy_price": 10.5,
            "sell_price": 15.0,
            "weight_in_kilograms": 2.5,
            "expiration_date": "2024-12-31T23:59:59"
        },
        "msg": null
    }
    ```

    ### Exemplo de Dados de Saída (Erro):
    ```json
    {
        "success": false,
        "product": null,
        "msg": "product already exists"
    }
    ```
    """
    res = await use_case.execute(input_dto)
    return ORJSONResponse(
        content=res.model_dump_json(), status_code=return_200_if_success(res)
    )


@router.get(
    "/",
    response_model=OutputProductGetDTO,
    summary="Obter informações sobre um produto",
)
async def get_product(
    code: str,
    supplier: str,
    expiration_date: datetime,
    use_case: ProductGetUseCase = Depends(factory_singleton_product_get_use_case),
) -> ORJSONResponse:
    """
    Obtém informações sobre um produto com base no código, fornecedor e data de validade fornecidos.

    ## Parâmetros:
    - **code**: Código do produto.
    - **supplier**: Fornecedor do produto.
    - **expiration_date**: Data de validade do produto.

    ## Respostas:
    - **200 OK**: Produto encontrado com sucesso. Retorna um objeto `OutputProductGetDTO` com detalhes do produto.
    - **404 Not Found**: Produto não encontrado com os critérios fornecidos.
    - **500 Internal Server Error**: Ocorreu um erro interno ao tentar obter informações do produto.

    ## Modelo de Dados de Entrada:
    - **InputProductGetDTO**: Contém os parâmetros necessários para obter informações sobre um produto.

    ## Modelo de Dados de Saída:
    - **OutputProductGetDTO**: Contém detalhes sobre o resultado da busca do produto.

    ### Exemplo de Dados de Entrada:
    - **code**: "123456"
    - **supplier**: "Fornecedor A"
    - **expiration_date**: "2024-12-31"

    ### Exemplo de Dados de Saída (Sucesso):
    ```json
    {
        "success": true,
        "product": {
            "title": "Produto Exemplo",
            "description": "Descrição do produto",
            "code": "123456",
            "supplier": "Fornecedor A",
            "inventory_quantity": 100,
            "buy_price": 10.5,
            "sell_price": 15.0,
            "weight_in_kilograms": 2.5,
            "expiration_date": "2024-12-31T23:59:59"
        },
        "msg": null
    }
    ```

    ### Exemplo de Dados de Saída (Erro):
    ```json
    {
        "success": false,
        "product": null,
        "msg": "product does not exists"
    }
    ```
    """
    input_dto = InputProductGetDTO(
        code=code, supplier=supplier, expiration_date=expiration_date
    )
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))


@router.put(
    "/",
    response_model=OutputProductUpdateDTO,
    summary="Atualizar informações de um produto",
)
async def update_product(
    input_dto: InputProductUpdateDTO,
    use_case: ProductUpdateUseCase = Depends(factory_singleton_product_update_use_case),
) -> ORJSONResponse:
    """
    Atualiza informações de um produto com base nos dados fornecidos no corpo da requisição.

    ## Corpo da Requisição (JSON):
    - **code**: Código do produto a ser atualizado.
    - **supplier**: Fornecedor do produto.
    - **expiration_date**: Data de validade do produto.
    - **update**: Objeto contendo as informações atualizadas do produto. Este objeto pode conter os seguintes campos opcionais:
        - **title**: Título do produto.
        - **description**: Descrição do produto.
        - **buy_price**: Preço de compra do produto.
        - **sell_price**: Preço de venda do produto.
        - **weight_in_kilograms**: Peso em quilogramas do produto.

    ## Respostas:
    - **200 OK**: Informações do produto atualizadas com sucesso. Retorna um objeto `OutputProductUpdateDTO` com detalhes do produto atualizado.
    - **404 Not Found**: Produto não encontrado com os critérios fornecidos.
    - **400 Bad Request**: Solicitação inválida. Retorna uma mensagem informando que a solicitação não contém informações para atualização ou nenhum campo válido para atualização foi fornecido.
    - **500 Internal Server Error**: Ocorreu um erro interno ao tentar atualizar as informações do produto.

    ## Modelo de Dados de Entrada:
    - **InputProductUpdateDTO**: Contém os parâmetros necessários para atualizar informações sobre um produto.

    ## Modelo de Dados de Saída:
    - **OutputProductUpdateDTO**: Contém detalhes sobre o resultado da atualização do produto.

    ### Exemplo de Corpo da Requisição:
    ```json
    {
        "code": "123456",
        "supplier": "Fornecedor A",
        "expiration_date": "2024-12-31T23:59:59",
        "update": {
            "title": "Novo Título",
            "buy_price": 15.99,
            "sell_price": 25.99
        }
    }
    ```

    ### Exemplo de Resposta (Sucesso):
    ```json
    {
        "success": true,
        "product": {
            "title": "Novo Título",
            "description": "Descrição atualizada",
            "code": "123456",
            "supplier": "Fornecedor A",
            "inventory_quantity": 100,
            "buy_price": 15.99,
            "sell_price": 25.99,
            "weight_in_kilograms": 2.5,
            "expiration_date": "2024-12-31T23:59:59"
        },
        "msg": null
    }
    ```

    ### Exemplo de Resposta (Erro - Produto Não Encontrado):
    ```json
    {
        "success": false,
        "product": null,
        "msg": "Product not found"
    }
    ```
    """
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))


@router.delete(
    "/",
    response_model=OutputProductDeleteDTO,
    summary="Remover um produto"
)
async def delete_product(
    input_dto: InputProductDeleteDTO,
    use_case: ProductDeleteUseCase = Depends(factory_singleton_product_delete_use_case),
) -> ORJSONResponse:
    """
    Remove um produto com base nos dados fornecidos no corpo da requisição.

    ## Corpo da Requisição (JSON):
    - **code**: Código do produto a ser removido.
    - **supplier**: Fornecedor do produto.
    - **expiration_date**: Data de validade do produto.

    ## Respostas:
    - **200 OK**: Produto removido com sucesso. Retorna um objeto `OutputProductDeleteDTO` com o ID do produto removido.
    - **404 Not Found**: Produto não encontrado com os critérios fornecidos.
    - **400 Bad Request**: Solicitação inválida. Retorna uma mensagem informando que o produto não existe.
    - **500 Internal Server Error**: Ocorreu um erro interno ao tentar remover o produto.

    ## Modelo de Dados de Entrada:
    - **InputProductDeleteDTO**: Contém os parâmetros necessários para remover um produto.

    ## Modelo de Dados de Saída:
    - **OutputProductDeleteDTO**: Contém detalhes sobre o resultado da remoção do produto.

    ### Exemplo de Corpo da Requisição:
    ```json
    {
        "code": "123456",
        "supplier": "Fornecedor A",
        "expiration_date": "2024-12-31T23:59:59"
    }
    ```

    ### Exemplo de Resposta (Sucesso):
    ```json
    {
        "success": true,
        "product_id": "123456",
        "msg": null
    }
    ```

    ### Exemplo de Resposta (Erro - Produto Não Encontrado):
    ```json
    {
        "success": false,
        "product_id": null,
        "msg": "Product not exists"
    }
    ```

    ### Exemplo de Resposta (Erro - Produto Não Removido):
    ```json
    {
        "success": false,
        "product_id": null,
        "msg": "product not deleted"
    }
    ```

    """
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))


@router.post(
    "/send/inventory",
    response_model=OutputProductSendInventoryDTO,
    summary="Enviar informações de inventário para processamento",
)
async def delete_product(
    input_dto: InputProductSendInventoryDTO,
    use_case: ProductSendInventoryUseCase = Depends(
        factory_singleton_inventory_use_case
    ),
) -> ORJSONResponse:
    """
    Envie informações de inventário para processamento em uma fila de mensagens.
    ### Obs:
    #### Este serviço foi desenvolvido para simular um processamento mais extenso, por isso não está tão útil,
    #### já que não há muita informação para processar no momento, mas serviu para integrar o RabbitMQ.

    ## Corpo da Requisição (JSON):
    - **code**: Código do produto.
    - **supplier**: Fornecedor do produto.
    - **expiration_date**: Data de validade do produto.
    - **action**: Ação a ser executada no inventário (pode ser 'add' ou 'remove').

    ## Respostas:
    - **200 OK**: Informações de inventário enviadas com sucesso para processamento.
    - **404 Not Found**: Produto não encontrado com os critérios fornecidos.
    - **400 Bad Request**: Solicitação inválida. Retorna uma mensagem informando que o produto não existe.
    - **500 Internal Server Error**: Ocorreu um erro interno ao tentar enviar as informações de inventário para processamento.

    ## Modelo de Dados de Entrada:
    - **InputProductSendInventoryDTO**: Contém os parâmetros necessários para enviar informações de inventário.

    ## Modelo de Dados de Saída:
    - **OutputProductSendInventoryDTO**: Contém detalhes sobre o resultado do envio das informações de inventário.

    ### Exemplo de Corpo da Requisição:
    ```json
    {
        "code": "123456",
        "supplier": "Fornecedor A",
        "expiration_date": "2024-12-31T23:59:59",
        "action": "add"
    }
    ```

    ### Exemplo de Resposta (Sucesso):
    ```json
    {
        "success": true,
        "message": "sent event"
    }
    ```

    ### Exemplo de Resposta (Erro - Produto Não Encontrado):
    ```json
    {
        "success": false,
        "message": "product not exists"
    }
    ```

    """
    res = await use_case.execute(input_dto)
    return ORJSONResponse(content=res.json(), status_code=return_200_if_success(res))
