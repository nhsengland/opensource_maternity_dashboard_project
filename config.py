measure_dict = {
        "AgeAtBookingMotherGroup": {
        "numerator": ["35 to 39", "40 to 44", "45 or Over"],
        "denominator": ["Under 20", "20 to 24", "25 to 29", "30 to 34", "35 to 39", "40 to 44", "45 or Over"],
        "map_title": "Percentage of Mothers OVER the age of 35",
        "rate_col": "Percent"
    },
    "ApgarScore5TermGroup7": {
        "numerator": ["7 to 10"],
        "denominator": ["0 to 6", "7 to 10"],
        "map_title": "Percentage of babies with an APGAR score of 7 to 10",
        "rate_col": "Percent"
    },
    "BabyFirstFeedBreastMilkStatus": {
        "numerator": ["Maternal or Donor Breast Milk"],
        "denominator": ["Maternal or Donor Breast Milk", "Not Breast Milk"],
        "map_title": "Percentage of babies whose first feed was breast milk",
        "rate_col": "Percent"
    },
    "BirthweightTermGroup2500": {
        "numerator": ["2500g and over"],
        "denominator": ["2500g and over", "Under 2500g"],
        "map_title": "Percentage of babies born with a weight over 2500g",
        "rate_col": "Percent"
    },
    "ComplexSocialFactorsInd": {
        "numerator": ["Y"],
        "denominator": ["Y", "N"],
        "map_title": "Percentage of mothers with complex social factors indicators",
        "rate_col": "Percent"
    },
    "DeliveryMethodBabyGroup": {
        "numerator": ["Spontaneous"],
        "denominator": ["Elective caesarean section", "Emergency caesarean section", "Instrumental", "Other", "Spontaneous"],
        "map_title": "Percentage of Births classed as 'Spontaneous'",
        "rate_col": "Percent"
    },
    "DeprivationDecileAtBooking": {
        "numerator": ["01 - Most deprived"],
        "denominator": ["01 - Most deprived", "02", "03", "04", "05", "06", "07", "08", "09", "10 - Least deprived"],
        "map_title": "Percentage of Mothers living in the Most Deprived areas",
        "rate_col": "Percent"
    },
    "FolicAcidSupplement": {
        "numerator": ["Has been taking prior to becoming pregnant","Started taking once pregnancy confirmed"],
        "denominator": ["Has been taking prior to becoming pregnant","Started taking once pregnancy confirmed", 
                        "Not taking folic acid supplement", "Not Stated (Person asked but declined to provide a response)"],
        "map_title": "Percentage of mothers taking folic acid supplement",
        "rate_col": "Percent"
    },
    "GestAgeFormalAntenatalBookingGroup": {
        "numerator": ["0 to 70 days"],
        "denominator": ["0 to 70 days", "141+ days", "71 to 90 days", "91 to 140 days"],
        "map_title": "Percentage of Antenatal Bookings made at gestional length of up to 70 days",
        "rate_col": "Percent"
    },
    "GestationLengthBirthGroup37": {
        "numerator": [">=37 weeks"],
        "denominator": [">=37 weeks", "<37 weeks"],
        "map_title": "Percentage of babies with a gestational length of at least 37 weeks (full term)",
        "rate_col": "Percent"
    },
    "OnsetOfLabour": {
        "numerator": ["Spontaneous"],
        "denominator": ["Caesarean Section", "Medical induction", "Not known", "Spontaneous", "Surgical and medical induction", "Surgical induction"],
        "map_title": "Percentage of labours with a spontaneous onset",
        "rate_col": "Percent"
    },
    "PreviousLiveBirthsGroup": {
        "numerator": ["No previous live births"],
        "denominator": ["No previous live births", "1", "2", "3", "4", "5+"],
        "map_title": "Percentage of mothers with no previous live births",
        "rate_col": "Percent"
    },
    "PlaceTypeActualDeliveryMidwifery": {
        "numerator": ["NHS Obstetric unit (including theatre)"],
        "denominator": ["Home (NHS care)", "Home (private care)", "In transit (with NHS ambulance services)", 
                        "In transit (with private ambulance services)", "In transit (without healthcare services present)",
                        "Maternity assessment or triage unit/ area", "NHS Alongside midwifery unit",
                        "NHS Freestanding midwifery unit (FMU)", "NHS Obstetric unit (including theatre)",
                        "NHS ward/health care setting without delivery facilities", "Non-domestic and non-health care setting",
                        "Not known (not recorded)", "Other (not listed)", "Private hospital"],
        "map_title": "Percentage of deliveries in an NHS Obstetric unit (including theatre)",
        "rate_col": "Percent"
    },
    "SkinToSkinContact1HourTerm": {
        "numerator": ["Yes"],
        "denominator": ["Yes", "No"],
        "map_title": "Percentage of mothers that had skin to skin contact within 1 hour of birth",
        "rate_col": "Percent"
    },
    "PreviousCaesareanSectionsGroup": {
        "numerator": ["At least one Caesarean"],
        "denominator": ["At least one Caesarean", '"At least one Previous Birth, zero Caesareans"', "Zero Previous Births"],
        "map_title": "Percentage of mothers, giving birth, who have already had at least one caesarean",
        "rate_col": "Percent"
    },
    "SmokingStatusGroupBooking": {
        "numerator": ["Smoker"],
        "denominator": ["Smoker", "Non-Smoker / Ex-Smoker"],
        "map_title": "Percentage of Smokers at Booking",
        "rate_col": "Percent"
    },
    "TotalBabies": {
        "numerator": [],
        "denominator": [],
        "map_title": "Rate of babies born per 1000 people",
        "rate_col": "Rate"
    },
        "TotalDeliveries": {
        "numerator": [],
        "denominator": [],
        "map_title": "Rate of deliveries per 1000 people",
        "rate_col": "Rate"
    }
}

"""
Dimensions still to be considered:
BirthweightTermGroup
- Already is a plus/minus 2500g
EthnicCategoryMotherGroup
- All one colour, hover to see chart.
- Unless could find population estimates for ethnicity and therefore get rate of mothers
GestationLengthBirth
- 39 weeks is most common for all. get rate of this against all others?
- plus minus 37 is already a category. this is premature cutoff
"""

