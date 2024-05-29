import dataretrieval.nwis as nwis
from s3fs import S3FileSystem, S3Map
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import holoviews as hv
import plotly.express as px

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

#######################################

def resample_to_daily(df):
    return df.resample('1D').mean()

def cubicftsec_to_cubicmsec(series):
    new_name = series.name.split('(')[0] + '(m^3 s^-1)'
    return (series * 0.0283168).rename(new_name)

#######################################

def visualize_summary_statistics(df):
    print(df.describe())

def visualize_matplotlib_comparison(series1, series2, save_figure = False):
    fig, ax = plt.subplots()
    ax.plot(series1, linewidth=2.0, label=f'Series 1: {series1.name}')
    ax.plot(series2, linewidth=2.0, label=f'Series 2: {series2.name}')
    plt.legend()
    ax.set_title(f'{series1.name} vs. {series2.name}')
    if save_figure:
        plt.savefig('comparison.png')
    else:
        plt.show()

def visualize_matplotlib(series):
    fig, ax = plt.subplots()
    ax.plot(series, linewidth=2.0)
    ax.set_title(series.name)
    plt.show()

def visualize_seaborn(series):
    sns.lineplot(series)

# Use as: hv.render(visualize_holoviews(series))
def visualize_holoviews(series):
    return hv.Curve(series)

def visualize_plotly(series):
    fig = px.line(series, title=series.name)
    fig.show()


