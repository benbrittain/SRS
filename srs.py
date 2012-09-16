import os, json, time, uuid, datetime
from mongo import *

def makeCard(frontVar, backVar):
    card = Card(uniqueId = unicode(uuid.uuid1()), 
            front = frontVar,
            back = backVar,
            interval = 0,
            eFactor = 2.5,
            status = "",
            lastDone = datetime.datetime.now(),
            isDue = False)
    return card

def get_card(deck):
    activeReview = []
    for card in deck:
        if (datetime.datetime.now() - card.lastDone) < card.interval:
            print "got card from due section"
            activeReview.append(card)

    allNew = []
    for card in deck:
        if card.status == "new":
            print "got card from new section"
            return card

    for card in deck:
        if size(allNew) >= 10:
            break
        else:
            print "allNew! broken out of making pending new"
            if card.status == "pending":
                card.status = "new"

    pendingDeck = []
    for card in deck:
        if card.status == "pending":
            print "got card from pending section!"
            if pendingDeck > 10:
                break
            pendingDeck.append(card)
            return card
    for card in deck:
        if card.status == "new":
            print "got card from new section"
            return card

#    maxQuality = 5
#qualitySubtractor = 5
#eFactorFloor = 1.3
#
#def scoreCard(card, quality):
#    qFactor = qualitySubtractor - quality
#    newFactor = card.eFactor + (0.1 - qFactor * (0.08 + qFactor * 0.02))
#    if newFactor < eFactorFloor:
#        newFactor = eFactorFloor
#    card.eFactor = newFactor
#
#def calculateInterval(card):
#    interval = 1
#    if card.eFactor < 3:
#        card.count = 1
#    if card.count == 2:
#        interval = 6
#    else if card.count > 2:
#        card.Interval * card.eFactor
#    card.interval = interval
#
