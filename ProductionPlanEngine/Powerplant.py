import json

config = json.load(open("ProductionPlanEngine/config.json", "r"))

class Powerplant:
    """The Powerplant object is an object that represents a powerplant.
    It store the powerplant's name, type, efficiency, pmin and pmax. It also
    give access to functions that can be used to calculate the cost of
    producing a given amount of power.
    """

    fuelCalulated = False

    def __init__(self, name: str, type: str, efficiency: int, pmin: int, pmax: int) -> None:
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = self.def_pmin = pmin
        self.pmax = self.def_pmax = pmax

    def calcFuelCost(self, type_to_fuel: dict, fuels: dict) -> None:
        """calcFuelCost is a function that calculate the fuel cost of the
        powerplant object in function of the powerplant type.

        Args:
            type_to_fuel (dict): A dictionary containing the fuel type of
                each powerplant type.
            fuel_cost (dict): A dictionary containing the cost of the
                available resources.
        """

        fuel_cost = fuels["euro/MWh"]
        fuel_efficiency = fuels["%"]

        self.fuelType = type_to_fuel[self.type]

        # Calculate the fuel cost
        if self.type in config["FreePowerplantTypes"]:
            # If the powerplant is free, the fuel cost is 0 and pmin and pmax depend on the efficency
            self.fuelCost = 0
            self.prodCost = 0
            self.pmin = self.def_pmin * fuel_efficiency[self.fuelType] / 100
            self.pmax = self.def_pmax * fuel_efficiency[self.fuelType] / 100
        else:
            # If the powerplant is not free, the produciton cost calculated from the fuel cost and the efficiency
            self.fuelCost = fuel_cost[self.fuelType]
            self.prodCost = self.fuelCost / self.efficiency
    
            if self.fuelType in config["Co2Cost"].keys():
                # If the fuel type is in the Co2Cost dictionary, the production cost is increased by the Co2 cost
                self.prodCost += self.prodCost * config["Co2Cost"][self.fuelType]


        self.fuelCalulated = True

    def getProdCost(self) -> float:
        """getProdCost is a function that return the production cost of the
        powerplant object.

        Returns:
            float: The production cost of the powerplant object.
        """
        if self.fuelCalulated:
            return self.prodCost
        else:
            raise Exception("Fuel cost not calculated.")
