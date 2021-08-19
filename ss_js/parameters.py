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
    REQUIRED_LABOR_SET = "required_labor_set"


class ComponentParams(Enum):
    LABOR = "labor"
    ZONE = "zone"
    TASK = "task"


class ModelParams(Enum):
    START = 'start'
    DURATION = 'duration'
    END = 'end'
    INTERVAL = 'interval'
    PRESENCE = 'presence'