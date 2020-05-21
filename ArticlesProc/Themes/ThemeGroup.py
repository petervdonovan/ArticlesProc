from People.ContributorsDB import ContributorsDB
from Articles.ArticlesDB import ArticlesDB

from Articles.ArticlesDB import ArticlesDB
from People.ContributorsDB import ContributorsDB
import matplotlib.pyplot as plt
import time

class AlreadyGroupedException(Exception):
    pass

class ThemeGroup(object):
    """A group of related Articles and Contributors."""
    alreadyGrouped = set() # in operator has O(1) for set. Nice.
    def __init__(self, classRepresentative, getRelatedContributorsFunction, nonIntersecting=True):
        '''Uses the class representative to construct a 
        group of Contributors.'''
        if classRepresentative is not None:
            if nonIntersecting:
                if classRepresentative in ThemeGroup.alreadyGrouped:
                    raise AlreadyGroupedException
            self.contributors = getRelatedContributorsFunction(classRepresentative)
            self.articles = set(
                article
                for contributor in self.contributors
                for article in contributor.getArticles()
                )
            ThemeGroup.alreadyGrouped = ThemeGroup.alreadyGrouped.union(self.contributors)
    def getContributorsCount(self):
        '''Returns the number of contributors.'''
        return len(self.contributors)
    def getArticlesCount(self):
        '''Returns the number of articles.'''
        return len(self.articles)
    def getPicklable(self):
        '''Returns a tuple with names and ids, not 
        Article or Contributor objects.'''
        contributorNames = set(
            contributor.getName() for contributor in self.contributors
            )
        articleIds = set(article.getId() for article in self.articles)
        return (contributorNames, articleIds)
    @classmethod
    def getFromPicklable(cls, picklable):
        '''Factory method that returns a ThemeGroup from the pickled
        version of itself. Precondition: ArticlesDB and 
        ContributorsDB initialized.'''
        tg = cls(None, None)
        tg.contributors = set(ContributorsDB().get(name) for name in picklable[0])
        tg.articles = set(ArticlesDB().get(id) for id in picklable[1])
    @staticmethod
    def setFactory(cls):
        '''Returns a set of CitationGroups. Requirement:
        ArticlesDB and ContributorsDB already loaded with
        the appropriate items.'''

        # For progress updates
        contributorCount = 0
        groupsCount = 0
        numContributors = ContributorsDB().size()
        startTime = time.time()
        contributorCounts = []
        articleCounts = []
        # Gather the data
        citationGroups = set()
        for contributor in ContributorsDB():
            if contributorCount > 0 and contributorCount % 10 == 0:
                print(
                    'Contributor #{} of {} ({}% complete), with {} groups created. Elapsed time {} seconds.'
                    .format(
                        contributorCount,
                        numContributors,
                        round(contributorCount / numContributors * 100),
                        groupsCount,
                        time.time() - startTime
                    )
                )
            try:
                group = cls(contributor) # throws AlreadyGroupedException
                citationGroups.add(group) # this is the important part
                # The rest is progress monitoring
                articleCounts.append(group.getArticlesCount())
                contributorCounts.append(group.getContributorsCount())
                groupsCount += 1
            except AlreadyGroupedException:
                pass
            contributorCount += 1
        try:
            plt.hist(contributorCounts)
            plt.show()
            plt.hist(articleCounts)
            plt.show()
            plt.scatter(contributorCounts, articleCounts)
            plt.show()
        except:
            print("creating diagrams failed.")
        return citationGroups