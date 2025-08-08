import joblib
from typing import List
from pathlib import Path

model_components = None

current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
model_path = project_root / "modelo_recomendacao.pkl"

try:
    if model_path.exists():
        model_components = joblib.load(model_path)
        print("Todos os componentes do modelo foram carregados com sucesso no serviço!")  # noqa: E501
    else:
        raise FileNotFoundError(f"Arquivo do modelo não encontrado: {model_path}")  # noqa: E501
except FileNotFoundError as e:
    print(f"ERRO: {e}. O serviço de recomendação não estará disponível.")
except Exception as e:
    print(f"ERRO: Não foi possível carregar os componentes do modelo: {e}")
    model_components = None


def get_recommendations_from_title(title: str) -> List[str]:
    """
    Gera recomendações de livros com base em um título.
    Esta função encapsula a lógica de negócio do modelo.
    """
    if model_components is None:
        raise RuntimeError("O serviço de recomendação não está disponível.")

    cosine_sim_matrix = model_components['cosine_sim_matrix']
    df_data = model_components['df_model']
    indices = model_components['indices']

    if title not in indices:
        raise ValueError("O título do livro não foi encontrado no catálogo.")

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]
    recommended_books = df_data[['title']].iloc[book_indices]['title'].tolist()

    return recommended_books
