import plotly as py
import plotly.figure_factory as ff
import pandas as pd
from ss_js import utils


def create_gantt(self, data_path, schedule):
    df = pd.DataFrame(self.figure_data)
    pyplt = py.offline.plot
    colors = {}
    for workpackage_id in schedule.workpackage_list():
        colors[workpackage_id] = utils.random_rgb_txt()

    fig = ff.create_gantt(
        df,
        colors= colors,
        index_col='Resource',
        show_colorbar = True,
        group_tasks = True
    )
    pyplt(fig, filename=data_path, auto_open=False)
    print("간트차트")
    return