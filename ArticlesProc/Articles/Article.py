class Article(object):
    """Describes both real and virtual articles."""
    id = 0
    def __init__(self, properties=None):
        '''Initializes an Article with a title and contributors that are 
        gotten from... somewhere'''
        self.articlesThatCiteThis = []
        '''The list of articles that cite this article.'''
        self.properties = {}
        if properties:
            self.properties = properties
        '''Dictionary containing found properties of the article -- to be filled in lazily as specific properties are requested.'''
        self.properties['id'] = Article.id
        '''The unique id of this article.'''
        Article.id += 1
    def getTitle(self):
        if not 'title' in self.properties:
            return None
        return self.properties['title']
    def __equals__(self, other):
        '''Checks if two articles are similar (and therefore should have same id)'''
        if isInstance(other, Article):
            return (self.title.upper().find(other.title.upper()) != -1
                    or other.title.upper().find(self.title.upper()) != -1) \
                    and set(self.contributors) == set(other.contributors)
        return False
    def addArticleThatCitesThis(self, additionalArticle):
        '''add an article to the list of articles that cite this article iff 
        that article is not already in the list'''
        for article in self.articlesThatCiteThis:
            #Check if same id article already exists
            if article.id == additionalArticle.id:
                return
        self.articlesThatCiteThis.append(additionalArticle)
    def getId(self):
        return self.properties['id']
    def setDiscipline(self, discipline):
        self.properties['discipline'] = discipline
    def getDiscipline(self):
        try:
            return self.properties['discipline']
        except:
            return None
