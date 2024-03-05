"""
作者:博博不吃菠菜
日期:2023-12-18   16：27
名称：data_choose
"""


import pandas as pd

# 读取 Excel 文件
file_path = 'SCC_ceemd_17.xlsx'
df = pd.read_excel(file_path,header=0,engine='openpyxl')
date = pd.read_csv(r'/home/wjx/桌面/lzb/attention2-main/data/2015年11月-2016年4月期间的实时EVSCF.csv')

# 删除第2到5列
df = df.drop(df.columns[1:10], axis=1)
date = date['date']
length = int(len(date)*0.1)
date = date.iloc[0:length]
df = pd.concat([date,df],axis=1)
# 保存为 CSV 文件
csv_file_path = 'data_choose_result.csv'
df.to_csv(csv_file_path, index=False)

print(f"已删除列并保存为 CSV 文件：{csv_file_path}")

