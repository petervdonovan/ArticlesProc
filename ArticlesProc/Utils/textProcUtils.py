import re
def stripMarkup(text):
    '''Takes the string form of some HTML or XML and returns it with markup removed.'''
    str = ' '.join(
            [piece.strip() for piece in re.split(r'<[^>]*>', text)]
        )
    str = re.sub(r'&amp;', '&', str)
    return str
def replaceWhiteSpaceWithSpace(text):
    '''Returns the text with all whitespace (carriage returns, etc.) replaced with 
    just a space.'''
    return re.sub(r'\s', ' ', text)
def escapeDoubleQuotes(text):
    '''Inserts a \ before any straight double quotes.'''
    return re.sub(r'"', r'\"', text)
def capitalizeFirstLetterEachWord(text):
    '''Capitalizes the first letter of each word.'''
    return ''.join(
        [piece.capitalize() for piece in re.split(r'\b', text)]
        )