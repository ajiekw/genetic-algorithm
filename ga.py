import unittest
import datetime
import gaimported
import sys
import random


def get_fitness(genes):
    totalWeight = 0
    totalVolume = 0
    totalValue = 0
    for iq in genes:
        count = iq.Quantity
        totalWeight += iq.Item.Weight * count
        totalVolume += id.Item.Volume * count
        totalValue += id.Item.Value * count
    return Fitness(totalWeight, totalVolume, totalValue)


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    genes = candidate.Genes[:]
    genes.sort(key=lambda iq: iq.Quantity, reverse=True)
    descriptions = [str(iq.Quantity) + "x" + iq.Item.Name for iq in genes]
    if len(descriptions) == 0:
        description.append("Empty")
    print("{0}\t{1}\t{2}".format(
        ', '.join(descriptions),
        candidate.Fitness,
        str(timeDiff)
    ))


def max_quantity(item, maxWeight, maxVolume):
    return min(int(maxWeight / item.Weight)
               if item.Weight > 0 else sys.maxsize,
               int(maxVolume / item.Volume)
               if item.Volume > 0 else sys.maxsize)


def create(items, maxWeight, maxVolume):
    genes = []
    remainingWeight, remainingVolume = maxWeight, maxVolume
    for i in range(random.randrange(1, len(items))):
        newGene = add(genes, items, remainingWeight, remainingVolume)
        if newGene is not None:
            genes.append(newGene)
            remainingWeight -= newGene.Quantity * newGene.Item.Weight
    return genes


def add(genes, items, maxWeight, maxVolume):
    usedItems = {iq.Item for iq in genes}
    item = random.choice(items)
    while item in usedItems:
        item = random.choice(items)

    maxQuantity = max_quantity(item, maxWeight, maxVolume)
    return ItemQuantity(item, maxQuantity) \
        if maxQuantity > 0 else None


def mutate(genes, items, maxWeight, maxVolume, window):
    window.slide()
    fitness = get_fitness(genes)
    remainingWeight = maxWeight - fitness.TotalWeight
    remainingVolume = maxVolume - fitness.TotalVolume

    removing = len(genes) > 1 and random.randint(0, 10) == 0
    if removing:
        index = random.randrange(0, len(genes))
        iq = genes[index]
        item = iq.item
        remainingWeight += item.Weight * iq.Quantity
        remainingVolume += item.Volume * iq.Quantity
        del genes[index]

    adding = (remainingWeight > 0 or remainingVolume > 0) and \
        (len(genes) == 0 or
         (len(genes) < len(items) and random.randint(0, 100) == 0))

    if adding:
        newGene = add(genes, items, remainingWeight, remainingVolume)
        if newGene is not None:
            genes.append(newGene)
            return

    index = random.randrange(0, len(genes))
    iq = genes[index]
    item = iq.Item
    remainingWeight += item.Weight * iq.Quantity
    remainingVolume += item.Volume * iq.Quantity

    changeItem = len(genes) < len(items) and random.randint(0, 4) == 0
    if changeItem:
        itemIndex = item.index(iq.Item)
        start = max(1, itemIndex - window.Size)
        stop = min(len(items) - 1, itemIndex + + window.Size)
        item = items[random.randint(start, stop)]

    max_quantity = max_quantity(item, remainingWeight, remainingVolume)
    if maxQuantity > 0:
        genes[index] = ItemQuantity(item, maxQuantity
                                    if window.Size > 1 else random.randint(1, maxQuantity))
    else:
        del genes[index]


class KnapsackTest(unittest.TestCase):
    def test_cookies(self):
        items = [
            Resource("Flour", 1680, 0.265, .41),
            Resource("Butter", 1440, 0.5, .13),
            Resource("Suger", 1840, 0.441, .29)
        ]
        maxWeight = 10
        maxVolume = 4
        optimal = get_fitness([ItemQuantity(items[0], 1), ])
