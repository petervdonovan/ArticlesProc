from Utils.search import searchWithGuess

class ContributorsDB:
    """A singleton contributors registration system, documenting
    all known contributors (people who write Articles) in one 
    place."""
    class __ContributorsDB:
        '''The private single instance of the Contributors 
        registration system.'''
        def __init__(self):
            '''Create the starting list of known contributors.'''
            # Alphabetized by name for rapid searching
            self.db = list()
            '''A list of Contributors.'''
        def search(self, name, start=0, end=0):
            '''Returns the index of the equivalent contributor
            in the database. If there is no equivalent 
            contributor, returns a float index indicating where
            the new contributor would belong relative to the others,
            if it were in the database.
            (Uses binary search as of 4/4/2020)'''
            if len(self.db) == 0:
                return -0.5
            if end == 0: end = len(self.db)
            # Base case
            if end - start == 1:
                #print('self.db:_______________________________________')
                #for contributor in self.db:
                #    print(contributor)
                if name == self.db[start].name:
                    result = searchWithGuess(self.db, start, name, 
                                           nearMatch=(
                                               lambda search, itemInList:
                                               search == itemInList.name
                                               ),
                                           match=(
                                               lambda search, itemInList: 
                                               search.contains(itemInList.name) or \
                                                   itemInList.name.contains(search)
                                               )
                                           )
                    if result != -1:
                        return result
                if name < self.db[0].name:
                    return -0.5
                return (end + start) / 2
            # Recursive case
            midpoint = int((start + end) / 2)
            if self.db[midpoint].name <= name:
                return self.search(name, start=midpoint, 
                                   end=end)
            else:
                return self.search(name, start=start, 
                                   end=midpoint)
        def add(self, contributor):
            '''Adds a new Contributor to the database, or combines
            it with an existing Contributor if possible.'''
            idx = self.search(contributor.name)
            if int(idx) == idx:
                self.db[idx].add(contributor)
            else:
                idx +=1
                idx = int(idx)
                self.db.insert(idx, contributor)
        def get(self, name):
            '''Gets the Contributor who has this name. If no such 
            Contributor exists, return None.'''
            idx = self.search(name)
            if idx != int(idx):
                return None
            return self.db[int(idx)]
    instance = None
    def __init__(self):
        '''Create instance of the singleton.'''
        if ContributorsDB.instance is None:
            ContributorsDB.instance = ContributorsDB.__ContributorsDB()
    def registerContributor(self, contributor):
        '''Adds a Contributor to the database as needed and returns 
        the result of a search for the Contributor. This search result
        may have more complete information about the person described.'''
        ContributorsDB.instance.add(contributor)
        return self.get(contributor.name)
    def registerArticle(self, article):
        '''Stores an Article in this database, under the names of 
        the contributors to the Article.'''
        contributors = article.getContributors()
        for contributor in contributors:
            if contributor.name.surname == 'Almeida':
                print(article)
            contributor.addArticle(article)
            self.registerContributor(contributor)
    def get(self, name):
        result = ContributorsDB.instance.get(name)
        return result
    def print(self):
        for contributor in ContributorsDB.instance.db:
            print(contributor)