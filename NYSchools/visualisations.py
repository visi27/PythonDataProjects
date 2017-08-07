# Continued from project.py. Check and combine together with jupyter notebook

# Compute correlations between columns in the dataset
correlations = combined.corr()

# Keep only the column with correlations to sat_result
correlations = correlations["sat_score"]
print(correlations)

# Total enrollment and sat_score seem correlated. Lets plot a scatter plot to show this relation
import matplotlib.pyplot as plt

combined.plot.scatter(x="total_enrollment", y="sat_score")
plt.show()

# From the scatter plot we can see the relation beteen the above fields is not strong at all.
# But there is a cluster in the bottom left where both values are low. 
# Lets extract the schools of this cluster and see if we can find any interesting fact about this relation

low_enrollment = combined[(combined["total_enrollment"]<1000) & (combined["sat_score"]<1000)]
print(low_enrollment)

# Judging from the name af the schools this seem to be oriented to international students. 
# In fact the percentage of english learners is high. This must be strongly related to sat_scores. Lets explore this

combined.plot.scatter(x="ell_percent", y="sat_score")
plt.show()

# We still have a cluster of schools with low sat scores. These are the same as above.
# Lets explore which areas of the city have more english learners

# First scatter all schools on map
from mpl_toolkits.basemap import Basemap
m = Basemap(
    projection='merc', 
    llcrnrlat=40.496044, 
    urcrnrlat=40.915256, 
    llcrnrlon=-74.255735, 
    urcrnrlon=-73.700272,
    resolution='i'
)

m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)

latitudes = combined["lat"].tolist()
longitudes = combined["lon"].tolist()

m.scatter(longitudes, latitudes, s=20, zorder=2, latlon=True)
plt.show()

# Lets scatter the schools with different colours based on ell_percent
m.scatter(longitudes, latitudes, s=20, zorder=2, latlon=True, c=combined["ell_percent"], cmap="summer")
plt.show()

# Due to the high number of schools it's difficult to see which distrits have more schools with high ell_percent. 
# Lets aggregate ell_percent by district.
import numpy

districts = combined.groupby("school_dist").agg(numpy.mean)
districts.reset_index(inplace=True)
print(districts.head())

# Let scatter the data of districts on map
latitudes = districts["lat"].tolist()
longitudes = districts["lon"].tolist()

m.scatter(longitudes, latitudes, s=20, zorder=2, latlon=True, c=districts["ell_percent"], cmap="summer")
plt.show()