#Only Crisis
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import main
plt.style.use('ggplot')
FSC = 'FSC'
CRISIS = 1
df_merge = pd.read_excel("Domain merge.xlsx")
#df_merge = df_merge[df_merge['Assessment: Created By_followup'] == FSC]
df_merge.reset_index(inplace=True, drop=True)
n = len(df_merge.index)
df_crisis = pd.DataFrame()
names = {
    'Prevention Line 1': 'Income',
    'Prevention Line 2': 'Employment',
    'Prevention Line 3': 'Housing',
    'Prevention Line 4': 'Transportation',
    'Prevention Line 5': 'Food Security',
    'Prevention Line 6': 'Child Care',
    'Prevention Line 7': 'Child Education',
    'Prevention Line 8': 'Adult Education',
    'Prevention Line 9': 'Cash Savings',
    'Prevention Line 10': 'Debt',
    'Prevention Line 11': 'Health Coverage',
    'Prevention Line 12': 'Physical Health',
    'Prevention Line 13': 'Mental Health',
    'Prevention Line 14': 'Substance Abuse',
}
def crisis(baseline, followup):
    if baseline == CRISIS and followup > CRISIS:
        return 'Moved out of Crisis'
    elif baseline > CRISIS and followup == CRISIS:
        return 'Moved to Crisis'
    elif baseline > CRISIS and followup > CRISIS:
        return 'Stayed out of Crisis'
    elif baseline == CRISIS and followup == CRISIS:
        return 'Stayed in Crisis'

for i in range(0, n):
    for j in range(1, 15):
        df_crisis.loc[i, 'Client'] = df_merge.loc[i, 'Client']
        df_crisis.loc[i, 'Prevention Line ' + str(j)] = crisis(df_merge.iloc[i, 21+j], df_merge.iloc[i, 4+j])

df_crisis.rename(columns=names).to_excel(f'{FSC}/Crisis {FSC}.xlsx')

df_crisis_grouped = pd.DataFrame(index=['Moved to Crisis', 'Stayed in Crisis', 'Stayed out of Crisis', 'Moved out of Crisis'])
for i in range(1, 15):
   df_crisis_grouped['Dimension_'+str(i)] = df_crisis['Prevention Line '+str(i)].value_counts(normalize=True)
df_crisis_grouped = df_crisis_grouped.fillna(0)
df_crisis_grouped = df_crisis_grouped.multiply(100)


category_names = ['Moved to Crisis', 'Stayed in Crisis', 'Stayed out of Crisis', 'Moved out of Crisis']
results = {
    'Income': df_crisis_grouped['Dimension_1'],
    'Employment': df_crisis_grouped['Dimension_2'],
    'Housing': df_crisis_grouped['Dimension_3'],
    'Transportation': df_crisis_grouped['Dimension_4'],
    'Food Security': df_crisis_grouped['Dimension_5'],
    'Child Care': df_crisis_grouped['Dimension_6'],
    'Child Education': df_crisis_grouped['Dimension_7'],
    'Adult Education': df_crisis_grouped['Dimension_8'],
    'Cash Savings': df_crisis_grouped['Dimension_9'],
    'Debt': df_crisis_grouped['Dimension_10'],
    'Health Coverage': df_crisis_grouped['Dimension_11'],
    'Physical Health': df_crisis_grouped['Dimension_12'],
    'Mental Health': df_crisis_grouped['Dimension_13'],
    'Substance Abuse': df_crisis_grouped['Dimension_14'],
}

def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*. The order is assumed
        to be from 'Strongly disagree' to 'Strongly aisagree'
    category_names : list of str
        The category labels.
    """

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    middle_index = (data.shape[1] // 2) -1
    offsets = data[:, range(middle_index)].sum(axis=1) + data[:, middle_index] / 1

    # Color Mapping
    category_colors = plt.get_cmap('coolwarm_r')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(10, 5), tight_layout=True, dpi=300)

    # Plot Bars
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths - offsets

        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)


    # Add Title
    plt.title(f"{FSC} n={n}", fontsize=10)
    plt.suptitle('Crisis Line', fontsize=16, y=0.95, x=0.55)

    # Add Zero Reference Line
    ax.axvline(0, linestyle='--', color='black', alpha=.25)

    # X Axis
    ax.set_xlim(-100, 100)
    ax.set_xticks(np.arange(-100, 110, 20))
    ax.xaxis.set_major_formatter(lambda x, pos: str(abs(int(x)))+'%')

    # Y Axis
    ax.invert_yaxis()

    # Remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Legend
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0.5, -0.2), loc='lower center', fontsize='small')


    # Set Background Color
    fig.set_facecolor('#FFFFFF')

    return fig, ax


fig, ax = survey(results, category_names)
plt.savefig(f'{FSC}/Crisis Line {FSC}.jpg')
#plt.show()

