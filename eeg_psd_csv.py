import os

import mne
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def raw_data_info():
    raw = mne.io.read_raw_brainvision(
        '/home/public2/eegData/health_control/eyeclose/jkdz_cc_20180430_close.vhdr', preload=True)
    channel_names = raw.info['ch_names']
    bad_channels = []
    return channel_names, bad_channels


def calculate_eeg_psd(raw, eid):
    #data_path='D:\health_control\eyeopen'
    #fname=data_path+'\jkdz_dhl_20180411_open.vhdr'
    # print(__doc__)
    # raw=mne.io.read_raw_brainvision(fname,preload=True)
    # psd_subfreq = {}

    psd_all, _ = mne.time_frequency.psd_welch(
        raw, fmin=0.5, fmax=40, n_fft=2048, n_jobs=1)
    # psd_subfreq['delta'],freqs1=mne.time_frequency.psd_welch(raw,fmin=0.5,fmax=4,n_fft=2048,n_jobs=1)
    # psd_subfreq['theta'],freqs2=mne.time_frequency.psd_welch(raw,fmin=4,fmax=7,n_fft=2048,n_jobs=1)
    # psd_subfreq['alpha1'],freqs3=mne.time_frequency.psd_welch(raw,fmin=8,fmax=10,n_fft=2048,n_jobs=1)
    # psd_subfreq['alpha2'] ,freqs4=mne.time_frequency.psd_welch(raw,fmin=10,fmax=12,n_fft=2300,n_jobs=1)
    # psd_subfreq['beta'],freqs5=mne.time_frequency.psd_welch(raw,fmin=13,fmax=30,n_fft=256,n_jobs=1)
    # psd_subfreq['gamma'],freqs6=mne.time_frequency.psd_welch(raw,fmin=30,fmax=40,n_fft=512,n_jobs=1)

    rpsd_sub = {}
    rpsd_sub['delta'] = []
    rpsd_sub['theta'] = []
    rpsd_sub['alpha1'] = []
    rpsd_sub['alpha2'] = []
    rpsd_sub['beta'] = []
    rpsd_sub['gamma'] = []

    # for i in range(0,64):
    #     sum_all=sum(psd_all[i])
    #     rpsd_sub['delta'].append(sum(psd_subfreq['delta'][i])/sum_all)
    #     rpsd_sub['theta'].append(sum(psd_subfreq['theta'][i])/sum_all)
    #     rpsd_sub['alpha1'].append(sum(psd_subfreq['alpha1'][i])/sum_all)
    #     rpsd_sub['alpha2'].append(sum(psd_subfreq['alpha2'][i])/sum_all)
    #     rpsd_sub['beta'].append(sum(psd_subfreq['beta'][i])/sum_all)
    #     rpsd_sub['gamma'].append(sum(psd_subfreq['gamma'][i])/sum_all)
    for i in range(0, 64):
        sum_all = sum(psd_all[i])
        rpsd_sub['delta'].append(sum(psd_all[i][0:1])/sum_all)
        rpsd_sub['theta'].append(sum(psd_all[i][1:3])/sum_all)
        rpsd_sub['alpha1'].append(sum(psd_all[i][3:4])/sum_all)
        rpsd_sub['alpha2'].append(sum(psd_all[i][4:5])/sum_all)
        rpsd_sub['beta'].append(sum(psd_all[i][5:13])/sum_all)
        rpsd_sub['gamma'].append(sum(psd_all[i][13:])/sum_all)

    # for (key, val) in psd_subfreq.items():
    # 	temp_all = [t[0] for t in psd_all]
    # 	if 0 not in temp_all:
    # 		temp_sub = [t[0] for t in psd_subfreq[key]]
    # 		psd_subfreq[key] = [x/y for x,y in zip(temp_sub,temp_all)]
    # 	else:
    # 		print("ERROR! id=" + eid + ' has a psd_all=0')
    # return psd_subfreq
    return rpsd_sub


