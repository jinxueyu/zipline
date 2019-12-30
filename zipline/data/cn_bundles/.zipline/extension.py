import pandas as pd

from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

start_session = None #pd.Timestamp('2016-1-1', tz='utc')
end_session = None #pd.Timestamp('2018-1-1', tz='utc')

register(
    'cn-csvdir-bundle',
    csvdir_equities(
        ['daily']
    ),
    calendar_name='XSHG',
    start_session=start_session,
    end_session=end_session
)
