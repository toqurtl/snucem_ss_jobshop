import collections
from components import LaborType, Task, Zone, Labor
from typing import Dict, List
from ortools.sat.python import cp_model
from utils import Generate
from functools import reduce
from parameters import ModelParams
import json


class Environment(object):
    def __init__(self, data):
         # data setting: 데이터를 일단 들고 있는 상태 
        self.labor_type_dict = {} # str, labortype
        self.task_type_dict = {} # str, tasktype
        self.labor_type_num = {} # labortype, int

        self.labor_pool = {} # labor_type, [labors]
        self.zone_dict = {} # str, zone

        self._generate_type_dicts(data)
        self._generate_pool_dicts()

    def _generate_type_dicts(self, data):
        Generate.labor_type_dict(self, data)
        Generate.task_type_dict(self, data)
        Generate.zone_dict(self, data)       
        return

    def _generate_pool_dicts(self):        
        Generate.labor_pool(self)
        Generate.task_pool(self)
        return

    def num_labor(self, type: LaborType):
        return self.labor_type_num[type.id]

    def labor_type(self, labor_type_str) -> LaborType:
        return self.labor_type_dict[labor_type_str]

    def task_dict(self):
        task_dict = {}
        for zone in self.zone_dict.values():
            for task in zone.task_dependency:
                task_dict[task.id] = task
        return task_dict


    @property
    def max_horizon(self):
        horizon = 0        
        for zone in self.zone_dict.values():
            horizon += sum(map(lambda x: x.duration, zone.task_dependency))                   
        return horizon       
        # fun
        # return sum(map(lambda x: sum(map(lambda y: y.duration, x.task_dependency)), self.zone_dict.values()))



class Schedule(cp_model.CpModel):
    def __init__(self, data):
        super().__init__()
        self.env = Environment(data)     

        # Global storage of variables for js problem
        self.interval_per_labors = {} # labor_type: [{labor: []}]
        self.start_var_dict = {}
        self.presences = {}
        self.zone_ends = []

        self._initialize()

    def _initialize(self):
        for labor_type_id, labor_list in self.labor_pool.items():
            self.interval_per_labors[labor_type_id] = {}
            for labor in labor_list:                
                self.interval_per_labors[labor_type_id][labor.id] = []

    @property
    def zone_dict(self) -> Dict[str, Zone]:
        return self.env.zone_dict
    
    @property
    def labor_pool(self) -> Dict[LaborType, List[Labor]]:
        return self.env.labor_pool
    
    @property
    def task_dict(self) -> Dict[str, Task]:
        return self.env.task_dict()

    @property
    def horizon(self):
        return self.env.max_horizon

    @property
    def num_zone(self):
        return len(self.zone_dict)

    def num_labor(self, labor_type: LaborType):
        return self.env.num_labor(labor_type)

    def labor_type(self, labor_type_id)->LaborType:
        return self.env.labor_type(labor_type_id)

    def create_intervals(self):
        for zone in self.zone_dict.values():
            previous_end_var = None            
            for task in zone.task_dependency:                
                previous_end_var = self.add_var_of_task(task, previous_end_var)

    def create_labor_contraints(self):
        for labor_type_id, labor_list in self.labor_pool.items():
            for labor in labor_list:
                intervals = self.interval_per_labors[labor_type_id][labor.id]
                if len(intervals) > 1:
                    self.AddNoOverlap(intervals)
    
    # TODO
    def create_presecne_contraints(self):
        pass


    def add_var_of_task(self, task: Task, previous_end_var):
        suffix_start = ModelParams.START.value+"_"+task.id
        suffix_end = ModelParams.END.value+"_"+task.id
        suffix_interval = ModelParams.INTERVAL.value+"_"+task.id
        start_var = self.NewIntVar(0, self.horizon, suffix_start)
        end_var = self.NewIntVar(0, self.horizon, suffix_end)
        interval = self.NewIntervalVar(start_var, task.duration, end_var, suffix_interval)
        self.start_var_dict[task.id] = start_var
        for labor_type_id in task.required_labor_set.keys():            
            interval_per_labor_type = self.interval_per_labors[labor_type_id]
            for labor_id, interval_list in interval_per_labor_type.items():
                interval_list.append(interval)
        
        if previous_end_var is not None:
            self.Add(start_var >= previous_end_var)
        previous_end_var = end_var
        self.zone_ends.append(previous_end_var)

        return previous_end_var


    def set_makespan_objective(self):
        makespan = self.NewIntVar(0, self.horizon, 'makespan')
        self.AddMaxEquality(makespan, self.zone_ends)
        self.Minimize(makespan)
                        
        

def test_func():
    pass



if __name__ == '__main__':    
    file_path = "data/data.json"
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    s = Schedule(json_data)    
    s.create_intervals()
    s.create_labor_contraints()
    s.set_makespan_objective()
    

