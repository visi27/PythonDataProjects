import matplotlib.pyplot as plt
import pandas as pd

nba_stats = pd.read_csv("nba_2013.csv")
# CALCULATING VARIANCE
# To do so we will follow this steps:
# 1. subtract every value from the mean 2. square each value  3. Average the values.
# Find the mean value of the column.
pf_mean = nba_stats["pf"].mean()
# Initialize variance at zero.
variance = 0
# Loop through each item in the "pf" column.
for p in nba_stats["pf"]:
    # Calculate the difference between the mean and the value.
    difference = p - pf_mean
    # Square the difference. This ensures that the result isn't negative.
    # If we didn't square the difference, the total variance would be zero.
    # ** in python means "raise whatever comes before this to the power of whatever number is after this."
    square_difference = difference ** 2
    # Add the difference to the total.
    variance += square_difference
# Average the total to find the final variance.
variance = variance / len(nba_stats["pf"])

print(variance)

# Calculate varianace of "pts" column
pts_mean = nba_stats["pts"].mean()
point_variance = 0

for point in nba_stats["pts"]:
    diff = point-pts_mean
    sqr_diff = diff ** 2
    point_variance += sqr_diff

point_variance = point_variance / len(nba_stats["pts"])
print(point_variance)


def nba_std_deviation(col):
    mean = nba_stats[col].mean()
    variance = 0

    for val in nba_stats[col]:
        diff = val - mean
        sqr_diff = diff ** 2
        variance += sqr_diff

    variance = variance / len(nba_stats[col])
    std_deviation = variance ** (1/2)
    return std_deviation

mp_dev = nba_std_deviation("mp")
ast_dev = nba_std_deviation("ast")

# Analyse standart deviation
plt.hist(nba_stats["pf"])
mean = nba_stats["pf"].mean()
plt.axvline(mean, color="r")
# We can calculate standard deviation by using the std() method on a pandas series.
std_dev = nba_stats["pf"].std()
# Plot a line one standard deviation below the mean.
plt.axvline(mean - std_dev, color="g")
# Plot a line one standard deviation above the mean.
plt.axvline(mean + std_dev, color="g")

# We can see how many of the data points fall within one standard deviation of the mean.
# The more that fall into this range, the more dense the data is.
plt.show()

# We can calculate how many standard deviations a data point is from the mean by doing some subtraction and division.
# First, we find the total distance by subtracting the mean.
total_distance = nba_stats["pf"][0] - mean
# Then we divide by standard deviation to find how many standard deviations away the point is.
standard_deviation_distance = total_distance / std_dev
print(standard_deviation_distance)

point_10 = nba_stats["pf"][9]
point_100 = nba_stats["pf"][99]

# We can calculate how many standard deviations a data point is from the mean by doing some subtraction and division.
# First, we find the total distance by subtracting the mean.
total_distance = nba_stats["pf"][0] - mean
# Then we divide by standard deviation to find how many standard deviations away the point is.
standard_deviation_distance = total_distance / std_dev

point_10_std = (point_10 - mean) / std_dev
point_100_std = (point_100 - mean) / std_dev


# Plot field goals attempted (number of shots someone takes in a season) vs. point scored in a season.
# Field goals attempted is on the x-axis, and points is on the y-axis.
# As you can tell, they are very strongly correlated. The plot is close to a straight line.
# The plot also slopes upward, which means that as field goal attempts go up, so do points.
# That means that the plot is positively correlated.
plt.scatter(nba_stats["fga"], nba_stats["pts"])
plt.show()

# If we make points negative (so the people who scored the most points now score the least,
# because 3000 becomes -3000), we can change the direction of the correlation.
# Field goals are negatively correlated with our new "negative" points column -- the more
# free throws you attempt, the less negative points you score.
# We can see this because the correlation line slopes downward.
plt.scatter(nba_stats["fga"], -nba_stats["pts"])
plt.show()

# Now, we can plot total rebounds (number of times someone got the ball back for
# their team after someone shot) vs total assists (number of times someone helped another person score).
# These are uncorrelated, so you don't see the same nice line as you see with the plot above.
plt.scatter(nba_stats["trb"], nba_stats["ast"])
plt.show()

# free throws attempted vs points, strong correlation
plt.scatter(nba_stats["fta"], nba_stats["pts"])
plt.show()

# steals
plt.scatter(nba_stats["stl"], nba_stats["pf"])
plt.show()


# Make a function that calculates covariance.
# STEPS:
# First, calculate the mean of the x and y vectors.
# # Then, subtract the mean from each element in the x vector.
# Do the same for the y vectors.
# Multiply the elements at each position by each other, starting at 0, and make a new vector.
# Add up all of the elements in the new vector, then divide by its length.
def covariance_a_b(a, b):
    mean_a = sum(a) / len(a)
    mean_b = sum(b) / len(b)
    covariance = 0

    # create a new vector by substracting the mean value from each element
    substracted_a = [i - mean_a for i in a]
    substracted_b = [i - mean_b for i in b]

    codeviates = [substracted_a[i] * substracted_b[i] for i in range(len(a))]

    covariance = sum(codeviates) / len(codeviates)
    return covariance

cov_stl_pf = covariance_a_b(nba_stats["stl"], nba_stats["pf"])
cov_fta_pts = covariance_a_b(nba_stats["fta"], nba_stats["pts"])