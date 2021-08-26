from ss_js.env.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.parameters import Params
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
        self.num_labor_dict = {} # t:{labor_type_id: num_labor}
        self.task_dict = {} # t: task_id, alter_dict
        return

    @property # 최적화 성공 여부
    def is_optimal(self):
        return self.status == cp_model.OPTIMAL

    @property
    def optimal_makespan(self):
        return int(self.solver.ObjectiveValue())

    def optimal_schedule(self):
        for zone in self.schedule.zone_dict.values():
            for task in zone.task_dependency:
                start_value = self.solver.Value(task.start_var)
                end_value = self.solver.Value(task.end_var)
                for alter in task.alt_dict.values():
                    if self.solver.Value(alter.presence_var):
                        duration = alter.duration
                        selected = alter.id
                        labor_info = alter.info[Params.REQUIRED_LABOR]
                print(task.id, selected, start_value, end_value, labor_info)

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

    def set_task_dict(self):
        makespan = self.solver.ObjectiveValue()        
        for time in range(0, int(makespan)):
            self.task_dict[time] = {}
            self.num_labor_dict[time] = {}
            for task in self.schedule.task_dict.values():
                self.put_alter_of_task_at_time(task, time)
        print(self.task_dict)
        print(self.num_labor_dict)
        return
                
    def create_gantt(self):
        df = pd.DataFrame(self.task_dict.values())
        fig = ff.create_gantt(
            df,
            index_col = 'Resource',
            show_colorbar = True,
            group_tasks = True
        )
    







