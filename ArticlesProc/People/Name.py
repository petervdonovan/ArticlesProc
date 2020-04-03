import re

class Name(object):
    """Stores a name."""
    def __init__(self, givenName='', middleName = '', surname='', 
                 givenNameInitials=[], middleNameInitials=[]):
        '''Stores the person's given name and surname.'''
        self.givenNameInitials = givenNameInitials
        '''The first letter of every word in the given name.'''
        self.middleNameInitials = middleNameInitials
        '''The first letter of every word in the middle name.'''
        self.setGivenName(givenName)
        '''The given name (also called the first name).'''
        self.setMiddleName(middleName)
        '''The given name (also called the first name).'''
        self.surname = surname
        '''The surname (also called the last name).'''
    def getAsTuple(self):
        return (tuple(self.givenNameInitials), self.givenName, 
                tuple(self.middleNameInitials), self.surname)
    def __hash__(self):
        return hash(self.getAsTuple())
    def __eq__(self, other):
        '''Returns whether this name is exactly identical to another name.'''
        return self.__hash__() == other.__hash__()
    def __lt__(self, other):
        '''Returns whether this name comes alphabetically before another name.'''
        return str(self) < str(other)
    def __le__(self, other):
        '''Returns whether this name comes alphabetically before another name,
        or if it is equal to the other name.'''
        return str(self) <= str(other)
    def __gt__(self, other):
        '''Returns whether this name comes alphabetically after another name.'''
        return str(self) > str(other)
    def __le__(self, other):
        '''Returns whether this name comes alphabetically after another name,
        or if it is equal to the other name.'''
        return str(self) >= str(other)
    def contains(self, other):
        '''Returns whether the other name could be the same name as this name.
        This will return true if not enough information is available to prove 
        that the two names are different.'''
        if self.surname != other.surname:
            return False
        if self.givenName and other.givenName and self.givenName != other.givenName:
            return False
        if self.givenName and other.givenName and self.givenName != other.givenName:
            return False
        if self.givenNameInitials and other.givenNameInitials and \
            not set(other.givenNameInitials).issubset(self.givenNameInitials):
            return False
        if self.middleNameInitials and other.middleNameInitials and \
            not set(other.givenNameInitials).issubset(self.givenNameInitials):
            return False

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
        if not self.middleName:
            middleNameStandIn = ''.join(initial + '.' for initial in self.middleNameInitials)
        else:
            middleNameStandIn = self.middleName
        if not self.givenName:
            givenNameStandIn = ''.join(initial + '.' for initial in self.givenNameInitials)
        else:
            givenNameStandIn = self.givenName
        out = self.surname
        if givenNameStandIn or middleNameStandIn: out +=  ','
        if givenNameStandIn: out += ' ' + givenNameStandIn
        if middleNameStandIn: out += ' ' + middleNameStandIn
        return out


