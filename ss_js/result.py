from ss_js.env.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.parameters import Params
import datetime
import plotly as py
import plotly.figure_factory as ff
import pandas as pd


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def on_solution_callback(self):
        """Called at each new solution."""
        print('Solution %i, time = %f s, objective = %i' %
              (self.__solution_count, self.WallTime(), self.ObjectiveValue()))
        self.__solution_count += 1


class OptimalResult(object):
    def __init__(self, schedule: Schedule):
        self.solver = cp_model.CpSolver()                
        self.schedule = schedule
        self.status = self.solver.SolveWithSolutionCallback(self.schedule, SolutionPrinter())        
        
        # results
        self.num_labor_dict = {} # t:{labor_type_id: num_labor}
        self.task_dict = {} # t: task_id, alter_dict
        self.result_data = []
        self.figure_data = []

        self.labor_dict = {} # type_id: [1,2,3,4,5]        
        self.optimal_schedule()
        self.set_task_dict()
        return

    @property # 최적화 성공 여부
    def is_optimal(self):
        return self.status == cp_model.OPTIMAL

    @property
    def optimal_makespan(self):
        return int(self.solver.ObjectiveValue())

    

    def optimal_schedule(self):
        dt = datetime.datetime
        time_delta = datetime.timedelta
        today = dt.today()
        start_date = dt(today.year,today.month,today.day)
        # for zone in self.schedule.zone_dict.values():
            # for task in zone.task_list:
        for task in self.schedule.task_dict.values():            
            start_value = self.solver.Value(task.start_var)                
            end_value = self.solver.Value(task.end_var)                
            for alter in task.alt_dict.values():
                if self.solver.Value(alter.presence_var):
                    duration = alter.duration
                    selected = alter.id
                    labor_info = alter.info[Params.REQUIRED_LABOR]
            self.figure_data.append(dict(
                Task=task.id,
                Start= start_date + time_delta(0, start_value),
                Finish=start_date + time_delta(0, end_value),
                # complete=zone.id,
                Resource=task.space_id_list[0]
            ))
            
            self.result_data.append([task.id, selected, start_value, end_value, labor_info])
        return

    def create_gantt(self, data_path):
        df = pd.DataFrame(self.figure_data)
        pyplt = py.offline.plot
        colors = {
            'm_cme4_1': 'rgb(255,0,0)',
            'm_cme4_2': 'rgb(0, 255, 0)'
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
        makespan = self.solver.ObjectiveValue()        
        for time in range(0, int(makespan)):
            self.task_dict[time] = {}
            self.num_labor_dict[time] = {}
            for task in self.schedule.task_dict.values():
                self.put_alter_of_task_at_time(task, time)
        return
                
    def put_num_labor_dict_of_alter_at_time(self, time, alter):
        for labor_type_id in alter.labor_type_id_list():
            if labor_type_id in self.num_labor_dict[time].keys():
                self.num_labor_dict[time][labor_type_id] += alter.num_labor_type(labor_type_id)
            else:
                self.num_labor_dict[time][labor_type_id] = alter.num_labor_type(labor_type_id)
        return


    def put_alter_of_task_at_time(self, task, time):        
        for alter in task.alt_dict.values():
            if self.solver.Value(alter.presence_var):
                start_value, end_value = self.solver.Value(task.start_var), self.solver.Value(task.end_var)
                if start_value <= time < end_value:
                    self.task_dict[time] = (task.id, alter.id)
                    self.put_num_labor_dict_of_alter_at_time(time, alter)
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





