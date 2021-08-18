from parameters import Params

class Labor(object):
    def __init__(self, labor_data):
        self.labor_id = labor_data.get(Params.LABOR_ID.value)
        self.labor_name = labor_data.get(Params.LABOR_NAME.value)
    
    def __str__(self):
        return self.labor_id+"_"+self.labor_name


class Zone(object):
    def __init__(self, zone_data):
        self.zone_id = zone_data.get(Params.ZONE_ID.value)
        self.zone_name = zone_data.get(Params.ZONE_NAME.value)
        self.task_dependency_str = zone_data.get(Params.TASK_DEPENDENCY.value)
        self.task_dependency = []
    
    def __str__(self):
        return self.zone_id+"_"+self.zone_name

        
class Task(object):
    def __init__(self, task_data):
        self.task_id = task_data.get(Params.TASK_ID.value)
        self.task_name = task_data.get(Params.TASK_NAME.value)
        self.duration = task_data.get(Params.DURATION.value)
        self.required_labor_set = task_data.get(Params.REQUIRED_LABOR_SET.value)

    def __str__(self):
        return self.task_id+"_"+self.task_name