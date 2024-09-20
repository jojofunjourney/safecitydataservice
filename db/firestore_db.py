import logging
from google.cloud import firestore
from typing import List, Dict, Any
import json

def save_to_firestore(city, data):
    logging.info(f"Starting to save data for {city} to Firestore")
    logging.debug(f"Data size: {len(data)} records")

    db = firestore.Client()
    collection_ref = db.collection('city_data').document(city)

    # Start with a smaller chunk size
    chunk_size = 500000  # ~500 KB
    data_str = json.dumps(data)
    chunks = [data_str[i:i + chunk_size] for i in range(0, len(data_str), chunk_size)]
    
    logging.info(f"Splitting data into {len(chunks)} chunks")

    for idx, chunk in enumerate(chunks):
        retries = 3
        while retries > 0:
            try:
                logging.debug(f"Saving chunk {idx+1}/{len(chunks)} for {city}")
                collection_ref.collection('chunks').document(f'chunk_{idx}').set({'data': chunk})
                logging.debug(f"Successfully saved chunk {idx+1}/{len(chunks)} for {city}")
                break  # Success, exit the retry loop
            except Exception as e:
                retries -= 1
                if "longer than 1048487 bytes" in str(e):
                    # If the error is due to chunk size, reduce the chunk size and retry
                    chunk_size = int(chunk_size * 0.8)  # Reduce chunk size by 20%
                    logging.warning(f"Chunk too large. Reducing chunk size to {chunk_size} and retrying.")
                    chunks = [data_str[i:i + chunk_size] for i in range(0, len(data_str), chunk_size)]
                elif retries == 0:
                    error_msg = f"Error saving chunk {idx+1}/{len(chunks)} for {city} to Firestore: {str(e)}"
                    logging.error(error_msg)
                    raise Exception(error_msg)
                else:
                    logging.warning(f"Error saving chunk. Retrying... ({retries} attempts left)")

    logging.info(f"Successfully saved all data for {city} to Firestore")