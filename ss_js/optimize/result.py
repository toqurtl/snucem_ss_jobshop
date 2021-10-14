from ss_js.schedule.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.parameters import Params
import datetime
import plotly as py
import plotly.figure_factory as ff
import pandas as pd


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, schedule: Schedule, target_obj = 2000, monitoring_cycle = 10):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0
        self.schedule = schedule
        self.target_obj = target_obj  
        self.monitoring_cycle = monitoring_cycle
        # results
        self.num_labor_dict = {} # t:{labor_type_id: num_labor}
        self.task_dict = {} # t: task_id, alter_dict
        self.result_data = []
        self.figure_data = []
        self.labor_dict = {} # type_id: [1,2,3,4,5]   

    def on_solution_callback(self):
        """Called at each new solution."""
        print('Solution %i, time = %f s, objective = %i' %
              (self.__solution_count, self.WallTime(), self.ObjectiveValue()))                   
        
        # 확인하고 싶은 데이터 저장
        if self.__solution_count % self.monitoring_cycle == 0:                        
            self.set_task_dict()
            # print(self.get_work_data_of_solution())
            # for time, task in self.task_dict.items(): 
            #     print(time, task)
            # for time, labor_info in self.num_labor_dict.items():
            #     print(time, labor_info)
            
        if self.ObjectiveValue() < self.target_obj:
            self.StopSearch()
            
        self.__solution_count += 1
    
    def get_work_data_of_solution(self):
        # dt = datetime.datetime
        # time_delta = datetime.timedelta
        # today = dt.today()
        # start_date = dt(today.year,today.month,today.day)
        result_data = []
        for task in self.schedule.task_dict.values():            
            start_value = self.Value(task.start_var)                
            end_value = self.Value(task.end_var)                
            for alter in task.alt_dict.values():
                if self.Value(alter.presence_var):
                    duration = alter.duration
                    selected = alter.id
                    labor_info = alter.info[Params.REQUIRED_LABOR]           
            result_data.append([task.id, start_value, end_value, labor_info])        
        return result_data

    def create_gantt(self, data_path):
        df = pd.DataFrame(self.figure_data)
        pyplt = py.offline.plot
        colors = {
            'cme4': 'rgb(255,0,0)',
            'cep13': 'rgb(0,255,0)',
            'cme5': 'rgb(0,0,255)',                 
        }
        fig = ff.create_gantt(
            df,
            colors= colors,
            index_col='Resource',
            show_colorbar = True,
            group_tasks = True
        )
        pyplt(fig, filename=data_path, auto_open=False)
        return
    
    # 시간별 task
    def set_task_dict(self):
        makespan = self.ObjectiveValue()        
        for time in range(0, int(makespan)):
            self.task_dict[time] = {}
            self.num_labor_dict[time] = {}
            for task in self.schedule.task_dict.values():
                self.put_alter_of_task_at_time(task, time)
        return
                
    def put_alter_of_task_at_time(self, task, time):        
        for alter in task.alt_dict.values():
            if self.Value(alter.presence_var):
                start_value, end_value = self.Value(task.start_var), self.Value(task.end_var)
                if start_value <= time < end_value:
                    self.task_dict[time][task.id] = (task.space_id, alter)
                    self.put_num_labor_dict_of_alter_at_time(time, alter)
        return

    def put_num_labor_dict_of_alter_at_time(self, time, alter):
        for labor_type_id in alter.labor_type_id_list():
            if labor_type_id in self.num_labor_dict[time].keys():
                self.num_labor_dict[time][labor_type_id] += alter.num_labor_type(labor_type_id)
            else:
                self.num_labor_dict[time][labor_type_id] = alter.num_labor_type(labor_type_id)
        return

    # 시간별 labor 숫자 관련
    def set_labor_allocation(self):
        for labor_type_id in self.num_labor_dict.keys():
            max_num = self.max_num_of_labor_type(labor_type_id)
            self.labor_dict[labor_type_id] = []
            for i in range(0, max_num):
                self.labor_dict[labor_type_id].append(labor_type_id+str(i))

    def max_num_of_labor_type(self, labor_type_id):
        num_labor_type_id_at_t_list = []
        for labor_info in self.num_labor_dict.values():            
            if labor_type_id in labor_info.keys():
                num_labor = labor_info[labor_type_id]
                num_labor_type_id_at_t_list.append(num_labor)        
        return max(num_labor_type_id_at_t_list)


