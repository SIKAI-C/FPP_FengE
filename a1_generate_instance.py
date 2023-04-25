import numpy as np

sizes_list = list(range(5,55,5))
cars_list = [2,3,4,5]
days_list = [3,6]
demand_range = [10,100]
inventory_capacity_list = [200,300]
low_holding_cost_range = [0.01,0.05]
high_holding_cost_range = [0.1,0.5]
car_capacity = 1.5

def generateInstance(days=6, size=20, cars=3, holding_cost="low"):
    
    coordinates = np.random.randint(0, 500, (size+1, 2))
    differences = coordinates[:, np.newaxis, :] - coordinates[np.newaxis, :, :]
    distances = np.sqrt(np.sum(differences ** 2, axis=-1))

    inventory_capacity = 300
    demand = np.random.randint(10, 100, (days, size))
    I_0 = [inventory_capacity-d for d in demand[0]]
    I_0 = [0] + I_0
    demand = [[0]+d.tolist() for d in demand]
    tot_demand = 0
    for d in demand: tot_demand += sum(d)
    car_capacity = int(1.5 * tot_demand / days)

    if holding_cost == "low": hc = np.random.uniform(0.01, 0.05, size)
    else: hc = np.random.uniform(0.1, 0.5, size)
    hc = [0] + hc.tolist()

    res = {}
    res["T"] = days
    res["n"] = size
    res["m"] = cars
    res["coordinates"] = coordinates
    res["distances"] = distances
    res["r"] = demand
    res["U"] = inventory_capacity
    res["hc"] = hc
    res["Q"] = car_capacity
    res["I_0"] = I_0

    return res