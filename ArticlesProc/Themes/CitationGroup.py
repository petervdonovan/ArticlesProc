from Themes.relations import getRelatedByCitationOrAuthorship
from Themes.ThemeGroup import ThemeGroup, AlreadyGroupedException

class CitationGroup(ThemeGroup):
    """Defines a theme of discussion as the research
    of Contributors who cite each other and are cited
    by each other. After selecting a class representative,
    a Contributor is part of this group iff they cite
    or are cited by a contributor in this group,
    or if they are co-authors of contributors in this group."""
    def __init__(self, classRepresentative):
        super().__init__(classRepresentative, getRelatedByCitationOrAuthorship)
    @classmethod
    def setFactory(cls):
        return super().setFactory(cls)
    