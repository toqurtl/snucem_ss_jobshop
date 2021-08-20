from ss_js.parameters import Params, ModelParams
from ortools.sat.python import cp_model
from typing import List


class Zone(object):
    def __init__(self, zone_data):
        self.id = zone_data.get(Params.ZONE_ID.value)
        self.name = zone_data.get(Params.ZONE_NAME.value)
        self.task_type_dependency = zone_data.get(Params.TASK_DEPENDENCY.value)
        self.task_dependency = []        
    
    def __str__(self):
        return self.id+"_"+self.name

    @property
    def num_tasks(self):
        return len(self.task_dependency)