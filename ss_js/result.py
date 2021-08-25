from ss_js.env.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.parameters import Params


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


class OptimalResult(cp_model.CpSolver):
    def __init__(self, schedule: Schedule):
        self.schedule = schedule
        self.solution_printer = SolutionPrinter()
        self.status = self.SolveWithSolutionCallback(schedule, self.solution_printer)
        self.num_labor_dict = {} # t:{labor_type_id: num_labor}

    def optimal_schedule(self):
        for zone in self.schedule.zone_dict.values():
            for task in zone.task_dependency:
                start_value = self.Value(task.start_var)
                end_value = self.Value(task.end_var)
                for alter in task.alt_dict.values():
                    if self.Value(alter.presence_var):
                        duration = alter.duration
                        selected = alter.id
                        labor_info = alter.info[Params.REQUIRED_LABOR]
                print(task.id, selected, start_value, end_value, labor_info)

    # TODO
    def set_num_labor_dict(self, time, labor_type_id):
        makespan = self.solution_printer.ObjectiveValue()
        for t in range(0, makespan):
            self.num_labor_dict[t] = {}            
            for labor_type in self.schedule.labor_type_dict.values():
                for task in self.schedule.task_dict.values():
                    for alter in task.alt_dict.values():
                        if self.Value
                        start_value, end_value = self.Value(task.start_var), self.Value(task.end_var)
                    task
                    if start_value <= t < end_value:
                        self.num_labor_dict[t][labor_type.id] = num_labor
                
        

    







