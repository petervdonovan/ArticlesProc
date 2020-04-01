from datetime import datetime

def getStringTimestamp():
    return datetime.now().strftime("%d-%b-%Y (%H_%M)")