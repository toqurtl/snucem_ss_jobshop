from ss_js.parameters import Params


class Space(object):
    def __init__(self, space_data):
        self.id = space_data.get(Params.SPACE_ID.value)
        self.name = space_data.get(Params.SPACE_NAME.value)
        
        self.task_list = []
        self.interval_var_list = []

    
