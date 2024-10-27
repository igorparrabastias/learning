import plotly.express as px
import pandas as pd
import os
import faiss
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Constants
DB_PATH = 'db'
INDEX_FILE = os.path.join(DB_PATH, "faiss_index/index.faiss")
VECTORSTORE_FILE = os.path.join(DB_PATH, "faiss_index/index.pkl")

# Cargar el índice de FAISS
index = faiss.read_index(INDEX_FILE)

# Obtener el número total de vectores en el índice
ntotal = index.ntotal

# Reconstruir todos los vectores de manera individual y almacenarlos en una lista
vectors = np.array([index.reconstruct(i) for i in range(ntotal)])

# Ajustar el número de componentes para PCA según el número de características
n_components = min(10, vectors.shape[0], vectors.shape[1])

# Reducir las dimensiones (PCA seguido de t-SNE)
pca = PCA(n_components=n_components).fit_transform(vectors)


def visualize_faiss():

    # Ajustar la perplexity para t-SNE (debe ser menor que el número de muestras)
    perplexity = min(30, ntotal - 1)  # t-SNE sugiere perplexity < n_samples

    # Aplicar t-SNE
    tsne = TSNE(n_components=2, perplexity=perplexity).fit_transform(pca)

    # Visualizar en 2D
    plt.scatter(tsne[:, 0], tsne[:, 1])
    plt.title("Visualización 2D de FAISS")
    plt.show()


def visualize_faiss_pandas():

    # Convertir los embeddings en un DataFrame de Pandas
    df = pd.DataFrame(vectors, columns=[
        f"dim_{i}" for i in range(vectors.shape[1])])
    print(df.head())  # Inspeccionar los primeros embeddings


def visualize_faiss_3d():
    # Ajustar el número de componentes para PCA según el número de características
    n_components = min(10, vectors.shape[0], vectors.shape[1])

    # Reducir las dimensiones con PCA
    pca = PCA(n_components=n_components).fit_transform(vectors)

    # Ajustar la perplexity para t-SNE (debe ser menor que el número de muestras)
    perplexity = min(30, vectors.shape[0] - 1)

    # Aplicar t-SNE en 3D
    tsne_3d = TSNE(n_components=3, perplexity=perplexity).fit_transform(pca)

    # Visualizar en 3D con Plotly
    fig = px.scatter_3d(
        x=tsne_3d[:, 0],
        y=tsne_3d[:, 1],
        z=tsne_3d[:, 2],
        title="Visualización 3D de FAISS"
    )
    fig.show()
