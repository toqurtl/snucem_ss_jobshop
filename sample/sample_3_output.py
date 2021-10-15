import json
from ss_js.schedule.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.optimize.optimizer import OptimizerCallback
from ss_js import io
from ss_js.optimize import chart



save_dir = "experiment/light_experiment_0"
file_path = save_dir+"/input/input.xlsx"
generated_path = save_dir+"/input/input.json"

io.generate_json(file_path, generated_path)

with open(generated_path, 'r', encoding="utf-8") as f:
    json_data = json.load(f)

schedule = Schedule(json_data)
print('schedule generated, optimization start')
solver = cp_model.CpSolver()
opti_callback = OptimizerCallback(
    schedule=schedule, 
    target_obj=300,
    monitoring_cycle=10, 
    save_dir=save_dir+"/output"
)
solver.SolveWithSolutionCallback(schedule, opti_callback)

## chart

chart.create_gantt(save_dir+"/output/solution20_tasklist.json", save_dir+"/output", schedule)
# excel
json_tasklist_path = save_dir+"/output/solution20_tasklist.json"
excel_tasklist_path = save_dir+"/output/solution20_tasklist.xlsx"
chart.task_list_to_excel(json_tasklist_path, excel_tasklist_path)

json_labortime_path = save_dir+"/output/solution20_labortime.json"
excel_labortime_path = save_dir+"/output/solution20_labortime.xlsx"
chart.labor_time_to_excel(json_labortime_path, excel_labortime_path)
