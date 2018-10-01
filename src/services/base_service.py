
class BaseService():

    def __init__(self, p=None):
        self.p = p
        self.init_params( )


    def init_params(self, params=None):
        if (params):
            self.p = params

        self.allModels_process = self.p['allModels_process']
        self.nModels = self.p['nModels']
