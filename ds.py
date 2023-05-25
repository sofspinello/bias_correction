
from abc import abstractmethod
import xarray as xr 

class DS():
    
    def __init__(self, variable, data_source_path, name):
        
        self.variable=variable
        self.data_source_path=data_source_path
        self.name = name
        
        #self.year = time[:4]
        #self.month= time[5:7]
        #self.day = time[8:10]
    
    @property
    def latitude(self):
        return self.coordinates["latitude"]
    
    @property 
    def longitude(self):
        return self.coordinates["longitude"]
    
    @property 
    def timestep(self):
        return self.coordinates["time"]
    
    def __repr__(self):
        print("")
        return str(self)
    
    @abstractmethod
    def get_filepath(self):
        pass
    
    def open_ds(self):
        ds=xr.open_mfdataset(self.filepath)
        return ds
    
    def open_da(self):
        da=xr.open_dataarray(self.filepath)
        return da
