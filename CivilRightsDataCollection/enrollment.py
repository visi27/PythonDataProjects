import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("data/CRDC2013_14.csv", encoding="Latin-1")
    
    data["total_enrollment"] = data["TOT_ENR_M"] + data["TOT_ENR_F"]
    
    enrollment_sums = {}
    enrollment_columns = [
        "SCH_ENR_HI_M",
        "SCH_ENR_HI_F",
        "SCH_ENR_AM_M",
        "SCH_ENR_AM_F",
        "SCH_ENR_AS_M",
        "SCH_ENR_AS_F",
        "SCH_ENR_HP_M",
        "SCH_ENR_HP_F",
        "SCH_ENR_BL_M",
        "SCH_ENR_BL_F",
        "SCH_ENR_WH_M",
        "SCH_ENR_WH_F",
        "SCH_ENR_TR_M",
        "SCH_ENR_TR_F"
    ]
    
    for col in enrollment_columns:
        enrollment_sums[col] = data[col].sum()
        
    all_enrollment = data["total_enrollment"].sum()
    print(enrollment_sums)
    print(all_enrollment)
    
    for key, value in enrollment_sums.items():
        print(key + " " + str((value/all_enrollment)*100))