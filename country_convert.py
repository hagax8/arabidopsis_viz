import sys
import numpy as np

from pycountry_convert import (
    map_countries,
    country_alpha2_to_country_name,
    country_name_to_country_alpha2,
    country_alpha3_to_country_alpha2,
    country_alpha2_to_continent_code,
    COUNTRY_NAME_FORMAT_UPPER
)


continent_dico = {
    "EU": "Europe",
    "NA": "North America",
    "OC": "Oceania",
    "SA": "South America",
    "AS": "Asia",
    "AN": "Antarctica",
    "AF": "Africa"
}

alpha3_ico = {
    "UK": "GBR",
    "ALG": "DZA",
    "ASA": "ASM",
    "ANG": "AGO",
    "ANT": "ATG",
    "ARU": "ABW",
    "BAH": "BHS",
    "BRN": "BHR",
    "BAN": "BGD",
    "BAR": "BRB",
    "BIZ": "BLZ",
    "BER": "BMU",
    "BHU": "BTN",
    "BOT": "BWA",
    "IVB": "VGB",
    "BRU": "BRN",
    "BUL": "BGR",
    "BUR": "BFA",
    "CAM": "KHM",
    "CAY": "CYM",
    "CHA": "TCD",
    "CHI": "CHL",
    "CGO": "COG",
    "CRC": "CRI",
    "CRO": "HRV",
    "DEN": "DNK",
    "ESA": "SLV",
    "GEQ": "GNQ",
    "FIJ": "FJI",
    "GAM": "GMB",
    "GER": "DEU",
    "GRE": "GRC",
    "GRN": "GRD",
    "GUA": "GTM",
    "GUI": "GIN",
    "GBS": "GNB",
    "HAI": "HTI",
    "HON": "HND",
    "INA": "IDN",
    "IRI": "IRN",
    "KUW": "KWT",
    "LAT": "LVA",
    "LIB": "LBN",
    "LES": "LSO",
    "LBA": "LBY",
    "MAD": "MDG",
    "MAW": "MWI",
    "MAS": "MYS",
    "MTN": "MRT",
    "MRI": "MUS",
    "MON": "MCO",
    "MGL": "MNG",
    "MYA": "MMR",
    "NEP": "NPL",
    "NED": "NLD",
    "NCA": "NIC",
    "NIG": "NER",
    "NGR": "NGA",
    "OMA": "OMN",
    "PLE": "PSE",
    "PAR": "PRY",
    "PHI": "PHL",
    "POR": "PRT",
    "PUR": "PRI",
    "SKN": "KNA",
    "VIN": "VCT",
    "SAM": "WSM",
    "KSA": "SAU",
    "SEY": "SYC",
    "SIN": "SGP",
    "SLO": "SVN",
    "SOL": "SLB",
    "RSA": "ZAF",
    "SRI": "LKA",
    "SUD": "SDN",
    "SUI": "CHE",
    "TPE": "TWN",
    "TAN": "TZA",
    "TOG": "TGO",
    "TGA": "TON",
    "TRI": "TTO",
    "UAE": "ARE",
    "ISV": "VIR",
    "URU": "URY",
    "VAN": "VUT",
    "VIE": "VNM",
    "ZAM": "ZMB",
    "ZIM": "ZWE",
}

countrynames = []
continentcodes = []

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if line == "UNK":
            countrynames.append("Kosovo")
            continentcodes.append(continent_dico["EU"])
        else:
            try:
                countrynames.append(country_alpha2_to_country_name(
                                    country_alpha3_to_country_alpha2(line)))
            except:
                line = alpha3_ico[line]
                countrynames.append(country_alpha2_to_country_name(
                                    country_alpha3_to_country_alpha2(line)))

            continentcodes.append(continent_dico[country_alpha2_to_continent_code(
                                  country_alpha3_to_country_alpha2(line))])

np.savetxt("continents.csv", continentcodes, delimiter=',', fmt="%s")
np.savetxt("countrynames.csv", countrynames, delimiter=',', fmt="%s")
