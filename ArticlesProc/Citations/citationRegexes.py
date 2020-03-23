from Utils.regexes import regexes
# Names regexes
nameRegexes = {}
nameRegexes['surname, given name'] = r'(' + regexes['name'] + r', ' + regexes['name'] + r')'
nameRegexes['surname, given name middle name'] = r'(' + nameRegexes['surname, given name'] + r' ' + regexes['name'] + r')'
nameRegexes['surname, given name and optionally middle name'] = r'(' + nameRegexes['surname, given name'] + r'( ' + regexes['name'] + r')?)'
nameRegexes['surname, given name and optionally middle initial'] = r'(' + nameRegexes['surname, given name'] + r' ' + regexes['initial'] + '\.( ' + regexes['initial'] + r'\b){0,2})'
nameRegexes['given name optionally middle name surname'] = r'(' + regexes['name'] + r' ' + regexes['name'] + r' (' + regexes['name'] + r')?)'
nameRegexes['given name optionally middle initial surname'] = r'(' + regexes['name'] + r' (' + regexes['initial'] + '\. )?' + regexes['name'] + r')'
nameRegexes['surname, first initial'] = r'(' + regexes['name'] + r', ' + regexes['initial'] + '\.)'
nameRegexes['surname, initials'] = r'(' + regexes['name'] + r' ' + regexes['initial'] + '{1,3}\b)'
nameRegexes['surname, initials with dot optional space optional'] = r'(' + regexes['name'] + r',? (\.? ?' + regexes['initial'] + '){1,3}((\.)|\b))'
nameRegexes['surname, initials with dot'] = r'(' + regexes['name'] + r',?( ' + regexes['initial'] + '\.){1,3})'
nameRegexes['surname, initials with dot space optional'] = r'(' + regexes['name'] + r',? ?( ?' + regexes['initial'] + '\.){1,3})'
nameRegexes['surname initial(s)'] = r'(' + regexes['name'] + r' ' + regexes['initial'] + '(' + regexes['initial'] + '){0,2}\b)'
nameRegexes['surname, initial(s) no dots no spaces'] = r'(' + regexes['name'] + r',? [^\s0-9a-z\.,‘"\'’“”\(\)\[\]]([^\s0-9a-z\.,‘"\'’“”\(\)\[\]]){0,2}\b)'
nameRegexes['initials with dot space surname'] = r'((' + regexes['initial'] + '\. ){0,3}' + regexes['name'] + r')'
nameRegexes['initials with dot surname'] = r'((' + regexes['initial'] + '\. ?){0,3} ' + regexes['name'] + r')'
# Name lists
nameListRegexes = {}
nameListRegexes['ama name list'] = r'(' + nameRegexes['surname initial(s)'] + r'(, ' + nameRegexes['surname initial(s)'] + r')*?((\.)|(, et al.)))'
nameListRegexes['apa name list'] = r'(' + nameRegexes['surname, initials with dot optional space optional'] + r'((, ' + nameRegexes['surname, initials with dot optional space optional'] + r')*' + \
        r',? (&|((\.){3,4})|…) ' + nameRegexes['surname, initials with dot optional space optional'] + r')?)'
nameListRegexes['chicago/turabian name list'] = r'(' + r'(((' + nameRegexes['surname, given name and optionally middle name'] + r')|(' + \
    nameRegexes['surname, given name and optionally middle initial'] + r'))((, (' + nameRegexes['given name optionally middle name surname'] + \
    r'|' + nameRegexes['given name optionally middle initial surname'] + r'))*?,? ((and)|e|y) ' + r'(' + \
    nameRegexes['given name optionally middle name surname'] + r'|' + nameRegexes['given name optionally middle initial surname'] + r')' + r')?((\.)|,)' + r')' \
    + r'|' + nameRegexes['surname, given name and optionally middle initial'] + r')'
nameListRegexes['harvard: australian name list'] = r'(' + nameRegexes['surname, initial(s) no dots no spaces'] + r'((, ' + nameRegexes['surname, initial(s) no dots no spaces'] + r')*' + \
    r' & ' + nameRegexes['surname, initial(s) no dots no spaces'] + r')?)'

nameListRegexes['mla name list'] = r'((' + nameRegexes['surname, given name and optionally middle name'] + r'((, et al)?)|' + \
        nameRegexes['surname, given name and optionally middle initial'] + r'(, et al)?)' + \
        r'(, (((and)|e|y) )?' + nameRegexes['given name optionally middle initial surname'] + r')?' + r'\.)'
nameListRegexes['harvard name list'] = r'(' + nameRegexes['surname, initials with dot'] + r'(, ' + \
         nameRegexes['surname, initials with dot'] + r')*( ((and)|e|y) ' + nameRegexes['surname, initials with dot'] + \
         r')?( et al.)?' + r')'
