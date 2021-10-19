import json
from ss_js.schedule.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.optimize.optimizer import OptimizerCallback
from ss_js import io
from ss_js.optimize import chart
import sys

folder_name = sys.argv[1]
monitoring_cycle = int(sys.argv[2])
target_obj = int(sys.argv[3])


save_dir = "experiment/"+folder_name
# file_path = save_dir+"/input/input.xlsx"
# generated_path = save_dir+"/input/input.json"
file_path = save_dir+"/input/"+folder_name+".xlsx"
generated_path = save_dir+"/input/input.json"

# io.generate_json(file_path, generated_path)

with open(generated_path, 'r', encoding="utf-8") as f:
    json_data = json.load(f)

schedule = Schedule(json_data)

print('schedule generated, optimization start')
solver = cp_model.CpSolver()
opti_callback = OptimizerCallback(
    schedule=schedule, 
    target_obj=target_obj,
    monitoring_cycle=monitoring_cycle, 
    save_dir=save_dir+"/output"
)
solver.SolveWithSolutionCallback(schedule, opti_callback)
