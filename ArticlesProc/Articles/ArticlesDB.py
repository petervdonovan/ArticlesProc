from Utils.search import DB
class ArticlesDB:
    """A singleton rapid lookup table for Article objects."""
    instance = None
    def __init__(self):
        if ArticlesDB.instance is None:
            ArticlesDB.instance=DB(
                dbItemIdFunc=lambda article: article.getId(),
                itemNearMatchFunc=lambda search, article: search == article.getId(),
                itemMatchFunc=lambda search, article2: search == article2.getId()
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
    def clear(self):
        '''Clears away all articles stored in ArticlesDB.'''
        ArticlesDB.instance.clear()
    def __iter__(self):
        '''Initializes iteration over the articles in the DB.'''
        self.selectedIdx = 0
        return self
    def __next__(self):
        '''Returns the next item in iteration.'''
        if self.selectedIdx == len(ArticlesDB.instance.db):
            raise StopIteration
        self.selectedIdx += 1
        return ArticlesDB.instance.db[self.selectedIdx - 1]