#nameListRegexes['chicago/turabian name list no end on dot requirement'] = r'(' + r'(((' + nameRegexes['surname, given name and optionally middle name'] + r')|(' + \
#    nameRegexes['surname, given name and optionally middle initial'] + r'))((, (' + nameRegexes['given name optionally middle name surname'] + \
#    r'|' + nameRegexes['given name optionally middle initial surname'] + r'))*?, ((and)|e|y) ' + r'(' + \
#    nameRegexes['given name optionally middle name surname'] + r'|' + nameRegexes['given name optionally middle initial surname'] + r')' + r')?\.?' + r')' \
#    + r'|' + nameRegexes['surname, given name and optionally middle initial'] + r')'
#Non-style-guide-specific nameLists
nameListRegexes['with semicolons'] = r'(' + nameRegexes['surname, initials with dot space optional'] + '(; ' + nameRegexes['surname, initials with dot space optional'] + r')*(, ((and)|e|y) ' + nameRegexes['surname, initials with dot space optional'] + r')?)'
nameListRegexes['pure surname initials'] = r'((' + nameRegexes['surname, initials'] + r',? )+)'
nameListRegexes['pure surname initials no dots no spaces'] = r'((' + nameRegexes['surname, initial(s) no dots no spaces'] + r'(,|(\.))? )+(et al.)?)'
nameListRegexes['pure initials surname with dots'] = r'((' + nameRegexes['initials with dot surname'] + r'(,|(\.))?( ((and)|e|y))? )+(et al.)?)'
nameListRegexes['surname initials then initials surname'] = r'(' + nameRegexes['surname, initials with dot'] + r'(, ' + nameRegexes['initials with dot space surname'] + r')*' + r'(,? ((and)|e|y) ' + nameRegexes['initials with dot space surname'] + r')?)'
nameListRegexes['surname initials et al.'] = r'(' + nameRegexes['surname, initials with dot space optional'] + r', et al\.' + r')'
nameListRegexes['surname initials list with "and"'] = r'(' + nameRegexes['surname, initials with dot space optional'] + r'((, ' + nameRegexes['surname, initials with dot space optional'] + r')*' + \
        r',? ((and)|e|y) ' + nameRegexes['surname, initials with dot space optional'] + r')?)'
#nameListRegexes['pure surname initials list'] = r'(' + nameRegexes['surname, initials with dot space optional'] + r'(, ' + nameRegexes['surname, initials with dot space optional'] + r')*)'
'''
The following style guides were found in the EBSCO citation generator.
Initial development set for regexes for apa, mla, and chicago:
- the first 5 results for a search for 'lopez' on JSTOR
- the first 5 results for a search for 'robert' on JSTOR
This development set was used both to initially create the regexes and to initially "test" them.
Subsequent development set:
The first 5 results for the following searches on EBSCO academic search complete (after finding that stopwords yield no results in their search)
- drowning
- dessication
- blue
'''
styleGuideRegexes = {
    'abnt': r'random',
    'ama': r'(' + nameListRegexes['ama name list'] + r' [^"“].*?' + regexes['recent year'] + r';.*$)',
    #'apa': r'(^' + nameListRegexes['apa name list'] + r') \(' + regexes['recent year'] + r'\)\. ' + r'.*?[^\.]$',
    'apa': r'(^' + nameListRegexes['apa name list'] + r') \(' + regexes['recent year'] + r'\)\. ' + r'.*?$',
    'chicago': r'(^' + nameRegexes['surname, given name and optionally middle name'] + r'\. )?' \
        + regexes['title in quotes'] + r' In .*?Accessed ' + regexes['long month'] + r' ' + \
        regexes['day of month'] + r', ' + regexes['recent year'] + r'\. [^\s]*?\.$', #does not exist in EBSCO citation generator, but does exist in JSTOR
    'chicago/turabian: author-date': r'(' + nameListRegexes['chicago/turabian name list'] + r' ' + \
        regexes['recent year'] + r'\. ' + regexes['title in quotes'] + r'.*?\.$)',
    'harvard: australian': r'(' + nameListRegexes['harvard: australian name list'] + r' ' + \
        regexes['recent year'] + r', ' + regexes['title in single quotes'] + r'.*?viewed ' + \
        regexes['day of month'] + r' ' + regexes['long month'] + r' ' + regexes['recent year'] + \
        r', \<' + regexes['url'] + r'\>\.$)',
    'harvard': r'(' + nameListRegexes['harvard name list'] + r' \(' + regexes['recent year'] + r'\) ' + \
        regexes['title in single quotes'] + r'.*?\.$)', 
    'chicago/turabian: humanities': r'(' + nameListRegexes['chicago/turabian name list'] + r' ' + \
        regexes['title in quotes'] + r'.*?(\(((' + regexes['season'] + r')|(' + regexes['long month'] + \
        r')|(' + regexes['short month'] + r')) (' + regexes['day of month'] + r', )?' + \
        regexes['recent year'] + r'\)\:).*?\.$)',
    #'mla': r'^(((((' + nameRegexes['surname, given name and optionally middle name'] + r'|' + nameRegexes['surname, given name and optionally middle initial'] + r'), (and )?)' + \
    #    r'(' + nameRegexes['given name optionally middle name surname'] + r'\.|' + nameRegexes['given name optionally middle initial surname'] + r'))|(' + 
    #    nameRegexes['surname, given name and optionally middle name'] + r'\.|' + nameRegexes['surname, given name and optionally middle initial'] + r')) )?' + \
    #    regexes['title in quotes'] + ' .*?(Accessed ' + regexes['day of month'] + ' ' + regexes['short month'] + \
    #    ' ' + regexes['recent year'] + ')?\.$',
    'mla': r'^(' + nameListRegexes['mla name list'] + r' )?' + regexes['title in quotes'] + \
        r'.*?' + regexes['recent year'] + r', .*?\.$',
    'vancouver/icmje': r'(' + nameListRegexes['ama name list'] + r'.*?' + regexes['recent year'] + \
        r' (' + regexes['short month'] + r'|' + regexes['season'] + r').*?Available from:.*?$)'
    }
'''Dictionary containing Regex patterns of some of the common style guides.'''