import pandas as pd


def get_csv_data(
        path_file: str
        ) -> pd.DataFrame:
    """Função para obter o conteúdo de um arquivo CSV e retornar um DataFrame do Pandas.
    O arquivo CSV deve estar no formato correto, com colunas separadas por ponto e vírgula.

    Parameters:
    ----------
    path_file : str
        Caminho para o arquivo CSV a ser lido.
    Returns:
    -------
    pd.DataFrame
        DataFrame contendo os dados do arquivo CSV.
    Raises:
    ------
    Exception
        Se ocorrer um erro ao ler o arquivo CSV, a função retornará uma exceção.
    """  # noqa: E501
    try:
        print(f"Lendo arquivo CSV de: {path_file}")
        df = pd.read_csv(path_file, sep=';')
        # A coluna de data não vinha com o formato de data, vinha como object
        df['created_at'] = pd.to_datetime(
            df['created_at'], errors='coerce'
        )
        # Converte para string para evitar erro de validação no Pydantic
        df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        # Evitando valores negativos nas colunas float
        df['price_including_tax'] = df['price_including_tax'].apply(
            lambda x: abs(x)
        )
        df['price_excluding_tax'] = df['price_excluding_tax'].apply(
            lambda x: abs(x)
        )
        df['tax'] = df['tax'].apply(lambda x: abs(x))
        # Preenchendo valores vazios na coluna de categoria
        df = df.fillna("--")
    except Exception as error:
        return error
    return df


def get_unique_items(
        df: pd.DataFrame,
        column_name: str
        ):
    """Função para obter uma lista de itens únicos de uma coluna específica de um DataFrame.

    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame do qual os itens únicos serão extraídos.
    column_name : str
        Nome da coluna do DataFrame da qual os itens únicos serão extraídos.
    """  # noqa: E501
    try:
        if column_name not in df.columns:
            raise ValueError(
                f"A coluna '{column_name}' não existe na base de dados"
            )
        unique_items = df[column_name].drop_duplicates().tolist()
        return unique_items
    except Exception as error:
        return error


def get_rating(
        df: pd.DataFrame,
        name_column: str,
        required_number: int,
        default_response: int = 0
        ) -> int:
    """Função para obter a contagem de um número específico de avaliações de uma coluna.
    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame do qual a contagem de avaliações será extraída.
    name_column : str
        Nome da coluna do DataFrame da qual a contagem de avaliações será extraída.
    required_number : int
        Número específico de avaliações a serem contadas.
    default_response : int, optional
        Valor padrão a ser retornado se o número específico não for encontrado, por padrão 0.

    Returns:
    -------
    int
        Contagem de avaliações do número específico na coluna, ou o valor padrão se não encontrado.
    """  # noqa: E501
    rating = int(
        df[name_column].value_counts().get(required_number, default_response)
    )
    return rating


def get_price_range(df, name_column, min_price, max_price):
    result = df.query(
        f'{name_column} >= {min_price} and {name_column} <= {max_price}'
        )
    return result
