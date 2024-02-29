
---

# Desafio Maitha Tech

## Configuração

Para configurar o programa, siga os passos abaixo:

### 1. Iniciando os Contêineres

Execute o seguinte comando usando Docker Compose para iniciar os contêineres da aplicação e do banco de dados:

```shell
docker-compose up -d db broker
docker-compose up app_dev
``` 

### 2. Objetivo

Meu objetivo era adicionar uma camada de cache além de um serviço de mensageria, porém encontrei alguns problemas no processo. Normalmente, utilizo TDD (Desenvolvimento Orientado por Testes), mas também encontrei alguns problemas para configurar o TestClient.

### 3. Estrutura do Projeto

Aqui está a estrutura do projeto:

```
src/
│
├── domain/
│   ├── contracts/
│   │   ├── repositories/
│   ├── entities/
│   ├── use_cases/
│
├── infra/
│   ├── amqp/
│   │   ├── repositories/
│   ├── http/
│   │   ├── routers/
│   ├── sqlalchemy/
│   │   ├── repositories/
```

### 4. Camadas da Aplicação

- **`domain`**: Contém todas as regras de negócio da aplicação, agnósticas de tecnologia.
- **`infra`**: Contém todas as conexões, repositórios e componentes externos à regra de negócio.

### 5. Acesso às Rotas HTTP

Para acessar as rotas HTTP, visite:

```
src/infra/http/routers
```

### 6. Repositórios Gerenciados por Tecnologia

Os repositórios são gerenciados por tecnologia. Por exemplo, se precisar dos repositórios implementados em RabbitMQ:

```
src/infra/amqp/repositories
```

### 7. Contratos do Domínio

Todos os repositórios seguem contratos diretos do domínio:

```
src/domain/contracts
```

### 8. Documentação da API

Toda a documentação da API está disponível em:

```
localhost:8081/docs
```
ou
```
localhost:8081/redoc
```

### 9. Regras de Negócio

Todas as regras de negócio estão localizadas em:

```
src/domain/use_cases
```

---