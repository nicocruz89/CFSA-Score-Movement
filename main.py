import pandas as pd
import numpy as np

df = pd.read_excel("Domain advancement.xlsx")
df.drop(columns=['Unnamed: 0'], inplace=True)
df = df[9:]
new_header = df.iloc[0]  # grab the first row for the header
df = df[1:]  # take the data less the header row
df.columns = new_header  # set the header row as the df header
df.drop(df.columns[1], axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)

# Convert answers to integers
questions = df.columns[4:]
for question in questions:
    df[question] = df[question].astype(str).str[0]
    pd.to_numeric(df[question], errors='coerce')

df_baseline = df[df['CFSA Type'] == 'Baseline']
df_baseline = df_baseline.sort_values(['Assessment: Created Date'],ascending=True).groupby('Client').head(1)
df_baseline_crisis = df_baseline[df_baseline.isin(['1']).any(axis=1)]

df_followup = df[df['CFSA Type'] == 'Follow Up']
df_followup = df_followup.sort_values(['Assessment: Created Date'],ascending=True).groupby('Client').tail(1)


df_merge = pd.merge(df_followup[df.columns], df_baseline[df.columns], how='inner', left_on=['Client'],
                       right_on=['Client'], suffixes=('_followup', '_baseline'))
df_merge = df_merge.replace(['n', 'd', 'N'], np.NaN)

df_movement = pd.DataFrame()
df_movement['Client'] = df_merge['Client']
for question in questions:
    df_merge[question+'_followup'] = df_merge[question+'_followup'].astype(float)
    df_merge[question+'_baseline'] = df_merge[question+'_baseline'].astype(float)
    df_movement[question] = df_merge[question+'_followup'] - df_merge[question+'_baseline']



df_baseline.to_excel('Domain movement baseline.xlsx')
df_followup.to_excel('Domain movement followup.xlsx')
df_merge.to_excel('Domain merge.xlsx')
df_movement.to_excel('Domain movement.xlsx')
