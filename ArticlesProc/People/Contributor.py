from Articles.ArticleSet import ArticleSet
from People.ContributorsDB import ContributorsDB
from People.Name import Name

def sameContributor(name, otherName):
    '''Returns True iff two names correspond to the same Contributor.'''
    if not ContributorsDB().get(name):
        Contributor.make(name)
    if not ContributorsDB().get(otherName):
        Contributor.make(otherName)
    return ContributorsDB().get(name) == ContributorsDB().get(otherName)
class Contributor(object):
    """Describes a person who contributes to one
    or more Articles."""
    def __init__(self, name, articles=None):
        '''Create a contributor, who shall be 
        identified by his or her name.
        Do not initialize using this method unless 
        the Contributor is not intended to be registered 
        in the database. If the contributor is to be 
        registered, use the factory method 
        Contributor.register'''
        self.name = name
        '''The Name of the contributor.'''
        if articles is not None:
            self.articles = articles
            '''The articles published under the name
            of this Contributor.'''
        else:
            self.articles = ArticleSet(set())
    @classmethod
    def make(cls, name, articles=None):
        '''Factory method to create a Contributor and 
        register it in the database. If the Contributor
        already exists, then merely update its 
        information. This is the only way to get the 
        version of the Contributor with the most updated 
        information.'''
        ContributorsDB().registerContributor(
            cls(name, articles=articles)
            )
        return ContributorsDB().get(name)
    def addArticle(self, article):
        '''Add an article that was published under 
        the name of this Contributor.'''
        self.articles = self.articles + ArticleSet(set([article]))
    def add(self, other):
        '''Combine the information of this Contributor with
        that of another (presumably because it turns out 
        that they are the same person).'''
        self.articles = self.articles + other.articles
    def getArticles(self):
        '''Returns the Articles attributed to this Contributor.'''
        return self.articles
    def isEquivalent(self, other):
        return (self.name.contains(other.name) or 
                other.name.contains(self.name))
    def __ne__(self, other):
        return not self == other
    def __str__(self):
        return str(self.name) + \
            " with {0} articles".format(len(self.articles))
