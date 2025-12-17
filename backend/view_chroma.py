"""
ChromaDB Vector Database Viewer
Inspect and explore the contents of your Qnix AI vector database
"""

import sys
import os

# Add parent directory to path to import from app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.vector_store import get_vector_store, CHROMA_DB_DIR, COLLECTION_NAME
import json
from typing import Optional


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(text: str):
    """Print a formatted section"""
    print(f"\n📊 {text}")
    print("-" * 70)


def view_collection_info():
    """Display basic collection information"""
    print_header("ChromaDB Collection Information")
    
    vector_store = get_vector_store()
    
    print(f"📁 Storage Path: {os.path.abspath(CHROMA_DB_DIR)}")
    print(f"📦 Collection Name: {COLLECTION_NAME}")
    
    count = vector_store.count()
    print(f"📝 Total Chunks: {count}")
    
    if count == 0:
        print("\n⚠️  Database is empty. Upload some documents first!")
        return False
    
    return True


def view_all_documents():
    """List all unique documents in the database"""
    print_section("Documents in Database")
    
    vector_store = get_vector_store()
    
    # Get all data
    results = vector_store.get(
        include=['metadatas']
    )
    
    if not results or not results.get('metadatas'):
        print("No documents found.")
        return
    
    # Extract unique documents
    documents = {}
    for metadata in results['metadatas']:
        file_id = metadata.get('file_id')
        filename = metadata.get('filename')
        
        if file_id not in documents:
            documents[file_id] = {
                'filename': filename,
                'chunks': 0
            }
        documents[file_id]['chunks'] += 1
    
    # Display documents
    for i, (file_id, info) in enumerate(documents.items(), 1):
        print(f"\n{i}. 📄 {info['filename']}")
        print(f"   File ID: {file_id}")
        print(f"   Chunks: {info['chunks']}")


def view_document_chunks(file_id: Optional[str] = None, limit: int = 5):
    """View chunks from a specific document or all chunks"""
    if file_id:
        print_section(f"Chunks for File ID: {file_id}")
    else:
        print_section(f"Recent Chunks (showing first {limit})")
    
    vector_store = get_vector_store()
    
    # Query chunks
    if file_id:
        results = vector_store.get(
            where={"file_id": file_id},
            include=['documents', 'metadatas']
        )
    else:
        results = vector_store.get(
            limit=limit,
            include=['documents', 'metadatas']
        )
    
    if not results or not results.get('documents'):
        print("No chunks found.")
        return
    
    # Display chunks
    for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas']), 1):
        print(f"\n--- Chunk {i} ---")
        print(f"📄 File: {metadata.get('filename', 'Unknown')}")
        print(f"🔢 Chunk Index: {metadata.get('chunk_index', 'N/A')} / {metadata.get('total_chunks', 'N/A')}")
        print(f"📝 Content Preview:")
        
        # Show first 200 characters
        preview = doc[:200] + "..." if len(doc) > 200 else doc
        print(f"   {preview}")


def search_database(query: str, top_k: int = 5):
    """Search the database with a query"""
    print_section(f"Search Results for: '{query}'")
    
    vector_store = get_vector_store()
    
    # Note: This requires embeddings, which we'll generate
    from app.utils.ollama_client import generate_embeddings
    import asyncio
    
    try:
        # Generate embedding for query
        print("🔍 Generating query embedding...")
        query_embedding = asyncio.run(generate_embeddings(query))
        
        # Search
        results = vector_store.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        if not results or not results.get('documents') or not results['documents'][0]:
            print("No results found.")
            return
        
        # Display results
        for i, (doc, metadata, distance) in enumerate(
            zip(results['documents'][0], results['metadatas'][0], results['distances'][0]), 
            1
        ):
            similarity = 1 - distance  # Convert distance to similarity
            print(f"\n{i}. 📄 {metadata.get('filename', 'Unknown')}")
            print(f"   Similarity: {similarity:.2%}")
            print(f"   Chunk: {metadata.get('chunk_index', 'N/A')} / {metadata.get('total_chunks', 'N/A')}")
            print(f"   Content Preview:")
            preview = doc[:200] + "..." if len(doc) > 200 else doc
            print(f"   {preview}")
            
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        print("Make sure Ollama is running and the embedding model is installed.")


def export_to_json(output_file: str = "chroma_export.json"):
    """Export entire database to JSON"""
    print_section(f"Exporting to {output_file}")
    
    vector_store = get_vector_store()
    
    # Get all data
    results = vector_store.get(
        include=['documents', 'metadatas', 'embeddings']
    )
    
    # Prepare export data
    export_data = {
        "collection_name": COLLECTION_NAME,
        "total_chunks": len(results.get('ids', [])),
        "chunks": []
    }
    
    for chunk_id, doc, metadata in zip(
        results.get('ids', []),
        results.get('documents', []),
        results.get('metadatas', [])
    ):
        export_data['chunks'].append({
            "id": chunk_id,
            "document": doc,
            "metadata": metadata
        })
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {export_data['total_chunks']} chunks to {output_file}")


def interactive_menu():
    """Interactive menu for exploring the database"""
    print_header("Qnix AI - ChromaDB Viewer")
    
    if not view_collection_info():
        return
    
    while True:
        print("\n" + "=" * 70)
        print("Options:")
        print("  1. View all documents")
        print("  2. View chunks from a document")
        print("  3. View recent chunks")
        print("  4. Search database")
        print("  5. Export to JSON")
        print("  6. Refresh stats")
        print("  0. Exit")
        print("=" * 70)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            view_all_documents()
            
        elif choice == "2":
            file_id = input("Enter file ID: ").strip()
            view_document_chunks(file_id=file_id)
            
        elif choice == "3":
            try:
                limit = int(input("How many chunks to show? (default 5): ").strip() or "5")
                view_document_chunks(limit=limit)
            except ValueError:
                print("Invalid number, using default (5)")
                view_document_chunks(limit=5)
                
        elif choice == "4":
            query = input("Enter search query: ").strip()
            if query:
                try:
                    top_k = int(input("How many results? (default 5): ").strip() or "5")
                    search_database(query, top_k=top_k)
                except ValueError:
                    search_database(query, top_k=5)
            else:
                print("Query cannot be empty.")
                
        elif choice == "5":
            filename = input("Output filename (default: chroma_export.json): ").strip()
            export_to_json(filename or "chroma_export.json")
            
        elif choice == "6":
            view_collection_info()
            
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
