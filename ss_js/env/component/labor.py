from ss_js.parameters import Params, ModelParams
from ortools.sat.python import cp_model
from typing import List


class LaborType(object):    
    def __init__(self, labor_data):
        self.id = labor_data.get(Params.LABOR_ID.value)
        self.name = labor_data.get(Params.LABOR_NAME.value)
        self.num_labor = labor_data.get(Params.LABOR_NUMBER.value)
    
    def __str__(self):
        return self.id+"_"+self.name

    def __eq__(self, other):
        return self.id == other.id

    
class Labor(object):
    id_list = []
    def __init__(self, labor_idx, type_id, env):     
        self.type: LaborType = env.labor_type(type_id)         
        self.id = None
        self.set_id(self.type.id + "_" + labor_idx) 
               
        self.interval_var_dict = {}            
        
        # alt_id: [task_id, interval_var]
        # (AddNoOverlap(interval).OnlyEnforce(presence))     

    def __str__(self):
        return self.id

    def set_id(self, possible_id):
        if possible_id in Labor.id_list:
            print("labor id exists in already")
        else:
            self.id = possible_id
            Labor.id_list.append(self.id)
        return

    @property
    def type_id(self):
        return self.type.id

    @property
    def type_name(self):
        return self.type.name  

    @property
    def num_interval_vars(self):
        return len(self.interval_var_list)

    def add_interval_var(self, task_id, alt_id, interval_var: cp_model.IntervalVar):
        self.interval_var_dict[alt_id] = [task_id, interval_var]        
        return
