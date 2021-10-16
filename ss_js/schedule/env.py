from ss_js.component.task import Task, TaskType
from ss_js.component.labor import Labor, LaborType
from ss_js.parameters import ComponentParams, Params

# Input 데이터를 받기 위한 class
# labor_type, task_type, labor 정보를 가지고 있음
class Environment(object):
    def __init__(self, data):         
        self.labor_type_dict = {} # str, labortype
        self.task_type_dict = {} # str, tasktype        
        self.zone_dict = {} # zone
        self.work_dict = {}
        self.task_dict = {}
        self.labor_dict = {} # (labor)
        self.section_list = []
        self.workpackage_list = []
        self.dep_list = []
        self.last_tasktype_id = []
        
        # 수정 1012
        self.space_dict = {}

        self._initialize(data)
        
    # =========================== 초기화를 위한 함수=====================================
    def _initialize(self, data):        
        self._generate_labor_type_dict(data)
        self._generate_task_type_dict(data)
        self._generate_space_dict(data)                
        self._generate_work_dict(data)
        self._generate_labor_dict()
        # self._generate_task_pool()
        self._generate_dependency_list(data)
        self.section_list = data.get(ComponentParams.SECTION.value)
        self.workpackage_list = data.get(ComponentParams.WORKPACKAGE.value)
        self.last_tasktype_id = data.get(ComponentParams.LAST_TASKTYPE.value)        
        
        return

    def _generate_dependency_list(self, data):
        dep_list = data.get(ComponentParams.DEPENDENCY.value)
        for dep in dep_list:
            pre_task = self.task_dict[dep[0]]
            suc_task = self.task_dict[dep[1]]
            self.dep_list.append((pre_task, suc_task))
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
    
    def _generate_work_dict(self, data):
        work_list = data.get(ComponentParams.WORK.value)
        for work_info in work_list:            
            task_type = self.task_type_dict[work_info[Params.TASKTYPE_ID.value]]
            task = Task(work_info, task_type)
            self.task_dict[task.id] = task
        return 
    
    # deprecated
    def _generate_space_dict(self, data):
        # space_list = data.get(ComponentParams.SPACE.value)
        # for space_info in space_list:
        #     space = Space(space_info)
        #     self.space_dict[space.id] = space
        return
    
    def _generate_labor_dict(self):        
        for labor_type_id, labor_type in self.labor_type_dict.items():
            for i in range(0, labor_type.num_labor):
                labor = Labor(str(i), labor_type_id, self)                
                self.labor_dict[labor.id] = labor
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
        for task in self.task_dict.values():            
            horizon += task.max_duration
        return horizon
