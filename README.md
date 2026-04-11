# Service Monitor API 🚀

Uma API robusta e assíncrona para monitoramento de disponibilidade e latência de serviços externos, construída com foco em boas práticas de engenharia e observabilidade.

## 🛠️ Stack Técnica
- **Linguagem:** Python 3.11
- **Framework:** FastAPI (Arquitetura Assíncrona)
- **Persistência:** SQLAlchemy + SQLite (v1)
- **Validação:** Pydantic (DTO Pattern)
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI)

## 🏗️ Decisões de Arquitetura
O projeto foi estruturado seguindo princípios de **Clean Architecture** e **Separation of Concerns (SoC)**:
- **DTO Pattern:** Utilização de objetos de transporte de dados (pasta `dtos/`) para desacoplar a camada de API da camada de persistência.
- **Service Layer:** Centralização da lógica de negócio em serviços especializados, facilitando testes e manutenibilidade.
- **Repository Pattern:** Abstração da lógica de banco de dados para garantir que a troca de infraestrutura (ex: SQLite para PostgreSQL) seja transparente para o negócio.
- **Async HTTP:** Uso de `httpx` para realizar checagens de saúde de forma não bloqueante, permitindo alta performance.

## 📋 Endpoints Principais
- `GET /health` - Saúde da própria API.
- `POST /services` - Cadastro de novos serviços para monitoramento.
- `GET /services` - Listagem de serviços monitorados.
- `POST /services/{id}/check` - Execução manual de checagem de disponibilidade.
- `GET /services/{id}/history` - Histórico completo de uptime e tempo de resposta.

## 🐳 Como rodar com Docker
Certifique-se de ter o Docker e Docker Compose instalados e execute:

```bash
docker-compose up --build