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
            # Use strict=False to handle corrupted PDFs more gracefully
            try:
                pdf_reader = PyPDF2.PdfReader(file, strict=False)
            except PyPDF2.errors.PdfReadError as e:
                if "EOF marker not found" in str(e):
                    raise Exception(
                        "PDF file appears to be corrupted or incomplete. "
                        "Please try:\n"
                        "1. Re-downloading the file\n"
                        "2. Opening and re-saving it with a PDF viewer\n"
                        "3. Using a different PDF file"
                    )
                else:
                    raise Exception(f"Cannot read PDF file: {str(e)}")
            
            total_pages = len(pdf_reader.pages)
            
            if total_pages == 0:
                raise Exception("PDF file has no pages")
            
            print(f"   PDF has {total_pages} pages")
            
            # Extract text from each page
            for page_num in range(total_pages):
                try:
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        text_content.append(page_text)
                    
                    # Progress indicator for large PDFs
                    if (page_num + 1) % 10 == 0:
                        print(f"   Processed {page_num + 1}/{total_pages} pages")
                        
                except Exception as page_error:
                    print(f"   ⚠️  Warning: Could not extract text from page {page_num + 1}: {str(page_error)}")
                    continue
            
            # Combine all pages
            full_text = "\n\n".join(text_content)
            
            if not full_text or len(full_text.strip()) < 10:
                raise Exception(
                    "No text could be extracted from the PDF. "
                    "The file might be:\n"
                    "1. A scanned image (requires OCR)\n"
                    "2. Password protected\n"
                    "3. Corrupted or invalid"
                )
            
            print(f"   Extracted {len(full_text)} characters")
            
            return full_text
            
    except Exception as e:
        # Re-raise with context if it's already our custom exception
        if "PDF file appears to be corrupted" in str(e) or "No text could be extracted" in str(e):
            raise
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
        
        # Use strict=False to handle corrupted PDFs more gracefully
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file, strict=False)
        except PyPDF2.errors.PdfReadError as e:
            if "EOF marker not found" in str(e):
                raise Exception(
                    "PDF file appears to be corrupted or incomplete. "
                    "Please try re-downloading or using a different file."
                )
            else:
                raise Exception(f"Cannot read PDF file: {str(e)}")
        
        for page in pdf_reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
            except Exception as page_error:
                # Skip problematic pages
                continue
        
        full_text = "\n\n".join(text_content)
        
        if not full_text or len(full_text.strip()) < 10:
            raise Exception(
                "No text could be extracted from the PDF. "
                "The file might be a scanned image, password protected, or corrupted."
            )
        
        return full_text
        
    except Exception as e:
        if "PDF file appears to be corrupted" in str(e) or "No text could be extracted" in str(e):
            raise
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
