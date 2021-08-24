from ss_js.env.schedule import Schedule
from ortools.sat.python import cp_model


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

    def labor_presence_result(self):
        for alter in self.schedule.alter_dict.values():
            for labor_type_id, labor_dict in alter.labor_dict.items():
                alter_pre = self.Value(alter.presence_var)
                print(alter.id, alter_pre, labor_type_id)
                for labor in labor_dict.values():                              
                    print(self.Value(labor.labor_presence_var(alter.id)), end=" ")
                print()







