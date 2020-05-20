from Utils.timeUtils import getStringTimestamp
import pickle

def binarySearch(desiredId, db, dbItemIdFunc, itemNearMatchFunc, itemMatchFunc, start=0, end=0):
    '''Returns the index of the equivalent contributor
    in the database. If there is no equivalent 
    contributor, returns a float index indicating where
    the new contributor would belong relative to the others,
    if it were in the database.
    (Uses binary search as of 4/4/2020)'''
    # Branches intended to be important only in the inital call
    if len(db) == 0:
        return -0.5
    if end == 0: end = len(db)
    # Base case
    if end - start == 1:
        if itemNearMatchFunc(desiredId, db[start]):
            result = searchWithGuess(db, start, desiredId, 
                                   nearMatch=itemNearMatchFunc,
                                   match=itemMatchFunc
                                   )
            if result != -1:
                return result
        if desiredId < dbItemIdFunc(db[0]):
            return -0.5
        return (end + start) / 2
    # Recursive case
    midpoint = int((start + end) / 2)
    if dbItemIdFunc(db[midpoint]) <= desiredId:
        return binarySearch(
            desiredId, db, dbItemIdFunc, itemNearMatchFunc, itemMatchFunc, 
            start=midpoint, end=end
            )
    else:
        return binarySearch(
            desiredId, db, dbItemIdFunc, itemNearMatchFunc, itemMatchFunc, 
            start=start, end=midpoint)
    
def searchWithGuess(
    list, guess, searchFor,
    radius=0, 
    nearMatch=lambda search, itemInList: True,
    match=lambda search, itemInList: search==itemInList
    ):
    '''Returns the index of the item nearest to the index
    given by guess that matches searchFor. Returns -1 if 
    there exists a distance d from the guess such that the items
    found in the list are not near matches to searchFor
    (i.e., nearMatch returns False) and such that all items 
    closer to the guess than that distance are not matches.'''
    # Base case: Something found at radius distance
    # away from guess
    try:
        if match(searchFor, list[guess - radius]):
            return guess - radius
    except IndexError: pass
    try:
        if match(searchFor, list[guess + radius]):
            return guess + radius
    except IndexError: pass
    # Base case: nothing found
    if (
            guess - radius < 0 or 
            not nearMatch(searchFor, list[guess - radius])
        ) and \
        (
            guess + radius >= len(list) or 
            not nearMatch(searchFor, list[guess + radius])
        ):
        return -1
    # Recursive case: There still could be a matching
    # item in the list nearby.
    return searchWithGuess(list, guess, searchFor, 
                           radius=radius+1, 
                           nearMatch=nearMatch, 
                           match=match)

class DB(object):
    '''Generalized class for rapid lookup. Requirement: items in the db
    must have some method add, that allows the one item to be combined
    into another item, providing additional information about the
    modeled entity that is represented by both items.'''
    def __init__(self, dbItemIdFunc, itemNearMatchFunc, itemMatchFunc):
        '''Create database. The database must know how to 
        a) get ID of an item, b) get whether 2 items nearly
        match and are likely to have similar IDs, and c) get whether
        2 items match (a function that can be independent of ID).
        The term ID is used loosely, to simply mean any piece of
        identifying information, and it is possible for the ID to
        not be unique.
        itemNearMatchFunc and itemMatchFunc are functions of (the 
        identifying characteristic used to search for the item) (arg1)
        and (the item itself) (arg2).'''
        self.db = list()
        self.dbItemIdFunc = dbItemIdFunc
        self.itemNearMatchFunc = itemNearMatchFunc
        self.itemMatchFunc = itemMatchFunc
    def search(self, desiredId):
        '''Returns the index of the item of the desired ID
        in the database. If there is no such item,
        returns a float index indicating where
        the new contributor would belong relative to the others,
        if it were in the database.
        (Theta class is log(n) where n is the database length.)'''
        return binarySearch(
            desiredId, self.db, 
            self.dbItemIdFunc, self.itemNearMatchFunc, self.itemMatchFunc
            )
    def get(self, desiredId):
            '''Gets the item who has this ID. If no such 
            item exists, return None.'''
            idx = self.search(desiredId)
            if idx != int(idx):
                return None
            return self.db[int(idx)]
    def add(self, item):
        '''Adds a new item to the database, or combines
        it with an existing item if possible.'''
        idx = self.search(self.dbItemIdFunc(item))
        if int(idx) == idx:
            if item is not self.db[idx]:
                self.db[idx].add(item)
        else:
            idx += 1
            idx = int(idx)
            self.db.insert(idx, item)
    def pickle(self, fileName='db'):
        '''Pickles list of items in DB to a file at location and name
        given by fileName.'''
        dbfile = open(fileName + "_" + getStringTimestamp(), 'ab')
        pickle.dump(self.db, dbfile)
        print("data dumped to", fileName + "_" + getStringTimestamp())
        dbfile.close()
    def getFromPickle(self, fileName):
        '''Gets the database from a pickle file and replaces the current 
        list of items in the db with the items in the pickled list.'''
        dbfile = open(fileName, 'rb')
        db = pickle.load(dbfile)
        self.db = db
    def clear(self):
        '''Clears all items from DB and starts afresh with an empty set.'''
        self.db = list()