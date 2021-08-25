from ss_js.parameters import Params, ModelParams
from ortools.sat.python import cp_model
from typing import List


class LaborType(object):    
    def __init__(self, labor_data):
        self.id = labor_data.get(Params.LABOR_ID.value)
        self.name = labor_data.get(Params.LABOR_NAME.value)
        self.num_labor = labor_data.get(Params.LABOR_NUMBER.value)
        self.interval_var_list = []
        self.demand_list = []
    
    def __str__(self):
        return self.id+"_"+self.name

    def __eq__(self, other):
        return self.id == other.id

    def add_interval_var(self, interval):
        self.interval_var_list.append(interval)
    
    def add_demand(self, demand):
        return self.demand_list.append(demand)

    def capacity(self):
        return self.num_labor

    
class Labor(object):
    id_list = []
    def __init__(self, labor_idx, type_id, env):     
        self.type: LaborType = env.labor_type(type_id)         
        self.id = None
        self.set_id(self.type.id + "_" + labor_idx) 
               
        self.alt_dict = {}
        self.labor_presence_vars = {} # alt_id, labor_presence        

    def __str__(self):
        return self.id

    def set_id(self, possible_id):
        if possible_id in Labor.id_list:
            # TODO - make exception
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
        return len(self.alt_dict)

    def add_alter(self, alter, model: cp_model.CpModel):
        self.alt_dict[alter.id] = alter
        self.labor_presence_vars[alter.id] = model.NewBoolVar('labor_presence_'+alter.id+"_"+self.id)        
        return

    def labor_presence_var(self, alt_id):
        return self.labor_presence_vars[alt_id]

    def labor_presence_var_list(self):
        return [var for var in self.labor_presence_vars.values()]
   
    def interval_var(self, alt_id):
        return self.alt_dict[alt_id].interval_var

    def interval_var_list(self):
        return [alter.interval_var for alter in self.alt_dict.values()]

    def alt_list(self):
        return list(self.alt_dict.values())
