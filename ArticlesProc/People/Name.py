import re

class Name(object):
    """Stores a name."""
    def __init__(self, givenName='', middleName = '', surname='', givenNameInitials=[], middleNameInitials=[]):
        '''Stores the person's given name and surname.'''
        self.givenNameInitials = givenNameInitials
        '''The first letter of every word in the given name.'''
        self.middleNameInitials = middleNameInitials
        '''The first letter of every word in the middle name.'''
        self.givenName = self.setGivenName(givenName)
        '''The given name (also called the first name).'''
        self.middleName = self.setMiddleName(middleName)
        '''The given name (also called the first name).'''
        self.surname = surname
        '''The surname (also called the last name).'''
    def getAsTuple(self):
        return (tuple(self.givenNameInitials), self.givenName, tuple(self.middleNameInitials), self.surname)
    def __hash__(self):
        return hash(self.getAsTuple())
    def __eq__(self, other):
        '''Returns whether this name is exactly identical to another name.'''
        return self.__hash__() == other.__hash__()
    @staticmethod
    def getInitialsFromString(str):
        return [match for match in re.findall(r'\b.', str)]
    def setGivenName(self, givenName):
        '''Sets the given name and updates initials as needed.'''
        self.givenName = givenName
        if givenName: # givenName is not an empty string
            givenNameInitials = Name.getInitialsFromString(givenName)
    def setMiddleName(self, middleName):
        '''Sets the middle name and updates initials as needed.'''
        self.middleName = middleName
        if middleName: # givenName is not an empty string
            middleNameInitials = Name.getInitialsFromString(middleName)
    def __str__(self):
        '''Returns the string representation of the name.'''
        nameStr = ''
        for namePart in self.getAsTuple():
            if type(namePart) == str:
                nameStr += namePart + ' '
        return nameStr.strip()


