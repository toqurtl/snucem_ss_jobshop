import plotly as py
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
from ss_js import utils
from ss_js.schedule.schedule import Schedule
import json
import openpyxl


def task_list_to_excel(data_path, result_path):
    with open(data_path, 'r', encoding="utf-8") as f:
        task_list_data = json.load(f)
    col_names = ["task_id", "workpackage_id", "section", "space_id", "start_value", "end_value","duration", "labor_type", "num_labor", "productivity"]
    wb = openpyxl.Workbook()
    wb.create_sheet('task_list')    
    task_list_sheet = wb['task_list']    

    for seq, name in enumerate(col_names):
        task_list_sheet.cell(row=1, column=seq+1, value=name)
    
    for idx, data in enumerate(task_list_data):
        for seq, name in enumerate(col_names):            
            task_list_sheet.cell(row=idx+2, column=seq+1, value=data[name])
    
    wb.save(result_path)
    wb.close()
    return


def get_labor_time_col_list(labor_data):
    labor_list = ["time"]
    for labor_info in labor_data.values():
        for labor_type in labor_info.keys():
            if labor_type not in labor_list:
                labor_list.append(labor_type)
    return labor_list

def labor_time_to_excel(data_path, result_path):
    with open(data_path, 'r', encoding="utf-8") as f:
        labor_time_data = json.load(f)
    col_names = ["task_id", "workpackage_id", "section", "space_id", "start_value", "end_value","duration", "labor_type", "num_labor", "productivity"]
    wb = openpyxl.Workbook()    
    wb.create_sheet('labor_time')        
    labor_time_sheet = wb['labor_time']

    labor_time_col_list = get_labor_time_col_list(labor_time_data)

    for seq, name in enumerate(labor_time_col_list):
        labor_time_sheet.cell(row=1, column=seq+1, value=name)
    
    idx = 0    
    for time, labor_info in labor_time_data.items():
        for seq, labor_type_id in enumerate(labor_time_col_list):
            if seq == 0:
                labor_time_sheet.cell(row=idx+2, column=1, value=time)
            else: 
                if labor_type_id in labor_info.keys():
                    num_labor = labor_info[labor_type_id]
                    labor_time_sheet.cell(row=idx+2, column=seq+1, value=num_labor)
                else:
                    labor_time_sheet.cell(row=idx+2, column=seq+1, value=0)
        idx += 1
    
    wb.save(result_path)
    wb.close()
    return


def create_gantt(data_path, out_dir, schedule: Schedule):
    with open(data_path, 'r', encoding="utf-8") as f:
        json_data = json.load(f)

    figure_data = []
    workpackage_list = []
    section_list = []
    for data in json_data:        
        section = data['section']
        workpackage = data['workpackage_id']
        figure_data.append(dict(
            Task=data["task_id"],
            Start=data["start_value"],
            Finish=data['end_value'],
            Workpackage=data['workpackage_id'],
            Section=data['section']
        ))
        if section not in section_list:
            section_list.append(section)
        if workpackage not in workpackage_list:
            workpackage_list.append(workpackage)

    df = pd.DataFrame(figure_data)
    df['delta'] = df['Finish'] - df['Start']
    pyplt = py.offline.plot
    wp_colors = {}
    # for workpackage_id in schedule.workpackage_list():
    for workpackage_id in workpackage_list:
        wp_colors[workpackage_id] = utils.random_rgb_txt()
    
    sc_colors = {}
    # for section in schedule.section_list():
    for section in section_list:
        sc_colors[section] = utils.random_rgb_txt()

    fig = ff.create_gantt(
        df,
        colors= wp_colors,        
        index_col='Workpackage',
        show_colorbar = True,
        group_tasks = True
    )
    fig.layout.xaxis.type = 'linear'

    fig_2 = px.timeline(df, x_start="Start", x_end="Finish", color="Section")
    fig_2.layout.xaxis.type ='linear'
    fig_3 = ff.create_gantt(
        df,
        colors = sc_colors,
        index_col='Section',
        show_colorbar=True,
        group_tasks=True
    )
    fig_3.layout.xaxis.type = 'linear'

    pyplt(fig, filename=out_dir+"/workpackage_chart.html", auto_open=False)    
    pyplt(fig_3, filename=out_dir+"/section_chart.html", auto_open=False)  
    return