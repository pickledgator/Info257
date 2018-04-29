
import dataset
from stuf import stuf
import pprint
import database_helpers

#Given a new insurance claim, determine whether to increase a customer's premium
def premium_change(db, CustomerID):
    claims = list(db.query("Select * from claims WHERE CustomerID==" + CustomerID))

    New_RiskScore = ( \
    sum(1 if float(claim['Severity']) == 0 else 0 for claim in claims) *.3 + \
    sum(1 if float(claim['Severity']) == 1 else 0 for claim in claims) *.4 + \
    sum(1 if float(claim['Severity']) == 2 else 0 for claim in claims) *.5 + \
    sum(1 if float(claim['Severity']) == 3 else 0 for claim in claims) *.7 + \
    sum(1 if float(claim['Severity']) == 5 else 0 for claim in claims) *.9 + \
    sum(1 if float(claim['Severity']) == 5 else 0 for claim in claims) *1.2)

    print("Customer new Risk Score {}".format(New_RiskScore))

    RiskScore = float(list(db.query("Select RiskScore from customer WHERE CustomerID==" + CustomerID))[0]['RiskScore'])
    #RiskScore = list(db.query("Select RiskScore from customer WHERE CustomerID==" + CustomerID))[0]['RiskScore']
    print("Customer original Risk Score {}".format(RiskScore))

    if New_RiskScore > (RiskScore * 1.5):
        print("The customer's premium has increased")
        #dict_data = [dict(CustomerID=CustomerID, RiskScore=New_RiskScore)]
        #database_helpers.update_table(db, dict_data, "customer", ['CustomerID'])
        return New_RiskScore

    else:
        print("The customer's premium has not changed")
        return RiskScore

def claim_cost_to_repair(Severity, BookValue):
    claim_cost_to_repair = []

    if Severity == 0:
        claim_cost_to_repair = BookValue * .2
    if Severity == 1:
        claim_cost_to_repair = BookValue * .3
    if Severity == 2:
        claim_cost_to_repair = BookValue * .3
    if Severity == 3:
        claim_cost_to_repair = BookValue * .5
    if Severity == 4:
        claim_cost_to_repair = BookValue * .8
    if Severity == 5:
        claim_cost_to_repair = BookValue * 1

    print("The cost to repair is {} for a car worth {}".format(claim_cost_to_repair, BookValue))
    return claim_cost_to_repair



def generate_report(db, input_data):
    # call helper calculation functions to compute all of the new numbers
    #...

    # populate output data structure to send to front end
    report_data = {}
    report_data['customer_name'] = "Rachelle Kresch"
    report_data['customer_id'] = "1000404"
    report_data['policy_details'] = "Some text about the policy"
    report_data['deductible'] = "1000"
    report_data['premium'] = "1000"
    report_data['customer_number_of_vehicles'] = 2
    report_data['customer_risk_score'] = 1.0
    report_data['claim_id'] = 10024
    report_data['claim_description'] = "This is some text"
    report_data['claim_cost_to_repair'] = 5000
    report_data['claim_vehicle_make_model'] = "Toyota Camry"
    report_data['claim_vehicle_year'] = 2015
    report_data['claim_vehicle_image_url'] = "http://st.motortrend.com/uploads/sites/10/2016/07/2017-toyota-camry-se-hybrid-sedan-angular-front.png"
    report_data['claim_vehicle_value'] = 10000
    report_data['claim_covered_repair_value'] = 4500
    report_data['claim_out_of_pocket_expense'] = 500
    report_data['claim_deductible_contributions'] = 500
    report_data['claim_remaining_deductible'] = 0
    report_data['claim_new_risk_score'] = 2.4
    report_data['claim_new_premium'] = 2000
    return report_data


if __name__ == "__main__":
    db = dataset.connect('sqlite:///AutoInsurace.db', row_type=stuf)
    premium_change(db, "100420")
    claim_cost_to_repair(1, 7000)
