from Utils.search import DB
class ArticlesDB(object):
    """A singleton rapid lookup table for Article objects."""
    instance = None
    def __init__(self):
        if ArticlesDB.instance is None:
            ArticlesDB=DB(
                dbItemIdFunc=lambda article: article.getId(),
                itemNearMatchFunc=lambda article1, article2: article1.getId() == article2.getId(),
                itemMatchFunc=lambda article1, article2: article1.getId() == article2.getId()
                )
    # The remaining functions should be trivial boilerplate because
    # the essence of this class is in the common instance.
    def add(self, article):
        '''Adds an article to the DB.'''
        ArticlesDB.instance.add(article)
    def get(self, id):
        '''Gets the article of the desired ID.'''
        assert(type(id) == int)
        return ArticlesDB.instance.get(id)
    def pickle(self, fileName="ArticlesDB"):
        '''Pickles the list of articles.'''
        ArticlesDB.instance.pickle(fileName)
    def getFromPickle(self, fileName):
        '''Inits the db instance from a pickle.'''
        ArticlesDB.instance.getFromPickle(fileName)