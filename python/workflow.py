from modules import *

# Acquire / Filter
#df = acquire_streamflow_nwis_iv(site='04294000', start='2022-06-01', end='2022-11-01')
df = acquire_streamflow_nwm_retrospective(166176984, '2016-06-01', '2016-11-01')

# Manipulate
daily = resample_to_daily(df)

# Visualize
visualize_summary_statistics(daily)