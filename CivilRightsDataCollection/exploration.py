import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("dataCRDC2013_14.csv", encoding="Latin-1")
    print(data["JJ"].value_counts())
    print(data["SCH_STATUS_MAGNET"].value_counts())
    
    jj_pivot = pd.pivot_table(data, values=["TOT_ENR_M", "TOT_ENR_F"], index="JJ", aggfunc="sum")
    sch_pivot = pd.pivot_table(data, values=["TOT_ENR_M", "TOT_ENR_F"], index="SCH_STATUS_MAGNET", aggfunc="sum")
    
    print(jj_pivot)
    print(sch_pivot)