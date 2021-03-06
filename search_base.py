class SearchEngine:
    """Base class to implement search interface for different storages"""

    def __init__(self, client=None):
        self.client = client

    def search(self, query):
        """Executes search"""
        raise NotImplementedError

    def insert(self, text):
        """Inserts text"""
        raise NotImplementedError
    
    def get_key(self, text):
        """Gets entry based on key"""
        raise NotImplementedError

    def delete_all(self):
        """Deletes all data"""
        raise NotImplementedError