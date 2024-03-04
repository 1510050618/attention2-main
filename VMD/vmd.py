from __future__ import division, print_function # Loading modules
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyEMD import EMD, EEMD, CEEMDAN # CEEMDAN # pip install EMD-signal
from sampen import sampen2 # Sample Entropy
from sklearn.cluster import KMeans
from vmdpy import VMD # VMD

start = time.time()

# 读取 Excel 文件
file_path = r'/home/wjx/桌面/lzb/attention2-main/MIC/ceemd-NoScc.csv'
df = pd.read_csv(file_path)


# 删除第2到5列
# df = df.drop(df.columns[0], axis=1)
# date = date['date']
# length = int(len(date)*0.1)
# date = date.iloc[0:length]
# df = pd.concat([date,df],axis=1)
def ceemdan_decompose(series=None, trials=10, num_clusters = 3): # CEEMDAN Decompose
    decom = CEEMDAN()
    decom.trials = trials # Number of the white noise input
    df_ceemdan = pd.DataFrame(decom(series.values).T)
    df_ceemdan.columns = ['imf'+str(i) for i in range(len(df_ceemdan.columns))]
    return df_ceemdan
def sample_entropy(df_ceemdan=None, mm=1, r=0.1): # Sample Entropy Calculate; mm = 1 or 2; r = 0.1 or 0.2
    np_sampen = []
    for i in range(len(df_ceemdan.columns)):
        i = i+1
        sample_entropy = sampen2(list(df_ceemdan['IMF'+str(i)].values),mm=mm,r=r,normalize=True)
        np_sampen.append(sample_entropy[1][1])
    df_sampen = pd.DataFrame(np_sampen, index=['IMF'+str(i) for i in range(len(df_ceemdan.columns))], columns=[file_path])
    return df_sampen

def kmeans_cluster(df_sampen=None, num_clusters=3): # K-Means Cluster by Sample Entropy
    np_integrate_form = KMeans(n_clusters=num_clusters, random_state=9).fit_predict(df_sampen)
    df_integrate_form = pd.DataFrame(np_integrate_form, index=['imf'+str(i) for i in range(len(df_sampen.index))], columns=['Cluster'])
    return df_integrate_form

def integrate_imfs(df_integrate_form=None, df_ceemdan=None): # Integrate IMFs and Residue to be 3 Co-IMFs
    df_tmp = pd.DataFrame()
    for i in range(df_integrate_form.values.max()+1):
        df_tmp['imf'+str(i)] = df_ceemdan[df_integrate_form[(df_integrate_form['Cluster']==i)].index].sum(axis=1)
    df_integrate_result = df_tmp.T # Use Sample Entropy sorting the Co-IMFs
    df_integrate_result['sampen'] = sample_entropy(df_tmp).values
    df_integrate_result.sort_values(by=['sampen'], ascending=False, inplace=True)
    df_integrate_result.index = ['co-imf'+str(i) for i in range(df_integrate_form.values.max()+1)]
    df_integrate_result = df_integrate_result.drop('sampen', axis=1, inplace=False)
    return df_integrate_result.T

df_sampen = sample_entropy(df)  # 9，1
time_end2 = time.time()
cost_time2 = time_end2 -start
print('时间花费：{}'.format(cost_time2))
#  df_sampen.plot(title='Sample Entropy')

# 4.K-Means Cluster by Sample Entropy
df_integrate_form = kmeans_cluster(df_sampen)  # 聚类 9，1
print(df_integrate_form)

# 5.Integrate IMFs and Residue to be 3 Co-IMFs
df_integrate_result = integrate_imfs(df_integrate_form, df)  # 将分解的9个聚类为3个
df_integrate_result.to_csv('df_integrate_result.scv')  # 保存三类

# df_integrate_result.plot(title='Integrated IMFs (Co-IMFs) of CEEMDAN', subplots=True)
file_path = r'/home/wjx/桌面/lzb/attention2-main/vmd/df_integrate_result.scv'
df_integrate_result = pd.read_csv(file_path)
print(df_integrate_result)

# 6.Secondary Decompose the high-frequency Co-IMF0 by VMD
df_vmd_co_imf0 = vmd_decompose(
    df_integrate_result['co-imf1'])  # 4858，10  vmd decomposition (The number of dataset must be even)
# df_vmd_co_imf0.plot(title='VMD Decomposition of Co-IMF0', subplots=True)


#
df1_inter_result_re = df_integrate_result.drop('co-imf1', axis=1)
# df_vmd_co_imf0.drop('date',axis=1)
df_co_vmd = pd.concat([df1_inter_result_re, df_vmd_co_imf0], axis=1)
df_co_vmd = pd.concat([df4, df_co_vmd], axis=1)
df_co_vmd.drop('Unnamed', axis=1)

df_co_vmd.to_csv('2-ceemd-vmd.csv', index=False)

time_end3 = time.time()
cost_time3 = time_end3 - start
print('zong时间花费：{}'.format(cost_time3))