"""
Simple 3D Visualization of ChromaDB Embeddings
Just run this script to view your embeddings in 3D
"""
import chromadb
from sklearn.decomposition import PCA
import plotly.express as px
import os

# Get the correct path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(SCRIPT_DIR, "data", "chroma_db")
COLLECTION_NAME = "qnix_documents"

# 1. Get embeddings from your ChromaDB instance
print("Loading ChromaDB...")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(COLLECTION_NAME)
results = collection.get(include=['embeddings', 'documents', 'metadatas'])

if len(results['embeddings']) == 0:
    print("No embeddings found! Upload some documents first.")
    exit()

embeddings = results['embeddings']
docs = results['documents']
metadatas = results['metadatas']

print(f"Found {len(embeddings)} document chunks")

# Create labels from metadata
labels = [f"{m.get('filename', 'Unknown')} (chunk {m.get('chunk_index', 0)})" 
          for m in metadatas]

# 2. Reduce dimensionality to 3 components using PCA
print("Reducing to 3D with PCA...")
pca = PCA(n_components=3)
vis_dims = pca.fit_transform(embeddings)

print(f"Variance explained: {sum(pca.explained_variance_ratio_):.1%}")

# 3. Create an interactive 3D plot
print("Creating visualization...")
fig = px.scatter_3d(
    x=vis_dims[:, 0],
    y=vis_dims[:, 1],
    z=vis_dims[:, 2],
    color=[m.get('filename', 'Unknown') for m in metadatas],  # Color by file
    hover_name=labels,
    hover_data={'text': [d[:100] + '...' if len(d) > 100 else d for d in docs]},
    labels={'x': 'PCA Component 1', 'y': 'PCA Component 2', 'z': 'PCA Component 3'},
    title='3D Visualization of Document Embeddings',
    height=800
)

fig.update_traces(marker=dict(size=5, opacity=0.7))

print("Opening in browser...")
fig.show()  # This will open an interactive plot in your web browser
