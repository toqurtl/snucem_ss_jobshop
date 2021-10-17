import json
from ss_js.schedule.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.optimize.optimizer import OptimizerCallback
from ss_js import io
from ss_js.optimize import chart
import sys

folder_name = sys.argv[1]
solution_ctn = sys.argv[2]

save_dir = "experiment/"+folder_name
file_path = save_dir+"/input/input.xlsx"
generated_path = save_dir+"/input/input.json"


with open(generated_path, 'r', encoding="utf-8") as f:
    json_data = json.load(f)

schedule = Schedule(json_data)


## chart

chart.create_gantt(save_dir+"/output/solution"+solution_ctn+"_tasklist.json", 
    save_dir+"/result/solution"+solution_ctn+"_", schedule
)
print("gantt chart generated")
# excel
json_tasklist_path = save_dir+"/output/solution"+solution_ctn+"_tasklist.json"
excel_tasklist_path = save_dir+"/result/solution"+solution_ctn+"_tasklist"
chart.task_list_to_excel(json_tasklist_path, excel_tasklist_path)
print("task_list_excel file generated")

json_labortime_path = save_dir+"/output/solution"+solution_ctn+"_labortime.json"
excel_labortime_path = save_dir+"/result/solution"+solution_ctn+"_labortime"
chart.labor_time_to_excel(json_labortime_path, excel_labortime_path)
print("labor_time excel file generated")

chart.create_labor_chart(
    save_dir+"/output/solution"+solution_ctn+"_labortime.json",
    save_dir+"/result/solution"+solution_ctn+"_"
)
print("labor chart generated")