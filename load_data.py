import pickle

def load_clients(pickle_path):
    """
    Loads the clients matrix from a pickle file.
    
    Args:
        pickle_path (str): Path to the pickle file (e.g., 'clients_matrix.pkl')
        
    Returns:
        list: A list of 10,000 dictionaries (one per client), or None if error.
    """
    try:
        with open(pickle_path, "rb") as f:
            clients = pickle.load(f)
        return clients
    except Exception as e:
        print(f"Failed to load pickle file: {e}")
        return None

# USAGE: load_clients("clients.pkl")