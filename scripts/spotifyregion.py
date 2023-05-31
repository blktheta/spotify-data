class SpotifyRegion:
    """
    External application that configures the regional information,
    such as regional area, country name and ISO code.
    """

    def __init__(self, region: str) -> None:
        self.current_region = region
        self.country_codes = self.get_country_codes(region)
        self.country_names = self.get_country_names(region)
        self.country_regions = self.get_country_regions()
        return

    def get_country_codes(self, region: str) -> list:
        """
        Appends the regional country codes to the instance.
        """
        if region == "AF": 
            country_codes = list(self.african_region().keys())

        if region == "AS":
            country_codes = list(self.asian_region().keys())

        if region == "EU":
            country_codes = list(self.european_region().keys())

        if region == "NASAOC":
            country_codes = list(self.nasaoc_region().keys())
        return country_codes

    def get_country_names(self, region: str) -> dict:
        """
        Appends the regional dictionary to the instance.
        """
        if region == "AF":      country_names = self.african_region()
        if region == "AS":      country_names = self.asian_region()
        if region == "EU":      country_names = self.european_region()
        if region == "NASAOC":  country_names = self.nasaoc_region()
        return country_names

    def get_country_regions(self) -> dict:
        """
        Replaces 'country_name' values of regional dictionaries 
        with their 'regional_name'.
        """
        africa          = {key:"Africa" for key in self.african_region()}
        asia            = {key:"Asia" for key in self.asian_region()}
        europe          = {key:"Europe" for key in self.european_region()}
        north_america   = {key:"North America" for key in self.north_american_region()}
        south_america   = {key:"South America" for key in self.south_american_region()}
        oceania         = {key:"Oceania" for key in self.oceanian_region()}

        country_regions = dict()
        country_regions.update(africa) 
        country_regions.update(asia) 
        country_regions.update(europe) 
        country_regions.update(north_america) 
        country_regions.update(south_america) 
        country_regions.update(oceania)
        return country_regions
    
    # Full list of markets available in Spotify Web API.
    def african_region(self) -> dict:
        return {
            "DZ": "Algeria",
            "AO": "Angola",
            "BJ": "Benin",
            "BW": "Botswana",
            "BF": "Burkina Faso",
            "BI": "Burundi",
            "CM": "Cameroon",
            "CV": "Cape Verde",
            "TD": "Chad",
            "KM": "Comoros",
            "CG": "Republic of the Congo",
            "CD": "Democratic Republic of the Congo",
            "CI": "Côte d'Ivoire",
            "DJ": "Djibouti",
            "EG": "Egypt",
            "GQ": "Equatorial Guinea",
            "ET": "Ethiopia",
            "GA": "Gabon",
            "GM": "Gambia",
            "GH": "Ghana",
            "GN": "Guinea",
            "GW": "Guinea-Bissau",
            "KE": "Kenya",
            "LS": "Lesotho",
            "LR": "Liberia",
            "LY": "Libya",
            "MG": "Madagascar",
            "MW": "Malawi",
            "ML": "Mali",
            "MR": "Mauritania",
            "MU": "Mauritius",
            "MA": "Morocco",
            "MZ": "Mozambique",
            "NA": "Namibia",
            "NE": "Niger",
            "NG": "Nigeria",
            "RW": "Rwanda",
            "ST": "Sao Tome and Principe",
            "SN": "Senegal",
            "SC": "Seychelles",
            "SL": "Sierra Leone",
            "ZA": "South Africa",
            "SZ": "Swaziland",
            "TZ": "Tanzania",
            "TG": "Togo",
            "TN": "Tunisia",
            "UG": "Uganda",
            "ZM": "Zambia",
            "ZW": "Zimbabwe",
        }   # 49

    def asian_region(self) -> dict:
        return {
            "AM": "Armenia",
            "AZ": "Azerbaijan",
            "BH": "Bahrain",
            "BD": "Bangladesh",
            "BT": "Bhutan",
            "BN": "Brunei Darussalam",
            "KH": "Cambodia",
            "GE": "Georgia",
            "HK": "Hong Kong",
            "IN": "India",
            "ID": "Indonesia",
            "IQ": "Iraq",
            "IL": "Israel",
            "JP": "Japan",
            "JO": "Jordan",
            "KR": "Korea",
            "KW": "Kuwait",
            "KG": "Kyrgyzstan",
            "LA": "Lao People's Democratic Republic",
            "LB": "Lebanon",
            "MO": "Macao",
            "MY": "Malaysia",
            "MV": "Maldives",
            "MN": "Mongolia",
            "NP": "Nepal",
            "OM": "Oman",
            "PK": "Pakistan",
            "PS": "Palestine, State of",
            "PH": "Philippines",
            "QA": "Qatar",
            "SA": "Saudi Arabia",
            "SG": "Singapore",
            "LK": "Sri Lanka",
            "TW": "Taiwan",
            "TJ": "Tajikistan",
            "TH": "Thailand",
            "TL": "Timor-Leste",
            "AE": "United Arab Emirates",
            "UZ": "Uzbekistan",
            "VN": "Viet Nam",
        }   # 40

    def european_region(self) -> dict:
        return {
            "AL": "Albania",
            "AD": "Andorra",
            "AT": "Austria",
            "BY": "Belarus",
            "BE": "Belgium",
            "BA": "Bosnia",
            "BG": "Bulgaria",
            "HR": "Croatia",
            "CY": "Cyprus",
            "CZ": "Czech Republic",
            "DK": "Denmark",
            "EE": "Estonia",
            "FI": "Finland",
            "FR": "France",
            "DE": "Germany",
            "GR": "Greece",
            "HU": "Hungary",
            "IS": "Iceland",
            "IE": "Ireland",
            "IT": "Italy",
            "KZ": "Kazakhstan",
            "XK": "Kosovo",
            "LV": "Latvia",
            "LI": "Liechtenstein",
            "LT": "Lithuania",
            "LU": "Luxembourg",
            "MK": "North Macedonia",
            "MT": "Malta",
            "MD": "Moldova",
            "MC": "Monaco",
            "ME": "Montenegro",
            "NL": "Netherlands",
            "NO": "Norway",
            "PL": "Poland",
            "PT": "Portugal",
            "RO": "Romania",
            "SM": "San Marino",
            "RS": "Serbia",
            "SK": "Slovakia",
            "SI": "Slovenia",
            "ES": "Spain",
            "SE": "Sweden",
            "CH": "Switzerland",
            "TR": "Turkey",
            "UA": "Ukraine",
            "GB": "United Kingdom",
        }   # 46
    
    def nasaoc_region(self) -> dict:
        """
        Helper method that combines  smaller regions.
        """
        nasaoc_countries = dict()
        nasaoc_countries.update(self.north_american_region())
        nasaoc_countries.update(self.south_american_region())
        nasaoc_countries.update(self.oceanian_region())
        return nasaoc_countries

    def north_american_region(self) -> dict:
        return {
            "AG": "Antigua and Barbuda",
            "BS": "Bahamas",
            "BB": "Barbados",
            "BZ": "Belize",
            "CA": "Canada",
            "CR": "Costa Rica",
            "CW": "Curaçao",
            "DM": "Dominica",
            "DO": "Dominican Republic",
            "SV": "El Salvador",
            "GD": "Grenada",
            "GT": "Guatemala",
            "HT": "Haiti",
            "HN": "Honduras",
            "JM": "Jamaica",
            "MX": "Mexico",
            "NI": "Nicaragua",
            "PA": "Panama",
            "KN": "Saint Kitts and Nevis",
            "LC": "Saint Lucia",
            "VC": "Saint Vincent and the Grenadines",
            "TT": "Trinidad and Tobago",
            "US": "United States",
        }   # 23

    def south_american_region(self) -> dict:
        return {
            "AR": "Argentina",
            "BO": "Bolivia",
            "BR": "Brazil",
            "CL": "Chile",
            "CO": "Colombia",
            "EC": "Ecuador",
            "GY": "Guyana",
            "PY": "Paraguay",
            "PE": "Peru",
            "SR": "Suriname",
            "UY": "Uruguay",
            "VE": "Venezuela",
        }   # 12

    def oceanian_region(self) -> dict:
        return {
            "AU": "Australia",
            "FJ": "Fiji",
            "KI": "Kiribati",
            "MH": "Marshall Islands",
            "FM": "Micronesia",
            "NR": "Nauru",
            "NZ": "New Zealand",
            "PW": "Palau",
            "PG": "Papua New Guinea",
            "WS": "Samoa",
            "SB": "Solomon Islands",
            "TO": "Tonga",
            "TV": "Tuvalu",
            "VU": "Vanuatu",
        }   # 14
