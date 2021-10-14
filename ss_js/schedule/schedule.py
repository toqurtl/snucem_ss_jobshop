from ss_js.schedule.env import Environment
from ss_js.schedule.builder import Builder
from ss_js.component.labor import LaborType
from ss_js.component.task import Task
from ss_js.component.zone import Zone
from ss_js.component.space import Space
from ortools.sat.python import cp_model
from typing import Dict


# Schedule을 표현하고 있음. Builder를 통해 variable과 constraint를 설정하여 모델을 만들어냄
class Schedule(cp_model.CpModel):
    def __init__(self, data):
        super().__init__()
        self.env = Environment(data)        
        self.alter_dict = {}
        self.alter_presence_vars = {}
        # Global storage of variables for js problem        
        
        self._initialize()

    # 초기화
    def _initialize(self):
        # alter presence var 세팅        
        for task_id in self.task_dict.keys():
            self.alter_presence_vars[task_id] = []
        # builder
        builder = Builder(self)
        builder.set_var_and_constraints()
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

    @property
    def space_dict(self) -> Dict[str, Space]:
        return self.env.space_dict

    @property
    def dep_list(self):
        return self.env.dep_list

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
    
    def section_list(self):
        section_list = []
        for section in self.env.section_list:
            section_list.append(section["section"])
        return section_list

    def workpackage_list(self):
        workpackage_list = []
        for wp in self.env.workpackage_list:
            workpackage_list.append(wp["workpackage_id"])
        return workpackage_list   
