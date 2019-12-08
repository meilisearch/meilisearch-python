from ._httprequests import HttpRequests
import urllib

class Document:
    document_path = 'documents'

    def __init__(self, parent_path, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path
        pass
    
        
    def get_one_document(self, id):
        return HttpRequests.put(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            id
            )).json()

    # TODO stringify params
    def get_documents(self, **parameters):
        # maybe quote_plus
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

    def delete_one_document(self, id):
        return HttpRequests.delete(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            id
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