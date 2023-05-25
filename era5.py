from ds import DS


class Era5(DS):
    
    def __init__(self, variable, data_source_path, name):
        super().__init__(variable, data_source_path, name)
        
    def get_filepath(self, filename=None):
        
        if not filename:
            self.filepath = self.data_source_path + self.name + self.variable + '/era5_*'
        else:
            self.filepath = self.data_source_path + filename
        

            
            

