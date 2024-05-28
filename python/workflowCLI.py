from modules import *
import sys

# Get command line args
# Remember sys.argv[0] is the script name
start = sys.argv[1]
end = sys.argv[2]

# Acquire / Filter
#df = acquire_streamflow_nwis_iv(site='04294000', start='2022-06-01', end='2022-11-01')
df = acquire_streamflow_nwm_retrospective(166176984, start, end)

# Manipulate
daily = resample_to_daily(df)

# Visualize
visualize_summary_statistics(daily)