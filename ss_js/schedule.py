from ortools.sat.python import cp_model
from components import Zone, Labor, Task
from parameters import ComponentParams
import os
import json

class Schedule(cp_model.CpModel):
    def __init__(self, data):            
        self.zone_dict = {}
        self.labor_dict = {}
        self.task_dict = {}
        
        self.data_set = {
            "starts": {},
            "presences": {},
            "zone_ends": []
        }
        
        self.__generate_components(data)
        self.max_horizon()

    
    def __generate_components(self, data):
        labor_dict = data.get(ComponentParams.LABOR.value)
        for labor_info in labor_dict.values():
            l = Labor(labor_info)
            self.labor_dict[l.labor_id] = l

        task_dict = data.get(ComponentParams.TASK.value)
        for task_info in task_dict.values():
            t = Task(task_info)
            self.task_dict[t.task_id] = t
        
        zone_dict = data.get(ComponentParams.ZONE.value)
        for zone_info in zone_dict.values():
            z = Zone(zone_info)
            self.zone_dict[z.zone_id] = z
            # TODO - labor class

        # TODO - check data exception
        return

    def max_horizon(self):
        for zone in self.zone_dict.values():
            print(zone.task_dependency)
        return 5

if __name__ == '__main__':    
    file_path = "data/data.json"
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    Schedule(json_data)