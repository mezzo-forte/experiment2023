import json 
import settings


def load_data(path):
    with open(path, 'r', encoding="utf-8") as f:
        return json.loads(f.read())

def save_data(path, data):
    with open(path, "w") as g:
        g.write(json.dumps(data, indent=2))

def calculate_gross_income(earned, model):
    if model == 'UBI':
        gross_income = earned + settings.amount_UBI
    elif model == 'WS':
        gross_income = earned * (1 + settings.subsidy_rate_WS)
    elif model == 'UBIWS':
        gross_income = settings.amount_UBIWS + earned * (1 + settings.subsidy_rate_UBIWS)
    else: gross_income = 0
    return gross_income


def calculate_taxable_income(total_earned, model):
    taxable_income = 0
    if model== 'UBI':
        taxable_income = total_earned
    elif model == 'WS':
        taxable_income = total_earned 
    elif model == 'UBIWS':
        taxable_income = total_earned
    return taxable_income


# def calculate_net_income(taxable, model, active_part):
#     net_income = 0
#     if model == 'UBI':
#         if active_part == 1:
#             net_income = taxable * (1 - settings.flat_tax_rate) + settings.amount_UBI
#         elif active_part == 2:
#             if taxable <= settings.cutoff_income_high:
#                 net_income = settings.amount_UBI + taxable * (1 - settings.progressive_tax_rate_low)
#             else: 
#                 net_income = settings.cutoff_income_high * (1 - settings.progressive_tax_rate_low) + (taxable - settings.cutoff_income_high) * (1 - settings.progressive_tax_rate_high) + settings.amount_UBI

#     elif model == 'WS':
#         if active_part == 1:
#             if taxable <= settings.cutoff_income_low:
#                 net_income = taxable * (1 + settings.subsidy_rate_WS)
#             else:
#                 net_income = taxable * (1 + settings.subsidy_rate_WS) - settings.flat_tax_rate * (taxable - settings.cutoff_income_low) 
        
#         elif active_part == 2:
#             if taxable * (1 + settings.subsidy_rate_WS) <= settings.cutoff_income_low:
#                 net_income = taxable * (1 + settings.subsidy_rate_WS)
#             elif taxable * (1 + settings.subsidy_rate_WS) <= settings.cutoff_income_high:
#                 net_income = taxable * (1 + settings.subsidy_rate_WS) - settings.progressive_tax_rate_low * (taxable - settings.cutoff_income_low) 
#             else: 
#                 net_income = taxable * (1 + settings.subsidy_rate_WS) - settings.progressive_tax_rate_low * settings.diff_cutoff_income_high_to_low - settings.progressive_tax_rate_high * (taxable - settings.cutoff_income_high)

#         elif model == 'UBIWS':
#             if active_part == 1:
#                 if taxable * (1 + settings.subsidy_rate_UBIWS) <= settings.cutoff_income_low:
#                     net_income = settings.amount_UBIWS + taxable * (1 + settings.subsidy_rate_UBIWS)
#                 else:
#                     net_income = settings.amount_UBIWS + taxable * (1 + settings.subsidy_rate_UBIWS - settings.flat_tax_rate)

#             elif active_part == 2:
#                 if taxable * (1 + settings.subsidy_rate_UBIWS) <= settings.cutoff_income_low:
#                     net_income = settings.amount_UBIWS + taxable * (1 + settings.subsidy_rate_UBIWS)
#                 elif taxable * (1 + settings.subsidy_rate_UBIWS) <= settings.cutoff_income_high:
#                     net_income = settings.amount_UBIWS + (taxable - settings.cutoff_income_low) * (1 + settings.subsidy_rate_UBIWS - settings.progressive_tax_rate_low)
#                 else: 
#                     net_income = settings.amount_UBIWS + taxable * (1 + settings.subsidy_rate_UBIWS) - settings.progressive_tax_rate_low * settings.diff_cutoff_income_high_to_low - settings.progressive_tax_rate_high * (taxable - settings.cutoff_income_high)
    
#     return net_income


def calculate_tax_amount(taxable, model, active_part):
# def calculate_tax_amount(net_income, gross_income):
    tax_amount = 0
    if model == 'UBI':
        if active_part == 1:
            tax_amount = taxable * settings.flat_tax_rate
        elif active_part == 2:
            if taxable <= settings.cutoff_income_high:
                tax_amount = taxable * settings.progressive_tax_rate_low
            else: 
                tax_amount = settings.cutoff_income_high * settings.progressive_tax_rate_low + (taxable - settings.cutoff_income_high) * settings.progressive_tax_rate_high
 
    elif model == 'WS':
        if active_part == 1:
            if taxable <= settings.cutoff_income_low:
                tax_amount = 0
            else:
                tax_amount = (taxable - settings.cutoff_income_low) * settings.flat_tax_rate

        elif active_part == 2:
            if taxable <= settings.cutoff_income_low:
                tax_amount = 0
        # second tax bracket        
            elif taxable <= settings.cutoff_income_high:
                tax_amount = (taxable - settings.cutoff_income_low) * settings.progressive_tax_rate_low
        # third tax bracket
            else: 
                tax_amount = settings.progressive_tax_rate_low * settings.diff_cutoff_income_high_to_low + (taxable - settings.cutoff_income_high) * settings.progressive_tax_rate_high
                
    elif model=='UBIWS':
        if active_part == 1:
            if taxable <= settings.cutoff_income_low:
                tax_amount = 0
            else:
                tax_amount = (taxable - settings.cutoff_income_low) * settings.flat_tax_rate

        elif active_part == 2:
            if taxable <= settings.cutoff_income_low:
                tax_amount = 0
        # second tax bracket        
            elif taxable <= settings.cutoff_income_high:
                tax_amount = (taxable - settings.cutoff_income_low) * settings.progressive_tax_rate_low
        # third tax bracket
            else: 
                tax_amount = settings.progressive_tax_rate_low * settings.diff_cutoff_income_high_to_low + (taxable - settings.cutoff_income_high) * settings.progressive_tax_rate_high

    return tax_amount

def calculate_subsidy_amount(model, earned):
    subsidy_amount = "n/a"
    if model == 'WS':
        subsidy_amount = settings.subsidy_rate_WS * earned
    elif model == "UBIWS":
        subsidy_amount = settings.subsidy_rate_UBIWS * earned
    return subsidy_amount 

def calculate_transfer_amount(model, earned):
    transfer_amount = "n/a"
    if model == 'UBI':
        transfer_amount = settings.number_of_questions_per_stage * settings.amount_UBI
    elif model == 'UBIWS':
        transfer_amount = settings.number_of_questions_per_stage * settings.amount_UBIWS
    return transfer_amount
