from ss_js.parameters import Params, ModelParams
from ortools.sat.python import cp_model
from typing import List


class Zone(object):
    def __init__(self, zone_data):
        self.id = zone_data.get(Params.ZONE_ID.value)
        self.name = zone_data.get(Params.ZONE_NAME.value)
        self.quantity = zone_data.get(Params.QUANTITY.value)
        # depreceate
        self.task_type_list = zone_data.get(Params.TASK_LIST.value)
        self.task_type_dependency = zone_data.get(Params.TASK_DEPENDENCY.value)        
        self.last_task_type_id_list = zone_data.get(Params.LAST_TASK_TYPE.value)

        self.space_id_list = zone_data.get(Params.SPACE_ID.value)
        self.space_list = []

        # depreceate
        self.task_list = []    
        self.task_dependency = []
        self.last_task_type_list = []

        self.quantity = zone_data.get(Params.QUANTITY.value)
        self.vars = []
    
    def __str__(self):
        return self.id+"_"+self.name

    @property
    def num_tasks(self):
        return len(self.task_list)
    
    @property
    def last_task_list(self):
        task_list = []
        for last_task_type in self.last_task_type_list:
            task_list.append(self.task_of_type(last_task_type))
        return task_list
        
    def add_task(self, task):        
        self.task_list.append(task)
        for space in self.space_list:
            space.task_list.append(task)
    
    def task_of_type(self, task_type):        
        for task in self.task_list:            
            if task.type == task_type:
                return task
        return
    
    def set_var(self, model: cp_model.CpModel):
        self.vars[ModelParams.SPACE_PRESENCE] = model.NewBoolVar('presence_' + self.id)
        return
