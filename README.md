# t_test
t-test analyses

The analysis starts by examining the normality of the data distribution using the Shapiro-Wilk test for both groups. If either group’s data is not normally distributed or if the variances are unequal (checked with the Levene test), the code automatically switches to the Mann-Whitney U test, which is a non-parametric alternative. If both normality and equal variance assumptions are met, a two-sided t-test is performed to compare the means of the two groups. This automated approach ensures that the appropriate statistical test is used based on the characteristics of the data.
