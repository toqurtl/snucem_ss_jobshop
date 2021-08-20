from ss_js.parameters import Params, ModelParams
from ortools.sat.python import cp_model
from typing import List


class TaskType(object):
    def __init__(self, task_data):
        self.id = task_data.get(Params.TASK_ID.value)
        self.name = task_data.get(Params.TASK_NAME.value)        
        self.labor_set_list = task_data.get(Params.LABOR_SET.value)

    def __str__(self):
        return self.id+"_"+self.name

    @property
    def num_alternatives(self):
        return len(self.labor_set_list)

    @property
    def alt_id_list(self):        
        return [labor_set[Params.ALT_ID.value] for labor_set in self.labor_set_list]
        
    @property
    def min_du(self):
        min_du, _ = self._duration_range()
        return min_du

    @property
    def max_du(self):
        _, max_du = self._duration_range()
        return max_du

    @property
    def related_labor_id_list(self):
        labor_id_list = []
        for labor_set in self.labor_set_list:
            for labor_info in labor_set[Params.REQUIRED_LABOR.value]:
                if labor_info[0] not in labor_id_list:
                    labor_id_list.append(labor_info[0])
        return labor_id_list

    def _duration_range(self):
        min_du = self.labor_set_list[0][Params.DURATION.value]
        max_du = self.labor_set_list[0][Params.DURATION.value]
        for labor_set in self.labor_set_list:
            alt_du = labor_set[Params.DURATION.value]
            min_du, max_du = min(alt_du, min_du), max(alt_du, max_du)
        return min_du, max_du


class Task(object):
    def __init__(self, zone_id, task_type: TaskType):
        self.id = zone_id +"_"+task_type.id
        self.type: TaskType = task_type
        self.alt_labor_set_dict = {}        
        self.vars = {            
            ModelParams.START: None,
            ModelParams.DURATION: None,
            ModelParams.END: None,
            ModelParams.INTERVAL: None
        }
        self.alt_vars = {}
        self._set_alt_labor_set_dict()
        # model.Add(sum(labor_set_selected) ==1)
        # model.Add(sum(labor_selected)==2)

    def _set_alt_labor_set_dict(self):
        for labor_set in self.type.labor_set_list:
            new_alt_id = self.id + "_alt" + str(labor_set[Params.ALT_ID.value])
            new_dict = {
                Params.REQUIRED_LABOR: labor_set[Params.REQUIRED_LABOR.value],
                Params.DURATION: labor_set[Params.DURATION.value]
            }
            self.alt_labor_set_dict[new_alt_id] = new_dict
            self.alt_vars[new_alt_id] = {
                ModelParams.PRESENCE: None,
                ModelParams.START: None,                
                ModelParams.END: None,
                ModelParams.INTERVAL: None
            }

    @property
    def type_id(self):
        return self.type.id

    @property
    def type_name(self):
        return self.type.name

    @property
    def duration_range(self):
        return self.type.duration_range()

    @property
    def max_duration(self):
        return self.type.max_du

    @property
    def min_duration(self):
        return self.type.min_du

    @property
    def alt_keys(self):
        return self.alt_vars.keys()

    @property
    def related_labor_id_list(self):
        return self.type.related_labor_id_list

    @property
    def labor_set_info_of_alt(self, alt_id, params: Params):
        return self.alt_labor_set_dict[alt_id][params]

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

    def set_var(self, model: cp_model.CpModel, horizon):
        suffix_start = ModelParams.START.value+"_"+self.id
        suffix_duration = ModelParams.DURATION.value+"_"+self.id
        suffix_end = ModelParams.END.value+"_"+self.id
        suffix_interval = ModelParams.INTERVAL.value+"_"+self.id
        min_du, max_du = self.type.min_du, self.type.max_du
        start_var = model.NewIntVar(0, horizon, suffix_start)
        duration_var = model.NewIntVar(min_du, max_du, suffix_duration)
        end_var = model.NewIntVar(0, horizon, suffix_end)
        interval = model.NewIntervalVar(start_var, duration_var, end_var, suffix_interval)        
        self.vars[ModelParams.START] = start_var
        self.vars[ModelParams.DURATION] = duration_var
        self.vars[ModelParams.END] = end_var
        self.vars[ModelParams.INTERVAL] = interval  
        return        

    def set_alt_var(self, model: cp_model.CpModel, horizon):                   
        for alt_id in self.alt_labor_set_dict.keys():                
            self._add_alt_var(model, horizon, alt_id)
        return

    def _add_alt_var(self, model: cp_model.CpModel, horizon, alt_id):
        labor_set = self.alt_labor_set_dict[alt_id]
        l_presence = model.NewBoolVar('presence_'+alt_id)
        l_start = model.NewIntVar(0, model.horizon, "start_" + alt_id)
        l_duration = labor_set[Params.DURATION]
        l_end = model.NewIntVar(0, model.horizon, 'end'+alt_id)
        l_interval = model.NewOptionalIntervalVar(
            l_start, l_duration, l_end, l_presence, 'interval_'+alt_id
        )
        alt_var_dict = self.alt_vars[alt_id]
        alt_var_dict[ModelParams.PRESENCE] = l_presence
        alt_var_dict[ModelParams.START] = l_start
        alt_var_dict[ModelParams.END] = l_end
        alt_var_dict[ModelParams.INTERVAL] = l_interval
        return
        
    def labor_id_list_of_alt(self, alt_id):
        print(self.alt_labor_set_dict[Params.REQUIRED_LABOR])

    def _set_labor_alternative(self):
        pass

    def required_num_labor(self, type_id) -> int:
        if type_id in self.type.required_labor_set.keys():
            return self.type.required_labor_set[type_id]
        else:
            return 0