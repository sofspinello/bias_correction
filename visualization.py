import matplotlib.pyplot as plt 
import geopandas as gpd
import xarray as xr

class Visualization():
    
    def __init__(self, da ):
        self.da = da
        
    def histogram(self):

        return self.da.plot()
        
    def first_map(self):
        
        return self.da.isel(time=0).plot(x="longitude")
        
        
    def mask_geoDataFrame(self, shp_path):
        """_summary_

        Args:
            shp_path (_type_): _description_
        """
        gdf_mask = gpd.read_file(shp_path)
        self.da.rio.write_crs("epsg:4326", inplace=True)
        self.da.rio.clip(gdf_mask.geometry.values, gdf_mask.crs)
        
    def hvplot_kde(self, line_width,  xlim, line_color, line_dash=None, fill_color=None ):
        """_summary_

        Args:
            line_width (_type_): _description_
            clim (_type_): _description_
            line_color (_type_): _description_
            fill_color (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return self.da.hvplot.kde(fill_color=fill_color, line_color=line_color, line_width=line_width, line_dash=line_dash, xlim=xlim)
   
    
    def hvplot_map(self, cmap, color):
        """_summary_

        Args:
            cmap (_type_): _description_
            color (_type_): _description_

        Returns:
            _type_: _description_
        """
        data_array = self.da[0, :, :].hvplot(geo=True, cmap=cmap)
        sp = self.mask_geoDataFrame.hvplot(geo=True, color=color)
        return data_array * sp



        
    