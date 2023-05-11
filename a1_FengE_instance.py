import json
import random
from tqdm import tqdm

MAX_DISTANCE = 1000000


class LOADDATA:

    def __init__(self, verbose=False):
        # self.file1_dir = r"/Users/sikai/Library/CloudStorage/OneDrive-Personal/Desktop/A2_Research/code_FengE_FPP/data/2022-11-09-1.json"
        # self.file2_dir = r"/Users/sikai/Library/CloudStorage/OneDrive-Personal/Desktop/A2_Research/code_FengE_FPP/data/2022-11-09-2.json"
        # self.file3_dir = r"/Users/sikai/Library/CloudStorage/OneDrive-Personal/Desktop/A2_Research/code_FengE_FPP/data/2022-11-09-3.json"
        # self.file4_dir = r"/Users/sikai/Library/CloudStorage/OneDrive-Personal/Desktop/A2_Research/code_FengE_FPP/data/2022-11-09-4.json"
        # self.recorded_distance_dir = r"/Users/sikai/Library/CloudStorage/OneDrive-Personal/Desktop/A2_Research/code_FengE_FPP/data/processed/recorded_distance.json"
        # self.recorded_routes_dir = r"/Users/sikai/Library/CloudStorage/OneDrive-Personal/Desktop/A2_Research/code_FengE_FPP/data/processed/recorded_record.json"
        
        self.file1_dir               = r"data/2022-11-09-1.json"
        self.file2_dir               = r"data/2022-11-09-2.json"
        self.file3_dir               = r"data/2022-11-09-3.json"
        self.file4_dir               = r"data/2022-11-09-4.json"
        self.recorded_distance_dir   = r"data/processed/recorded_distance.json"
        self.recorded_routes_dir     = r"data/processed/recorded_record.json"

        self.distance_dict = self.__loadDistance(verbose)
        self.manager_dict = self.__loadManager(verbose)
        self.verbose = verbose

    def __loadDistance(self, verbose=False):
        if verbose:
            print("a_load_data - initialization - distance")
        with open(self.recorded_distance_dir, "r") as f:
            data = json.load(f)
        print()
        return data

    def __loadManager(self, verbose=False):
        manager_dict = {}
        file1_dict = {}
        file2_dict = {}

        with open(self.file1_dir, "r") as f:
            file1 = json.load(f)
        with open(self.file2_dir, "r") as f:
            file2 = json.load(f)

        def __getFile1(d):
            if d["manager_id"] not in file1_dict: file1_dict[d["manager_id"]] = {}
            if d["shelf_id"] not in file1_dict[d["manager_id"]]: file1_dict[d["manager_id"]][d["shelf_id"]] = []
            file1_dict[d["manager_id"]][d["shelf_id"]].append(d["final_suggest_fill_qty"])

        def __getFile2(d):
            if d["manager_id"] not in file2_dict: file2_dict[d["manager_id"]] = {}
            file2_dict[d["manager_id"]]["vehicle"] = d["delivery_vehicle"]
            file2_dict[d["manager_id"]]["capacity"] = d["max_transport"]
            file2_dict[d["manager_id"]]["warehouse"] = d["warehouse_id"]
        if verbose:
            for info in tqdm(file1, desc="a_load_data - initialization - shelves"): __getFile1(info)
            for info in tqdm(file2, desc="a_load_data - initialization - manager"): __getFile2(info)
            print()
        else:
            for info in file1: __getFile1(info)
            for info in file2: __getFile2(info)

        for k, v in file1_dict.items():
            if k in file2_dict:
                manager_dict[k] = {}
                manager_dict[k]["shelves"] = v
                manager_dict[k]["vehicle"] = file2_dict[k]["vehicle"]
                manager_dict[k]["capacity"] = file2_dict[k]["capacity"]
                manager_dict[k]["warehouse"] = file2_dict[k]["warehouse"]

        return manager_dict

    def getAManagerAndShelves(self, idx):
        manager_list = list(self.manager_dict.keys())
        res = {}
        manager = manager_list[idx]
        warehouse = self.manager_dict[manager]["warehouse"]
        shelves = sorted(list(self.manager_dict[manager]["shelves"].keys()))
        shelf_demand_dict = self.manager_dict[manager]["shelves"]
        capacity = self.manager_dict[manager]["capacity"]
        vehicle = "car" if self.manager_dict[manager]["vehicle"] == 2 else "pedelec"
        id_list = [warehouse] + shelves
        distance = [[0 for _ in range(len(id_list))] for _ in range(len(id_list))]
        for i in range(len(id_list)):
            for j in range(len(id_list)):
                if i != j:
                    if id_list[i] in self.distance_dict and id_list[j] in self.distance_dict[id_list[i]]:
                        distance[i][j] = self.distance_dict[id_list[i]][id_list[j]]["duration"][vehicle]
                    else:
                        distance[i][j] = MAX_DISTANCE
        res["manager"] = manager
        res["warehouse"] = warehouse
        res["shelves"] = shelves
        res["shelf_demand_dict"] = shelf_demand_dict
        res["capacity"] = capacity
        res["vehicle"] = vehicle
        res["id_list"] = id_list
        res["distance"] = distance
        return res
