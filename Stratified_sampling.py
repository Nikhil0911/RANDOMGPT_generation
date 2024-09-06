import numpy as np
import pandas as pd

# Create a large population with an additional 'City' column to represent strata
np.random.seed(0)  # For reproducibility
population_size = 1000000
population = pd.DataFrame({
    'Age': np.random.randint(1, 100, size=population_size),
    'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Boston'], size=population_size)
})

# Function to perform stratified sampling
def stratified_sampling(population, stratify_col, sample_size):
    # Get the proportion of each group in the population
    strata = population[stratify_col].value_counts(normalize=True)
    
    # Empty list to store sampled data
    sampled_data = []
    
    # For each group in the strata, sample proportionally
    for group, proportion in strata.items():
        group_data = population[population[stratify_col] == group]
        group_sample_size = int(np.round(proportion * sample_size))
        
        # Randomly sample from this group
        sampled_group = group_data.sample(group_sample_size, replace=False)
        sampled_data.append(sampled_group)
    
    # Concatenate all the stratified samples
    sampled_data = pd.concat(sampled_data)
    return sampled_data

# Parameters
sample_size = 1000  # Total sample size
num_samples = 5  # Number of samples

# Step 1: Calculate the average of each stratified sample
sample_averages = []
for _ in range(num_samples):
    stratified_sample = stratified_sampling(population, stratify_col='City', sample_size=sample_size)
    sample_avg = stratified_sample['Age'].mean()
    sample_averages.append(sample_avg)

# Step 2: Calculate the final average of the 5 sample averages
final_average_of_samples = np.mean(sample_averages)

# Step 3: Calculate the actual average of the entire population
population_average = population['Age'].mean()

# Print the results
print(f"Final average from the 5 samples' averages: {final_average_of_samples}")
print(f"Actual population average: {population_average}")
print(f"Difference: {abs(final_average_of_samples - population_average)}")
