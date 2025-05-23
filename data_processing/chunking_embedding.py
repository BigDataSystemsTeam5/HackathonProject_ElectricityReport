from chunking_evaluation.chunking import RecursiveTokenChunker
import json
from sentence_transformers import SentenceTransformer
import tiktoken
from chunking_evaluation.utils import openai_token_count
from logger_code import get_logger

chunk_analyse_logger = get_logger("chunk_analyze", "chunk_analyze.log")
chunk_embed_logger = get_logger("chunk_embed", "chunk_embed.log")

def embed_chunks(chunks):

    # Embedding settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    # Initialize the embedding model
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = embedding_model.encode(chunks)

    return embeddings




def analyze_chunks(chunks, use_tokens=False):
    """
    Analyze a list of chunks to show statistics and overlaps.
    
    Args:
        chunks: List of text chunks
        use_tokens: Whether to analyze overlap by tokens instead of characters
    """
    # Print basic stats
    chunk_analyse_logger.info("\nNumber of Chunks:", len(chunks))
    
    # Show examples of chunks
    if len(chunks) >= 2:
        chunk_analyse_logger.info("\n", "="*50, f"Chunk #{len(chunks)//3}", "="*50)
        chunk_analyse_logger.info(chunks[len(chunks)//3])
        chunk_analyse_logger.info("\n", "="*50, f"Chunk #{2*len(chunks)//3}", "="*50)
        chunk_analyse_logger.info(chunks[2*len(chunks)//3])
    
    # Calculate average chunk size
    if use_tokens:
        encoding = tiktoken.get_encoding("cl100k_base")
        chunk_sizes = [len(encoding.encode(chunk)) for chunk in chunks]
        chunk_analyse_logger.info(f"\nAverage chunk size: {sum(chunk_sizes)/len(chunk_sizes):.1f} tokens")
        chunk_analyse_logger.info(f"Min chunk size: {min(chunk_sizes)} tokens")
        chunk_analyse_logger.info(f"Max chunk size: {max(chunk_sizes)} tokens")
    else:
        chunk_sizes = [len(chunk) for chunk in chunks]
        chunk_analyse_logger.info(f"\nAverage chunk size: {sum(chunk_sizes)/len(chunk_sizes):.1f} characters")
        chunk_analyse_logger.info(f"Min chunk size: {min(chunk_sizes)} characters")
        chunk_analyse_logger.info(f"Max chunk size: {max(chunk_sizes)} characters")
    
    # Find overlaps if there are at least two chunks
    if len(chunks) >= 2:
        chunk1, chunk2 = chunks[len(chunks)//2], chunks[len(chunks)//2 + 1]
        
        if use_tokens:
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens1 = encoding.encode(chunk1)
            tokens2 = encoding.encode(chunk2)
            
            # Find overlapping tokens
            for i in range(min(len(tokens1), 50), 0, -1):
                if tokens1[-i:] == tokens2[:i]:
                    overlap = encoding.decode(tokens1[-i:])
                    chunk_analyse_logger.info("\n", "="*50, f"\nOverlapping text ({i} tokens):", overlap)
                    return
            chunk_analyse_logger.info("\nNo token overlap found")
        else:
            # Find overlapping characters
            for i in range(min(len(chunk1), 200), 0, -1):
                if chunk1[-i:] == chunk2[:i]:
                    chunk_analyse_logger.info("\n", "="*50, f"\nOverlapping text ({i} chars):", chunk1[-i:])
                    return
            chunk_analyse_logger.info("\nNo character overlap found")



#def save_chunks_to_json(chunks, year, output_dir="chunk_embed_output"):
def save_chunks_to_json(chunks, year):
    """
    Save chunks to a JSON file for later analysis or reference.
    
    Args:
        chunks: List of text chunks
        strategy_name: Name of the chunking strategy
        output_dir: Directory to save the JSON file
        
    Returns:
        Path to the JSON file
    """
    # Create strategy directory if it doesn't exist
    #strategy_dir = os.path.join(output_dir, strategy_name)
    #os.makedirs(strategy_dir, exist_ok=True)
    
    try:
    # Create a JSON object
        chunks_data = []

        # Add each chunk with metadata
        for i, chunk in enumerate(chunks):
            encoder = tiktoken.get_encoding("cl100k_base")
            chunk_count = len(chunks)
            char_length = len(chunk)
            token_length = len(encoder.encode(chunk))

            result = embed_chunks(chunk)
            embeddings = result.tolist()

            chunk_info = {
                "id": str(i),
                "values": embeddings,
                "metadata": {
                            "year": year,
                            "chunk_count": chunk_count,
                            "content": chunk,
                            "char_length": char_length,
                            "token_length": token_length
                            }
            }

            chunks_data.append(chunk_info)
            chunk_embed_logger.info(f"Chunk ID {i} for {year} is embedded and appended to JSON")

        result = json.dumps(chunks_data)   

    # Save to JSON file
    #output_path = os.path.join(strategy_dir, f"chunks_2024_3.json")
    #with open(output_path, 'w', encoding='utf-8') as f:
    #    json.dump(chunks_data, f, indent=2)

    except Exception as e:
        chunk_embed_logger.error(f"Error while saving chunks to json: {str(e)}")
        return
    
    #print(f"Chunks saved to {output_path}")
    return result



#def chunking_strategy(document, year, quarter):
def chunking_embedding_strategy(document, year):

    # Load the sample document
    #with open(r"C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\docling_output_md\NVIDIA.md", 'r', encoding='utf-8') as file:
        #document = file.read()

    try:
        # Get the total token count
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(document)
        chunk_embed_logger.info(f"Total document length: {len(tokens)} tokens")


        # With overlap
        recursive_token_overlap_chunker = RecursiveTokenChunker(
            chunk_size=400,
            chunk_overlap=50,
            length_function=openai_token_count,
            separators=["\n\n", "\n", ".", "?", "!", " ", ""]
        )

        recursive_token_overlap_chunks = recursive_token_overlap_chunker.split_text(document)

        analyze_chunks(recursive_token_overlap_chunks, use_tokens=True)

        # Save overlap chunks to JSON
        result = save_chunks_to_json(recursive_token_overlap_chunks,  year)

    except Exception as e:
        chunk_embed_logger.error(f"Error in chunking and embedding of file: {str(e)}")
        return

    return result

#chunking_embedding_strategy(2024, 4)