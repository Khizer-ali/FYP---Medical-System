"""
Document Agent - Handles medical document upload, parsing, and storage
"""
import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2

class DocumentAgent:
    """Agent responsible for processing medical documents"""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'txt']
    
    def parse_document(self, file_path, filename):
        """Parse document and extract text"""
        try:
            file_ext = filename.split('.')[-1].lower()
            
            if file_ext == 'pdf':
                return self._parse_pdf(file_path)
            elif file_ext == 'txt':
                return self._parse_txt(file_path)
            else:
                # Try OCR for images
                return self._parse_image_ocr(file_path)
        except Exception as e:
            return f"Error parsing document: {str(e)}"
    
    def _parse_pdf(self, file_path):
        """Extract text from PDF"""
        try:
            # Try text extraction first
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                if text.strip():
                    return text
            
            # If no text, try OCR
            return self._parse_pdf_ocr(file_path)
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"
    
    def _parse_pdf_ocr(self, file_path):
        """Extract text from PDF using OCR"""
        try:
            images = convert_from_path(file_path)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img) + "\n"
            return text
        except Exception as e:
            return f"Error with PDF OCR: {str(e)}"
    
    def _parse_txt(self, file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def _parse_image_ocr(self, file_path):
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            return pytesseract.image_to_string(image)
        except Exception as e:
            return f"Error with image OCR: {str(e)}"
    
    def store_document(self, patient_id, filename, file_path, parsed_text, document_type, db_session):
        """Store document in database"""
        from database import Document
        
        doc = Document(
            patient_id=patient_id,
            filename=filename,
            file_path=file_path,
            parsed_text=parsed_text,
            document_type=document_type
        )
        db_session.add(doc)
        db_session.commit()
        return doc.to_dict()

