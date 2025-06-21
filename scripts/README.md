# Web Scraping

## Descrição

Este projeto realiza web scraping do site [Books to Scrape](http://books.toscrape.com), coletando informações detalhadas sobre livros e salvando os dados em arquivos CSV e JSON. O código utiliza Python, BeautifulSoup, requests, pandas e multithreading para acelerar a coleta dos dados.

Para rodar o web scraping e salvar os dados:

```bash
python scripts/main.py
```

Os arquivos `books.csv` e `books.json` serão salvos na pasta `data/`.

## Estrutura dos dados

Cada livro extraído contém os seguintes campos:

- `book_id`
- `title`
- `description`
- `review_rating`
- `category`
- `product_upc`
- `currency`
- `price_including_tax`
- `price_excluding_tax`
- `tax`
- `number_available`
- `created_at`
- `image_url`
- `url`

## Observações

- O script utiliza multithreading para acelerar a coleta dos detalhes dos livros.
- Caso algum livro não possua descrição, o campo será `null` no JSON/CSV.
- O scraping respeita a estrutura pública do site Books to Scrape.