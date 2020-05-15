def binarySearch(self, desiredId, db, dbItemIdFunc, itemNearMatchFunc, itemMatchFunc, start=0, end=0):
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
        if itemNearMatchFunc(desiredId, dbItemIdFunc(db[start])):
            result = searchWithGuess(db, start, desiredId, 
                                   nearMatch=itemNearMatchFunc,
                                   match=itemMatchFunc
                                   )
            if result != -1:
                return result
        if name < dbItemIdFunc(db[0]):
            return -0.5
        return (end + start) / 2
    # Recursive case
    midpoint = int((start + end) / 2)
    if getItemIdFunc(db[midpoint]) <= desiredId:
        return binarySearch(
            desiredId, db, dbItemIdFunc, itemNearMatchFunc, itemMatchFunc, 
            start=midpoint, end=end
            )
    else:
        return self.search(
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
