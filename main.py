import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv('../Data-visualization/healthcare-dataset-stroke-data.csv')
df['age'] = df['age'].astype(int)

# Graph 1
marriage_stroke_counts = df.groupby('ever_married')['stroke'].sum()

plt.pie(marriage_stroke_counts, labels=marriage_stroke_counts.index, autopct='%1.1f%%')
plt.title('Stroke Occurrence by Marriage Status')
plt.show()

# Graph 2
grouped_data = df.groupby(['age', 'ever_married']).sum().reset_index()

ever_married_categories = df['ever_married'].unique()

age_categories = np.arange(df['age'].min(), df['age'].max() + 1)

# Create a new DataFrame with all combinations of age and ever married
com_data = pd.DataFrame(
    [(age, ever_married) for age in age_categories for ever_married in ever_married_categories],
    columns=['age', 'ever_married'])

# Merge the complete DataFrame with the grouped data
merged_data = pd.merge(com_data, grouped_data, on=['age', 'ever_married'], how='left')
merged_data.fillna(0, inplace=True)

# Plot the bar chart
fig, ax = plt.subplots(figsize=(10, 6))
for category in ever_married_categories:
    data = merged_data[merged_data['ever_married'] == category]
    if category == 'Yes':
        label = 'Married or Married Before'
    else:
        label = 'Not Married or Not Married Before'

    ax.bar(data['age'], data['stroke'], label=label)
# Set the x-axis tick locations and labels
x_ticks = np.arange(0, df['age'].max() + 1, 10)
ax.set_xticks(x_ticks)

ax.set_xlabel('Age')
ax.set_ylabel('Stroke Occurrences')
ax.set_title('Stroke Occurrences by Age and Marital Status')
ax.legend(loc='upper left')
plt.savefig('Marital.png', transparent=True)
plt.show()

# Graph 3
df_filtered = df[['ever_married', 'stroke']]
ever_married_count = df_filtered[df_filtered['stroke'] == 1].count()
all_count = df_filtered['stroke'].count

married_stroke_percentage = (df_filtered[df_filtered['ever_married'] == 'Yes']['stroke'] == 1).mean() * 100
unmarried_stroke_percentage = (df_filtered[df_filtered['ever_married'] == 'No']['stroke'] == 1).mean() * 100

categories = ['Married', 'Unmarried']
percentages = [married_stroke_percentage, unmarried_stroke_percentage]
plt.bar(categories, percentages)
plt.xlabel('Marital Status')
plt.title('Percentage of Stroke by Marital Status')
# Add percentages on top of the bars
for i, percentage in enumerate(percentages):
    plt.text(i, percentage, f'{percentage:.2f}%', ha='center', va='bottom')

plt.yticks([])
plt.show()

# Graph 4
df.groupby(df['Residence_type']).sum().plot(kind='pie', y='stroke', autopct='%1.0f%%')
plt.axis('off')
plt.show()

# Graph 5
df_res = df.groupby(['age', 'Residence_type']).sum().reset_index()
sns.lineplot(data=df_res, x='age', y="stroke", hue="Residence_type")
plt.savefig('lineplot.png', transparent=True)
plt.show()

# Graph 6
df_filtered = df[['smoking_status', 'stroke']]

# Count the occurrences of each smoking status
smoking_counts = df_filtered['smoking_status'].value_counts()
plt.pie(smoking_counts, labels=smoking_counts.index, autopct='%1.1f%%')
plt.title('Overall Smoking Status')
plt.show()

# Graph 7
grouped_data = df.groupby('smoking_status')['stroke'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='smoking_status', y='stroke', data=grouped_data)
plt.xlabel('Smoking Status')
plt.ylabel('Stroke Ratio')
plt.title('Stroke Ratio by Smoking Status')
plt.savefig('SSmoking.png', transparent=True)
plt.show()

# Graph 8
df_filtered = df[(df['age'] >= 40) & (df['age'] <= 50)]


def calculate_stroke_ratio(category):
    count = df_filtered[df_filtered['smoking_status'] == category]['stroke'].value_counts()
    total_count = df_filtered['smoking_status'].value_counts()[category]
    return count, total_count


# Create pie charts for each smoking status category
categories = ['smokes', 'never smoked', 'formerly smoked']
labels = ['No Stroke', 'Stroke']
# Graph 9-11(not used), it only used for viewing stoke ratio of age group 40-50
for category in categories:
    count, total_count = calculate_stroke_ratio(category)
    plt.figure(figsize=(6, 6))
    plt.pie(count, labels=labels, autopct='%1.1f%%')
    plt.title(f'Stroke Count Ratio for {category.capitalize()} in age group 40-50')
    plt.savefig(f'{category.capitalize()}.png', transparent=True)
    plt.show()
# Graph 12
df_ssa = df[df['smoking_status'] != 'Unknown']
df_ssa = df_ssa.groupby(['age', 'smoking_status']).sum().reset_index()
sns.lineplot(data=df_ssa, x='age', y='stroke', hue='smoking_status')
plt.ylabel('Stroke count')
plt.savefig('StrokeS.png', transparent=True)
plt.show()

# Graph 13
# Replace the label "Govt_job" with "Government job"
df['work_type'] = df['work_type'].replace('Govt_job', 'Government job')
df['work_type'] = df['work_type'].replace('children', 'Children')
grouped_data = df.groupby('work_type')['stroke'].mean().reset_index()

# Create the bar chart using Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='work_type', y='stroke', data=grouped_data)
plt.xlabel('Job Category')
plt.title('Stroke Ratio by Job Category')
plt.savefig('Job.png', transparent=True)
plt.show()
