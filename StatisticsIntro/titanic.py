import pandas
import matplotlib.pyplot as plt
import numpy
from scipy.stats import skew
from scipy.stats import kurtosis

f = "titanic_survival.csv"
titanic_survival = pandas.read_csv(f)

# Luckily, pandas DataFrames have a method that can drop rows that have missing data
# Let's look at how large the DataFrame is first
print(titanic_survival.shape)

# There were 1,310 passengers on the Titanic, according to our data
# Now let's drop any rows that have missing data
# The DataFrame dropna method will do this for us
# It will remove any rows with that contain missing values
new_titanic_survival = titanic_survival.dropna()

# Hmm, it looks like we were too zealous with dropping rows that contained NA values
# We now have no rows in our DataFrame
# This is because some of the later columns, which aren't immediately relevant to our analysis,
# contain a lot of missing values
print(new_titanic_survival.shape)

# We can use the subset keyword argument to the dropna method so that it only drops rows if there are
# NA values in certain columns
# This line of code will drop any row where the embarkation port (where people boarded the Titanic)
# or cabin number is missing
new_titanic_survival = titanic_survival.dropna(subset=["embarked", "cabin"])

# This result is much better. We've only removed the rows we needed to.
print(new_titanic_survival.shape)

new_titanic_survival = titanic_survival.dropna(subset=["age", "sex"])
print(new_titanic_survival.shape)
print(new_titanic_survival.head())

# Plot a histogram of the "age" column in new_titanic_survival.
# Add a green line for the median.
# Add a red line for the mean.
plt.hist(new_titanic_survival["age"])

plt.axvline(new_titanic_survival["age"].mean(), color="r")
plt.axvline(numpy.median(new_titanic_survival["age"]), color="g")

plt.show()

# Calculate the mean of the "age" column
mean_age = new_titanic_survival["age"].mean()
# Calculate the median of the "age" column
median_age = numpy.median(new_titanic_survival["age"])
# Calculate the skew of the "age" column
skew_age = skew(new_titanic_survival["age"])
# Calculate the kurtosis of the "age" column
kurtosis_age = kurtosis(new_titanic_survival["age"])