from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import json

import numpy as np
import pandas as pd

from apexpy import Apex
from dipole import Dipole
from viresclient import SwarmRequest


date = pd.Timestamp('2025-05-26')
f107 = 125.0  # daily observed F10.7 [sfu]

end = date + pd.Timedelta(days=1)
tag = date.strftime('%Y%m%d')

repository = Path(__file__).resolve().parents[1]
data_directory = repository / 'data' / f'gdh_{tag}'
data_directory.mkdir(parents=True, exist_ok=True)

request = SwarmRequest()
request.set_collection('SW_OPER_AUX_OBSM2_:GDH')
request.set_products(measurements=['B_NEC', 'Quality'], models={'CHAOS-internal': ''CHAOS-Core' + 'CHAOS-Static''}, residuals=True)
ground = request.get_between(start_time=date.to_pydatetime(), end_time=end.to_pydatetime()).as_dataframe(expand=True)

residual_name = next(column.rsplit('_', 1)[0] for column in ground.columns if column.startswith('B_NEC_res_') and column.endswith('_N'))
ground_output = pd.DataFrame(index=pd.to_datetime(ground.index, utc=True))
ground_output['B_N_res_CHAOS_nT'] = ground[f'{residual_name}_N'].to_numpy()
ground_output['B_E_res_CHAOS_nT'] = ground[f'{residual_name}_E'].to_numpy()
ground_output['B_C_res_CHAOS_nT'] = ground[f'{residual_name}_C'].to_numpy()
ground_output['quality'] = ground['Quality'].to_numpy()
ground_output['geocentric_latitude_deg'] = ground['Latitude'].to_numpy()
ground_output['longitude_deg_east'] = ground['Longitude'].to_numpy()
ground_output.index.name = 'time_utc'

hapi_query = urlencode({'id': 'OMNI_HRO_1MIN', 'parameters': 'Time,BY_GSM,BZ_GSM,flow_speed,proton_density,SYM_H', 'time.min': date.strftime('%Y-%m-%dT00:00:00Z'), 'time.max': end.strftime('%Y-%m-%dT00:00:00Z'), 'format': 'json'})
with urlopen('https://cdaweb.gsfc.nasa.gov/hapi/data?' + hapi_query) as response:
    omni_json = json.load(response)

omni = pd.DataFrame(omni_json['data'], columns=[parameter['name'] for parameter in omni_json['parameters']])
omni['Time'] = pd.to_datetime(omni['Time'], utc=True)
omni = omni.set_index('Time')
for column in omni.columns:
    omni[column] = pd.to_numeric(omni[column], errors='coerce')

omni['BY_GSM'] = omni['BY_GSM'].mask(omni['BY_GSM'].abs() > 100)
omni['BZ_GSM'] = omni['BZ_GSM'].mask(omni['BZ_GSM'].abs() > 100)
omni['flow_speed'] = omni['flow_speed'].mask(omni['flow_speed'] > 5000)
omni['proton_density'] = omni['proton_density'].mask(omni['proton_density'] > 500)
omni['SYM_H'] = omni['SYM_H'].mask(omni['SYM_H'].abs() > 10000)

times = pd.date_range(date.tz_localize('UTC'), end.tz_localize('UTC'), freq='1min', inclusive='left')
omni = omni.reindex(times)

gdh_geodetic_latitude = 69.25
gdh_longitude = 306.47
apex = Apex(date=date.to_pydatetime())
gdh_qd_latitude, gdh_qd_longitude = apex.geo2qd(gdh_geodetic_latitude, gdh_longitude, 0)
gdh_mlt = apex.mlon2mlt(np.full(len(times), gdh_qd_longitude), times.to_pydatetime())
tilt = Dipole(epoch=date.year + (date.dayofyear - 1) / 365.25).tilt(times.to_pydatetime())

drivers = pd.DataFrame(index=times)
drivers['By_GSM_nT'] = omni['BY_GSM']
drivers['Bz_GSM_nT'] = omni['BZ_GSM']
drivers['speed_km_s'] = omni['flow_speed']
drivers['proton_density_cm3'] = omni['proton_density']
drivers['SYM_H_nT'] = omni['SYM_H']
drivers['dipole_tilt_deg'] = tilt
drivers['F107_sfu'] = f107
drivers['GDH_QD_latitude_deg'] = gdh_qd_latitude
drivers['GDH_QD_longitude_deg'] = gdh_qd_longitude
drivers['GDH_MLT_hours'] = gdh_mlt
drivers.index.name = 'time_utc'

ground_path = data_directory / f'gdh_magnetic_residual_{tag}_1min.csv'
drivers_path = data_directory / f'swipe_drivers_{tag}_1min.csv'
ground_output.to_csv(ground_path)
drivers.to_csv(drivers_path)

print(f'Saved {ground_path} ({len(ground_output)} samples)')
print(f'Saved {drivers_path} ({len(drivers)} samples)')
print(ground.columns.tolist())
