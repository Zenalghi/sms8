import scipy.io as sio
import pandas as pd
import numpy as np
import os

matfile = 'Model_Baterai_EKF.mat'
print('matfile exists', os.path.exists(matfile))
if not os.path.exists(matfile):
    raise FileNotFoundError(matfile)

data = sio.loadmat(matfile)
print('keys', [k for k in data.keys() if not k.startswith('__')])

Q_Ah_Nominal = float(np.squeeze(data['Q_Ah_Nominal']))
Q_As = float(np.squeeze(data['Q_As']))

ocv_data = data['ocv_table']
ocv_items = ocv_data[0][0]
# ocv_items is tuple (soc_array, ocv_array)
ocv_df = pd.DataFrame({'SOC': ocv_items[0].flatten(), 'OCV_V': ocv_items[1].flatten()})

ecm_data = data['df_ecm_clean']
ecm_items = ecm_data[0][0]
ecm_df = pd.DataFrame({'SOC_percent': ecm_items[0].flatten(), 'R0_ohm': ecm_items[1].flatten(), 'R1_ohm': ecm_items[2].flatten(), 'C1_farad': ecm_items[3].flatten(), 'Tau_s': ecm_items[4].flatten()})

csv_model_filename = 'Model_Baterai_EKF.csv'
with open(csv_model_filename, 'w', encoding='utf-8') as f:
    f.write('# Model Baterai LiFePO4 - Format CSV untuk Python\n')
    f.write('# Source: Model_Baterai_EKF.mat\n')
    f.write('#\n')
    f.write('=== BATTERY PARAMETERS ===\n')
    pd.DataFrame({'Parameter':['Q_Ah_Nominal','Q_As'], 'Value':[Q_Ah_Nominal,Q_As], 'Unit':['Ah','As'], 'Description':['Kapasitas nominal baterai','Kapasitas dalam ampere-sekon']}).to_csv(f,index=False)
    f.write('\n=== OCV LOOKUP TABLE ===\n')
    ocv_df.to_csv(f,index=False)
    f.write('\n=== ECM PARAMETERS (1-RC Thevenin) ===\n')
    ecm_df.to_csv(f,index=False)

print('[SUCCESS] wrote', csv_model_filename)
print('Q_Ah_Nominal', Q_Ah_Nominal, 'Q_As', Q_As, 'len_ocv', len(ocv_df), 'len_ecm', len(ecm_df))
