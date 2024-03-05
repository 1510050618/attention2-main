"""
作者:博博不吃菠菜
日期:2023-12-11   16：46
名称：12
"""
import pandas as pd
import datetime
import pandas as pd

# 定义一个日期解析函数
date_parser = lambda x: pd.to_datetime(x, format='%m/%d/%Y %H:%M')

# 文件路径
file_path = r'D:\Study\程序\Python_Code\attention2-main\data\2015年11月-2016年4月期间的实时EVSCF.csv'

# 使用pd.read_csv读取CSV文件，并指定date_parser参数
try:
    df = pd.read_csv(file_path, parse_dates=['date'], date_parser=date_parser)
    # 请将 'your_date_column' 替换为包含日期信息的列名
    # 输出读取的数据框
    print(df)
except FileNotFoundError:
    print(f"文件 {file_path} 未找到，请检查路径是否正确。")
except pd.errors.EmptyDataError:
    print(f"文件 {file_path} 存在但为空。")
except pd.errors.ParserError:
    print(f"无法解析文件 {file_path}，请检查文件格式。")


# 创建 df1，只包含 'date' 列
df1 = df[['date']].copy()

# 创建一个与 df1 长度相同的示例数据框 df_example
# 这里假设你的示例数据是一个与 'date' 列等长的一列数字，你可以根据实际情况调整
df_example = pd.DataFrame({'example_column': range(len(df1))})

# 合并 df1 和 df_example，命名为 df2
df2 = pd.concat([df1, df_example], axis=1)

# 输出 df2
print(df2)