import requests
from bs4 import BeautifulSoup
import logging
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os


class BooksToScrape():

    """Classe para realizar web scraping de livros do site "Books to Scrape".

    Esta classe contém métodos para obter o conteúdo HTML de uma URL,
    analisar datas, converter palavras em inteiros, buscar detalhes de livros
    e salvar os dados em arquivos CSV e JSON.

    Attributes:
    -----------
        base_url (str): A URL base do site "Books to Scrape".

    Methods:
    --------
        _get_soup(
            url: str
        ) -> BeautifulSoup:
            Obtém o conteúdo HTML de uma URL e retorna um objeto BeautifulSoup.
        _parse_date(
            date_str: str
        ) -> datetime:
            Converte uma string de data no formato "dd MMM yyyy HH:mm" para um
            objeto datetime.
        _word_to_int(
            word: str
        ) -> int:
            Converte uma palavra representando um número em seu valor inteiro
            correspondente.
        _fetch_book_details(
            suffix_url: str
        ) -> dict:
            Obtém os detalhes de um livro a partir de uma URL específica.
        get_books() -> list:
            Obtém uma lista de livros do site "Books to Scrape".
        save_books_to_csv(
            books: list,
            filename: str = "data/books.csv"
        ) -> None:
            Salva a lista de livros em um arquivo CSV.
        save_books_to_json(
            books: list,
            filename: str = "data/books.json"
        ) -> None:
            Salva a lista de livros em um arquivo JSON.

    Usage:
    -------
        books_scraper = BooksToScrape()
        books = books_scraper.get_books()
        books_scraper.save_books_to_csv(books)
        books_scraper.save_books_to_json(books)
    """

    def __init__(self):
        self.base_url = "http://books.toscrape.com"

    def _get_soup(
            self,
            url: str
            ) -> BeautifulSoup:
        """Obtém o conteúdo HTML de uma URL e retorna um objeto BeautifulSoup.
        Esta função faz uma requisição HTTP GET para a URL fornecida, define
        a codificação como UTF-8, e utiliza BeautifulSoup para analisar o
        conteúdo HTML retornado. Se a requisição falhar, uma exceção
        será levantada.

        Args:
        -------
            url (str): A URL da página a ser obtida.
        Returns:
        -------
            BeautifulSoup: Um objeto BeautifulSoup contendo o conteúdo
            HTML da página.
        """
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def _parse_date(
            self,
            date_str: str
            ) -> datetime:
        """Converte uma string de data no formato "dd MMM yyyy HH:mm"
        para um objeto datetime. Esta função remove sufixos como "st", "nd",
        "rd" e "th" dos dias antes de fazer a conversão.

        Args:
        -------
            date_str (str): A string de data a ser convertida.
        Returns:
        -------
            datetime: Um objeto datetime representando a data e hora.
        """
        date_str = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date_str)
        return datetime.strptime(date_str, "%d %b %Y %H:%M")

    def _word_to_int(
            self,
            word: str
            ) -> int:
        """Converte uma palavra representando um número em seu valor
        inteiro correspondente.

        Args:
        -------
            word (str): A palavra a ser convertida, como "One", "Two", etc.
        Returns:
        -------
            int: O valor inteiro correspondente à palavra, ou None se
            a palavra não for reconhecida.
        """
        mapping = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        return mapping.get(word, None)

    def _fetch_book_details(
            self,
            suffix_url: str
            ) -> dict:
        """Obtém os detalhes de um livro a partir de uma URL específica.
        Esta função faz uma requisição HTTP GET para a URL do livro, analisa
        o conteúdo HTML e extrai informações como título, descrição, categoria,
        avaliação, preço, disponibilidade, data de criação e URL da imagem.
        Retorna um dicionário com essas informações.

        Args:
        -------
            suffix_url (str): O sufixo da URL do livro, geralmente no
            formato "index.html".

        Returns:
        -------
            dict: Um dicionário contendo os detalhes do livro, incluindo ID,
            título, descrição, categoria, avaliação, preço, disponibilidade,
            data de criação e URL da imagem.
        """
        try:
            book_url = f"{self.base_url}/catalogue/{suffix_url}"
            book_details = self._get_soup(
                url=book_url
                )
            book_id = int(suffix_url.replace("/index.html", "").split("_")[-1])
            title = (
                book_details.find("div", class_="product_main")
                .find("h1")
                .get_text(strip=True)
            )
            created_at = self._parse_date(
                date_str=book_details.find("head")
                .find("meta", attrs={"name": "created"})
                .get("content")
            )
            desc_div = book_details.find("div", id="product_description")
            if desc_div:
                description = (
                    desc_div.find_next_sibling("p")
                    .get_text(strip=True)
                    .replace(" ...more", "")
                )
            else:
                description = None
            category = (
                book_details.find("ul", class_="breadcrumb")
                .find_all("li")[2]
                .get_text(strip=True)
            )
            review_rating = self._word_to_int(
                word=book_details.find("div", class_="product_main")
                .find("p", class_="star-rating")["class"][1]
            )
            suffix_image_url = (
                book_details.find("div", class_="item active")
                .find("img")["src"]
                .replace("../../", "")
            )
            image_url = f"{self.base_url}/{suffix_image_url}"
            table = book_details.find("table", class_="table table-striped")
            details = {}
            for row in table.find_all("tr"):
                key = row.find("th").get_text(strip=True)
                value = row.find("td").get_text(strip=True)
                details[key] = value
            book_info = {
                "book_id": book_id,
                "title": title,
                "description": description,
                "review_rating": review_rating,
                "category": category,
                "product_upc": details["UPC"],
                "currency": 'GBP'
                if details["Price (incl. tax)"][:1] == '£'
                else 'UNKNOWN',
                "price_including_tax": float(details["Price (incl. tax)"][1:]),
                "price_excluding_tax": float(details["Price (excl. tax)"][1:]),
                "tax": float(details["Tax"][1:]),
                "number_available": int(details['Availability'].split('(')[1]
                                        .split(' ')[0]),
                "created_at": created_at,
                "image_url": image_url,
                "url": book_url
            }
            return book_info
        except Exception as e:
            logging.error(f"Error fetching book details from {book_url}: {e}")

    def get_books(self) -> list:
        """Obtém uma lista de livros do site "Books to Scrape".
        Esta função navega pelas páginas do site, coleta URLs de livros e
        utiliza múltiplas threads para buscar detalhes de cada livro. Retorna
        uma lista de dicionários contendo informações sobre cada livro, como
        título, descrição, categoria, avaliação, preço, disponibilidade, data
        de criação e URL da imagem.

        Returns:
        -------
            list: Uma lista de dicionários, cada um representando um livro
            com seus detalhes.
        """
        result = []
        url = None

        while True:
            if not url:
                url = f"{self.base_url}/catalogue/page-1.html"
            logging.info(f"Fetching books from {url}")
            soup = self._get_soup(
                url=url
                )
            books = soup.select("article.product_pod")
            suffix_urls = [
                book.find("div", class_="image_container").find("a")
                    .get("href")
                for book in books
            ]
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [
                    executor.submit(
                        self._fetch_book_details,
                        suffix_url=suffix_url
                        )
                    for suffix_url in suffix_urls
                    ]
                for future in futures:
                    result.append(future.result())
            next_link = soup.select_one("li.next > a")
            if next_link:
                next_page = next_link.get('href')
                url = f"{self.base_url}/catalogue/{next_page}"
            else:
                break
        return result

    def save_books_to_csv(
            self,
            books: list,
            filename: str = "data/books.csv"
            ) -> None:
        """Salva a lista de livros em um arquivo CSV.
        Esta função utiliza a biblioteca pandas para criar um DataFrame a
        partir da lista de livros e salva o DataFrame em um arquivo CSV.

        Args:
        -------
            books (list): A lista de dicionários contendo detalhes dos livros.
            filename (str): O nome do arquivo CSV onde os dados serão salvos.
            Padrão é "books.csv".
        """
        output_dir = os.path.dirname(filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir) 
            logging.info(f"Directory '{output_dir}' created.")
        
        df = pd.DataFrame(books)
        df.to_csv(filename, index=False, sep=';', encoding='utf-8')
        logging.info(f"Books saved to {filename}")

    def save_books_to_json(
            self,
            books: list,
            filename: str = "data/books.json"
            ) -> None:
        """Salva a lista de livros em um arquivo JSON.
        Esta função utiliza a biblioteca pandas para criar um DataFrame a
        partir da lista de livros e salva o DataFrame em um arquivo JSON.

        Args:
        -------
            books (list): A lista de dicionários contendo detalhes dos livros.
            filename (str): O nome do arquivo JSON onde os dados serão salvos.
            Padrão é "books.json".
        """
        df = pd.DataFrame(books)
        df.to_json(filename, orient='records', lines=True)
        logging.info(f"Books saved to {filename}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    books_scraper = BooksToScrape()
    result = books_scraper.get_books()
    logging.info(f"Total books fetched: {len(result)}")
    books_scraper.save_books_to_csv(books=result)
    books_scraper.save_books_to_json(books=result)
    logging.info("Script completed successfully.")
