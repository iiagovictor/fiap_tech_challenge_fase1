import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# --- Carregamento de Dados ---
from app.api.root import dados_csv
df_bruto = dados_csv

# --- Funções de Pré-processamento e Auxiliares ---
def tratar_dados_livros(df_bruto: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o pré-processamento do DataFrame
    """
    features = ['book_id', 'title', 'description', 'review_rating', 'category', 'price_including_tax', 'number_available']

    df_tratativa = df_bruto[features].copy()
    df_tratativa = df_tratativa.rename(columns={'price_including_tax': 'price'})
    df_tratativa['description'] = df_tratativa['description'].fillna('')

    df_tratativa['price'] = df_tratativa['price'].astype(str).str.replace(',', '.', regex=False)
    df_tratativa['price'] = pd.to_numeric(df_tratativa['price'], errors='coerce')
    df_tratativa['price'] = df_tratativa['price'].apply(lambda x: abs(x) if pd.notna(x) else x)

    return df_tratativa.copy()

def sanitize_single_value(x):
    """
    Limpa um único valor (string), removendo todos os espaços e convertendo para minúsculas.
    Retorna uma string vazia se o valor não for uma string.
    """
    if isinstance(x, str):
        return str.lower(x.replace(" ", ""))
    else:
        return ''

def preparar_modelo_recomendacao(df_tratado: pd.DataFrame):
    """
    Prepara os componentes necessários para o sistema de recomendação de conteúdo.
    """
    df_model = df_tratado[['book_id', 'title', 'description', 'category']].copy()
    df_model = df_model.reset_index(drop=True)

    for feature in ['description', 'category']:
        df_model[feature] = df_model[feature].apply(sanitize_single_value)

    df_model['combined_features'] = df_model['description'] + ' ' + df_model['category']
    df_model['combined_features'] = df_model['combined_features'].str.strip()

    count_vectorizer = CountVectorizer(stop_words='english')
    count_matrix = count_vectorizer.fit_transform(df_model['combined_features'])

    cosine_sim_matrix = cosine_similarity(count_matrix, count_matrix)

    indices = pd.Series(df_model.index, index=df_model['title']).drop_duplicates()

    return df_model, cosine_sim_matrix, indices

# --- Função de Recomendação Principal ---
def content_recommender(title: str,
                        cosine_sim_matrix_ref: np.ndarray,
                        df_data_ref: pd.DataFrame,
                        indices_map_ref: pd.Series) -> pd.DataFrame:
    """
    Gera recomendações de livros baseadas na similaridade de conteúdo.
    """
    if title not in indices_map_ref:
        print(f"Erro: O livro '{title}' não foi encontrado no catálogo.")
        return pd.DataFrame(columns=['book_id', 'title'])

    idx = indices_map_ref[title]

    sim_scores = list(enumerate(cosine_sim_matrix_ref[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    book_indices = [i[0] for i in sim_scores]

    return df_data_ref[['book_id','title']].iloc[book_indices].copy()

# --- Fluxo Principal de Execução para Geração de PKL Único ---
if __name__ == "__main__":
    # 1. Trata os dados brutos
    df_tratado = tratar_dados_livros(df_bruto)

    # 2. Prepara o modelo de recomendação
    df_model_final, cosine_sim_matrix_final, indices_final = preparar_modelo_recomendacao(df_tratado)

    # 3. Cria um dicionário com todos os componentes
    model_components = {
        'df_model': df_model_final,
        'cosine_sim_matrix': cosine_sim_matrix_final,
        'indices': indices_final
    }

    # 4. Salva o dicionário inteiro em um único arquivo .pkl com joblib
    joblib.dump(model_components, "modelo_recomendacao.pkl")
    print("Todos os componentes do modelo foram salvos em 'modelo_recomendacao.pkl.pkl'.")