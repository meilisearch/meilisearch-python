import urllib
from meilisearch._httprequests import HttpRequests

class Document:
    """
    Documents routes wrapper

    Index's parent that gives access to all the documents methods of meilisearch.
    https://docs.meilisearch.com/references/documents.html

    Attributes
    ----------
    document_path:
        Document url path
    """
    document_path = 'documents'

    def __init__(self, parent_path, config, uid=None, name=None):
        """
        Parameters
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        name: str
            Name of the index on which to perform the document actions.
        uid: str
            Uid of the index on which to perform the document actions.
        index_path: str
            Index url path
        """
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path


    def get_document(self, document_id):
        """Get one document with given document identifier

        Parameters
        ----------
        document_id: str
            Unique identifier of the document.
        Returns
        ----------
        document: `dict`
            Dictionnary containing the documents information
        """
        return HttpRequests.get(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            document_id
            )).json()

    def get_documents(self, parameters):
        """Get a set of documents from the index

        Parameters
        ----------
        parameters: dict
            parameters accepted by the get documents route: https://docs.meilisearch.com/references/documents.html#get-all-documents
        Returns
        ----------
        document: `dict`
            Dictionnary containing the documents information
        """
        return HttpRequests.get(
            self.config,
            '{}/{}/{}?{}'.format(
                self.index_path,
                self.uid, self.document_path,
                urllib.parse.urlencode(parameters))
            ).json()


    def add_documents(self, documents):
        """Add documents to the index

        Parameters
        ----------
        documents: list
            List of dics containing each a document, or json string
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            ),
            documents
            ).json()

    def update_documents(self, documents):
        """Update documents in the index

        Parameters
        ----------
        documents: list
            List of dics containing each a document, or json string
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.put(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            ),
            documents
            ).json()

    def delete_document(self, document_id):
        """Add documents to the index

        Parameters
        ----------
        document_id: str
            Unique identifier of the document.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path,
            document_id
        )).json()

    def delete_documents(self, ids):
        """Delete multiple documents of the index

        Parameters
        ----------
        list: list
            List of unique identifiers of documents.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(self.config, '{}/{}/{}/delete'.format(
            self.index_path,
            self.uid,
            self.document_path
        ),
        ids
        ).json()

    def delete_all_documents(self):
        """Delete all documents of the index

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.document_path
        )
        ).json()
