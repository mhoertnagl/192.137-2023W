import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# scipy contains statistical tests and other useful content
import scipy.stats
from scipy.stats import norm

# Parameters for data import to be set
file_A = "data/Daten.csv"
file_B = "data/Daten.csv"
name_A = "obj_A"
name_B = "obj_B"

# Parameters for the tests to be set
alternative = "two-sided"
alpha = 0.05

# Importing the data
df_A = pd.read_csv(file_A, sep = ";", decimal = ".", usecols = [name_A])
df_B = pd.read_csv(file_B, sep = ";", decimal = ".", usecols = [name_B])

data_A = df_A[name_A]
data_B = df_B[name_B]


def print_decision(pvalue, alpha):
    print("Test Result:")
    print("p-value = %.4f" % (pvalue))
    if pvalue < alpha:
        print("H0 can be rejected on a level of significance of " + str(alpha) + ".")
    else:
        print("H0 cannot be rejected on a level of significance of " + str(alpha) + ".")


def compute_pvalue(pvalue, diff, alternative):
    if alternative == "greater":
        if diff > 0:
            pvalue = pvalue / 2
        else:
            pvalue = 1 - pvalue / 2
    elif alternative == "less":
        if diff < 0:
            pvalue = pvalue / 2
        else:
            pvalue = 1 - pvalue / 2
    return pvalue


def plot_hist(data, group):
    # Plot a histogram
    plt.hist(data, density = True, alpha = 0.5)

    # Fit a normal distribution to the data
    mu, std = norm.fit(data)

    # Plot the probability density function
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 201)
    y = norm.pdf(x, mu, std)
    plt.plot(x, y, "black")
    title = "Fit results of " + group + ": mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
    plt.show()


plot_hist(data_A - data_B, "difference")

# Apply the statistical test
res = scipy.stats.ttest_rel(data_A, data_B)
pvalue = res.pvalue

# Compute the correct p-value (two-sided vs. one-sided)
pvalue = compute_pvalue(res.pvalue, np.mean(data_A) - np.mean(data_B), alternative)

# Print results
print_decision(pvalue, alpha)

# Apply the statistical test
res = scipy.stats.wilcoxon(data_A, data_B, alternative = alternative)

# Print results
print_decision(res.pvalue, alpha)

plot_hist(data_A, name_A)
plot_hist(data_B, name_B)

# Apply the statistical test
res = scipy.stats.ttest_ind(data_A, data_B)
pvalue = res.pvalue

# Compute the correct p-value (two-sided vs. one-sided)
pvalue = compute_pvalue(res.pvalue, np.mean(data_A) - np.mean(data_B), alternative)

# Print results
print_decision(pvalue, alpha)

# Apply the statistical test
res = scipy.stats.mannwhitneyu(data_A, data_B, alternative = alternative)

# Print results
print_decision(res.pvalue, alpha)
