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
        self.id = Article.id
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
        return self.id
    def setGroup(self, groupType, groupName):
        '''Records that this Article is a member of groupName, which is a kind of groupType.
        For instance, if groupType == "discipline" and groupName == "mathematics", then this 
        Article is a member of the "mathematics" Articles group, which is a kind of discipline.'''
        # Sets a key-value pair inside the groups dictionary in the properties dictionary.
        # The key is the type of group, and the value is the group. For instance, if articles are
        # to be grouped by discipline, and the discipline of this Article is mathematics, then
        # the key is "discipline" and the value is "mathematics".
        if not 'groups' in self.properties:
            self.properties['groups'] = {}
        #if not groupType in self.properties['groups']:
        #    self.properties['groups'][groupType] = []
        #if not groupName in self.properties['groups'][groupType]:
        #    self.properties['groups'][groupType].append(groupName)
        self.properties['groups'][groupType] = groupName
    def getIsMemberOfGroup(self, groupType, groupName):
        '''Returns whether or not this Article is a member of a certain grouping of Articles.'''
        if not 'groups' in self.properties or not groupType in self.properties['groups']:
            return False
        return groupName in self.properties['groups']['groupType']
    def getGroup(self, groupType):
        '''Returns which group[s] this Article falls under. For instance, if the groupType
        is "discipline", then this could return None or "biology" or "math".'''
        if not 'groups' in self.properties or not groupType in self.properties['groups']:
            return None
        return self.properties['groups'][groupType]
