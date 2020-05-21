from Articles.RealArticle import RealArticle
from People.ContributorsDB import ContributorsDB

def getCoAuthors(contributor):
    '''Gets the Contributors related to the given
    Contributor by the co-author relation.'''
    articles = contributor.getArticles()
    return set(
        contributor 
        for article in articles
        for contributor in article.getContributors() 
        )
def getRelatedByCitation(contributor):
    '''Gets the Contributors related to the given
    Contributor by the citation relation.'''
    articles = contributor.getArticles()
    return \
        set(
        contributor
        for myArticle in articles
        for citingArticle in myArticle.getArticlesThatCiteThis()
        for contributor in citingArticle.getContributors()
        ) | \
        set(
        contributor
        for myArticle in articles
        for citedArticle in myArticle.getArticlesThatThisCites()
        for contributor in citedArticle.getContributors()
        )

def getRelatedByCitationOrAuthorship(contributor):
    '''Returns all other contributors related by 
    citation or authorship.'''
    return getRelated(contributor, relations=[getCoAuthors, getRelatedByCitation])
def getRelatedByAuthorship(contributor):
    '''Returns all other contributors related by 
    authorship.'''
    return getRelated(contributor, relations=[getCoAuthors])

def getRelated(contributor, relations=[], flattenedUpperLevels=set(), depth=0):
    '''Returns all related Contributors (Contributors gotten through the relations)'''
    # Get all related Contributors
    combinedRelatedContribs = set()
    for rel in relations:
        combinedRelatedContribs = combinedRelatedContribs.union(rel(contributor))
    # Make sure the contributor passed is in the set of related
    # contributors
    assert(contributor in combinedRelatedContribs)
    # Alert the user if the recursion has gone too far
    if depth % 10 == 0:
        print("Depth: {}. {} contributors in upper levels ({}% of db) \
        {} related.".format(
            depth,
            len(flattenedUpperLevels),
            round(len(flattenedUpperLevels)/ContributorsDB().size()*100, 2),
            len(combinedRelatedContribs)
            )
        )
        #print(contributor)
        #print("flattened upper levels:")
        #for cb in flattenedUpperLevels:
        #    print(cb)
        #print("flattened upper levels.difference(set([contributor]))", 
        #      flattenedUpperLevels.difference(set([contributor])))
    # Base case
    if len(combinedRelatedContribs.difference(flattenedUpperLevels)) == 1:
        # In this case, the only related contributor is the 
        # contributor passed to this function. This case 
        # prevents infinite recursion where the argument 
        # never changes.
        return combinedRelatedContribs
    # Recursive case
    allContributors = set()
    for relatedContrib in combinedRelatedContribs.difference(flattenedUpperLevels):
        allContributors = allContributors.union(
            getRelated(
                relatedContrib, 
                relations = relations,
                flattenedUpperLevels=flattenedUpperLevels.union(combinedRelatedContribs).union(allContributors),
                depth=depth+1
                )
            )
    return allContributors