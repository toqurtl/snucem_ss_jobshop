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
from itertools import combinations


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
        self.alter_dict = {}
        

        # Global storage of variables for js problem
        self.start_var_dict = {}        
        self.alter_presence_vars = {}     
        self.zone_ends = []
        self._initialize()

    def _initialize(self):
        for task_id in self.task_dict.keys():
            self.alter_presence_vars[task_id] = []

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
    def labor_type_dict(self) -> Dict[str, LaborType]:
        return self.env.labor_type_dict

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
        
    def set_alter_dict(self):
        for task in self.task_dict.values():
            for alter in task.alt_dict.values():
                self.alter_dict[alter.id] = alter
        return
    
    def set_zone_ends(self):
        for zone in self.zone_dict.values():
            last_task = zone.task_dependency[-1]
            self.zone_ends.append(last_task.end_var)

    #################### set_var #######################
    def set_vars_of_task(self):
        for zone in self.zone_dict.values():
            for task in zone.task_dependency:                
                task.set_var(self, self.horizon)                
        return

    def set_vars_of_alter(self):
        for zone in self.zone_dict.values():
            for task in zone.task_dependency:
                for alt in task.alt_dict.values():
                    alt.set_var(self, self.horizon)

    # 모든 task에 대해서 각 task의 alter boolean 변수를 alter_select에 추가
    # alter_select: task별로 alter 관련 presence 변수를 모아둠
    # 이후 task_id별로 sum(alt_presence) == 1 constraint 설정
    def set_alter_presence_vars(self):
        for task_id, task in self.task_dict.items():        
            for alter in task.alt_dict.values():                
                self.alter_presence_vars[task_id].append(alter.presence_var)   

    # 각 labor의 관련된 alt_interval들을 각 labor에 담아둠
    # set_labor_constraints와 관련
    def allocate_interval_vars_to_labor(self):
        for task in self.task_dict.values():
            for alter in task.alt_dict.values():            
                for labor_type_id in alter.labor_type_id_list():
                    labor_list = self.labor_list_of_type(labor_type_id)                
                    labor_type = self.labor_type_dict[labor_type_id]
                    labor_type.add_interval_var(alter.interval_var)
                    labor_type.add_demand(alter.num_labor_type(labor_type_id))
                    for labor in labor_list:                    
                        labor.add_alter(alter, self)                        
                        alter.set_labor(labor)      
                                 
        return

    
    ###################### constraints ###########################    
    def set_interval_to_alter(self):
        for task in self.task_dict.values():            
            for alter in task.alt_dict.values():                           
                self.Add(task.start_var == alter.start_var).OnlyEnforceIf(alter.presence_var)
                self.Add(task.duration_var == alter.duration_var).OnlyEnforceIf(alter.presence_var)
                self.Add(task.end_var == alter.end_var).OnlyEnforceIf(alter.presence_var)
        return                 
    
    # 각 labor에 필요한 constriants
    # 1) 각 labor별 관련 interval들이 서로 중복되지 않게 함    
    def set_labor_interval_constraints(self):
        for labor in self.labor_dict.values():            
            if labor.num_interval_vars > 1:
                # TODO - 이 부분 때문에 원하는 결과가 안나옴. overlap을 좀더 복잡하게 해야 함
                # TODO - 현재는 labor_1이 task에 잡히든 안잡히든 무조건 overlap되지 않게 설정됨                            
                # self.AddNoOverlap(labor.interval_var_list())
                pass
                # alt_list = labor.alt_list()
                # combination_alt_list = combinations(alt_list, 2)                
                # for alt_1, alt_2 in combination_alt_list:                    
                #     labor_var_1, labor_var_2 = labor.labor_presence_var(alt_1.id), labor.labor_presence_var(alt_2.id)                    
                    # print(labor_var_1, labor_var_2, alt_1.interval_var, alt_2.interval_var)
                    # self.AddNoOverlap([alt_1.interval_var, alt_2.interval_var]).OnlyEnforceIf(labor_var_1)
                
                    
        return

    def set_cumulative(self):
        for labortype in self.labor_type_dict.values():
            self.AddCumulative(labortype.interval_var_list, labortype.demand_list, labortype.num_labor)

    # 2) 한 interval에 n명의 labor가 필요할 경우 n명이 선택되도록(num_presence)    
    # 2) 이것은 alt_interval별로 constraint을 걸어두되, constraint는 alt_presence가 True일 때만 작동
    # model.Add(sum(num_presences) == n).OnlyEnforce(alt_presence)
    def set_labor_presence_constraints(self):
        for task in self.task_dict.values():
            for alter in task.alt_dict.values():                
                for labor_type_id in alter.labor_type_id_list():
                    labor_presence_var_list = alter.labor_presence_var_list(labor_type_id)
                    labor_num = alter.num_labor_type(labor_type_id)                            
                    self.Add(sum(labor_presence_var_list) == labor_num).OnlyEnforceIf(alter.presence_var)
                    
        return      

    # 각 task의 alter들 중 하나만 선택되도록(alt_presence)
    def set_alter_constraints(self):
        for task_id, task in self.task_dict.items():            
            self.Add(sum(task.alt_presence_list()) == 1)
        return
    
    # task간 순서 관련 constraints(zone의 task_dependency list 순서)
    def set_dependency_constraints(self):
        for zone in self.zone_dict.values():
            previous_task = None
            for task in zone.task_dependency:
                if previous_task is not None:
                    self.Add(previous_task.end_var <= task.start_var)
                previous_task = task
                
        return       
      
    def set_makespan_objective(self):
        makespan = self.NewIntVar(0, self.horizon, 'makespan')
        self.AddMaxEquality(makespan, self.zone_ends)
        self.Minimize(makespan)
                        
        

def test_func():
    pass



