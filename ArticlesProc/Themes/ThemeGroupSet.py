from Themes.ThemeGroup import ThemeGroup
from Utils.timeUtils import getStringTimestamp

class ThemeGroupSet(object):
    """A set of ThemeGroups."""
    def __init__(self, themeGroups):
        '''Initializes the ThemeGroupSet from a set of 
        ThemeGroupSet.'''
        self.themeGroups = themeGroups
    def pickle(self, fileName='ThemeGroupSet'):
        '''Pickles itself, maintaining dependency on the 
        ArticlesDB and ContributorsDB that were loaded
        when it was created.'''
        print(
            'pickling themeGroupSet with {} themeGroups...'
            .format(len(self.themeGroups))
            )
        with open(fileName + "_" + getStringTimestamp(), 'ab') as file:
            pickle.dump(
                set(themeGroup.getPicklable() for themeGroup in self.themeGroups),
                file
                )
        print("data dumped to", fileName + "_" + getStringTimestamp())
    @classmethod
    def unpickle(cls, fileName):
        '''Unpickle a ThemeGroupSet from a pickle file.'''
        dbfile = open(fileName, 'rb')
        db = pickle.load(dbfile)
        dbfile.close()
        return cls(set(
            ThemeGroup.getFromPicklable(picklable)
            for picklable in db
            ))