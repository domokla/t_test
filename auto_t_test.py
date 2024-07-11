import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def generate_data(size, distribution='normal', loc=0, scale=1, low=-3, high=3):
    """
    Generate random data based on the specified distribution.

    Parameters:
    size (int): Number of data points to generate.
    distribution (str): Type of distribution ('normal' or 'uniform').
    loc (float): Mean of the normal distribution.
    scale (float): Standard deviation of the normal distribution.
    low (float): Lower bound of the uniform distribution.
    high (float): Upper bound of the uniform distribution.

    Returns:
    np.ndarray: Generated data.
    """
    np.random.seed(1234)
    if distribution == 'normal':
        return np.random.normal(loc=loc, scale=scale, size=size)
    elif distribution == 'uniform':
        return np.random.uniform(low=low, high=high, size=size)
    else:
        raise ValueError("Unsupported distribution type. Choose 'normal' or 'uniform'.")

def perform_stat_tests(output, data1, data2, description):
    """
    Perform statistical tests and save the results to a file.

    Parameters:
    output (str): Output file name.
    data1 (np.ndarray): First dataset.
    data2 (np.ndarray): Second dataset.
    description (str): Description of the analysis.
    """
    with open(output, 'w') as f:
        f.write(description + '\n')
        
        # Normal distribution tests
        shapiro_data1 = stats.shapiro(data1)
        shapiro_data2 = stats.shapiro(data2)
    
        # Results
        f.write(f"Shapiro-Wilk test (Data1): p-value = {shapiro_data1.pvalue}\n")
        if shapiro_data1.pvalue < 0.05:
            f.write("Data1 Sample is NOT Normally Distributed.\n")
        else:
            f.write("Data1 Sample is Normally Distributed.\n")
    
        f.write(f"Shapiro-Wilk test (Data2): p-value = {shapiro_data2.pvalue}\n")
        if shapiro_data2.pvalue < 0.05:
            f.write("Data2 Sample is NOT Normally Distributed.\n")
        else:
            f.write("Data2 Sample is Normally Distributed.\n")
    
        # Levene's test for checking the equality of variances
        levene_test = stats.levene(data1, data2)
        f.write(f"Levene-test: p-value = {levene_test.pvalue}\n")
        if levene_test.pvalue < 0.05:
            f.write("The variances are NOT equal.\n")
        else:
            f.write("The variances are equal.\n")
    
        # If the distribution is not normal or the variances are not equal, we use the Mann-Whitney U test.
        if shapiro_data1.pvalue < 0.05 or shapiro_data2.pvalue < 0.05 or levene_test.pvalue < 0.05:
            u_stat, u_p_value = stats.mannwhitneyu(data1, data2)
            f.write(f"Mann-Whitney U test: U = {u_stat}, p-value = {u_p_value}\n")
            if u_p_value < 0.05:
                f.write("The means are significantly different (Mann-Whitney U test).\n")
            else:
                f.write("The means are NOT significantly different (Mann-Whitney U test).\n")
        else:
            t_statistic, p_value = stats.ttest_ind(data1, data2, alternative='two-sided')
            f.write(f"T-statistic: {t_statistic}\n")
            f.write(f"P-value: {p_value}\n")
            if p_value < 0.05:
                f.write("The means are significantly different (t-test).\n")
            else:
                f.write("The means are NOT significantly different (t-test).\n")

def plot_histograms(data1, data2, histogram_filename):
    """
    Plot histograms of the data and save to a file.

    Parameters:
    data1 (np.ndarray): First dataset.
    data2 (np.ndarray): Second dataset.
    histogram_filename (str): Filename to save the histogram.
    """
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(data1, bins=10, alpha=0.7, label='Data1')
    plt.title('Histogram of Data1')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.hist(data2, bins=10, alpha=0.7, label='Data2')
    plt.title('Histogram of Data2')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(histogram_filename, dpi=300)
    plt.show()

# Set working directory
os.chdir('/path/to/your/directory')


# Generate data
np.random.seed(1234)
normal_data1 = generate_data(200, distribution='normal')
normal_data2 = generate_data(200, distribution='normal')
non_normal_data1 = generate_data(200, distribution='uniform')
non_normal_data2 = generate_data(200, distribution='uniform')

# Run the analysis and plot for normal distribution data
perform_stat_tests('output_normal.txt', normal_data1, normal_data2, 'Analysis of Normally Distributed Data')
plot_histograms(normal_data1, normal_data2, 'normal_histogram.png')

# Run the analysis and plot for non-normal distribution data
perform_stat_tests('output_non_normal.txt', non_normal_data1, non_normal_data2, 'Analysis of Non-Normally Distributed Data')
plot_histograms(non_normal_data1, non_normal_data2, 'non_normal_histogram.png')
