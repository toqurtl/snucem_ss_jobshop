import plotly as py
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
from ss_js import utils
from ss_js.schedule.schedule import Schedule
import json

def create_gantt(data_path, schedule: Schedule):
    with open(data_path, 'r', encoding="utf-8") as f:
        json_data = json.load(f)

    figure_data = []
    
    for data in json_data:        
        figure_data.append(dict(
            Task=data["task_id"],
            Start=data["start_value"],
            Finish=data['end_value'],
            Workpackage=data['workpackage_id'],
            Section=data['section']
        ))
        print(data['section'])
    df = pd.DataFrame(figure_data)
    df['delta'] = df['Finish'] - df['Start']
    pyplt = py.offline.plot
    wp_colors = {}
    for workpackage_id in schedule.workpackage_list():
        wp_colors[workpackage_id] = utils.random_rgb_txt()
    
    sc_colors = {}
    for section in schedule.section_list():
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

    pyplt(fig, filename="test.html", auto_open=False)
    pyplt(fig_2, filename="test_2.html", auto_open=False)  
    pyplt(fig_3, filename="test_3.html", auto_open=False)  
    return