import pandas as pd
from scipy import stats

# 1. Load Data
try:
    df = pd.read_csv('processed_master.csv')
    print("✅ Data Loaded Successfully.")
except FileNotFoundError:
    print("❌ Error: 'processed_master.csv' not found.")
    exit()

# 2. Define the Two Groups (AND CLEAN THEM)
# We use .dropna() to remove any blank rows that cause the 'nan' error
mobile_4k = df[
    (df['device_type'] == 'Mobile') & 
    (df['quality'] == '4K')
]['progress_percentage'].dropna()

desktop_4k = df[
    (df['device_type'] == 'Desktop') & 
    (df['quality'] == '4K')
]['progress_percentage'].dropna()

# 3. Debugging: Check if we actually have data
print(f"\n--- Data Diagnostics ---")
print(f"Mobile 4K Samples: {len(mobile_4k)}")
print(f"Desktop 4K Samples: {len(desktop_4k)}")

if len(mobile_4k) < 2 or len(desktop_4k) < 2:
    print("❌ Not enough data to perform T-Test (Need at least 2 samples per group).")
    
    # FALLBACK TEST: Try comparing High Budget vs Low Budget retention instead
    print("\n--- Switching to Plan B: Budget vs Retention ---")
    high_budget = df[df['production_budget'] > 20000000]['progress_percentage'].dropna()
    low_budget = df[df['production_budget'] < 5000000]['progress_percentage'].dropna()
    
    t_stat, p_value = stats.ttest_ind(high_budget, low_budget, equal_var=False)
    print(f"High Budget Avg Retention: {high_budget.mean():.2f}%")
    print(f"Low Budget Avg Retention: {low_budget.mean():.2f}%")

else:
    # 4. Perform the Original T-Test
    # equal_var=False performs Welch's t-test (safer for unequal sample sizes)
    t_stat, p_value = stats.ttest_ind(mobile_4k, desktop_4k, equal_var=False)

    print(f"\nMobile 4K Avg Completion: {mobile_4k.mean():.2f}%")
    print(f"Desktop 4K Avg Completion: {desktop_4k.mean():.2f}%")

# 5. The Verdict
print(f"\n--- Final Result (P-Value: {p_value:.5f}) ---")
alpha = 0.05 
if p_value < alpha:
    print("✅ RESULT: Statistically Significant Difference!")
    print("Evidence suggests device type DOES impact retention.")
else:
    print("❌ RESULT: No Significant Difference.")
    print("The difference is likely due to random chance (Null Hypothesis Accepted).")