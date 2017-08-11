
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
