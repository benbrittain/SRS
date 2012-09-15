maxQuality = 5
qualitySubtractor = 5
eFactorFloor = 1.3

#cards need an interval added
#cards need an eFactor added
def scoreCard(card, quality):
    qFactor = qualitySubtractor - quality
    newFactor = card.eFactor + (0.1 - qFactor * (0.08 + qFactor * 0.02))
    if newFactor < eFactorFloor:
        newFactor = eFactorFloor
    card.eFactor = newFactor

def calculateInterval(card):
    interval = 1
    if card.eFactor < 3:
        card.count = 1
    if card.count == 2:
        interval = 6
    else if card.count > 2:
        card.Interval * card.eFactor
    card.interval = interval

