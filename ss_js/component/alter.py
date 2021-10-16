from ss_js.parameters import ModelParams, Params
from ortools.sat.python import cp_model


class Alter(object):
    def __init__(self, alt_id, labor_info, task):
        self.id = alt_id
        self.quantity = task.quantity     
        # labor_type_id: {labor_id: labor}
        self.labor_dict = {}
        # fixed duration 설정을 위함
        self.is_module = task.is_module
        self.fixed_start = task.fixed_start
        self.fixed_finish = task.fixed_finish
        self.info = {
            Params.REQUIRED_LABOR: labor_info[Params.REQUIRED_LABOR.value], # labor_type_id, num
            Params.DURATION: None,
            Params.PRODUCTVITY: labor_info[Params.PRODUCTVITY.value],
            Params.IS_PRODUCTIVITY: labor_info[Params.IS_PRODUCTIVITY.value],
            Params.FIXED_DURATION: labor_info[Params.FIXED_DURATION.value]
        } 
        self.setting()
        self.vars = {
            ModelParams.ALT_PRESENCE: None,
            ModelParams.START: None,
            ModelParams.DURATION: None,
            ModelParams.END: None,
            ModelParams.INTERVAL: None
        }
           

    def setting(self):
        for labor_type_id in self.labor_type_id_list():
            self.labor_dict[labor_type_id] = {}

        if self.is_module:
            self.info[Params.DURATION] = self.fixed_finish - self.fixed_start
            return

        if self.is_productivity:
            duration = round(self.quantity/self.productivity)
            self.info[Params.DURATION] = duration
        else:
            self.info[Params.DURATION] = self.fixed_duration 
        return
    

    def set_required_labor(self, required_labor_dict):
        self.info[Params.REQUIRED_LABOR] = required_labor_dict
        for labor_type_id in self.labor_type_id_list():
            self.labor_dict[labor_type_id] = {}
        return

    # def set_duration(self, duration):
    #     self.info[Params.DURATION] = duration
    #     return
    
    
    # def set_productivity(self, productivity):
    #     self.info[Params.PRODUCTVITY] = productivity

    def set_var(self, model: cp_model.CpModel, horizon):
        self.vars[ModelParams.ALT_PRESENCE] = model.NewBoolVar('presence_'+self.id)
        if self.is_module:
            self.vars[ModelParams.START] = self.fixed_start
            self.vars[ModelParams.END] = self.fixed_finish
            self.vars[ModelParams.DURATION] = self.fixed_finish - self.fixed_start
        else:
            self.vars[ModelParams.START] = model.NewIntVar(0, horizon, "start_" + self.id)        
            self.vars[ModelParams.DURATION] = self.info[Params.DURATION]
            self.vars[ModelParams.END] = model.NewIntVar(0, horizon, 'end'+self.id)
        
        self.vars[ModelParams.INTERVAL] = model.NewOptionalIntervalVar(
            self.vars[ModelParams.START], 
            self.vars[ModelParams.DURATION], 
            self.vars[ModelParams.END], 
            self.vars[ModelParams.ALT_PRESENCE], 
            'interval_'+self.id,
        )
        return
    
    def set_labor(self, labor):
        self.labor_dict[labor.type_id][labor.id] = labor

    # labor의 presence_var
    def labor_presence_var(self, labor_type_id, labor_id):
        return self.labor_presence_var_dict[labor_type_id][labor_id]

    # 한 labor_type의 모든 presence_var를 list로 반환
    def labor_presence_var_list(self, labor_type_id):
        return [labor.labor_presence_var(self.id) for labor in self.labor_dict[labor_type_id].values()]

    # 한 labor_type의 모든 labor_id list로 반환
    def labor_id_list(self, labor_type_id):
        return list(self.labor_dict[labor_type_id].keys())

    # 한 labor_type의 필요한 labor 수 반환
    def num_labor_type(self, labor_type_id):
        return self.info[Params.REQUIRED_LABOR][labor_type_id]

    def labor_type_id_list(self):
        return self.info[Params.REQUIRED_LABOR].keys()

    def add_labor(self, labor):
        self.labor_dict[labor.type_id] = labor
        return

    def labor_presence_var(self, labor_type_id, labor_id):
        return self.labor_dict[labor_type_id][labor_id].labor_presence_var(self.id)
    
    @property
    def duration(self):
        return self.info[Params.DURATION]

    @property
    def task_id(self):
        return self.id.split("_alt")[0]

    @property
    def presence_var(self):
        return self.vars[ModelParams.ALT_PRESENCE]

    @property
    def interval_var(self):
        return self.vars[ModelParams.INTERVAL]

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
    def fixed_duration(self):
        return self.info[Params.FIXED_DURATION]

    @property
    def is_productivity(self):
        return self.info[Params.IS_PRODUCTIVITY]

    @property
    def productivity(self):
        return self.info[Params.PRODUCTVITY]