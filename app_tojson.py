import json
from ss_js.schedule.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.optimize.optimizer import OptimizerCallback
from ss_js import io
from ss_js.data.converter import Converter
from ss_js.optimize import chart
import sys
import os

inter_duration = 100
folder_name = sys.argv[1]
if len(sys.argv) == 3:
    interference = sys.argv[2] == "true"
elif len(sys.argv) == 4:
    inter_duration = int(sys.argv[3]) 
else:
    interference = False



save_dir = "experiment/"+folder_name
save_file_name = ""
num_excel=0
for file_name in os.listdir(save_dir+"/input"):
    experiiment_name=file_name.split(".")[0]
    if file_name.split(".")[1] == "xlsx":
        num_excel += 1
        if num_excel > 1:
            print('엑셀파일은 하나여야 함')
            exit()
        save_file_name = file_name

file_path = save_dir+"/input/"+save_file_name
generated_path = save_dir+"/input/input.json"

# file_path = save_dir+"/input/input_whole.xlsx"
generated_path = save_dir+"/input/input.json"

print(file_path)
cvt = Converter(file_path)
if interference:
    target_tasktype_list = ["A3", "A4", "A5"]
    inter_info = {
        "task_id": "I1",
        "workpackage_id": "I",
        "workpackage_name": "간섭",
        "detail_id": 0,
        "task_name": "간섭1",
        "is_module": False,
        "labor_set": [
            {
                "alt_id": 0,
                "required": {
                    "l99": 1
                },
                "productivity": 0.03,
                "is_productivity": False,
                "fixed_duration": inter_duration
            }
        ]
    }

    data = cvt.add_interference(inter_info, target_tasktype_list, rate=0.3)

cvt.generate_json(generated_path)
# io.generate_json(file_path, generated_path)

