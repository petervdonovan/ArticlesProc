from People.Contributor import sameContributor
from People.ContributorsDB import ContributorsDB
from People.Name import Name

class Article(object):
    """Describes both real and virtual articles."""
    id = 0
    def __init__(self, properties=None, contributors=None, publicationYear=None):
        '''Initializes an Article with a title and contributors that are 
        gotten from... somewhere'''
        self.properties = dict()
        if properties:
            self.properties = properties
        '''Dictionary containing found properties of the article -- to be filled in lazily as specific properties are requested.'''
        if not 'id' in self.properties:
            self.properties['id'] = Article.id
            '''The unique id of this article.'''
        if contributors is not None:
            self.properties['contributors'] = contributors
        if publicationYear is not None:
            self.properties['publicationYear'] = publicationYear
        Article.id += 1
    def __str__(self):
        return (
            'Article #' + str(self.getId()) + ', published in ' + 
            str(self.getPublicationYear()) + ' by ' + 
            ', '.join(str(contributor) for contributor in self.getContributors())
            )
    def getTitle(self):
        '''Gets the title of this article, if the title is known.'''
        if not 'title' in self.properties:
            return None
        return self.properties['title']
    def getPublicationYear(self):
        '''Gets the publication year of this article, if the publication year is known.'''
        if not 'publicationYear' in self.properties:
            return None
        return self.properties['publicationYear']
    def contributorsAreSubsetOfOtherContributors(self, other):
        '''Returns True iff this article's contributors are a subset of another 
        article's contributors, without registering new Contributors unnecessarily.'''
        if not self.getContributorNames(): return True
        if not other.getContributorNames(): return False
        for name in self.getContributorNames():
            found = False
            for otherName in other.getContributorNames():
                if sameContributor(name, otherName):
                    found = True
                    break
            if not found:
                return False
        return True
    def contributorsAreOtherContributors(self, other):
        '''Returns True iff this Article has the same Contributors as another Article,
        without registering new Contributors unnecessarily.'''
        return self.contributorsAreSubsetOfOtherContributors(other) and \
              other.contributorsAreSubsetOfOtherContributors(self)
    def isEquivalent(self, other):
        '''Checks if two articles are similar (and therefore should have same id)'''
        if isinstance(other, Article):
            # Check if contributor lists are consistent
            if self.getContributorNames() and other.getContributorNames() and (
                not (
                self.contributorsAreSubsetOfOtherContributors(other) or 
                self.getEtAl() and self.contributorsAreSubsetOfOtherContributors(other) or
                other.getEtAl() and other.contributorsAreSubsetOfOtherContributors(self)
                ) or
                not (
                    sameContributor(self.getPrimaryContributorName(), other.getPrimaryContributorName())
                )
                ):
                return False
            # Check if publication years are consistent
            if (
                self.getPublicationYear() is not None and 
                other.getPublicationYear() is not None and
                self.getPublicationYear() != other.getPublicationYear()
                ):
                return False
        return True
    def getEtAl(self):
        '''Returns whether there may be other Contributors not included in
        the Contributors list that is returned by self.getContributors()'''
        if not self.getSelfCitation():
            return False
        return 'et al' in self.getSelfCitation().raw.lower()
    def getSelfCitation(self):
        '''Get the citation from which information about this Article came.'''
        if not 'citation' in self.properties:
            return None
        return self.properties['citation']
    def addArticleThatCitesThis(self, additionalArticle):
        '''add an article to the list of articles that cite this article iff 
        that article is not already in the list'''
        if not 'articlesThatCiteThis' in self.properties:
            self.properties['articlesThatCiteThis'] = []
        for article in self.properties['articlesThatCiteThis']:
            #Check if same id article already exists
            if article.id == additionalArticle.id:
                return
        self.properties['articlesThatCiteThis'].append(additionalArticle)
    def getId(self):
        return self.properties['id']
    def setDiscipline(self, discipline):
        self.properties['discipline'] = discipline
    def getDiscipline(self):
        try:
            return self.properties['discipline']
        except:
            return None
    def add(self, other):
        '''Returns the combination of the contents of two Articles.
        TODO: REVIEW IMPLEMENTATION FOR EQUALITIES THAT ARE NOT RECOGNIZED AS 
        EQUALITIES AND FOR UNHANDLED DATA TYPES.'''
        properties = dict()
        for prop in self.properties:
            if prop not in other.properties:
                properties[prop] = self.properties[prop]
            elif self.properties[prop] == other.properties[prop]:
                properties[prop] = self.properties[prop]
            else:
                if type(self.properties[prop]) == set:
                    properties[prop] = set(self.properties[prop]).union(other.properties[prop])
                elif type(self.properties[prop]) == list:
                    properties[prop] = self.properties[prop] + [
                        otherItem for otherItem in other.properties[prop] 
                        if otherItem not in self.properties[prop]
                        ]
                else:
                    properties[prop] = self.properties[prop]
        self.properties = properties
    def getSaveableData(self):
        return self.properties
    @classmethod
    def initFromRaw(cls, raw):
        if type(raw) is dict:
            return cls(properties=raw)
        else:
            raise TypeError('The parameter \'raw\' must be a dictionary.')
    def getContributors(self):
        '''Returns the people who contributed to this Article.'''
        if 'contributors' in self.properties:
            return [ContributorsDB().get(name) for name in self.properties['contributors']]
        else:
            return None
    def getContributorNames(self):
        '''Return the names of the Contributors to this Article.'''
        names = []
        for contributor in self.getContributors():
            names.append(contributor.name)
            return names
    def getPrimaryContributor(self):
        try:
            return self.getContributors()[0]
        except IndexError:
            return None
        except TypeError:
            return None
    def getPrimaryContributorName(self):
        '''Returns the name of the first contributor listed in the source from
        which this Article was derived.'''
        try:
            name = self.getContributorNames()[0]
            assert(type(name) == Name)
            return name
        except IndexError:
            print(type(self))
            return None
        except TypeError:
            print(type(self))
            return None
    def print(self):
        print('{}: ARTICLE PUBLISHED IN {}'.format(self.id, self.getPublicationYear()))
        if self.getContributors():
            print('Contributors:')
            for contributor in self.getContributors():
                print(contributor)
        print()