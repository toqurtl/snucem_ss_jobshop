from ss_js.env.schedule import Schedule
from ss_js.parameters import Params

def task_info(schedule: Schedule):
    for task in schedule.task_dict.values():
        print(task.alt_labor_set_dict)
    return

# 각 alter와 관련된 labor들을 출력
def labor_related_alter(schedule: Schedule):
    for task in schedule.task_dict.values():
        for alt_id, alt_info in task.alt_labor_set_dict.items():
            for labor_type_id, labor_num in alt_info[Params.REQUIRED_LABOR].items():                
                labor_list = schedule.labor_list_of_type(labor_type_id)
                print(alt_id, [labor.id for labor in labor_list], end=" ")
            print()
    return
    
def labor_related_alter_interval_var(schedule: Schedule):
    for labor in schedule.labor_dict.values():
        print(labor.interval_var_dict)