import re
from Citations.citationRegexes import styleGuideRegexes, \
                                      nameListRegexes, nameRegexes, \
                                      getParts
from Utils.regexes import regexes
from People.Name import Name

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
                styleGuides.append(styleGuide)
        return styleGuides
    def getNameList(self):
        '''Returns the list of contributor names from the citation, if
        such a list exists.'''
        matches = []
        for nameListType in nameListRegexes:
            match = re.match(nameListRegexes[nameListType], self.raw)
            if match:
                matches.append((nameListType, match))
        longestMatch = ('', None)
        for match in matches:
            if not longestMatch[1] or len(match[1].group(0)) > len(longestMatch[1].group(0)):
                longestMatch = match
        return longestMatch
    def getNames(self):
        '''Returns a list of names that appear in the citation.'''
        # Get namelist
        nameList = self.getNameList()
        # get the upper-level nameregexes that appear in the namelist
        if not nameList[0]: return []
        names = []
        nameRegexesInNameList = [
            nameRegex for nameRegex in nameRegexes 
            if nameRegexes[nameRegex] in nameListRegexes[nameList[0]]
            ]
        try:
            nameRegexesInNameList.remove('name')
        except: pass
        try:
            nameRegexesInNameList.remove('initial')
        except: pass
        # get matches with those regexes
        nl = nameList[1].group(0)
        while len(nl) > 1:
            for regex in nameRegexesInNameList:
                match = re.match(nameRegexes[regex], nl)
                if match:
                    names = [name for name in names if name[1] not in match.group(0)]
                    if not any(match.group(0) in name[1] for name in names):
                        names.append((regex, match.group(0)))
                    nl = ' ' + nl.replace(match.group(0), '')
            nl = nl[1:]
        # Get namepartses
        namePartses = [getParts(name[0], name[1]) for name in names]
        # convert namepartses in to Names and return
        return [
            Name(
                surname=parts['surname'], 
                givenName=parts['givenName'], 
                middleName=parts['middleName'],
                givenNameInitials=parts['givenNameInitials'],
                middleNameInitials=parts['middleNameInitials']
                ) 
            for parts in namePartses
            ]
    def getYear(self):
        return [groups[0] for groups in re.findall(regexes['citable year'], self.raw)]