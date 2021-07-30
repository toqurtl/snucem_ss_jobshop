from __future__ import print_function
import chardet
import time
import datetime
import random
import collections
import plotly as py
import plotly.figure_factory as ff
# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model

dt = datetime.datetime
time_delta = datetime.timedelta
pyplt = py.offline.plot

def load_text(file_name):
    try:
        with open(file_name, "rb") as f:
            f_read = f.read()
            f_cha_info = chardet.detect(f_read)
            final_data = f_read.decode(f_cha_info['encoding'])
            return final_data, True
    except FileNotFoundError:
        return str(None), False

def rgb():
        return random.randint(0, 256)

#print(data)
def MinimalJobshopSat(string):
    a = list(map(int,string.split()))    
    n, machines_count = a[0], a[1]
    all_machines = range(machines_count)
    jobs_data = []
    job = []
    for i,(j,k) in enumerate(zip(a[2::2],a[3::2])):
        job.append((j,k))
        if (i+1) % machines_count == 0:
            jobs_data.append(job)
            job = []
    
    """Minimal jobshop problem."""
    # Create the model.
    model = cp_model.CpModel()
    
    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(task[1] for job in jobs_data for task in job)

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(
                start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.Value(all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1]))

        # Create per machine output lines.
        print('User time: %.2fs' % solver.UserTime())
        print('Wall time: %.2fs' % solver.WallTime())
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())

        # Draw GanttChart
        df = []
        today = dt.today()
        start_date = dt(today.year,today.month,today.day)
        for machine in all_machines[::-1]:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            for assigned_task in assigned_jobs[machine]:
                #name = 'job_%i_%i' % (assigned_task.job, assigned_task.index)
                start = assigned_task.start
                duration = assigned_task.duration
                df.append(dict(Task="M%s" % (machine + 1), Start=start_date + time_delta(0, start),
                               Finish=start_date + time_delta(0, start + duration),
                               Resource="%s" % (assigned_task.job + 1), complete=assigned_task.job + 1))
        colors = {}
        for i in range(n):
            key = "%s" % (i + 1)
            colors[key] = "rgb(%s, %s, %s)" % (rgb(), rgb(), rgb())
        fig = ff.create_gantt(df, colors=colors, index_col='Resource', group_tasks=True, show_colorbar=True)
        pyplt(fig, filename=r"./GanttChart.html", auto_open=False)
        
data, check = load_text("sample.txt")
print(data)
print(check)
if data is not None:
    MinimalJobshopSat(data)