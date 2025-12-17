"""
PDF Text Extraction Utilities
Extracts text content from PDF files
"""

import PyPDF2
from typing import Optional
import io


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
        
    Raises:
        Exception: If PDF cannot be read or is empty
    """
    try:
        text_content = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            print(f"   PDF has {total_pages} pages")
            
            # Extract text from each page
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    text_content.append(page_text)
                
                # Progress indicator for large PDFs
                if (page_num + 1) % 10 == 0:
                    print(f"   Processed {page_num + 1}/{total_pages} pages")
            
            # Combine all pages
            full_text = "\n\n".join(text_content)
            
            print(f"   Extracted {len(full_text)} characters")
            
            return full_text
            
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes (useful for uploaded files)
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        Extracted text as a string
    """
    try:
        text_content = []
        
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
        
        return "\n\n".join(text_content)
        
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF bytes: {str(e)}")


def get_pdf_metadata(file_path: str) -> dict:
    """
    Extract metadata from PDF file
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Dictionary containing PDF metadata
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            metadata = pdf_reader.metadata
            
            return {
                "title": metadata.get("/Title", "Unknown"),
                "author": metadata.get("/Author", "Unknown"),
                "subject": metadata.get("/Subject", ""),
                "creator": metadata.get("/Creator", ""),
                "producer": metadata.get("/Producer", ""),
                "pages": len(pdf_reader.pages)
            }
            
    except Exception as e:
        return {"error": str(e)}
