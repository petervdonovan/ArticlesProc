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

def getRelatedByCitationOrAuthorship(tg, contributor):
    '''Returns all other contributors related by 
    citation or authorship.'''
    return getRelated(tg, contributor, relations=[getCoAuthors, getRelatedByCitation])
def getRelatedByAuthorship(tg, contributor):
    '''Returns all other contributors related by 
    authorship.'''
    return getRelated(tg, contributor, relations=[getCoAuthors])

#def getRelated(contributor, relations=[], flattenedUpperLevels=set(), depth=0):
#    '''Returns all related Contributors (Contributors gotten through the relations)'''
#    # Get all related Contributors
#    combinedRelatedContribs = set()
#    for rel in relations:
#        combinedRelatedContribs = combinedRelatedContribs.union(rel(contributor))
#    # Make sure the contributor passed is in the set of related
#    # contributors
#    assert(contributor in combinedRelatedContribs)
#    # Alert the user if the recursion has gone too far
#    if depth % 10 == 0:
#        print("Depth: {}. {} contributors in upper levels ({}% of db) \
#        {} related.".format(
#            depth,
#            len(flattenedUpperLevels),
#            round(len(flattenedUpperLevels)/ContributorsDB().size()*100, 2),
#            len(combinedRelatedContribs)
#            )
#        )
#        #print(contributor)
#        #print("flattened upper levels:")
#        #for cb in flattenedUpperLevels:
#        #    print(cb)
#        #print("flattened upper levels.difference(set([contributor]))", 
#        #      flattenedUpperLevels.difference(set([contributor])))
#    combinedRelatedContribs = combinedRelatedContribs.difference(flattenedUpperLevels)
#    # Base case
#    if len(combinedRelatedContribs) == 0:
#        # In this case, the only related contributor might be the 
#        # contributor passed to this function -- but that 
#        # person should have been removed, because they were 
#        # already in flattened upper levels.
#        return combinedRelatedContribs
#    # Recursive case
#    flattenedUpperLevels = flattenedUpperLevels.union(combinedRelatedContribs)
#    for relatedContrib in combinedRelatedContribs:
#        new = getRelated(
#                relatedContrib, 
#                relations = relations,
#                flattenedUpperLevels=flattenedUpperLevels,
#                depth=depth+1
#                )
#        flattenedUpperLevels = flattenedUpperLevels.union(new)
#    return flattenedUpperLevels


def getRelated(tg, contributor, relations=[], depth=0):
    '''Returns all related Contributors (Contributors gotten through the relations)'''
    # Get all related Contributors
    combinedRelatedContribs = set()
    for rel in relations:
        combinedRelatedContribs = combinedRelatedContribs.union(rel(contributor))
    # Make sure the contributor passed is in the set of related
    # contributors
    assert(contributor in combinedRelatedContribs)
    # Alert the user if the recursion has gone too far
    if depth % 10 == 0 and depth > 0:
        print("Depth: {}. {} contributors collected ({}% of db) \
        {} related.".format(
            depth,
            len(tg.contributors),
            round(len(tg.contributors)/ContributorsDB().size()*100, 2),
            len(combinedRelatedContribs)
            )
        )
        #print(contributor)
        #print("flattened upper levels:")
        #for cb in flattenedUpperLevels:
        #    print(cb)
        #print("flattened upper levels.difference(set([contributor]))", 
        #      flattenedUpperLevels.difference(set([contributor])))
    ## Base case
    #if len(combinedRelatedContribs) == 0:
    #    # In this case, the only related contributor might be the 
    #    # contributor passed to this function -- but that 
    #    # person should have been removed, because they were 
    #    # already in flattened upper levels.
    #    return
    # Recursive case
    tg.contributors = tg.contributors | combinedRelatedContribs
    for relatedContrib in combinedRelatedContribs:
        if relatedContrib not in tg.contributors:
            getRelated(
                tg,
                relatedContrib, 
                relations = relations,
                depth=depth+1
                )