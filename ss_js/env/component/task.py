from ss_js.parameters import Params, ModelParams
from ss_js.env.component.alter import Alter
from ortools.sat.python import cp_model
from typing import List


class TaskType(object):
    def __init__(self, task_data):
        self.id = task_data.get(Params.TASK_ID.value)
        self.name = task_data.get(Params.TASK_NAME.value)        
        self.labor_info_list = task_data.get(Params.LABOR_SET.value)

    def __str__(self):
        return self.id+"_"+self.name
    
    def __eq__(self, other):
        return self.id == other.id

    @property
    def num_alternatives(self):
        return len(self.labor_info_list)

    @property
    def alt_id_list(self):        
        return [labor_set[Params.ALT_ID.value] for labor_set in self.labor_info_list]
    

class Task(object):
    def __init__(self, zone, task_type: TaskType):
        self.zone = zone
        self.id = zone.id +"_"+task_type.id        
        self.type: TaskType = task_type        
        self.vars = {            
            ModelParams.START: None,
            ModelParams.DURATION: None,
            ModelParams.END: None,
            ModelParams.INTERVAL: None,            
        }
        self.space_id_list = zone.space_id_list
        self.alt_dict = {} # alt_id, alt        
        self._set_alt_dict()

    # zone의 quantity와 labor_set의 productivity로 duration을 계산
    def _set_alt_dict(self):
        for labor_info in self.type.labor_info_list:
            new_alt_id = self.id + "_alt" + str(labor_info[Params.ALT_ID.value])
            alter = Alter(new_alt_id, labor_info)
            alter.set_required_labor(labor_info[Params.REQUIRED_LABOR.value])                       
            duration = round(self.quantity / labor_info[Params.PRODUCTVITY.value])            
            alter.set_duration(duration)            
            self.alt_dict[new_alt_id] = alter
        return

    @property
    def quantity(self):
        return self.zone.quantity

    @property
    def start_var(self):
        return self.vars[ModelParams.START]
    
    @property
    def duration_var(self):
        return self.vars[ModelParams.DURATION]

    @property
    def end_var(self):
        return self.vars[ModelParams.END]
    
    @property
    def interval_var(self):
        return self.vars[ModelParams.INTERVAL]

    @property
    def type_id(self):
        return self.type.id

    @property
    def type_name(self):
        return self.type.name
    
    def duration_range(self):
        # TODO - 수정 필요
        min_du, max_du= 0, 9999
        for alt in self.alt_dict.values():            
            min_du, max_du = min(alt.duration, min_du), max(alt.duration, max_du)
        return min_du, max_du

    @property
    def max_duration(self):
        min_du, max_du = self.duration_range()        
        return max_du

    @property
    def min_duration(self):
        min_du, max_du = self.duration_range()        
        return min_du

    @property
    def alt_keys(self):
        return self.alt_dict.keys()

    @property
    def labor_set_info_of_alt(self, alt_id, params: Params):
        return self.alt_dict[alt_id].info[params]

    # for cpmodel
    @property
    def start_var(self):
        return self.vars[ModelParams.START]
    
    @property
    def end_var(self):
        return self.vars[ModelParams.END]

    @property
    def interval_var(self):
        return self.vars[ModelParams.INTERVAL]

    def alt_interval_var(self, alt_id):        
        return self.alt_dict[alt_id].vars[ModelParams.INTERVAL]

    # alt_id와 labor_type_id에 해당하는 labor_id 반환
    def labor_id_list_of_alt(self, alt_id, labor_type_id):
        return self.alt_dict[alt_id].labor_id_list(labor_type_id)

    # alt_id와 labor_type_id를 넣으면 필요한 인원수 반환
    def num_labor_type_of_alt(self, alt_id, labor_type_id):
        return self.alt_dict[alt_id].num_labor_type(labor_type_id)
    
    # alt_id를 넣으면 duration을 반환
    def duration_of_alt(self, alt_id):
        return self.alt_dict[alt_id].duration

    # task의 interval var을 세팅함(interval_var는 start-duration-end로 구성)
    def set_var(self, model: cp_model.CpModel, horizon):                
        min_du, max_du = self.min_duration, self.max_duration
        self.vars[ModelParams.START] = model.NewIntVar(0, horizon, self._suffix(ModelParams.START))        
        self.vars[ModelParams.DURATION] = model.NewIntVar(min_du, max_du, self._suffix(ModelParams.DURATION))
        self.vars[ModelParams.END] = model.NewIntVar(0, horizon, self._suffix(ModelParams.END))
        self.vars[ModelParams.INTERVAL] = model.NewIntervalVar(
            self.vars[ModelParams.START],
            self.vars[ModelParams.DURATION],
            self.vars[ModelParams.END],
            self._suffix(ModelParams.INTERVAL)
        )        
        return

    def alt_presence_list(self):
        return [alt.presence_var for alt in self.alt_dict.values()] 

    def _suffix(self, params: ModelParams):
        return params.value + "_" + self.id     