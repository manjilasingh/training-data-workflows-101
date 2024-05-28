import dataretrieval.nwis as nwis
from s3fs import S3FileSystem, S3Map
import xarray as xr

def acquire_streamflow_nwis_iv(site, start, end):
    df = nwis.get_record(sites=site, service='iv', start=start, end=end, parameterCD='00060')
    # https://help.waterdata.usgs.gov/parameter_cd?group_cd=PHY
    return df['00060'].rename('streamflow (ft^3/s)')

def acquire_streamflow_nwm_retrospective(site, start, end):
    bucket = 's3://noaa-nwm-retrospective-3-0-pds/CONUS/zarr'
    fs = S3FileSystem(anon=True)
    ds = xr.open_dataset(S3Map(f"{bucket}/chrtout.zarr", s3=fs), engine='zarr')

    ds = ds.sel({'feature_id': site})
    ds = ds.sel(time=slice(f'{start}T00:00:00', f'{end}T00:00:00'))

    return ds.get('streamflow').to_pandas().rename('streamflow (m^3 s^-1)')

def resample_to_daily(df):
    return df.resample('1D').mean()

def visualize_summary_statistics(df):
    print(df.describe())

