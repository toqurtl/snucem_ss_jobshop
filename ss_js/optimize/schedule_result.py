from ss_js.parameters import Params
import json


class ScheduleResult(object):
    def __init__(self):
        self.num_labor_dict = {} # t:{labor_type_id: num_labor}
        self.task_dict = {} # t: task, alter_dict
        self.labor_dict = {} # type_id: [1,2,3,4,5]
        self.result_data = []
        self.figure_data = []
        self.task_result_data = []

    def set_task_list_of_solution(self, callback, schedule):        
        for task in schedule.task_dict.values():            
            data = {}
            start_value, end_value = callback.Value(task.start_var), callback.Value(task.end_var)                          
            selected_alter = None
            for alter in task.alt_dict.values():
                if callback.Value(alter.presence_var):
                    selected_alter = alter

            for labor_type, num_labor in selected_alter.info[Params.REQUIRED_LABOR].items():
                pass
                
            data['task_id'] = task.id
            data['section'] = task.section
            data['start_value'] = start_value
            data['end_value'] = end_value
            data['duration'] = selected_alter.info[Params.DURATION]
            data['num_labor'] = num_labor
            data['labor_type'] = labor_type
            data['productivity'] = selected_alter.info[Params.PRODUCTVITY]
            data['workpackage_id'] = task.workpackage_id           
            self.task_result_data.append(data)

        return
    
    # 시간별 task
    def set_task_dict(self, callback, schedule):
        makespan = callback.ObjectiveValue()        
        for time in range(0, int(makespan)):
            self.task_dict[time] = {}
            self.num_labor_dict[time] = {}
            for task in schedule.task_dict.values():
                self.put_alter_of_task_at_time(task, time, callback)
        return
                
    def put_alter_of_task_at_time(self, task, time, callback):        
        for alter in task.alt_dict.values():
            if callback.Value(alter.presence_var):
                start_value, end_value = callback.Value(task.start_var), callback.Value(task.end_var)
                if start_value <= time < end_value:
                    self.task_dict[time][task.id] = {
                        "space_id": task.space_id_list,
                        "section": task.section
                    }
                    self.put_num_labor_dict_of_alter_at_time(time, alter)
        return

    def put_num_labor_dict_of_alter_at_time(self, time, alter):
        for labor_type_id in alter.labor_type_id_list():
            if labor_type_id in self.num_labor_dict[time].keys():
                self.num_labor_dict[time][labor_type_id] += alter.num_labor_type(labor_type_id)
            else:
                self.num_labor_dict[time][labor_type_id] = alter.num_labor_type(labor_type_id)
        return

    def save(self, file_path):
        with open(file_path+"_tasklist.json", 'w', encoding="utf-8") as make_file:
            json.dump(self.task_dict, make_file, ensure_ascii=False, indent="\t")
        
        with open(file_path+"_tasktime.json", 'w', encoding="utf-8") as make_file:
            json.dump(self.task_result_data, make_file, ensure_ascii=False, indent="\t")

        with open(file_path+"_labortime.json", 'w', encoding="utf-8") as make_file:
            json.dump(self.num_labor_dict, make_file, ensure_ascii=False, indent="\t")
        return