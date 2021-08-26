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
    def __init__(self, schedule: Schedule, solver: cp_model.CpSolver):
        self.solver = solver
        self.schedule = schedule
        self.solution_printer = SolutionPrinter()        
        self.num_labor_dict = {} # t:{labor_type_id: num_labor}
        self.task_dict = {} # t: task_id, alter_dict
        return

    def set_solution_printer(self):
        self.status = self.SolveWithSolutionCallback(self.schedule, self.solution_printer)

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

    # TODO
    def set_num_labor_dict(self):
        makespan = self.solver.ObjectiveValue()
        
        for t in range(0, int(makespan)):
            self.num_labor_dict[t] = {}            
            for labor_type in self.schedule.labor_type_dict.values():                
                for task in self.schedule.task_dict.values():
                    for alter in task.alt_dict.values():                                                
                        if self.solver.Value(alter.presence_var) and labor_type.id in alter.labor_type_id_list() :
                            start_value, end_value = self.solver.Value(task.start_var), self.solver.Value(task.end_var)                    
                            if start_value <= t < end_value:
                                self.num_labor_dict[t][labor_type.id] = alter.num_labor_type(labor_type.id)
        print(self.num_labor_dict)
        return

    def set_task_dict(self):
        makespan = self.solver.ObjectiveValue()        
        for t in range(0, int(makespan)):
            self.task_dict[t] = {}
            self.num_labor_dict[t] = {}
            for task in self.schedule.task_dict.values():
                 for alter in task.alt_dict.values():
                     if self.solver.Value(alter.presence_var):
                         start_value, end_value = self.solver.Value(task.start_var), self.solver.Value(task.end_var)
                         if start_value <= t < end_value:
                            self.task_dict[t] = (task.id, alter.id)
                            for labor_type_id in alter.labor_type_id_list():
                                if labor_type_id in self.num_labor_dict[t].keys():
                                    self.num_labor_dict[t][labor_type_id] += alter.num_labor_type(labor_type_id)
                                else:
                                    self.num_labor_dict[t][labor_type_id] = alter.num_labor_type(labor_type_id)

        print(self.num_labor_dict)
        print(self.task_dict)
                
    def create_gantt(self):
        df = pd.DataFrame(self.task_dict.values())
        fig = ff.create_gantt(
            df,
            index_col = 'Resource',
            show_colorbar = True,
            group_tasks = True
        )
    







