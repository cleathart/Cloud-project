import hashlib
from search_base import SearchEngine

from google.appengine.api import search

class SearchAPI(SearchEngine):
    """GAE Search API implementation, can be used only withing GAE"""

    def __init__(self, client=None):
        self.client = search.Index('recipes')  # setting Index

    def search(self, query):
        """Making search with SearchAPI and returning result"""
        try:
            search_results = self.client.search(query)
            results = search_results.results
            output = []
            for item in results:
                out = {
                    'recipe_name': item.field('recipe').value,
                    'ingredients': item.field('ingredients').value,
                    'method': item.field('method').value,
                    'image_url': item.field('image_url').value
                }
                output.append(out)
        except Exception:
            output = []
        return output

    def get_key(self, key):
        try:
            search_result = self.client.get(key)
            
            output = {
                'recipe_name': search_result.field('recipe').value,
                'ingredients': search_result.field('ingredients').value,
                'method': search_result.field('method').value,
                'image_url': search_result.field('image_url').value
            }
        except Exception:
            output = {}
        return output


    def insert(self, item, image_url):
        """Inserts document in the Search Index"""
        doc = search.Document(
            doc_id = hashlib.md5(item['recipe_name']).hexdigest(),
            fields=[
                search.TextField(name='recipe', value=item['recipe_name']),
                search.TextField(name='ingredients', value=' - '.join(item['ingredients'].split('\r\n'))),
                search.TextField(name='method', value=' - '.join(item['method'].split('\r\n'))),
                search.TextField(name='image_url', value = image_url)
            ]
        )
        self.client.put(doc)

    


    def delete_all(self):
        """Deletes all documents in Search Index"""

        while True:
            document_ids = [
                document.doc_id
                for document
                in self.client.get_range(ids_only=True)]

            # If no IDs were returned, we've deleted everything.
            if not document_ids:
                break

            # Delete the documents for the given IDs
            self.client.delete(document_ids)