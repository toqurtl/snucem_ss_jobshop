from ss_js.parameters import ModelParams, Params
from ortools.sat.python import cp_model


class Alter(object):
    def __init__(self, alt_id, model: cp_model.CpModel):
        self.id = alt_id        
        self.info = {
            Params.REQUIRED_LABOR: None, # labor_type_id, num
            Params.DURATION: None,
            Params.PRODUCTVITY: None
        }  
        self.vars = {
            ModelParams.ALT_PRESENCE: None,
            ModelParams.START: None,
            ModelParams.DURATION: None,
            ModelParams.END: None,
            ModelParams.INTERVAL: None
        }
        # labor_type_id: {labor_id: labor}
        self.labor_dict = {}

    def set_required_labor(self, required_labor_dict):
        self.info[Params.REQUIRED_LABOR] = required_labor_dict
        for labor_type_id in self.labor_type_id_list():
            self.labor_dict[labor_type_id] = {}
        return

    def set_duration(self, duration):
        self.info[Params.DURATION] = duration
        return
    
    def set_productivity(self, productivity):
        self.info[Params.PRODUCTVITY] = productivity

    def set_var(self, model: cp_model.CpModel, horizon):
        self.vars[ModelParams.ALT_PRESENCE] = model.NewBoolVar('presence_'+self.id)
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