from ss_js.env.component.task import Task, TaskType
from ss_js.env.component.labor import Labor, LaborType
from ss_js.env.component.zone import Zone
from ss_js.parameters import ComponentParams

# Input 데이터를 받기 위한 class
# labor_type, task_type, labor 정보를 가지고 있음
class Environment(object):
    def __init__(self, data):         
        self.labor_type_dict = {} # str, labortype
        self.task_type_dict = {} # str, tasktype        
        self.zone_dict = {} # zone
        self.task_dict = {}
        self.labor_dict = {} # (labor)

        self._initialize(data)
        
    # =========================== 초기화를 위한 함수=====================================
    def _initialize(self, data):
        self._generate_labor_type_dict(data)
        self._generate_task_type_dict(data)
        self._generate_zone_dict(data)
        self._generate_labor_dict()
        self._generate_task_pool()
        return

    def _generate_labor_type_dict(self, data):
        labor_type_list = data.get(ComponentParams.LABOR_TYPE.value)
        for labor_info in labor_type_list:
            labor_type = LaborType(labor_info)
            self.labor_type_dict[labor_type.id] = labor_type                        
        return
    
    def _generate_task_type_dict(self, data):
        task_type_list = data.get(ComponentParams.TASK_TYPE.value)        
        for task_type_info in task_type_list:
            task_type = TaskType(task_type_info)
            self.task_type_dict[task_type.id] = task_type            
        return

    def _generate_zone_dict(self, data):
        zone_list = data.get(ComponentParams.ZONE.value)
        for zone_info in zone_list:
            zone = Zone(zone_info)
            self.zone_dict[zone.id] = zone           
        # TODO - check data exception
        return
    
    def _generate_labor_dict(self):        
        for labor_type_id, labor_type in self.labor_type_dict.items():
            for i in range(0, labor_type.num_labor):
                labor = Labor(str(i), labor_type_id, self)                
                self.labor_dict[labor.id] = labor
        return

    def _generate_task_pool(self):
        for zone in self.zone_dict.values():
            for task_type_str in zone.task_type_dependency:                
                task_type = self.task_type_dict[task_type_str]
                task = Task(zone.id, task_type)
                self.task_dict[task.id] = task       
                zone.task_dependency.append(task)
        return

    # =========================== 데이터들을 정리해서 반환=====================================
    # labor_type_id를 input하면 labor에서 해당 labor들을 list 반환
    # deprecated
    def labor_list_of_type(self, labor_type_id):        
        return list(filter(lambda labor: labor.type_id == labor_type_id, self.labor_dict.values()))

    # labor_type_id를 input하면 해당 labor_type의 labor 수를 반환
    def num_labor_of_type(self, type: LaborType):
        return self.labor_type_dict[type.id].num_labor

    def labor_type(self, labor_type_str) -> LaborType:
        return self.labor_type_dict[labor_type_str]
        
    @property
    def max_horizon(self):
        horizon = 0        
        for zone in self.zone_dict.values():
            horizon += sum(map(lambda x: x.max_duration, zone.task_dependency))                   
        return horizon       
        # fun
        # return sum(map(lambda x: sum(map(lambda y: y.duration, x.task_dependency)), self.zone_dict.values()))
