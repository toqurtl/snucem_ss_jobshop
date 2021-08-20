import collections
from ss_js.env.env import Environment
from ss_js.env.component.labor import LaborType, Labor
from ss_js.env.component.task import Task, TaskType
from ss_js.env.component.zone import Zone
from typing import Dict, List, Union
from ortools.sat.python import cp_model
from functools import reduce
from ss_js.parameters import ModelParams, Params
import json


# Variables in the model
# 1) start_var, end_var, interval_var of task
# 2) bool_var representing labor selected(alternative)

# Required Constraints
# 1) dependency(predecessor task end <= successor task start) 
# 2) required labor set of task(e.g. Task A0 require 2 LaborType "L1", 1 LaborType "L2")
# 3) A labor can't be assigned to multiple tasks at the same time -> addNoOverLap


# 1) env
# 2) components
# 3) model variable
# 4) global variable storage
# 5) constraints
class Schedule(cp_model.CpModel):
    def __init__(self, data):
        super().__init__()
        self.env = Environment(data)     

        # Global storage of variables for js problem
        self.start_var_dict = {}
        self.presences = {}
        self.alter_select = {}
        self.zone_ends = []

    def _initialize(self):
        for task_id in self.task_dict.keys():
            self.alter_select[task_id] = []

    def set_vars_of_model(self):
        pass

    def set_constraints(self):
        pass

    ############################# property ####################################

    @property
    def zone_dict(self) -> Dict[str, Zone]:
        return self.env.zone_dict
    
    @property
    def labor_dict(self):
        return self.env.labor_dict
    
    @property
    def task_dict(self) -> Dict[str, Task]:
        return self.env.task_dict

    @property
    def horizon(self):
        return self.env.max_horizon

    @property
    def num_zone(self):
        return len(self.zone_dict)

    def num_labor(self, labor_type: LaborType):
        return self.env.num_labor_of_type(labor_type)

    def labor_type(self, labor_type_id)->LaborType:
        return self.env.labor_type(labor_type_id)

    def labor_list_of_type(self, labor_type_id):
        return self.env.labor_list_of_type(labor_type_id)

    #################### set_var #######################
    def set_vars_of_task(self):
        for zone in self.zone_dict.values():
            for task in zone.task_dependency:                
                task.set_var(self, self.horizon)
                task.set_alt_var(self, self.horizon)
        return

    # 모든 task에 대해서 각 task의 alter boolean 변수를 alter_select에 추가
    def set_alter_select(self):
        for task_id, task in self.task_dict.items():        
            for alt_var_dict in task.alt_vars.values():
                l_presence = alt_var_dict[ModelParams.PRESENCE]
                self.alter_select[task_id].append(l_presence)        

    def allocate_interval_vars_to_labor(self, task: Task):
        
        for labor_type_id in task.related_labor_id_list:
            labor_list = self.labor_list_of_type(labor_type_id)
            for labor in labor_list:
                labor.add_interval_var()

    
    ###################### constraints ###########################
    def set_labor_contraints(self):
        for labor in self.labor_dict.values():            
            if labor.num_interval_vars > 1:
                self.AddNoOverlap(labor.interval_var_list)
    
    def set_dependency_contraints(self):
        for zone in self.zone_dict.values():
            previous_task = None
            for task in zone.task_dependency:
                if previous_task is not None:
                    self.Add(previous_task.end_var <= task.start_var)
        return       

    # TODO
    def create_presecne_contraints(self):
        pass
 
        
    def set_makespan_objective(self):
        makespan = self.NewIntVar(0, self.horizon, 'makespan')
        self.AddMaxEquality(makespan, self.zone_ends)
        self.Minimize(makespan)
                        
        

def test_func():
    pass



