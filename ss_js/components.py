from parameters import Params
from typing import List


class Zone(object):
    def __init__(self, zone_data):
        self.id = zone_data.get(Params.ZONE_ID.value)
        self.name = zone_data.get(Params.ZONE_NAME.value)
        self.task_type_dependency = zone_data.get(Params.TASK_DEPENDENCY.value)
        self.task_dependency: List[Task] = []        
    
    def __str__(self):
        return self.id+"_"+self.name

    @property
    def num_tasks(self):
        return len(self.task_dependency)
        

class LaborType(object):
    def __init__(self, labor_data):
        self.id = labor_data.get(Params.LABOR_ID.value)
        self.name = labor_data.get(Params.LABOR_NAME.value)
    
    def __str__(self):
        return self.id+"_"+self.name

    def __eq__(self, other):
        return self.id == other.id


class TaskType(object):
    def __init__(self, task_data):
        self.id = task_data.get(Params.TASK_ID.value)
        self.name = task_data.get(Params.TASK_NAME.value)
        self.duration = task_data.get(Params.DURATION.value)
        self.required_labor_set = task_data.get(Params.REQUIRED_LABOR_SET.value)

    def __str__(self):
        return self.id+"_"+self.name


class Labor(object):
    def __init__(self, labor_id, labor_type: LaborType):        
        self.id = labor_type.id+"_"+labor_id
        self.type: LaborType = labor_type
        self.interval_list = []

    def __str__(self):
        return self.id

    @property
    def type_id(self):
        return self.type.id

    @property
    def type_name(self):
        return self.type.name  


class Task(object):
    def __init__(self, zone_id, task_type: TaskType):
        self.id = zone_id +"_"+task_type.id
        self.type: TaskType = task_type
        self.alter_labor_dict = {} # labor_type_id, [labor]

    def __str__(self):
        return self.id

    @property
    def type_id(self):
        return self.type.id

    @property
    def type_name(self):
        return self.type.name

    @property
    def duration(self):
        return self.type.duration

    @property
    def required_labor_set(self):
        return self.type.required_labor_set

    @property
    def num_labor_type(self):
        return len(self.required_labor_set.keys())

    def required_num_labor(self, type_id) -> int:
        if type_id in self.type.required_labor_set.keys():
            return self.type.required_labor_set[type_id]
        else:
            return 0

        