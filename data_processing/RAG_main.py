from web_scrapper import scrape_upload_electricity_pdfs
from web_scrapper_list import scrape_electricity_pdfs_list
from logger_code import get_logger
from docling_markdown import convert_and_save_document
from pinecone_upsert import upsert_pinecone
from chunking_embedding import chunking_embedding_strategy


bucket_name = "bigdatasystems2"

# Create separate loggers for each ETL process
web_scrape_logger = get_logger("web_scrape_hack", "web_scrape.log")
docling_markdown_logger = get_logger("docling_markdown_hack", "docling_markdown.log")
chunk_analyse_logger = get_logger("chunk_analyze_hack", "chunk_analyze.log")
chunk_embed_logger = get_logger("chunk_embed_hack", "chunk_embed.log")
pinecone_upsert_logger = get_logger("pinecone_upsert_hack", "pinecone_upsert.log")


web_scrape_logger.info("Data Pipeline execution started.")

base_url = "https://www.iea.org/reports/electricity-2025"

filelist = scrape_electricity_pdfs_list(base_url)
filelist.append(base_url)

web_scrape_logger.info("Webpage url list created")

for fileurl in filelist:
    try:
        year = fileurl.split("electricity-")[-1] 

        web_scrape_logger.info(f"Starting webpage scraping of {fileurl}")
        file, filename = scrape_upload_electricity_pdfs(fileurl, bucket_name)
        file_content = file.content
        web_scrape_logger.info(f"{filename} scraped and uploaded to S3")

        docling_markdown_logger.info(f'Starting markdown conversion for file: {filename}')
        markdown_file = convert_and_save_document(file_content)
        docling_markdown_logger.info(f'Markdown conversion finished for file: {filename}')

        chunk_embed_logger.info(f'Starting chunking and embedding for file: {filename}')
        embed_json = chunking_embedding_strategy(markdown_file, year)
        chunk_embed_logger.info(f'Finished chunking and embedding for file: {filename}')

        result = upsert_pinecone(embed_json, year)
        pinecone_upsert_logger.info(f'The chuncks are upserted to Pinecone along with its metadata. The statistics are: {result}')

    except Exception as e:
        web_scrape_logger.error(f"Error retrieving file: {str(e)}")

web_scrape_logger.info("Data Pipeline execution completed.")
    

