# schedule의 variable과 constraint를 세팅
# Variables와 constraint를 설정함
# 모델의 component
# task, alter, labortype, labor(향후 삭제할듯)

# Variable들의 종류
# variable_1) task 관련: start_var, end_var, duration_var, interval_var
# variable_2) alter 관련: alter_presence, start_var, end_var, duration_var, interval_var
#                * alter_presence: alter가 선택되었는 지 여부를 의미하는 bool 변수
# variable_3) labortype 관련: 각 labor_type에 demand(alter별 필요 인원)값들을 추가
# variable_4) labor 관련(향후 삭제할 듯): labor_presence (labor과 선택되었는지 여부 의미하는 bool 변수)

# Contraint
# constraint_1) task 간 dependency: previous_task.end_var <= task.start_var
# constraint_2) alter는 하나만 선택되어야 함: sum(alter_presence_list) == 1
# constraint_3) Task의 여러 alter 중 하나가 선택되면, task의 start/duration/end/interval은 alter의 것으로 세팅 (task.start_var == alter.start_var...) -> 
# constraint_4) labor_type은 특정 시간에 최대 지정된 명수를 넘을 수 없음 AddCumulative(labortype.interval_var_list, labortype.demand_list, labortype.num_labor)
# constraint_5) A labor can't be assigned to multiple tasks at the same time -> addNoOverLap

class Builder(object):
    def __init__(self, schedule, space_constraint=True):
        self.schedule = schedule
        self.space_constraint = space_constraint

    def set_var_and_constraints(self):
        # set variables
        self.set_vars_of_task()
        self.set_vars_of_alter()
        self.set_alter_dict()
        self.set_alter_presence_vars()
        self.allocate_interval_vars_to_labor()        
        # set constraints
        self.set_dependency_constraints()
        self.set_alter_constraints()
        self.set_interval_to_alter()
        self.set_cumulative()
        if self.space_constraint:            
            self.set_space_constraints()
        
        # set objective
        self.set_makespan_objective()
        return
     #################### set_var #######################
    # variable_1: task 관련
    def set_vars_of_task(self):
        for task in self.schedule.task_dict.values():            
            task.set_var(self.schedule, self.schedule.horizon)                      
        return

    # variable_2: alter 관련
    def set_vars_of_alter(self):
        for task in self.schedule.task_dict.values():
            for alt in task.alt_dict.values():
                alt.set_var(self.schedule, self.schedule.horizon)
        return

    # alter 세팅
    def set_alter_dict(self):
        for task in self.schedule.task_dict.values():
            for alter in task.alt_dict.values():
                self.schedule.alter_dict[alter.id] = alter
        return

    # space 세팅
    def set_space_of_dict(self):
        for zone in self.schedule.zone_dict.values():
            zone.set_var(self.schedule)

    # variable_1, 2: task/alter 관련(task_id에 해당하는 alter_presence_var들을 별도로 정리해둠: 향후 constraint를 쉽게 걸기 위함)
    def set_alter_presence_vars(self):
        for task_id, task in self.schedule.task_dict.items():        
            for alter in task.alt_dict.values():                
                self.schedule.alter_presence_vars[task_id].append(alter.presence_var)   
        return

    # zone들 중 마지막에 있는 task의 end_var을 별도로 저장
    def task_of_max_equality(self):
        task_list = []
        for task in self.schedule.task_dict.values():
            if task.type.id in self.schedule.env.last_tasktype_id:
                task_list.append(task.end_var)
        return task_list


    # 각 labor의 관련된 alt_interval들을 각 labor에 담아둠, set_labor_constraints와 관련된 것인데 향후 삭제할듯        
    def allocate_interval_vars_to_labor(self):
        for task in self.schedule.task_dict.values():
            for alter in task.alt_dict.values():            
                for labor_type_id in alter.labor_type_id_list():              
                    labor_type = self.schedule.labor_type_dict[labor_type_id]
                    labor_type.add_interval_var(alter.interval_var)
                    labor_type.add_demand(alter.num_labor_type(labor_type_id))                    
                            
        return

    ###################### constraints ###########################
    # constraint_1: task간 순서 관련 constraints(zone의 task_list list 순서)    
    def set_dependency_constraints(self):
        for pre_task, suc_task in self.schedule.dep_list:                      
            self.schedule.Add(pre_task.end_var <= suc_task.start_var)          
        return
    
    # constraint_2: 각 task의 alter들 중 하나만 선택되도록 하는 constraint
    def set_alter_constraints(self):
        for task_id, task in self.schedule.task_dict.items():            
            self.schedule.Add(sum(task.alt_presence_list()) == 1)
        return

    # constraint_3) Task의 여러 alter 중 하나가 선택되면, task의 start/duration/end/interval은 alter의 것으로 세팅
    def set_interval_to_alter(self):
        for task in self.schedule.task_dict.values():            
            for alter in task.alt_dict.values():                                 
                self.schedule.Add(task.start_var == alter.start_var).OnlyEnforceIf(alter.presence_var)
                self.schedule.Add(task.duration_var == alter.duration_var).OnlyEnforceIf(alter.presence_var)
                self.schedule.Add(task.end_var == alter.end_var).OnlyEnforceIf(alter.presence_var)
        return                 
    # constraint_4) labor_type은 특정 시간에 최대 지정된 명수를 넘을 수 없음
    def set_cumulative(self):
        for labortype in self.schedule.labor_type_dict.values():
            self.schedule.AddCumulative(labortype.interval_var_list, labortype.demand_list, labortype.num_labor)

    # space간 겹치지 않도록
    def set_space_constraints(self):
        for space in self.schedule.space_dict.values():
            for task in space.task_list:
                space.interval_var_list.append(task.interval_var)
            self.schedule.AddNoOverlap(space.interval_var_list)
        return

    # ====================== 최적화 목적 설정 ==============================
    def set_makespan_objective(self):
        makespan = self.schedule.NewIntVar(0, self.schedule.horizon, 'makespan')        
        self.schedule.AddMaxEquality(makespan, self.task_of_max_equality())
        self.schedule.Minimize(makespan)
        return
