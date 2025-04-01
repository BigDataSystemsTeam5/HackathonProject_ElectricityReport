import os
import tempfile
from docling.document_converter import DocumentConverter
from logger_code import get_logger

docling_markdown_logger = get_logger("docling_markdown", "docling_markdown.log")

def convert_and_save_document(pdf_bytes: bytes):

    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(pdf_bytes)
            temp_file_path = temp_file.name

#def convert_and_save_document(file_path):    
        # Initialize converter
        converter = DocumentConverter()
        result = converter.convert(temp_file_path)

        # Convert document
        final_result = result.document.export_to_markdown()

    except Exception as e:
        docling_markdown_logger.error(f"Error in markdwown conversion of file: {str(e)}")
        return

    return final_result


    # Create the base output directory if it doesn't exist
    #foldername = "dockling_output_md"
    #os.makedirs(foldername, exist_ok=True)

    #filename = "new_docling.md"
    #file_path = os.path.join(foldername, filename)

    # Save markdown content
    #with open(file_path, 'w', encoding='utf-8') as f:
    #    f.write(final_result)
    

# Example usage
#file_path = r"C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Hackathon\data_processing\new_pdf.pdf"
#output_path = convert_and_save_document(file_path)
#print("Markdown file saved")
