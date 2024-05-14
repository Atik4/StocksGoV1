import json

def load_data(file_path):
    """ Load the entire JSON data from the file. """
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(data, file_path):
    """ Save data to a JSON file. """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def split_json(file_path, max_size_mb=40):
    """ Split a large JSON array into multiple smaller files. """
    data = load_data(file_path)
    chunks = []
    current_chunk = []

    for item in data:
        current_chunk.append(item)
        # Check the size of the current chunk by converting to JSON string
        if len(json.dumps(current_chunk)) > max_size_mb * 1024 * 1024:  # max_size_mb in bytes
            current_chunk.pop()  # Remove last item that caused overflow
            chunks.append(current_chunk)
            current_chunk = [item]  # Start new chunk with the last item

    if current_chunk:  # Add the last chunk if it has data
        chunks.append(current_chunk)

    # Save chunks to separate files
    for i, chunk in enumerate(chunks):
        save_data(chunk, f'chunk_{i + 1}.json')

# Example usage
split_json('stock_ohlc.json')
