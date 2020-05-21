from Themes.relations import getRelatedByAuthorship
from Themes.ThemeGroup import ThemeGroup

class AuthorshipGroup(ThemeGroup):
    """Defines a theme of discussion as the research
    of Contributors co-author some of the same Articles. 
    After selecting a class representative,
    a Contributor is part of this group iff they 
    are co-authors with contributors in this group."""
    def __init__(self, classRepresentative):
        super().__init__(classRepresentative, getRelatedByAuthorship)
    @classmethod
    def setFactory(cls):
        return super().setFactory(cls)