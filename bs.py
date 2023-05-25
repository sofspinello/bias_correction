from cmethods import CMethods as cm
import xarray as xr

class BiasCorrection():
    
    def __init__(self, reference, model, data_to_be_corrected): 
        self.reference=reference
        self.model=model
        self.data_to_be_corrected=data_to_be_corrected   
        
        if self.check_baseline(self.reference) and self.check_baseline(self.model):
            print('Please choose one valid baseline, that is not less than 5')
            raise ValueError
        
    def quantile_mapping(self, var_obs, var_sim, n_quantiles):
        """_summary_

        Args:
            var_obs (_type_): _description_
            var_sim (_type_): _description_
            n_quantiles (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        print('Reference data to dataframe')
        reference=self.reference.to_dataframe().dropna(how='all')
        print('Model data to dataframe')
        model=self.model.to_dataframe().dropna(how='all')
        data_to_be_corrected= self.data_to_be_corrected.to_dataframe().dropna(how='all')
        print('Applyijg Bias Correction')
        qm_adjusted = cm.quantile_mapping(obs=reference[var_obs], simh=model[var_sim], 
                                          simp=data_to_be_corrected[var_sim], n_quantiles=n_quantiles)
        print('Creating output dataset')
        ds_adjusted = self.create_dataArray(qm_adjusted, var_sim)
        
        return ds_adjusted
    
    def create_dataArray(self, data_array, var_sim):
        """

        Args:
            data_array (_type_): _description_
            var_sim (_type_): _description_

        Returns:
            _type_: _description_
        """
        data_array = data_array.reshape(len(self.data_to_be_corrected.time.values), 
                                        len(self.data_to_be_corrected.latitude), 
                                        len(self.data_to_be_corrected.longitude))
        
        ds_adjusted = xr.DataArray (data_array, dims=["time","latitude", "longitude"], coords=[self.data_to_be_corrected.time,
                                                                                self.data_to_be_corrected.latitude,
                                                                                self.data_to_be_corrected.longitude])
        
        ds_adjusted.name = var_sim
        return ds_adjusted
    
    def write(self, ds, path_name):
        """_summary_

        Args:
            ds (_type_): _description_
            path_name (_type_): _description_
        """
        print('Saving in to the disk')
        ds.to_netcdf(path_name+'.nc')

    def check_baseline(self, dataset):
        """_summary_

        Args:
            dataset (_type_): _description_

        Returns:
            _type_: _description_
        """
        timestep = dataset['time']
        first_year = timestep.dt.year[0]
        last_year = timestep.dt.year[-1]
        baseline = last_year - first_year + 1
        
        return baseline < 5
       
