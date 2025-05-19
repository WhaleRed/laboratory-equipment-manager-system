import re

VALID_NAME = r'^([A-Z][a-z]+)([\s\-][A-Z][a-z]+)*$'
VALID_IDNUMBER = r'^d{4} - \d{4}'


def vaidateName(name: str):
    if re.match(VALID_NAME, name):
        return True
    else: 
        return False
    
def validateIDNumber(idNumber: str):
    if re.match(VALID_IDNUMBER, idNumber):
        return True
    else:
        return False
    