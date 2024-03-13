import seaborn as sns
import matplotlib.pyplot as plt

# Assuming df is your DataFrame
plt.figure(figsize=(10, 6))
sns.set_palette("husl")

for _, row in df.iterrows():
    sns.lineplot(x=row.index[1:], y=row.values[1:], label=row['instrument'])

plt.xlabel('Features')
plt.ylabel('Scores')
plt.legend(title='Companies', bbox_to_anchor=(1, 1))
plt.title('Company Trends Across Features')

# Save the plot
plt.savefig('seaborn_plot.png', bbox_inches='tight')
plt.show()
