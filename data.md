# Data

## What do I know aout the data?
### Column headings:

'Period': str
- This is the time period of the data.
- Possible values:
['2022-23']

'Dimension': str
- Possible Values:
['AgeAtBookingMotherGroup' 'ApgarScore5TermGroup7'
 'BabyFirstFeedBreastMilkStatus' 'BirthweightTermGroup'
 'BirthweightTermGroup2500' 'ComplexSocialFactorsInd'
 'DeliveryMethodBabyGroup' 'DeprivationDecileAtBooking'
 'EthnicCategoryMotherGroup' 'FolicAcidSupplement'
 'GestAgeFormalAntenatalBookingGroup' 'GestationLengthBirth'
 'GestationLengthBirthGroup37' 'OnsetOfLabour'
 'PlaceTypeActualDeliveryMidwifery' 'PreviousCaesareanSectionsGroup'
 'PreviousLiveBirthsGroup' 'SkinToSkinContact1HourTerm'
 'SmokingStatusGroupBooking' 'TotalBabies' 'TotalDeliveries']

'Org_Level': str
- Granularity of data. Is either National, NHS England (Region) or Provider
- Possible Values:
['National' 'NHS England (Region)' 'Provider']

'Org_Code': str
- Code for the Org, typical three characters or National

'Org_Name': str
- Name of the organisation

'Measure': str
- Sub group of the dimension
- Possible Values:
['Under 20' '20 to 24' '25 to 29' '30 to 34' '35 to 39' '40 to 44'
 '45 or Over' '0 to 6' '7 to 10'
 'Missing value / Value outside reporting parameters'
 'Maternal or Donor Breast Milk' 'Not Breast Milk' 'Under 1500g'
 '1500g to 1999g' '2000g to 2499g' '2500g to 2999g' '3000g to 3499g'
 '3500g to 3999g' '4000g to 4999g' '5000g and over' 'Under 2500g'
 '2500g and over' 'N' 'Y' 'Elective caesarean section'
 'Emergency caesarean section' 'Instrumental' 'Other' 'Spontaneous' '02'
 '03' '04' '05' '06' '07' '08' '09' '01 - Most deprived'
 '10 - Least deprived'
 'Pseudo postcode recorded (includes no fixed abode or resident overseas)'
 'Resident Elsewhere in UK, Channel Islands or Isle of Man'
 'Any other ethnic group' 'Asian or Asian British'
 'Black or Black British' 'Mixed' 'Not known' 'Not Stated' 'White'
 'Has been taking prior to becoming pregnant'
 'Not Stated (Person asked but declined to provide a response)'
 'Not taking folic acid supplement'
 'Started taking once pregnancy confirmed' '0 to 70 days' '141+ days'
 '71 to 90 days' '91 to 140 days' '27 weeks and under' '28 to 31 weeks'
 '32 to 33 weeks' '34 to 36 weeks' '37 weeks' '38 weeks' '39 weeks'
 '40 weeks' '41 weeks' '42 weeks' '43 weeks and over' '<37 weeks'
 '>=37 weeks' 'Caesarean Section' 'Medical induction'
 'Surgical and medical induction' 'Surgical induction' 'Home (NHS care)'
 'Home (private care)' 'In transit (with NHS ambulance services)'
 'In transit (with private ambulance services)'
 'In transit (without healthcare services present)'
 'Maternity assessment or triage unit/ area'
 'NHS Alongside midwifery unit' 'NHS Freestanding midwifery unit (FMU)'
 'NHS Obstetric unit (including theatre)'
 'NHS ward/health care setting without delivery facilities'
 'Non-domestic and non-health care setting' 'Not known (not recorded)'
 'Other (not listed)' 'Private hospital' 'At least one Caesarean'
 'At least one Previous Birth, zero Caesareans' 'Zero Previous Births' '1'
 '2' '3' '4' '5+' 'No previous live births' 'No' 'Yes'
 'Non-Smoker / Ex-Smoker' 'Smoker' nan]

'Count_Of': str
- Either "Babies" or "Deliveries"- seems to be what the measure is referring to?
- Possible Values:
['Deliveries' 'Babies']

'Value':num
- The value for the given row, rounded to the nearest 5
