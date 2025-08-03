# FIAP - TechChallenge - Fase 1

## O problema

**Desafio**: Criação de uma API Pública para Consulta de Livros.

Você foi contratado(a) como Engenheiro(a) de Machine Learning para um
projeto de recomendação de livros. A empresa está em sua fase inicial e ainda
não possui uma base de dados estruturada.
Seu primeiro desafio será montar a infraestrutura de extração,
transformação e disponibilização de dados via API pública para que cientistas de
dados e serviços de recomendação possam usar esses dados com facilidade.
Assim, seu objetivo será desenvolver um pipeline completo de dados e
uma API pública para servir esses dados, pensando na escalabilidade e
reusabilidade futura em modelos de machine learning.

## Requisitos

- Python 3.8+
- pip

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/iiagovictor/fiap_tech_challenge_fase1.git
   cd fiap_tech_challenge_fase1
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Como executar a API

Execute o seguinte comando na raiz do projeto para iniciar a API com recarregamento automático:

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Trigger do Scraping

Para iniciar manualmente o processo de scraping dos livros, utilize a rota protegida (requer autenticação):

```
POST /api/v1/scraping/trigger
```

Esta rota dispara o processo de extração dos dados dos livros e salva os arquivos atualizados em `app/data/books.csv` e `app/data/books.json`. O status do scraping pode ser consultado pela rota:

```
GET /api/v1/scraping/status/{scraping_id}
```

---

## Qualidade de Código

Este projeto segue o padrão PEP8 e utiliza o [Flake8](https://flake8.pycqa.org/) para análise de qualidade e lint do código Python.

A esteira de CI/CD irá validar automaticamente a qualidade do código a cada push, garantindo que o padrão seja seguido.

Para rodar o Flake8 localmente:

```bash
flake8 . --exclude=.venv,alembic
```

## Componentes

[Sistema de Web Scraping](app/utils/README.md)
