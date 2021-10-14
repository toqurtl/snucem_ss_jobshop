import json
from ss_js.schedule.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.optimize.optimizer import OptimizerCallback


file_path = "data/generated.json"
with open(file_path, 'r', encoding="utf-8") as f:
    json_data = json.load(f)

schedule = Schedule(json_data)
solver = cp_model.CpSolver()
opti_callback = OptimizerCallback(
        schedule=schedule, 
        target_obj=1700,
        monitoring_cycle=10, 
        save_dir="experiment"
    )

solver.SolveWithSolutionCallback(schedule, opti_callback)