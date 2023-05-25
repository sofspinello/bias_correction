
import geopandas
from datetime import date
from dateutil.relativedelta import relativedelta
import xarray as xr
import numpy as np
#import hvplot

class Processing():
    def __init__(self, ds):
        self.ds=ds
        #self.method=method
        
    @property
    def latitude(self):
        return self.coordinates["latitude"]
    
    @property 
    def longitude(self):
        return self.coordinates["longitude"]
    
    def celsius_to_kelvin(self, variable):
        
        self.ds[variable] = self.ds[variable] + 273.15
        self.ds.attrs["units"]="Kelvin"
        
    def kelvin_to_celsuis(self, variable):
        """_summary_

        Args:
            variable (_type_): _description_
        """
        self.ds[variable] = self.ds[variable] - 273.15
        self.ds.attrs["units"]="Celsuis"
    
    def meters_to_millimeters(self, variable):
        """_summary_

        Args:
            variable (_type_): _description_
        """
        self.ds[variable] = self.ds[variable] * 1000
        self.ds.attrs["units"]="mm"
        
    def millimeters_to_meters(self,variable):
        self.ds[variable] = self.ds[variable] / 1000
        self.ds.attrs["units"] = "m"
        
    def sort_latitude(self):
        """_summary_
        """
        self.ds = self.ds.sortby('latitude')
    
    def interp(self, latitudes, longitudes):
        """_summary_

        Args:
            latitudes (_type_): _description_
            longitudes (_type_): _description_
        """
        self.ds = self.ds.interp(latitude = latitudes, longitude = longitudes)
        
    def slice_coords(self, latitudes, longitudes, shapefile):
        
        sf = geopandas.read_file(filename=shapefile)
        min_max_val = sf.total_bounds
        #estremi di latitudine
        lat_min = min_max_val[1]
        lat_max = min_max_val[3]
        #estremi di longitudine
        lon_min = min_max_val[0]
        lon_max = min_max_val[2]
        
        lats = [l for l in latitudes if l < lat_max and l > lat_min]
        lons = [l for l in longitudes if l < lon_max and l > lon_min]
        
        return lats, lons
        
        
    def interp_like(self, dataset, method):
        self.ds=self.ds.interp_like(dataset, method = method)
    
    def resample(self, aggregation, frequency):
        """_summary_

        Args:
            aggregation (_type_): _description_
            frequency (_type_): _description_

        Raises:
            TypeError: _description_
        """
        if aggregation=="min":
            self.ds=self.ds.resample(time=frequency).min()
        elif aggregation=="max":
            self.ds=self.ds.resample(time=frequency).max()
        elif aggregation=="mean":
            self.ds=self.ds.resample(time=frequency).mean()
        else:
            print("Please choose one valid aggregation method between [min, max,mean]")
            raise TypeError
    
    def selection_point_location(self,longitude, latitude, method='linear'):
        self.ds=self.ds.sel(self.latitude==latitude, self.longitude==longitude, method=method)
    
    def selection_area(self, method):
        #ds.tp.isel(latitude=slice(10))
        self.ds=self.ds.sel(latitude=slice(self.latitude[0], self.latitude[1]), longitude=slice(self.longitude[0],self.longitude[1]), method=method)
    
    def selection_year(self, year):
        self.ds=self.ds.sel(time=self.ds.time.dt.year==year)
        
    def selection_month(self, month):
        self.ds=self.ds.sel(time=self.ds.time.dt.month==month)
        
    def selection_day(self, day):
        self.ds=self.ds.sel(time=self.ds.time.dt.day==day)
    
    def selection_timestep(self):
        self.ds=self.ds.sel(timestep=self.timestep)
        
    def sel_time_slice(self, time_start, baseline=20):
        """_summary_

        Args:
            time_start (_type_): _description_
            baseline (int, optional): _description_. Defaults to 20.
        """
        year = int(time_start[:4])
        month= int(time_start[5:7])
        day = int(time_start[8:10])
        
        #if baseline < 5:
         #   print("Please choose one valid baseline, that is not less than 5")
          #  raise ValueError
            
        time_end = date(year,month,day) + relativedelta(years=baseline)
        time_slice = slice(time_start, time_end)
        
        self.ds=self.ds.sel(time=time_slice)
    
    def selection_region(self, shapefile, region):
        gds = geopandas.read_file(filename=shapefile)
        self.ds.rio.write_crs("epsg:4326", inplace=True)
        
        geometry = gds.query(f'NOME_REG == "{region}" ')['geometry']
        
        self.ds = self.ds.rio.clip(geometry.values, gds.crs)
        
    
    def selection_shp_area(self, shapefile):
        """_summary_

        Args:
            shapefile (_type_): _description_
        """
        shp_area = geopandas.read_file(filename=shapefile)
        
        min_max_val = shp_area.total_bounds
        
        self.ds = self.ds.sel(longitude=slice(min_max_val[0],min_max_val[2]), latitude=slice(min_max_val[1],min_max_val[3]))
    
    def selection_prov(self, shapefile):
        prov=geopandas.read_file(filename=shapefile)
        return prov
    
    def write_disk(self, path_name):
        """_summary_

        Args:
            path_name (_type_): _description_
        """
        self.ds.to_netcdf(path_name+'.nc')
        
        
    
