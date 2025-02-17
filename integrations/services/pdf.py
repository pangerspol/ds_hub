import fitz, requests
from io import BytesIO
from integrations.services.sharepoint import SharePointManager
from typing import List, Optional

class PDFManager:
    """@staticmethod
    def merge_pdfs_from_sharepoint(pdf_urls: List[str], sharepoint_folder_id: str, document_type: str, custom_name: Optional[str] = None) -> str:
        sharepoint_manager = SharePointManager()
        
        merged_pdf = fitz.open()  # Empty PDF

        for url in pdf_urls:
            try:
                pdf_stream = sharepoint_manager.download_pdf(url)
                pdf_document = fitz.open("pdf", pdf_stream.read())
                if pdf_document.page_count == 0:
                    raise ValueError(f"PDF is empty: {url}")
                merged_pdf.insert_pdf(pdf_document)
            except (ValueError, IOError) as e:
                print(f"Error processing {url}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error processing {url}: {e}")
                continue  

        # Save merged PDF in memory
        merged_output = BytesIO()
        if merged_pdf.page_count == 0:
            raise ValueError(f"Document is empty: {url}")
        merged_pdf.save(merged_output)
        merged_output.seek(0)

        # Upload back to SharePoint
        merged_pdf_url = sharepoint_manager.upload_file_to_sharepoint(merged_output, sharepoint_folder_id, document_type, custom_name)

        return merged_pdf_url"""
    
    @staticmethod
    def merge_pdfs_from_sharepoint(file_ids: List[str], client_folder_id: str, document_type: str, custom_name: Optional[str] = None) -> str:
        sharepoint_manager = SharePointManager()
        
        merged_pdf = fitz.open()  # Empty PDF

        for file_id in file_ids:
            try:
                pdf_stream = sharepoint_manager.download_file(file_id)
                pdf_document = fitz.open("pdf", pdf_stream.read())
                if pdf_document.page_count == 0:
                    raise ValueError(f"PDF is empty: {file_id}")
                merged_pdf.insert_pdf(pdf_document)
            except (ValueError, IOError) as e:
                print(f"Error processing {file_id}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error processing {file_id}: {e}")
                continue  

        # Save merged PDF in memory
        merged_output = BytesIO()
        if merged_pdf.page_count == 0:
            raise ValueError(f"Document is empty: {file_id}")
        merged_pdf.save(merged_output)
        merged_output.seek(0)

        # Upload back to SharePoint
        merged_pdf_url = sharepoint_manager.upload_file_to_sharepoint(merged_output, client_folder_id, document_type, custom_name)

        return merged_pdf_url