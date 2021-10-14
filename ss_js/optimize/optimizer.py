from ortools.sat.python import cp_model
from ss_js.optimize.schedule_result import ScheduleResult


class OptimizerCallback(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, schedule=None, target_obj=1700, monitoring_cycle=10, save_dir=""):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0
        self.schedule = schedule
        self.target_obj = target_obj  
        self.monitoring_cycle = monitoring_cycle
        self.save_dir = save_dir      

    def on_solution_callback(self):
        """Called at each new solution."""
        print('Solution %i, time = %f s, objective = %i' %
              (self.__solution_count, self.WallTime(), self.ObjectiveValue()))
        if self.__solution_count % self.monitoring_cycle == 0:  
            sr = ScheduleResult()            
            sr.set_task_dict(self, self.schedule)
            sr.set_task_list_of_solution(self, self.schedule)            
            sr.save(self.save_dir+"/solution"+str(self.__solution_count))
            
        if self.ObjectiveValue() < self.target_obj:
            self.StopSearch()
            
        self.__solution_count += 1
        
        return
        