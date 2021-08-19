from parameters import ComponentParams, Params
from components import Zone, LaborType, TaskType, Labor, Task


class GeneralUtils(object):
    pass


class Generate(object):
    @staticmethod
    def labor_type_dict(env, data):
        labor_dict = data.get(ComponentParams.LABOR.value)
        for labor_info in labor_dict.values():
            labor_type = LaborType(labor_info)
            env.labor_type_dict[labor_type.id] = labor_type
            env.labor_type_num[labor_type.id] = labor_info.get(Params.LABOR_NUMBER.value)
            env.labor_pool[labor_type.id] = []
        return

    @staticmethod
    def task_type_dict(env, data):
        task_dict = data.get(ComponentParams.TASK.value)
        for task_info in task_dict.values():
            task = TaskType(task_info)
            env.task_type_dict[task.id] = task
        return
    
    @staticmethod
    def zone_dict(env, data):
        zone_dict = data.get(ComponentParams.ZONE.value)
        for zone_info in zone_dict.values():
            zone = Zone(zone_info)
            env.zone_dict[zone.id] = zone           
        # TODO - check data exception
        return

    @staticmethod
    def labor_pool(env):        
        for labor_type_id, num in env.labor_type_num.items():
            for i in range(0, num):
                labor = Labor(str(i), env.labor_type(labor_type_id))
                env.labor_pool[labor.type_id].append(labor)
        return

    @staticmethod
    def task_pool(env):
        for zone in env.zone_dict.values():
            for task_type_str in zone.task_type_dependency:
                task_type = env.task_type_dict[task_type_str]
                task = Task(zone.id, task_type)
                for labor_type_id in task.required_labor_set.keys():
                    labor_type = env.labor_type_dict[labor_type_id]
                    labor_list = env.labor_pool[labor_type.id]
                    task.alter_labor_dict[labor_type.id] = labor_list                    
                
                zone.task_dependency.append(task)
        return