import urllib
from ._httprequests import HttpRequests

class Document:
    document_path = 'documents'

    def __init__(self, parent_path, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path
    
        
    def get_one_document(self, document_id):
        return HttpRequests.put(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            document_id
            )).json()

    def get_documents(self, parameters):
        return HttpRequests.get(
            self.config, 
            '{}/{}/{}?{}'.format(
                self.index_path,
                self.uid, self.document_path,
                urllib.parse.urlencode(parameters))
            ).json()


    def add_documents(self, documents):
        return HttpRequests.post(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            ),
            documents
            ).json()

    def update_documents(self, documents):
        return HttpRequests.put(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            ),
            documents
            ).json()

    def delete_one_document(self, document_id):
        return HttpRequests.delete(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            document_id
        )).json()
    
    def delete_multiple_documents(self, ids):
        return HttpRequests.post(self.config, '{}/{}/{}/delete'.format(
            self.index_path,
            self.uid,
            self.document_path
        ),
        ids
        ).json()
        
    def delete_all_documents(self):
        return HttpRequests.delete(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path
        )
        ).json()