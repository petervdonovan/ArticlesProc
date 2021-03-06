from Articles.ArticleSet import ArticleSet
from People.ContributorsDB import ContributorsDB
from People.Name import Name
from Articles.ArticlesDB import ArticlesDB

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
        self.articles = set(
            article.getId() for article in 
            (self.getArticles() + ArticleSet(set([article]))).articles
            )
    def add(self, other):
        '''Combine the information of this Contributor with
        that of another (presumably because it turns out 
        that they are the same person).'''
        self.articles = set(
            article.getId() for article in 
            (self.getArticles() + other.getArticles()).articles
            )
    def getArticles(self):
        '''Returns the Articles attributed to this Contributor.'''
        if type(self.articles) == ArticleSet: # Backwards compatibility :(
            for article in self.articles.articles:
                ArticlesDB().add(article)
                if ArticlesDB().get(article.getId()) is None:
                    print(article)
                    print(ArticlesDB.instance.db)
                assert(ArticlesDB().get(article.getId()) is not None)
            #for article in self.articles.articles:
            #    if ArticlesDB().get(article.getId()) is None:
            #        try:
            #            print("none article inside getArticles... id", article.getId(), "path", article.getFullPath())
            #        except AttributeError:
            #            print("none article inside getArticles... id", article.getId())
            self.articles = set(article.getId() for article in self.articles.articles)
        return ArticleSet(
            set(
                ArticlesDB().get(id) for id in self.articles
                )
            )
    def isEquivalent(self, other):
        return (self.name.contains(other.name) or 
                other.name.contains(self.name))
    def __ne__(self, other):
        return not self == other
    def __str__(self):
        return str(self.name) + \
            " with {0} articles".format(len(self.articles))
