"""ProductionPlanEngine.py is a python library that provide tools to
calculate the production plan for a given set of orders and machines
depending on the cost of available resources and the load required.
"""

from .Powerplant import Powerplant
import json

config = json.load(open("ProductionPlanEngine/config.json", "r"))

def calculateProductionPlan(load: int, fuels: dict, powerplants: list) -> list:
    """calculateProductionPlan is a function that calculate the production
    plan for a given set of orders and machines depending on the cost of
    available resources and the load required.

    Args:
        load (int): The load required.
        fuels (dict): A dictionary containing the cost of the available
            resources.
        powerplants (list): A list of powerplants.
    
    Returns:
        list: A list of powerplants with their production level.
    """

    # Separate the fuels in a dictionary depending on their category
    fuels = separateFuel(fuels)

    # Create a list of powerplant objects
    powerplantObjects = []
    for powerplant in powerplants:
        powerplantObjects.append(Powerplant(**powerplant))
    
    # Set the fuel cost of each powerplant
    for powerplant in powerplantObjects:
        powerplant.calcFuelCost(config["TypeToFuel"], fuels)
    
    # Sort the powerplant list by production cost
    powerplantObjects.sort(key=lambda x: x.getProdCost(), reverse=False)

    # Inisialise the production plan
    productionPlan = [[False, 0] for _ in powerplantObjects]

    # Increase production of the cheapest powerplant until the load is reached or exeded
    increaseProduction(powerplantObjects, productionPlan, load)

    # If production is good, return the production plan
    if sumProdPlan(productionPlan) == load:
        return generateResponce(powerplantObjects, productionPlan)
    # If production after increase is too low, return error
    elif sumProdPlan(productionPlan) < load:
        raise Exception("The load cannot be reached.")
    
    # Decrease production of the most expensive powerplant until the load is reached
    decreaseProduction(powerplantObjects, productionPlan, load)

    # If production is good, return the production plan
    if sumProdPlan(productionPlan) == load:
        return generateResponce(powerplantObjects, productionPlan)
    
    # If this point is reached, the load can't be reached
    raise Exception("The load can't be reached")


def increaseProduction(powerplants: list, productionPlan: list, load: int) -> None:
    """This function increase the production of the cheapest powerplant until
    the load is reached or exeded.

    Args:
        powerplantObjects (list): A list of powerplant objects.
        productionPlan (list): A list of powerplant with their production level.
        load (int): The load required.
    """
    for i in range(len(powerplants)):

        # If the load is reached, stop
        if sumProdPlan(productionPlan) >= load:
            break

        # If the powerplant doesn't produce yes, start it
        if not(productionPlan[i][0]):
            productionPlan[i] = [True, powerplants[i].pmin]

        # If the load is reached, stop
        if sumProdPlan(productionPlan) >= load:
            break

        # If the powerplant is already producing and can produce pmax, produce pmax and continue to next powerplant
        if sumProdPlan(productionPlan) - powerplants[i].pmin + powerplants[i].pmax <= load:
            productionPlan[i][1] = powerplants[i].pmax
            continue

        # If this point is reached, the powerplant can add to the production to reach the load while production between pmin and pmax
        productionPlan[i][1] = 0
        productionPlan[i][1] = load - sumProdPlan(productionPlan)
        break

def decreaseProduction(powerplants: list, productionPlan: list, load: int) -> None:
    """This function decrease the production of the most expensive powerplant
    until the load is reached.

    Args:
        powerplantObjects (list): A list of powerplant objects.
        productionPlan (list): A list of powerplant with their production level.
        load (int): The load required.
    """
    for i in range(len(powerplants)-1, -1, -1):

        # If the load is reached, stop
        if sumProdPlan(productionPlan) == load:
            break
        
        # If the powerplant doesn't produce, continue to next powerplant
        if not(productionPlan[i][0]):
            continue

        # If the powerplant is already producing pmin but the sum is too high, continue to next powerplant
        if productionPlan[i][1] == powerplants[i].pmin and sumProdPlan(productionPlan) > load:
            continue

        # At this point, the powerplant is producing more than pmin and the sum is too high

        # If when the powerplant produce pmin, the sum is still too high, produce pmin and continue to next powerplant
        if sumProdPlan(productionPlan) - productionPlan[i][1] + powerplants[i].pmin > load:
            productionPlan[i][1] = powerplants[i].pmin
            continue

        # If this point is reached, the powerplant can decrease the production to reach the load while production between pmin and pmax
        productionPlan[i][1] = 0
        productionPlan[i][1] = load - sumProdPlan(productionPlan)
        break
        

def sumProdPlan(productionPlan: list) -> int:
    """This function calculate the sum of the production plan.

    Args:
        productionPlan (list): A list of powerplant with their production level.

    Returns:
        int: The sum of the production plan.
    """
    return sum([i[1] for i in productionPlan])

def generateResponce(powerplants: list, productionPlan: list) -> list:
    """This function generate the responce.

    Args:
        powerplants (list): A list of powerplant objects.
        productionPlan (list): A list of powerplant with their production level.

    Returns:
        list: A list of powerplants with their production level.
    """
    return [{"name": powerplants[i].name, "p": productionPlan[i][1]} for i in range(len(powerplants))]

def separateFuel(fuels: dict) -> dict:
    """This function separate the fuels in a dictionary depending on their category.
    By default, the fuel name is formatted this way: "fuel_type(categorie): value".
    We will format it this way: "categorie: {fuel_type: value}".

    Args:
        fuels (dict): A dictionary containing the cost of the available
            resources.

    Returns:
        dict: A dictionary containing the cost of the available
            resources.
    """
    out = {}
    for fuel_cat, val in fuels.items():
        [fuel, cat] = fuel_cat.split("(")
        cat = cat[:len(cat)-1]
        if cat not in out:
            out[cat] = {fuel: val}
        else:
            out[cat][fuel] = val
    return out
