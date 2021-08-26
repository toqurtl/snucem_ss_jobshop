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
import pandas as pd
import plotly.express as px
import csv

dt = datetime.datetime
time_delta = datetime.timedelta
pyplt = py.offline.plot


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def on_solution_callback(self):
        """Called at each new solution."""
        print('Solution %i, time = %f s, objective = %i' %
              (self.__solution_count, self.WallTime(), self.ObjectiveValue()))
        self.__solution_count += 1

def rgb():
    return random.randint(0, 256)

def flexible_zoneshop():
    """Solve a small flexible zoneshop problem."""
    # Data part.
    zones = [  # task = (processing_time, labor_id)
        [  # zone 0
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # zone 1
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # zone 2
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # zone 3
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # zone 4
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
    ]

    num_zones = len(zones)
    all_zones = range(num_zones)

    num_labors = 16
    all_labors = range(num_labors)

    # Model the flexible zoneshop problem.
    model = cp_model.CpModel()

    horizon = 0
    for zone in zones:
        for task in zone:
            max_task_duration = 0
            for alternative in task:
                max_task_duration = max(max_task_duration, alternative[0])
            horizon += max_task_duration

    print('Max Duration = %i' % horizon)

    # Global storage of variables.
    intervals_per_resources = collections.defaultdict(list)
    starts = {}  # indexed by (zone_id, task_id).
    presences = {}  # indexed by (zone_id, task_id, alt_id).
    zone_ends = []

    # Scan the zones and create the relevant variables and intervals.
    for zone_id in all_zones:
        zone = zones[zone_id]
        num_tasks = len(zone)
        previous_end = None
        for task_id in range(num_tasks):
            task = zone[task_id]

            min_duration = task[0][0]
            max_duration = task[0][0]

            num_alternatives = len(task)
            all_alternatives = range(num_alternatives)

            for alt_id in range(1, num_alternatives):
                alt_duration = task[alt_id][0]
                min_duration = min(min_duration, alt_duration)
                max_duration = max(max_duration, alt_duration)

            # Create main interval for the task.
            suffix_name = '_j%i_t%i' % (zone_id, task_id)
            start = model.NewIntVar(0, horizon, 'start' + suffix_name)
            duration = model.NewIntVar(min_duration, max_duration,
                                       'duration' + suffix_name)
            end = model.NewIntVar(0, horizon, 'end' + suffix_name)
            interval = model.NewIntervalVar(start, duration, end,
                                            'interval' + suffix_name)

            # Store the start for the solution.
            starts[(zone_id, task_id)] = start

            # Add precedence with previous task in the same zone.
            if previous_end is not None:
                model.Add(start >= previous_end)
            previous_end = end

            # Create alternative intervals.
            if num_alternatives > 1:
                l_presences = []
                for alt_id in all_alternatives:
                    alt_suffix = '_j%i_t%i_a%i' % (zone_id, task_id, alt_id)
                    l_presence = model.NewBoolVar('presence' + alt_suffix)
                    l_start = model.NewIntVar(0, horizon, 'start' + alt_suffix)
                    l_duration = task[alt_id][0]
                    l_end = model.NewIntVar(0, horizon, 'end' + alt_suffix)
                    l_interval = model.NewOptionalIntervalVar(
                        l_start, l_duration, l_end, l_presence,
                        'interval' + alt_suffix)
                    l_presences.append(l_presence)

                    # Link the master variables with the local ones.
                    model.Add(start == l_start).OnlyEnforceIf(l_presence)
                    model.Add(duration == l_duration).OnlyEnforceIf(l_presence)
                    model.Add(end == l_end).OnlyEnforceIf(l_presence)

                    # Add the local interval to the right labor.
                    intervals_per_resources[task[alt_id][1]].append(l_interval)

                    # Store the presences for the solution.
                    presences[(zone_id, task_id, alt_id)] = l_presence

                # Select exactly one presence variable.
                model.Add(sum(l_presences) == 1)
            else:
                intervals_per_resources[task[0][1]].append(interval)
                presences[(zone_id, task_id, 0)] = model.NewConstant(1)

        zone_ends.append(previous_end)

    # Create labors constraints.
    for labor_id in all_labors:
        intervals = intervals_per_resources[labor_id]
        if len(intervals) > 1:
            model.AddNoOverlap(intervals)

    # Makespan objective
    makespan = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(makespan, zone_ends)
    model.Minimize(makespan)

    # Solve model.
    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter()
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    

    # if status == cp_model.OPTIMAL:


    # Print final solution.
    result_zone_data = []
    
    today = dt.today()
    start_date = dt(today.year,today.month,today.day)

    for zone_id in all_zones:
        print('Zone %i:' % zone_id)        
        for task_id in range(len(zones[zone_id])):
            start_value = solver.Value(starts[(zone_id, task_id)])
            labor = -1
            duration = -1
            selected = -1
            for alt_id in range(len(zones[zone_id][task_id])):
                if solver.Value(presences[(zone_id, task_id, alt_id)]):
                    duration = zones[zone_id][task_id][alt_id][0]
                    labor = zones[zone_id][task_id][alt_id][1]
                    selected = alt_id
                    
                    result_zone_data.append(dict( # creating dictionary
                        Task="Labor %i" % labor,
                        Start=start_date + time_delta(0, start_value),
                        Finish=start_date + time_delta(0, start_value + duration),
                        Resource=task_id                  
                    )) 
            print(
                '  A%i starts at %i (alt %i, Labor %i, Duration %i)' %
                (task_id, start_value, selected, labor, duration))


    print(result_zone_data)
    
    df = pd.DataFrame(result_zone_data)

    colors = {}
    for i in range(n):
            key = "%s" % (i + 1)
            colors[key] = "rgb(%s, %s, %s)" % (rgb(), rgb(), rgb())

    fig = ff.create_gantt(
        df,
        index_col = 'Resource',
        show_colorbar = True,
        group_tasks = True
    )
    fig.show()

    exit()
    print('Solve status: %s' % solver.StatusName(status))
    print('Optimal objective value: %i' % solver.ObjectiveValue())
    print('Statistics')
    print('  - conflicts : %i' % solver.NumConflicts())
    print('  - branches  : %i' % solver.NumBranches())
    print('  - wall time : %f s' % solver.WallTime())

    # df = pd.DataFrame([
    #     dict(Task=labor, Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
    #     dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
    #     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    # ])

    # fig = px.timeline(df, x_start="Start", x_end="Finish", y="Resource", color="Resource")
    # fig.show()


flexible_zoneshop()
