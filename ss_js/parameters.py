from enum import Enum


class Params(Enum):
    LABOR_ID = "labor_id"
    LABOR_NAME = "labor_name"
    LABOR_NUMBER = "number"
    ZONE_ID = "zone_id"    
    ZONE_NAME = "zone_name"
    WORK_ID = "work_id"
    TASKTYPE_ID = "task_type_id"    
    TASK_ID = "task_id"
    TASK_NAME = "task_name"
    DURATION = "duration"    
    TASK_LIST = "task_list" # deprecated
    TASK_DEPENDENCY = "task_dependency" # deprecated
    LABOR_SET = "labor_set"
    REQUIRED_LABOR = "required"
    ALT_ID = "alt_id"    
    LAST_TASK_TYPE = "last_task_type" # deprecated
    SPACE_ID = "space_id" 
    SPACE_NAME = "space_name"
    PRODUCTVITY = "productivity"
    QUANTITY = "quantity"
    SECTION = "section"
    WORKPACKAGE_ID = "workpackage_id"
    WORKPACKAGE_NAME = "workpackage_name"


class ComponentParams(Enum):
    LABOR_TYPE = "labor_type"
    ZONE = "zone"
    WORK = "work"
    TASK_TYPE = "task_type"
    LABOR = "labor"
    ALTER = "alt"
    SPACE = "space"
    DEPENDENCY = "dependency"  
    LAST_TASKTYPE = "last_tasktype_id" 


class ModelParams(Enum):
    START = 'start'
    DURATION = 'duration'
    END = 'end'
    INTERVAL = 'interval'
    LABOR_PRESENCE = 'labor_presence'
    ALT_PRESENCE = 'alt_presence'
    SPACE_PRESENCE = 'space_presence'
    
    