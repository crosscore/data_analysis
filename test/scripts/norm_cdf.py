from scipy.stats import norm

probability = norm.cdf(2) - norm.cdf(-2)
print(probability)