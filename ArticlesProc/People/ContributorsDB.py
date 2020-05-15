from Utils.search import DB
from Utils.timeUtils import getStringTimestamp
from People.Name import Name
import pickle
import time

class ContributorsDB:
    """A singleton contributors registration system, documenting
    all known contributors (people who write Articles) in one 
    place."""
    instance = None
    def __init__(self):
        '''Create instance of the singleton.'''
        if ContributorsDB.instance is None:
            ContributorsDB.instance = DB(
                dbItemIdFunc = lambda contributor: contributor.name, 
                itemNearMatchFunc = lambda search, itemInList: search == itemInList.name, 
                itemMatchFunc = lambda search, itemInList: search.contains(itemInList.name) or \
                                                           itemInList.name.contains(search)
                )
    def registerContributor(self, contributor):
        '''Adds a Contributor to the database as needed and returns 
        the result of a search for the Contributor. This search result
        may have more complete information about the person described.'''
        t0 = time.time()
        ContributorsDB.instance.add(contributor)
        # if time.time()-t0 < 0.001:
        #     print('took a SHORT time to add to the ContributorsDB:')
        #     print(self.get(contributor.name))
        # if time.time()-t0 > 0.1:
        #     print('took a LONG time to add to the ContributorsDB:')
        #     print(self.get(contributor.name))
        #print('Time to registerContributor:', time.time() - t0)
        return self.get(contributor.name)
    def registerArticle(self, article):
        '''Stores an Article in this database, under the names of 
        the contributors to the Article.'''
        contributors = article.getContributors()
        for contributor in contributors:
            contributor.addArticle(article)
            self.registerContributor(contributor)
    def get(self, name):
        assert(type(name) == Name)
        result = ContributorsDB.instance.get(name)
        return result
    def print(self):
        for contributor in ContributorsDB.instance.db:
            print(contributor)
    def pickle(self, fileName='ContributorsDB'):
        '''Pickle list of stored Contributors.'''
        ContributorsDB.instance.pickle(fileName)
    def getFromPickle(self, fileName):
        '''Gets the Contributors database from a pickle file and 
        stores it in the singleton instance.'''
        ContributorsDB.instance.getFromPickle(fileName)