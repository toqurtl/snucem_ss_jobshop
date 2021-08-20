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
    TASK_DEPENDENCY = "task_dependency"
    LABOR_SET = "labor_set"
    REQUIRED_LABOR = "required"
    ALT_ID = "alt_id"   


class ComponentParams(Enum):
    LABOR_TYPE = "labor_type"
    ZONE = "zone"
    TASK_TYPE = "task_type"


class ModelParams(Enum):
    START = 'start'
    DURATION = 'duration'
    END = 'end'
    INTERVAL = 'interval'
    PRESENCE = 'presence'