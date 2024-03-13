import matplotlib.pyplot as plt
import seaborn as sns

# Assuming df is your DataFrame
plt.figure(figsize=(10, 6))
sns.set_palette("husl")
data = {
    'Instrument': ['Company A', 'Company B', 'Company C', 'Company A', 'Company B', 'Company C'],
    'Feature1': [10, 15, 13, 8, 14, 11],
    'Feature2': [5, 8, 7, 3, 5, 4],
    'Feature3': [12, 10, 15, 9, 12, 14],
    'Feature4': [8, 14, 11, 6, 10, 8],
    'Feature5': [20, 18, 22, 16, 20, 24]
}

df = pd.DataFrame(data)
for _, row in df.iterrows():
    plt.plot(row.index[1:], row.values[1:], label=row['instrument'])

plt.xlabel('Features')
plt.ylabel('Scores')
plt.legend(title='Companies', bbox_to_anchor=(1, 1))
plt.title('Company Trends Across Features')

# Save the plot
plt.savefig('matplotlib_seaborn_plot.png', bbox_inches='tight')
plt.show()