def eeg_psd(control_raw, patient_raw):
    #control_raw = {}
    channel_names, _ = raw_data_info()
    columns = channel_names.copy()
    columns.insert(0, 'groupId')
    columns.insert(0, 'id')
    columns = columns[:-1]
    columns.append('average')
    df_c_delta = pd.DataFrame(columns=columns)
    df_c_theta = pd.DataFrame(columns=columns)
    df_c_alpha1 = pd.DataFrame(columns=columns)
    df_c_alpha2 = pd.DataFrame(columns=columns)
    df_c_beta = pd.DataFrame(columns=columns)
    df_c_gamma = pd.DataFrame(columns=columns)

    df_p_delta = pd.DataFrame(columns=columns)
    df_p_theta = pd.DataFrame(columns=columns)
    df_p_alpha1 = pd.DataFrame(columns=columns)
    df_p_alpha2 = pd.DataFrame(columns=columns)
    df_p_beta = pd.DataFrame(columns=columns)
    df_p_gamma = pd.DataFrame(columns=columns)

    counter = 0
    for (eid, raw) in control_raw.items():
        psd_subfreq = calculate_eeg_psd(raw, eid)
        print('control: ' + str(counter))
        counter += 1
        temp = psd_subfreq['delta'].copy()
        # temp = list(psd_subfreq['delta'].copy())
        # temp = [t[0] for t in psd_subfreq['delta']]
        # control group id = 0
        temp.insert(0, 0)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['delta']))

        df_c_delta.loc[len(df_c_delta)] = temp

        temp = psd_subfreq['theta'].copy()
        # temp = list(psd_subfreq['theta'].copy())
        # temp = [t[0] for t in psd_subfreq['theta']]
        temp.insert(0, 0)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['theta']))

        df_c_theta.loc[len(df_c_theta)] = temp

        temp = psd_subfreq['alpha1'].copy()
        # temp = list(psd_subfreq['alpha1'].copy())
        # temp = [t[0] for t in psd_subfreq['alpha1']]
        temp.insert(0, 0)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['alpha1']))

        df_c_alpha1.loc[len(df_c_alpha1)] = temp

        temp = psd_subfreq['alpha2'].copy()
        # temp = list(psd_subfreq['alpha2'].copy())
        # temp = [t[0] for t in psd_subfreq['alpha2']]
        temp.insert(0, 0)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['alpha2']))

        df_c_alpha2.loc[len(df_c_alpha2)] = temp

        temp = psd_subfreq['beta'].copy()
        # temp = list(psd_subfreq['beta'].copy())
        # temp = [t[0] for t in psd_subfreq['beta']]
        temp.insert(0, 0)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['beta']))

        df_c_beta.loc[len(df_c_beta)] = temp

        temp = psd_subfreq['gamma'].copy()
        # temp = list(psd_subfreq['gamma'].copy())
        # temp = [t[0] for t in psd_subfreq['gamma']]
        temp.insert(0, 0)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['gamma']))

        df_c_gamma.loc[len(df_c_gamma)] = temp

    df_c_delta.to_csv('psd_c_delta.csv', index=True)
    df_c_theta.to_csv('psd_c_theta.csv', index=True)
    df_c_alpha1.to_csv('psd_c_alpha1.csv', index=True)
    df_c_alpha2.to_csv('psd_c_alpha2.csv', index=True)
    df_c_beta.to_csv('psd_c_beta.csv', index=True)
    df_c_gamma.to_csv('psd_c_gamma.csv', index=True)

    counter = 0
    for (eid, raw) in patient_raw.items():
        psd_subfreq = calculate_eeg_psd(raw, eid)
        print('patient #' + str(counter) + ': ' + eid)
        counter += 1

        temp = psd_subfreq['delta'].copy()
        # temp = list(psd_subfreq['delta'].copy())
        # temp = [t[0] for t in psd_subfreq['delta']]
        #Patient group id = 1
        temp.insert(0, 1)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['delta']))

        df_p_delta.loc[len(df_p_delta)] = temp

        temp = psd_subfreq['theta'].copy()
        # temp = list(psd_subfreq['theta'].copy())
        # temp = [t[0] for t in psd_subfreq['theta']]
        temp.insert(0, 1)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['theta']))

        df_p_theta.loc[len(df_p_theta)] = temp

        temp = psd_subfreq['alpha1'].copy()
        # temp = list(psd_subfreq['alpha1'].copy())
        # temp = [t[0] for t in psd_subfreq['alpha1']]
        temp.insert(0, 1)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['alpha1']))

        df_p_alpha1.loc[len(df_p_alpha1)] = temp

        temp = psd_subfreq['alpha2'].copy()
        # temp = list(psd_subfreq['alpha2'].copy())
        # temp = [t[0] for t in psd_subfreq['alpha2']]
        temp.insert(0, 1)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['alpha2']))

        df_p_alpha2.loc[len(df_p_alpha2)] = temp

        temp = psd_subfreq['beta'].copy()
        # temp = list(psd_subfreq['beta'].copy())
        # temp = [t[0] for t in psd_subfreq['beta']]
        temp.insert(0, 1)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['beta']))

        df_p_beta.loc[len(df_p_beta)] = temp

        temp = psd_subfreq['gamma'].copy()
        # temp = list(psd_subfreq['gamma'].copy())
        # temp = [t[0] for t in psd_subfreq['gamma']]
        temp.insert(0, 1)
        temp.insert(0, eid)
        temp.append(np.mean(psd_subfreq['gamma']))

        df_p_gamma.loc[len(df_p_gamma)] = temp

    df_p_delta.to_csv('psd_p_delta.csv', index=True)
    df_p_theta.to_csv('psd_p_theta.csv', index=True)
    df_p_alpha1.to_csv('psd_p_alpha1.csv', index=True)
    df_p_alpha2.to_csv('psd_p_alpha2.csv', index=True)
    df_p_beta.to_csv('psd_p_beta.csv', index=True)
    df_p_gamma.to_csv('psd_p_gamma.csv', index=True)

# fname = '/home/paulbai/eeg/eegData/mdd_patient/eyeclose/njh_after_xh_close_20180319.vhdr'
# raw = mne.io.read_raw_brainvision(fname,preload=True)
# psd_sub = calculate_eeg_psd(raw, 'eid')
# print(psd_sub['delta'])
# print(len(psd_sub['alpha1']))
# print(len(psd_sub['alpha2']))
# print(len(psd_sub['beta']))
# print(len(psd_sub['gamma']))

# channel_names, bad_channels = raw_data_info()
# columns = channel_names.copy()
# columns.insert(0, 'id')
# columns = columns[:-1]
# print(len(columns))
