from modules import *
import sys

# Get command line args
# Remember sys.argv[0] is the script name
start = sys.argv[1]
end = sys.argv[2]

# Acquire / Filter
print('Acquiring USGS Data...')
usgs = acquire_streamflow_nwis_iv(site='04294000', start=start, end=end)

print('Acquiring NWM Retrospective Data...')
nwm = acquire_streamflow_nwm_retrospective(site=166176984, start=start, end=end)

# Manipulate
usgs = cubicftsec_to_cubicmsec(usgs)

daily_usgs = resample_to_daily(usgs)
daily_nwm = resample_to_daily(nwm)

# Visualize
print('Daily USGS Summary')
visualize_summary_statistics(daily_usgs)

print('Daily NWM Retrospective Summary')
visualize_summary_statistics(daily_nwm)

visualize_matplotlib_comparison(usgs, nwm, save_figure = True)
