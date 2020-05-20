from Themes.relations import getRelatedByCitationOrAuthorship

class CitationGroup(object):
    """Defines a theme of discussion as the research
    of Contributors who cite each other and are cited
    by each other. After selecting a class representative,
    a Contributor is part of this group iff they cite
    or are cited by a contributor in this group,
    or if they are co-authors of contributors in this group."""
    alreadyGrouped = set() # in operator has O(1) for set. Nice.
    class AlreadyGroupedException(Exception):
        pass
    def __init__(classRepresentative):
        '''Uses the class representative to construct a 
        group of Contributors.'''
        if classRepresentative in CitationGroup.alreadyGrouped:
            raise AlreadyGroupedException
        self.contributors = \
            getRelatedByCitationOrAuthorship(classRepresentative)
    @classmethod
    def citationGroupFactory(cls):
        '''Searches the entire ContributorsDB for contributors
        and returns a set of citation groups.'''
        pass