from ds import DS

class Eobs(DS):   
    
    def __init__(self, variable, data_source_path, name):
        super().__init__(variable, data_source_path, name)
        
    def get_filepath(self, filename=None):
        
        if not filename:
            self.filepath = self.data_source_path + self.name + self.variable + '/tn_ens_mean_0.1deg_reg_v24.0e'
        else:
            self.filepath = self.data_source_path + filename