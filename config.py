measure_dict = {
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
    "PreviousLiveBirthsGroup": {
        "numerator": ["No previous live births"],
        "denominator": ["No previous live births", "1", "2", "3", "4", "5+"],
        "map_title": "Percentage of mothers with no previous live births",
        "rate_col": "Percent"
    },
    "SkinToSkinContact1HourTerm": {
        "numerator": ["Yes"],
        "denominator": ["Yes", "No"],
        "map_title": "Percentage of mothers that had skin to skin contact within 1 hour of birth",
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
AgeAtBookingMotherGroup
- All have 30-34 as most popular group. Could find proportion of that as a whole? 
- or which has the largest portion of oldest/youngest category? 
- an option for each age group?
- could find rate for all submitters for 30-34 and then note which has the most deviation from that?
BirthweightTermGroup
- Similar issue to age group. 
DeliveryMethodBabyGroup
- Spontaneous birth rate vs all others?
DeprivationDecileAtBooking
- there are 10: most common? Find a mean and round it?
EthnicCategoryMotherGroup
- All one colour, hover to see chart.
- Unless could find population estimates for ethnicity and therefore get rate of mothers
GestationLengthBirth
- 39 weeks is most common for all. get rate of this against all others?
OnsetOfLabour
- spontaneous vs others?
PlaceTypeActualDeliveryMidwifery
- maternity ward vs all others?
PreviousCaesareanSectionsGroup
- rate of mothers that had had at least one caesarean?
"""

