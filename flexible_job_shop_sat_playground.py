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


def flexible_zoneshop():
    """Solve a small flexible zoneshop problem."""
    # Data part.
    zones = [  # task = (processing_time, labor_id)
        [  # Zone 0
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # Zone 1
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # Zone 2
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # Zone 3
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A0 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A1 with 8 alternatives
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],  # A2 with 8 alternatives
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)],  # A3 with 8 alternatives
            [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15)],  # A4 with 8 alternatives
            [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)],  # A5 with 8 alternatives
        ],
        [  # Zone 4
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
    #     # Create one list of assigned tasks per labor.
    #     assigned_zones = collections.defaultdict(list)
    #     for zone_id, zone in enumerate(zones_data):
    #         for task_id, task in enumerate(zone):
    #             labor = task[0]
    #             assigned_zones[labor].append(
    #                 assigned_task_type(
    #                     start=solver.Value(all_tasks[zone_id, task_id].start),
    #                     zone=zone_id,
    #                     index=task_id,
    #                     duration=task[1]))

    #     # Create per labor output lines.
    #     print('User time: %.2fs' % solver.UserTime())
    #     print('Wall time: %.2fs' % solver.WallTime())
    #     print('Optimal Schedule Length: %i' % solver.ObjectiveValue())

    #     # Draw GanttChart
    #     df = []
    #     today = dt.today()
    #     start_date = dt(today.year,today.month,today.day)
    #     for labor in all_labors[::-1]:
    #         # Sort by starting time.
    #         assigned_zones[labor].sort()
    #         for assigned_task in assigned_zones[labor]:
    #             #name = 'zone_%i_%i' % (assigned_task.zone, assigned_task.index)
    #             start = assigned_task.start
    #             duration = assigned_task.duration
    #             df.append(dict(Task="M%s" % (labor + 1), Start=start_date + time_delta(0, start),
    #                            Finish=start_date + time_delta(0, start + duration),
    #                            Resource="%s" % (assigned_task.zone + 1), complete=assigned_task.zone + 1))
    #     colors = {}
    #     for i in range(n):
    #         key = "%s" % (i + 1)
    #         colors[key] = "rgb(%s, %s, %s)" % (rgb(), rgb(), rgb())
    #     fig = ff.create_gantt(df, colors=colors, index_col='Resource', group_tasks=True, show_colorbar=True)
    #     pyplt(fig, filename=r"./GanttChart.html", auto_open=False)

    # Print final solution.
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
            print(
                '  A%i starts at %i (alt %i, Labor %i, Duration %i)' %
                (task_id, start_value, selected, labor, duration))

    print('Solve status: %s' % solver.StatusName(status))
    print('Optimal objective value: %i' % solver.ObjectiveValue())
    print('Statistics')
    print('  - conflicts : %i' % solver.NumConflicts())
    print('  - branches  : %i' % solver.NumBranches())
    print('  - wall time : %f s' % solver.WallTime())


flexible_zoneshop()
