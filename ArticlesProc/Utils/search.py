
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
