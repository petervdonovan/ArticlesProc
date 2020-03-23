import re
from Citations.citationRegexes import styleGuideRegexes, nameListRegexes, nameRegexes

class Citation(object):
    """Store and process string references (sources cited in articles)"""
    def __init__(self, raw):
        '''Stores the raw string of this citation.'''
        self.raw = raw
    def __str__(self):
        '''Returns the string representation of this Citation.'''
        return self.raw
    def getStyleGuides(self):
        '''Returns a list of possible style guides for this citation.'''
        styleGuides = []
        for styleGuide in styleGuideRegexes:
            if re.match(styleGuideRegexes[styleGuide], self.raw):
                #print(re.match(styleGuideRegexes[styleGuide], self.raw))
                styleGuides.append(styleGuide)
        return styleGuides
    def getNameList(self):
        '''Returns the list of contributor names from the citation, if such a list exists.'''
        matches = []
        for nameListType in nameListRegexes:
            match = re.match(nameListRegexes[nameListType], self.raw)
            if match:
                print('match found with', nameListType)
                matches.append(match.group(0))
        longestMatch = ''
        for match in matches:
            if len(match) > len(longestMatch):
                longestMatch = match
        print('    ', self.raw[:100])
        return longestMatch
    def getNames(self):
        '''Returns a list of names that appear in the citation.'''
        print('The raw at the beginning of getNames is', self.raw)
        names = []
        for nameType in nameRegexes:
            print(nameType, self.raw[:30])
            matches = re.findall(nameRegexes[nameType], self.raw)
            if matches:
                for match in matches:
                    names.append(match)
        print('The raw at the end of getNames is', self.raw)
        return names