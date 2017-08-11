# Housefly wing lengths in millimeters
wing_lengths = [36, 37, 38, 38, 39, 39, 40, 40, 40, 40, 41, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 42, 42, 43, 43, 43,
                43, 43, 43, 43, 43, 44, 44, 44, 44, 44, 44, 44, 44, 44, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 46, 46,
                46, 46, 46, 46, 46, 46, 46, 46, 47, 47, 47, 47, 47, 47, 47, 47, 47, 48, 48, 48, 48, 48, 48, 48, 48, 49,
                49, 49, 49, 49, 49, 49, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 52, 52, 53, 53, 54, 55]
mean = sum(wing_lengths) / len(wing_lengths)
variances = [(i - mean) ** 2 for i in wing_lengths]
variance = sum(variances) / len(variances)
standard_deviation = variance ** (1 / 2)

standard_deviations = [(i - mean) / standard_deviation for i in wing_lengths]


def within_percentage(deviations, count):
    within = [i for i in deviations if i <= count and i >= -count]
    count = len(within)
    return count / len(deviations)


within_one_percentage = within_percentage(standard_deviations, 1)
within_two_percentage = within_percentage(standard_deviations, 2)
within_three_percentage = within_percentage(standard_deviations, 3)
print(within_one_percentage*100)
