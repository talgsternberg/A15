# An original calculation by Tal Sternberg for A15
# Using data of dwarf-spectral-type L-H values, this script compares the L-H values from the
# R08 census to these spectral classifications and if they match it assigns this star to
# having dwarftype properties.

from astropy.table import Table
import matplotlib.pyplot as plt

number_dwarfs = 0

# read in the R08 Values
R08 = Table.read("R08.txt", format="ascii.cds")

# read in modified spectral type J-H values
st = open("stellar-types.txt", "r")

# fill in a dictionary for number of stellar types all with keys all @ 0 count
stellar_types= {}
stellar_types_number_of = {}
stellar_JH = []
for line in st:
    spec = line.split(" ")
    if (spec[1] != 'null'):
      stellar_types[spec[0]] = float(spec[1])
      stellar_JH.append(spec[1])
      stellar_types_number_of[spec[0]] = 0
print(R08)


# for each object in the R08, pull calculate the J-H values and put in a list
JHR08 = []
for star in R08:
    if((star[5] != "--") and (star[6] != "--")):
        # J-H for R08
        JH = star[5]-star[6]
        JHR08.append(JH)

for star in JHR08:
    for type in stellar_types:
        if (((stellar_types[type]-0.01) <= star) and (star <= (stellar_types[type]+0.01))):
            number_dwarfs += 1
            stellar_types_number_of[type] += 1


percent_dwarf = (number_dwarfs/18949)*100

# hist R08
plt.xlabel('J-H value')
plt.ylabel('Frequency')
plt.title('J-H Value Frequency For The R08 Survey')
plt.hist(JHR08, 10)
plt.show()

number_other = 0
majority = {}
for key, val in stellar_types_number_of.items():
    if (14 < val):
        majority[key] = val
    elif val <= 14:
         number_other += val
majority["Other"] = number_other
print(majority)

# pie plot of spectral types present
plt.title('Spectral Types of Dwarf-Like Stars Observed Through R08')
labels = list(majority.keys())
values = list(majority.values())
plt.pie(values, labels=labels)
plt.show()


print("number of stellar objects with dwarflike J-H features: " + str(number_dwarfs))
print("Percent of total from R08: " + str(percent_dwarf) + "%" )
#print(stellar_types_number_of)
