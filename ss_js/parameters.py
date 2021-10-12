from enum import Enum


class Params(Enum):
    LABOR_ID = "labor_id"
    LABOR_NAME = "labor_name"
    LABOR_NUMBER = "number"
    ZONE_ID = "zone_id"
    ZONE_NAME = "zone_name"
    TASK_ID = "task_id"
    TASK_NAME = "task_name"
    DURATION = "duration"
    # deprecated
    TASK_LIST = "task_list"
    # deprecated
    TASK_DEPENDENCY = "task_dependency"
    LABOR_SET = "labor_set"
    REQUIRED_LABOR = "required"
    ALT_ID = "alt_id"
    # deprecated
    LAST_TASK_TYPE = "last_task_type" 
    SPACE_ID = "space_id" 
    SPACE_NAME = "space_name"
    PRODUCTVITY = "productivity"
    QUANTITY = "quantity"


class ComponentParams(Enum):
    LABOR_TYPE = "labor_type"
    ZONE = "zone"
    TASK_TYPE = "task_type"
    LABOR = "labor"
    ALTER = "alt"
    SPACE = "space"
    DEPENDENCY = "dependency"    


class ModelParams(Enum):
    START = 'start'
    DURATION = 'duration'
    END = 'end'
    INTERVAL = 'interval'
    LABOR_PRESENCE = 'labor_presence'
    ALT_PRESENCE = 'alt_presence'
    SPACE_PRESENCE = 'space_presence'
    