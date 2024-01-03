from scipy import stats

# IQ score, mean, standard deviation
iq_score = 188
mean_iq = 100
std_dev_iq = 17

# Calculate z-score
z_score = (iq_score - mean_iq) / std_dev_iq

# Calculate the probability that the z-score is less than or equal to the standard normal distribution
probability_below_z = stats.norm.cdf(z_score)
print(probability_below_z)

# Existence rate of iq_score or above
probability_above_iq_score = 1 - probability_below_z
print(probability_above_iq_score)

if probability_above_iq_score > 0:
    one_in_x = round(1 / probability_above_iq_score)
    print(f"One in {one_in_x} chance of getting IQ{iq_score} or above.")
else:
    print("No chance of getting iq_score or above.")