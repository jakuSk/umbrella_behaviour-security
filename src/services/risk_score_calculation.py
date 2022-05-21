def __calculate_risk_score_average(domain_list: list) -> float:
     """Calculate average risk score"""
     risk_score_sum = 0
     for domain in domain_list:
         risk_score_sum += domain['risk_score']

     if len(domain_list) > 0:
         return risk_score_sum / len(domain_list)

     return 0

 def __is_very_risky(domain_list: list) -> bool:
     """Check if the risk score is very risky"""
     for domain in domain_list:
         if domain['risk_score'] > 55:
             print('High risk lol')
             return True

     return False

 def __get_highest_risk(domain_list: list) -> int:
     """Get highest risk score"""
     highest_risk = 0
     for domain in domain_list:
         if domain['risk_score'] > highest_risk:
             highest_risk = domain['risk_score']

     return highest_risk

 def calculate_risk_score(domain_list: list) -> int:
     """Calculate risk score"""
     if (__is_very_risky(domain_list)):
         return __get_highest_risk(domain_list)
     else:
         return __calculate_risk_score_average(domain_list)