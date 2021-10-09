from ss_js.env.env import Environment
from ss_js.env.component.labor import LaborType
from ss_js.env.component.task import Task
from ss_js.env.component.zone import Zone
from ortools.sat.python import cp_model
from typing import Dict
from itertools import combinations

from ss_js.parameters import ModelParams

# Variables와 constraint를 설정함
# 모델의 component
# task, alter, labortype, labor(향후 삭제할듯)

# Variable들의 종류
# variable_1) task 관련: start_var, end_var, duration_var, interval_var
# variable_2) alter 관련: alter_presence, start_var, end_var, duration_var, interval_var
#                * alter_presence: alter가 선택되었는 지 여부를 의미하는 bool 변수
# variable_3) labortype 관련: 각 labor_type에 demand(alter별 필요 인원)값들을 추가
# variable_4) labor 관련(향후 삭제할 듯): labor_presence (labor과 선택되었는지 여부 의미하는 bool 변수)

# Contraint
# constraint_1) task 간 dependency: previous_task.end_var <= task.start_var
# constraint_2) alter는 하나만 선택되어야 함: sum(alter_presence_list) == 1
# constraint_3) Task의 여러 alter 중 하나가 선택되면, task의 start/duration/end/interval은 alter의 것으로 세팅 (task.start_var == alter.start_var...) -> 
# constraint_4) labor_type은 특정 시간에 최대 지정된 명수를 넘을 수 없음 AddCumulative(labortype.interval_var_list, labortype.demand_list, labortype.num_labor)
# constraint_5) A labor can't be assigned to multiple tasks at the same time -> addNoOverLap

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
        self.set_var_and_constraints()   
    
    def set_var_and_constraints(self):
        # set variables
        self.set_vars_of_task()
        self.set_vars_of_alter()
        self.set_alter_dict()
        self.set_alter_presence_vars()
        self.set_zone_ends()
        self.allocate_interval_vars_to_labor()

        self.set_vars_of_space()
        # set constraints
        self.set_dependency_constraints()
        self.set_alter_constraints()
        self.set_interval_to_alter()
        self.set_cumulative()
        # self.set_labor_interval_constraints()
        # self.set_labor_presence_constraints()
        # set objective
        self.set_makespan_objective()
        return        

    # ==============================이 밑에는 상세내용들 ==========================

    # 초기화
    def _initialize(self):
        for task_id in self.task_dict.keys():
            self.alter_presence_vars[task_id] = []
        return
    ############################# property(schedule의 정보들을 반환하는 함수들) ####################################

    @property # 모든 zone정보
    def zone_dict(self) -> Dict[str, Zone]:
        return self.env.zone_dict
    
    @property # 모든 labor 정보
    def labor_dict(self):
        return self.env.labor_dict
    
    @property # 모든 task 정보
    def task_dict(self) -> Dict[str, Task]:
        return self.env.task_dict

    @property # 모든 labor_type 정보
    def labor_type_dict(self) -> Dict[str, LaborType]:
        return self.env.labor_type_dict

    @property # 전체 기간의 가능한 최대 값
    def horizon(self):
        return self.env.max_horizon
    
    @property # zone의 개수
    def num_zone(self):
        return len(self.zone_dict)

    # labor_type에 배정된 labor 숫자
    def num_labor(self, labor_type: LaborType):
        return self.env.num_labor_of_type(labor_type)

    # labortype 반환
    def labor_type(self, labor_type_id)->LaborType:
        return self.env.labor_type(labor_type_id)

    # labor_type_id에 해당하는 labor들을 list로 반환
    def labor_list_of_type(self, labor_type_id):
        return self.env.labor_list_of_type(labor_type_id)
        
    #################### set_var #######################
    # variable_1: task 관련
    def set_vars_of_task(self):
        for zone in self.zone_dict.values():
            for task in zone.task_list:                
                task.set_var(self, self.horizon)                
        return

    # variable_2: alter 관련
    def set_vars_of_alter(self):
        for zone in self.zone_dict.values():
            for task in zone.task_list:
                for alt in task.alt_dict.values():
                    alt.set_var(self, self.horizon)
        return

    # alter 세팅
    def set_alter_dict(self):
        for task in self.task_dict.values():
            for alter in task.alt_dict.values():
                self.alter_dict[alter.id] = alter
        return

    # space 세팅
    def set_space_of_dict(self):
        for zone in self.zone_dict.values():
            zone.set_var(self)

    # variable_1, 2: task/alter 관련(task_id에 해당하는 alter_presence_var들을 별도로 정리해둠: 향후 constraint를 쉽게 걸기 위함)
    def set_alter_presence_vars(self):
        for task_id, task in self.task_dict.items():        
            for alter in task.alt_dict.values():                
                self.alter_presence_vars[task_id].append(alter.presence_var)   
        return

    ## 수정_1005
    # zone들 중 마지막에 있는 task의 end_var을 별도로 저장
    def set_zone_ends(self):
        for zone in self.zone_dict.values():
            # last_task = zone.task_list[-1]
            for last_task in zone.last_task_list:       
                self.zone_ends.append(last_task.end_var)
        return

    # 각 labor의 관련된 alt_interval들을 각 labor에 담아둠, set_labor_constraints와 관련된 것인데 향후 삭제할듯        
    def allocate_interval_vars_to_labor(self):
        for task in self.task_dict.values():
            for alter in task.alt_dict.values():            
                for labor_type_id in alter.labor_type_id_list():
                    # labor_list = self.labor_list_of_type(labor_type_id)                
                    labor_type = self.labor_type_dict[labor_type_id]
                    labor_type.add_interval_var(alter.interval_var)
                    labor_type.add_demand(alter.num_labor_type(labor_type_id))
                    # deprecated
                    # for labor in labor_list:                    
                    #     labor.add_alter(alter, self)                        
                    #     alter.set_labor(labor)                              
        return

    ###################### constraints ###########################
    # constraint_1: task간 순서 관련 constraints(zone의 task_list list 순서)
    ## 수정_1005
    def set_dependency_constraints(self):
        for zone in self.zone_dict.values():
            for pre_task, suc_task in zone.task_dependency:
                self.Add(pre_task.end_var <= suc_task.start_var)
            # previous_task = None
            # for task in zone.task_list:
            #     if previous_task is not None:
            #         self.Add(previous_task.end_var <= task.start_var)
            #     previous_task = task                
        return
    
    # constraint_2: 각 task의 alter들 중 하나만 선택되도록 하는 constraint
    def set_alter_constraints(self):
        for task_id, task in self.task_dict.items():            
            self.Add(sum(task.alt_presence_list()) == 1)
        return

    # constraint_3) Task의 여러 alter 중 하나가 선택되면, task의 start/duration/end/interval은 alter의 것으로 세팅
    def set_interval_to_alter(self):
        for task in self.task_dict.values():            
            for alter in task.alt_dict.values():                           
                self.Add(task.start_var == alter.start_var).OnlyEnforceIf(alter.presence_var)
                self.Add(task.duration_var == alter.duration_var).OnlyEnforceIf(alter.presence_var)
                self.Add(task.end_var == alter.end_var).OnlyEnforceIf(alter.presence_var)
        return                 
    # constraint_4) labor_type은 특정 시간에 최대 지정된 명수를 넘을 수 없음
    def set_cumulative(self):
        for labortype in self.labor_type_dict.values():
            self.AddCumulative(labortype.interval_var_list, labortype.demand_list, labortype.num_labor)
    
    # TODO - constraint_5) space끼리

    # 각 labor별 관련 interval들이 서로 중복되지 않게 함(향후 삭제, 현재 이거 적용시 solve되지 않음)
    # deprecated 
    def set_labor_interval_constraints(self):
        for labor in self.labor_dict.values():            
            if labor.num_interval_vars > 1:                
                alt_list = labor.alt_list()
                combination_alt_list = combinations(alt_list, 2)                
                for alt_1, alt_2 in combination_alt_list:                    
                    labor_var_1, labor_var_2 = labor.labor_presence_var(alt_1.id), labor.labor_presence_var(alt_2.id)                                        
                    self.AddNoOverlap([alt_1.interval_var, alt_2.interval_var]).OnlyEnforceIf([labor_var_1, labor_var_2])
        return

    # 어떤 labor가 alter에 allocate되는 지 설정하는 constraint(향후 삭제)
    # deprecated
    def set_labor_presence_constraints(self):
        for task in self.task_dict.values():
            for alter in task.alt_dict.values():                
                for labor_type_id in alter.labor_type_id_list():
                    labor_presence_var_list = alter.labor_presence_var_list(labor_type_id)
                    labor_num = alter.num_labor_type(labor_type_id)                            
                    self.Add(sum(labor_presence_var_list) == labor_num).OnlyEnforceIf(alter.presence_var)
        return      

    # space간 겹치지 않도록
    def set_space_presence_constraints(self):
        for zone in self.zone_dict.values():
            interval_var_list = []
            for task in zone.task_list:
                interval_var = task.vars[ModelParams.INTERVAL]
                interval_var_list.append(interval_var)
            self.AddNoOverlap(interval_var_list)


    # ====================== 최적화 목적 설정 ==============================
    def set_makespan_objective(self):
        makespan = self.NewIntVar(0, self.horizon, 'makespan')
        self.AddMaxEquality(makespan, self.zone_ends)
        self.Minimize(makespan)
        return
