import files_folders as paths
from tools import load_data

# Treatment settings 
group_size = 1
number_of_questions_per_stage = 12

# Parameters
amount_UBI = 1000
amount_UBIWS = 500
subsidy_rate_UBIWS = 0.05
subsidy_rate_WS = 0.10
wage_high = 4000
wage_low = 2500
flat_tax_rate = 0.25
progressive_tax_rate_low = 0.11
progressive_tax_rate_high = 0.41

# 17667 €
cutoff_income_low = round((wage_high*12-wage_low)/3+wage_low)

# 32833
cutoff_income_high = round((wage_high*12-wage_low)*2/3+wage_low)

# 15167 € (48000 - 32833 €)
diff_cutoff_income_high_to_wage_high = wage_high * number_of_questions_per_stage - cutoff_income_high

#32833 - 17667
diff_cutoff_income_high_to_low = cutoff_income_high - cutoff_income_low

button_names = ['Complex', 'Simple', 'Unpaid', 'Nowork']
task_ids = [1, 5, 10]

unpaid_assignment = {
    0: [1, 2],
    1: [3, 4],
    2: [5, 6],
    3: [7, 8],
    4: [9, 10],
    5: [11, 12],
    6: [13, 14],
    7: [15, 16],
    8: [17, 18],
    9: [19, 20],
    10: [21, 22],
    11: [23, 24]
}

complex_content1 = list(load_data(paths.path_complex1).keys())
complex_content2 = list(load_data(paths.path_complex2).keys())
complex_answers1 = list(load_data(paths.path_complex1).values())
complex_answers2 = list(load_data(paths.path_complex2).values())
simple_content1 = list(load_data(paths.path_simple1).keys())
simple_content2 = list(load_data(paths.path_simple2).keys())
simple_answers1 = list(load_data(paths.path_simple1).values())
simple_answers2 = list(load_data(paths.path_simple2).values())

