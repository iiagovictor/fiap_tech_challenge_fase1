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
## Qualidade de Código

Este projeto segue o padrão PEP8 e utiliza o [Flake8](https://flake8.pycqa.org/) para análise de qualidade e lint do código Python.

Para rodar o Flake8 localmente:

```bash
flake8 . --exclude=.venv
```

## Componentes

[Sistema de Web Scraping](scripts/README.md)
[API](api/readme.md)
