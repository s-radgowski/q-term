import datetime
import math
import pathlib
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup


# Data settings
today = datetime.datetime.today()
path = pathlib.Path(__file__).parent.resolve()
data_path = str(path) + "/data/"
user = "Shaun" # YOUR NAME GOES HERE FOR PERSONALIZATION!
headers = {
    "User-Agent": 
    "Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36"
}


# Formatting codes
bg_gr = "\x1b[6;30;42m"
bg_bl = "\x1b[0;30;44m"
bg_rd = "\x1b[0;30;41m"
no_bg = "\x1b[0m"
red = "\033[0;31m"
green = "\033[0;32m"
yellow = "\033[0;33m"
blue = "\033[0;34m"
pink = "\033[0;35m"
teal = "\033[0;36m"
gray = "\033[0;37m"
underline = "\033[4m"
bold = "\033[1m"
reset = "\033[0m"
line_length = 48

superscripts = ["\u2070", "\u00B9", "\u00B2", "\u00B3", "\u2074", 
    "\u2075", "\u2076", "\u2077", "\u2078", "\u2079"]   

subscripts = ["\u2080", "\u2081", "\u2082", "\u2083", "\u2084", 
    "\u2085", "\u2086", "\u2087", "\u2088", "\u2089"]  

dots = f"{red}•{blue}•{green}•{yellow}•{reset}"
header = """
   ______        ________                                 
  /      \      |        \                                
 |  $$$$$$\      \$$$$$$$$______    ______   ______ ____  
 | $$  | $$ ______ | $$  /      \  /      \ |      \    \ 
 | $$  | $$|      \| $$ |  $$$$$$\|  $$$$$$\| $$$$$$\$$$$\ 
 | $$ _| $$ \$$$$$$| $$ | $$    $$| $$   \$$| $$ | $$ | $$
 | $$/ \ $$        | $$ | $$$$$$$$| $$      | $$ | $$ | $$
  \$$ $$ $$        | $$  \$$     \| $$      | $$ | $$ | $$
   \$$$$$$\         \$$   \$$$$$$$ \$$       \$$  \$$  \$$
       \$$$
"""

def print_header(speed=0.1):
    print(dots * 15)
    print(blue)
    rows = header.split("\n")
    for row in rows:
        time.sleep(speed)
        print(row)

    print(dots * 15)
    time.sleep(speed)


# Glossary of common other names for countries
common_names = {
    "America": "United States",
    "Cote D'ivoire": "Ivory Coast",
    "Dprk": "North Korea",
    "Korea": "South Korea",
    "Holy See": "Vatican City",
    "The Vatican": "Vatican City",
    "Turkey": "Türkiye",
    "Vatican": "Vatican City",
}
common_abbrev2 = {
    "UK": "GB"
}
common_abbrev3 = {
    "ROK": "KOR",
    "DRC": "COD"
}
common_fabbrev3 = {
    "NTD": "TWD",
    "RMB": "CNY"
}

"""Correctly decypher common inputs for countries."""
def nat_title(name: str) -> str:
    t = name.title().replace("&", "and")
    t = t.replace(" And ", " and ")
    t = t.replace(" Of ", " of ")
    t = t.replace(" The ", " the ")
    if t in common_names.keys():
        return common_names[t]
    return t

pop_dict = {
    "Cape Verde": "Cabo Verde",
    "Czechia": "Czech Republic (Czechia)",
    "Democratic Republic of the Congo": "DR Congo",
    "Ivory Coast": "Côte d'Ivoire",
    "Vatican City": "Holy See",
    "Republic of the Congo": "Congo",
    "Saint Vincent and the Grenadines": "St. Vincent & the Grenadines",
    "Saint Kitts and Nevis": "Saint Kitts & Nevis",
    "São Tomé and Príncipe": "Sao Tome & Principe",
    "Türkiye": "Turkey"
}

lead_dict = {
    "Bahamas": "Bahamas, The",
    "Democratic Republic of the Congo": "Congo, Democratic Republic of The",
    "Republic of the Congo": "Congo, Republic of The",
    "Cote D'ivoire": "Côte d'Ivoire",
    "Cuba": "Cuba - NDE",
    "Czechia": "Czech Republic",
    "Gambia": "Gambia, The",
    "Iran": "Iran - NDE",
    "Micronesia": "Micronesia, Federated States of",
    "eSwatini": "Swaziland",
    "North Korea": "Korea, North",
    "United States": "United States of America",
    "South Korea": "Korea, South",
    "Türkiye": "Turkey"
}

maj_currs = ["USD", "GBP", "EUR", "JPY", "CHF", "CNY", "AUD", "INR", 
             "CAD", "MYR", "HKD", "KRW"]

maj_flags = ["🇺🇸", "🇬🇧", "🇪🇺", "🇯🇵", "🇨🇭", "🇨🇳", "🇦🇺", "🇮🇳", "🇨🇦", "🇲🇾",
             "🇭🇰", "🇰🇷"]

def pop_name(name: str) -> str:
    if name in pop_dict.keys():
        return pop_dict[name]
    return name

def lead_name(name: str) -> str:
    if name in lead_dict.keys():
        return lead_dict[name]
    return name

"""Scrapes the current Treasury rates from the web."""
def TreasuryRates(date=today):
    year = date.year
    month = date.month
    if month < 10:
        month = "0" + str(month)
    url = "https://home.treasury.gov/resource-center/data-chart-center/"
    url += "interest-rates/TextView?type=daily_treasury_yield_curve"
    url += f"&field_tdr_date_value_month={year}{month}"

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "views-table"})
    rows = table.find_all("tr")
    tds = rows[-1].find_all("td")
    
    if date.day == 1:
        new_date = date - datetime.timedelta(days=1)
        year = new_date.year
        month = new_date.month
        if month < 10:
            month = "0" + str(month)
        url = "https://home.treasury.gov/resource-center/data-chart-center/"
        url += "interest-rates/TextView?type=daily_treasury_yield_curve"
        url += f"&field_tdr_date_value_month={year}{month}"

        html2 = requests.get(url).text
        soup2 = BeautifulSoup(html2, "html.parser")
        table2 = soup2.find("table", {"class": "views-table"})
        rows2 = table2.find_all("tr")
        tds_y = rows2[-1].find_all("td")
    
    else:
        tds_y = rows[-2].find_all("td")

    yesterday = []
    for td in tds_y[10:]:
        yesterday.append(float(td.text.strip()))
    data = []
    for td in tds[10:]:
        data.append(float(td.text.strip()))

    labels = [" 1 Mo", " 2 Mo", " 3 Mo", " 4 Mo", " 6 Mo", " 1 Yr", 
            " 2 Yr", " 3 Yr", " 5 Yr", " 7 Yr", "10 Yr", "20 Yr", 
            "30 Yr"]
    return [labels, data, yesterday]

def PrintTreasuries(major=True):
    treasuries = TreasuryRates()
    print(f"{underline}TREASURY YIELDS{reset}")
    if major:
        selection = [0, 2, 5, 7, 8, 10, 12]
    else:
        selection = range(len(treasuries[0]))
    
    for i in selection:
        print(treasuries[0][i], end="  ")
    print()
    for i in selection:
        print(f"{treasuries[1][i]:.2f}%", end="  ")
    print()
    for i in selection:
        diff = treasuries[1][i] - treasuries[2][i]
        if diff < 0:
            print(f"{red}{diff:.2f}{reset}", end="  ")
        else:
            print(f"{green}+{diff:.2f}{reset}", end="  ")
    print("\n")

"""Scrapes standard indicators/indices from MarketWatch."""
def Indicators():
    url = "https://www.marketwatch.com/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "table--primary"})
    rows = table.find_all("tr")
    labels = []
    prices = []
    changes = []
    percents = []
    for row in rows:
        tds = row.find_all("td")
        labels.append(tds[1].text.strip().replace(",", ""))
        prices.append(tds[2].text.strip().replace(",", ""))
        changes.append(tds[3].text.strip().replace(",", ""))
        percents.append(tds[4].text.strip().replace(",", ""))
    
    prices = [float(p) for p in prices]
    changes = [float(c) for c in changes]
    percents = [float(p[:-1]) for p in percents]
    return [labels, prices, changes, percents]

def PrintIndicators():
    es = Indicators()
    print(f"{underline}INDICATOR PRICES{reset}")
    for i in range(len(es[0])):
        spaces = (22 - len(es[0][i]) - len(f"{es[1][i]:,.2f}")) * " "
        print(f"{es[0][i]}{spaces}{es[1][i]:,.2f}", end="")
        spaces2 = (9 - len(f"{es[2][i]:,.2f}")) * " "
        if es[2][i] > 0:
            print(f"{green}{spaces2}+{es[2][i]:,.2f}", end="")
        else:
            print(f"{red}{spaces2} {es[2][i]:,.2f}", end="")
        spaces3 = (8 - len(f"{es[3][i]:,.2f}")) * " "
        if es[3][i] > 0:
            print(f"{green}{spaces3}+{es[3][i]:,.2f}% ▲{reset}")
        else:
            print(f"{red}{spaces3} {es[3][i]:,.2f}% ▼{reset}")
    print()

"""Scrapes equity quotes & data from MarketWatch."""
class Equity():
    def __init__(self, ticker: str):
        url = "https://www.marketwatch.com/investing/stock/"
        url += f"{ticker.lower()}?mod=search_symbol"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        name = soup.find("h1", {"class": "company__name"})
        if name is None:
            self.found = False
        else:
            self.found = True
            self.name = name.text.strip()
            price = soup.find("bg-quote", {"class": "value"})
            self.price = float(price.text.strip())
            self.ticker = ticker

            status = soup.find("div", {"class": "status"})
            self.status = status.text.strip()
            if self.status == "After Hours":
                self.status = f"{blue}AH{reset}"

            change = soup.find_all("bg-quote", {"field": "change"})
            self.change = float(change[6].text.strip())

            pct_change = soup.find_all("bg-quote", {"field": "percentchange"})
            self.pct_change = float(pct_change[6].text.strip().replace("%", ""))

            data = soup.find_all("li", {"class": "kv__item"})
            self.data = [d.text.strip().replace("\n", " ") for d in data]

    def print(self, data="all"):
        print(f"{underline}{bold}{self.name} ({self.ticker.upper()}){reset}")
        if self.change == 0:
            print(f"{self.status}: ${self.price}   +0.0%")
        elif self.change > 0:
            print(f"{self.status}: {green}${self.price}    ", end=" ")
            print(f"+{self.change} +{self.pct_change}% ▲{reset}")
        elif self.change < 0:
            print(f"{self.status}: {red}${self.price}    ", end=" ")
            print(f"{self.change} {self.pct_change}% ▼{reset}")

        print()
        if data == "all":
            points = range(len(self.data))
        else:
            points = data

        for i in points:
            print(self.data[i])
        print()

"""Pulls national data from my personal dataset."""
class Nation():
    def __init__(self, name: str):
        df = pd.read_csv(f"{data_path}countries.csv")
        len_name = len(name)
        if len_name == 2:
            if name.upper() in common_abbrev2.keys():
                c_name = common_abbrev2[name.upper()]
                country = df[df["Alpha-2 Code"] == c_name]
            else:
                country = df[df["Alpha-2 Code"] == name.upper()]
        elif len_name == 3:
            if name.upper() in common_abbrev3.keys():
                c_name = common_abbrev3[name.upper()]
                country = df[df["Alpha-3 Code"] == c_name]
            else:
                country = df[df["Alpha-3 Code"] == name.upper()]
        elif len_name > 3:
            country = df[df["Country"] == nat_title(name)]
        else:
            country = []
        
        if len(country) != 1:
            self.found = False
        else:
            self.found = True
            self.name = country["Country"].item()

            capital = country["Capital"].item()
            if "|" in capital:
                self.capital = capital.split("|")
            else:
                self.capital = [capital]
            self.official = country["Official Name"].item()
            if isinstance(self.official, float):
                if math.isnan(self.official):
                    self.official = None
            self.local = country["Local Name"].item()
            if isinstance(self.local, float):
                if math.isnan(self.local):
                    self.local = None
            self.local_off = country["Local Official Name"].item()
            if isinstance(self.local_off, float):
                if math.isnan(self.local_off):
                    self.local_off = None

            self.flag = country["Flag Emoji"].item()
            self.alpha2 = country["Alpha-2 Code"].item()

            languages = country["Languages"].item()
            if "|" in languages:
                self.language = languages.split("|")
            else:
                self.language = [languages]
            
            currencies = country["Currency"].item()
            if "|" in currencies:
                self.currency = currencies.split("|")
            else:
                self.currency = [currencies]
            
            curr_codes = country["Currency Code"].item()
            if "|" in curr_codes:
                self.curr_code = curr_codes.split("|")
            else:
                self.curr_code = [curr_codes]

            call_codes = str(country["Calling Code"].item())
            if "|" in call_codes:
                self.call_code = call_codes.split("|")
            else:
                self.call_code = [call_codes]
            for i, c_i in enumerate(self.call_code):
                if c_i[0] != "+":
                    self.call_code[i] = "+" + self.call_code[i]
            
            # Population
            url = "https://www.worldometers.info/world-population/population-by-country/"
            html = requests.get(url=url, headers=headers).text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", {"id": "example2"})
            table_name = pop_name(self.name)
            for row in table.find_all("tr")[1:]:
                tds = row.find_all("td")
                name_i = tds[1].text
                if (name_i == table_name):
                    pop = tds[2].text.replace(",", "")
                    self.population = int(pop.strip())

                    change = tds[3].text.replace("%", "")
                    self.pop_change = float(change.strip())

                    dens = tds[5].text.replace(",", "")
                    self.density = int(dens.strip())

                    area = tds[6].text.replace(",", "")
                    self.area = int(area.strip())

                    if tds[8].text == "N.A.":
                        self.fertility = None
                    else:
                        self.fertility = float(tds[8].text)
                    
                    if tds[9].text == "N.A.":
                        self.med_age = None
                    else:
                        self.med_age = int(tds[9].text)

                    if tds[10].text == "N.A.":
                        self.urban = None
                    else:
                        urb = tds[10].text.replace("%", "")
                        self.urban = float(urb.strip())
                    row_found = True
                    continue

            if not row_found:
                self.population = None
                self.pop_change = None
                self.density = None
                self.area = None
                self.fertility = None
                self.med_age = None
                self.urban = None
            
            # Leaders
            l_url = "https://www.geni.com/projects/Current-World-Leaders/6177"
            html = requests.get(url=l_url, headers=headers).text
            soup = BeautifulSoup(html, "html.parser")
            div = soup.find("div", {"class": "bd wiki_container"})
            table = div.find_all("li")
            table_name = lead_name(self.name)
            row_found = False
            for row in table:
                text = row.text
                name_i = text.split(":", 1)[0].strip()
                if (name_i == table_name):
                    leaders = text.split(":", 1)[1].strip()
                    if ";" in leaders:
                        leaders_l = leaders.split(";")
                        
                    else:
                        leaders_l = [leaders]
                    
                    titles = []
                    names = []
                    for l in leaders_l:
                        if ":" in l:
                            titles.append(l.split(":")[0].strip())
                            names.append(l.split(":")[1].strip())
                        else:
                            if l.split("-")[0].strip() == "Capital":
                                pass
                            else:
                                if "-" in l:
                                    titles.append(l.split("-", 1)[0].strip())
                                    names.append(l.split("-", 1)[1].strip())

                    self.leader_titles = titles
                    self.leader_names = names
                    row_found = True
                    continue

            if not row_found:
                self.leader_titles = None
                self.leader_names = None

    def print(self):
        # Country name
        c = self.local
        f = self.flag
        if c is not None:
            print(f"{underline}{bold}{self.name} - {self.alpha2}{reset}", end=" ")
            if len(c) + len(self.name) + 8 > line_length:
                print(f"\n    {underline}{gray}({c}){reset} {f}")
            else:
                print(f"{underline}{gray}({c}){reset} {f}")
        else:
            print(f"{underline}{bold}{self.name} - {self.alpha2}{reset} {f}")
        
        # Official name
        o = self.official
        o_l = self.local_off
        if o is not None:
            if o_l is not None:
                if len(o_l) + len(o) > line_length:
                    print(f"{yellow}{o}\n {gray}({o_l}){reset}")
                else:
                    print(f"{yellow}{o} {gray}({o_l}){reset}")
            else:
                print(f"{yellow}{o}{reset}")
        print()
        
        # Capitals
        if len(self.capital) == 1:
            print(f"{blue}Capital:{reset} {self.capital[0]}")
        else:
            print(f"{blue}Capitals:{reset}", end=" ")
            print(", ".join(self.capital))

        # Leaders
        if self.leader_titles is not None:
            for i, title in enumerate(self.leader_titles):
                if len(self.leader_names[i]) > 0:
                    print(f"{blue}{title}:{reset} {self.leader_names[i]}")
        
        # Languages
        if len(self.language) == 1:
            print(f"{blue}Language:{reset} {self.language[0]}")
        else:
            print(f"{blue}Languages:{reset}", end=" ")
            print(", ".join(self.language))
        
        # Currencies
        code = self.curr_code
        if len(self.currency) == 1:
            print(f"{blue}Currency:{reset} {self.currency[0]} ({code[0]})")
        else:
            print(f"{blue}Currencies:{reset}", end=" ")
            cs = [f"{c[0]} ({c[1]})" for c in zip(self.currency, code)]
            print(", ".join(cs))
        
        # Calling Codes
        if len(self.call_code) == 1:
            print(f"{blue}Calling Code:{reset} {self.call_code[0]}")
        else:
            print(f"{blue}Calling Codes:{reset}", end=" ")
            print(", ".join(self.call_code))

        # Population
        if self.population is not None:
            print(f"\n{blue}Population:{reset} {self.population:,}", end=" ")
            if self.pop_change > 0:
                print(f"{green}(+{self.pop_change}%){reset}")
            elif self.pop_change < 0:
                print(f"{red}({self.pop_change}%){reset}")
            elif self.pop_change == 0:
                print(f"{gray}(+0.0%){reset}")
            
            s = superscripts[2]
            print(f"{blue}Density:{reset} {self.density:,} P/km{s}")

            if self.name == "Vatican City":
                print(f"{blue}Land Area:{reset} 0.49 km{s}")
                # Easter egg
                popes = 1
                x = popes / 0.49
                print(f"{blue}Popes per km{s}:{reset} {x:.2f}")
            else:
                print(f"{blue}Land Area:{reset} {self.area:,} km{s}")

            if self.fertility is not None:
                print(f"{blue}Fertility:{reset} {self.fertility:.1f}")
            if self.med_age is not None:
                print(f"{blue}Median Age:{reset} {self.med_age}")
            if self.urban is not None:
                print(f"{blue}Urban Pop.:{reset} {self.urban}%")

        print()

class City():
    def __init__(self, name: str):
        df = pd.read_csv(f"{data_path}cities.csv")
        df["name_lower"] = df["city_ascii"].apply(str.lower)
        city = df[df["name_lower"] == name.lower()]
        if len(city) == 0:
            df["name_lower2"] = df["city"].apply(str.lower)
            city = df[df["name_lower2"] == name.lower()]

        if len(city) == 0:
            self.found = False
        else:
            self.found = True

            # Take largest returned item
            city = city.iloc[0]
            self.name = city["city"]
            self.country = city["country"]

            country = Nation(self.country)
            if country.found:
                self.flag = country.flag
                self.language = country.language
                self.currency = country.currency
                self.curr_code = country.curr_code
                if self.name in country.capital:
                    self.capital = True
                else:
                    self.capital = False
            else:
                self.flag = ""
                self.language = None
                self.currency = None
                self.curr_code = None
                self.capital = False
            
            self.population = city["population"]
            if self.population != "":
                self.population = int(self.population)
            
            # Longitude and Latitude
            self.lat = float(city["lat"].item())
            self.lng = float(city["lng"].item())

            # Admin
            self.admin = city["admin_name"]
            self.admin_status = city["capital"]
            self.admin_title = city["admin_title"]
            if isinstance(self.admin_title, float):
                if math.isnan(self.admin_title):
                    self.admin_title = "Province"
            elif self.admin_title == "NONE":
                self.admin_title = None

    def print(self):
        # City name
        f = self.flag
        print(f"{underline}{bold}{self.name}{reset}")
        
        # Admin name
        a = self.admin
        a_s = self.admin_status
        a_t = self.admin_title
        if self.admin_title is None:
            a_t = ""
        if a is not None:
            if a_s == "admin":
                print(f"{gray}Capital of {yellow}{a}{gray} {a_t}{reset}")
            else:
                print(f"{yellow}{a}{gray} {a_t}{reset}")
        if self.capital:
            print(f"Capital of {yellow}{self.country}{reset} {self.flag}\n")
        else:
            print(f"{yellow}{self.country}{reset} {self.flag}\n")

        # Longitude and Latitude
        if self.lat >= 0 and self.lng >= 0:
            print(f"{self.lat:.4f}°N {self.lng:.4f}°E")
        elif self.lat >= 0 and self.lng < 0:
            print(f"{self.lat:.4f}°N {-self.lng:.4f}°W")
        if self.lat < 0 and self.lng >= 0:
            print(f"{-self.lat:.4f}°S {self.lng:.4f}°E")
        elif self.lat < 0 and self.lng < 0:
            print(f"{-self.lat:.4f}°S {-self.lng:.4f}°W")

        # Languages
        if len(self.language) == 1:
            print(f"{blue}Language:{reset} {self.language[0]}")
        else:
            print(f"{blue}Languages:{reset}", end=" ")
            print(", ".join(self.language))
        
        # Currencies
        code = self.curr_code
        if len(self.currency) == 1:
            print(f"{blue}Currency:{reset} {self.currency[0]} ({code[0]})")
        else:
            print(f"{blue}Currencies:{reset}", end=" ")
            cs = [f"{c[0]} ({c[1]})" for c in zip(self.currency, code)]
            print(", ".join(cs))        
        
        # Population
        print(f"{blue}Population:{reset} {math.trunc(self.population):,.0f}")

        print()

class Currency():
    def __init__(self, ticker: str):
        if ticker.upper() in common_fabbrev3.keys():
            self.ticker = common_fabbrev3[ticker.upper()]
        else:
            self.ticker = ticker.upper()
        df = pd.read_csv(f"{data_path}countries.csv")
        df2 = pd.read_csv(f"{data_path}currencies.csv")
        self.countries = []
        self.flags = []
        for _, row in df.iterrows():
            if self.ticker in row["Currency Code"]:
                self.countries.append(row["Country"])
                self.flags.append(row["Flag Emoji"])

        self.active = True
        self.found = False
        for _, row in df2.iterrows():
            if self.ticker == row["Currency Code"]:
                self.found = True
                self.name = row["Currency"]
                self.jurisdiction = row["Entity"].title()
                self.flag = row["Flag"]
                if isinstance(row["Withdrawal Date"], str):
                    self.active = False
                    self.withdrawal = row["Withdrawal Date"]
                elif not math.isnan(row["Withdrawal Date"]):
                    self.active = False
                    self.withdrawal = row["Withdrawal Date"]
                else:
                    self.active = True
                    continue

        if self.active and self.found:
            self.others = maj_currs.copy()
            self.o_flags = maj_flags.copy()
            if self.ticker in self.others:
                ind = self.others.index(self.ticker)
                self.others.remove(self.ticker)
                self.o_flags.pop(ind)
            urls_left = []
            urls_right = []
            for other in self.others:
                url_l = "https://www.x-rates.com/calculator/?from="
                url_l += f"{self.ticker}&to={other}&amount=1"
                urls_left.append(url_l)

                url_r = "https://www.x-rates.com/calculator/?from="
                url_r += f"{other}&to={self.ticker}&amount=1"
                urls_right.append(url_r)

            self.lefts = []
            pops = []
            for i, url in enumerate(urls_left):
                html = requests.get(url=url, headers=headers).text
                soup = BeautifulSoup(html, "html.parser")
                marquee = soup.find("span", {"class": "ccOutputRslt"})
                price = float(marquee.text[:-4].replace(",", ""))
                if price == 0:
                    pops.append(i)
                else:
                    self.lefts.append(price)

            for p in pops:
                urls_right.pop(p)
                self.others.pop(p)

            self.rights = []
            for url in urls_right:
                html = requests.get(url=url, headers=headers).text
                soup = BeautifulSoup(html, "html.parser")
                marquee = soup.find("span", {"class": "ccOutputRslt"})
                price = float(marquee.text[:-4].replace(",", ""))
                self.rights.append(price)

    def print(self):
        print(f"{underline}{bold}{self.name} ({self.ticker}){reset} {self.flag}")
        if not self.active:
            print(f"{blue}Former Currency of:{reset} {self.jurisdiction}")
            print(f"{red}Withdrawal Date: {self.withdrawal}{reset}")

        else:
            print(f"{blue}Currency of:{reset}", end=" ")
            if len(self.countries) == 0:
                print(self.jurisdiction)
            else:
                cs = [f"{c[0]} {c[1]}" for c in zip(self.countries, self.flags)]
                stop = len(cs) - 1
                for i, c in enumerate(cs):
                    if i % 3 == 0 and i > 0:
                        print()
                    if i == stop:
                        print(f"{c}", end="")
                    else:
                        print(f"{c} , ", end="")

            print(f"\n\n{blue}Exchange Rates:{reset}")
            for i, name in enumerate(self.others):
                size_l = len(str(self.lefts[i]))
                spaces_l = " " * max(0, 11 - size_l)
                print(f" 1 {teal}{self.ticker} ={reset}{spaces_l}", end=" ")
                print(f"{self.lefts[i]} {yellow}{name}{reset} ", end=" ")
                print(f"{pink}•{reset} {self.o_flags[i]}  {pink}•{reset}", end=" ")
                
                size_r = len(str(self.rights[i]))
                spaces_r = " " * max(0, 11 - size_r)
                print(f"1 {yellow}{name} ={reset}{spaces_r}", end=" ")
                print(f"{self.rights[i]} {teal}{self.ticker}{reset}")


"""Runs an information dashboard in terminal."""
def RunDashboard():
    print_header()
    print(f"Welcome, {user}. Gathering current data...\n")
    PrintTreasuries()
    PrintIndicators()

    query = True
    while query:
        print(f"\n{blue}[E - Equity; F - Currency; N - Nation]{reset}")
        print(f"{blue}[C - City;                 Q - Quit  ]{reset}")
        i = input(">> ")
        category = i[0].lower()

        # EQUITY
        if category == "e":
            if len(i.strip()) == 1:
                i = input(f">> {bg_gr} EQUITY TICKER: {no_bg} ")
                ticker = i.strip()
            else:
                ticker = i[2:].strip()
            
            e = Equity(ticker)
            if e.found:
                print(f"{bg_gr} PUBLIC EQUITY {no_bg}\n")
                e.print()
            else:
                print(f"{bg_rd}ERROR:{reset} No ticker {ticker} found.\n")
        
        # CURRENCY
        elif category == "f":
            if len(i.strip()) == 1:
                i = input(f">> {bg_gr} CURRENCY TICKER: {no_bg} ")
                ticker = i.strip()
            else:
                ticker = i[2:].strip()
            
            f = Currency(ticker)
            if f.found:
                print(f"{bg_gr} CURRENCY {no_bg}\n")
                f.print()
            else:
                print(f"{bg_rd}ERROR:{reset} No currency found.\n")
        
        # NATION
        elif category == "n":
            if len(i.strip()) == 1:
                i = input(f">> {bg_gr} COUNTRY NAME: {no_bg} ")
                name = i.strip()
            else:
                name = i[2:].strip()

            n = Nation(name)
            if n.found:
                print(f"{bg_gr} NATION {no_bg}\n")
                n.print()
            else:
                print(f"{bg_rd}ERROR:{reset} No country found.\n")

        # CITY
        elif category == "c":
            if len(i.strip()) == 1:
                i = input(f">> {bg_gr} CITY NAME: {no_bg} ")
                name = i.strip()
            else:
                name = i[2:].strip()

            c = City(name)
            if c.found:
                print(f"{bg_gr} CITY {no_bg}\n")
                c.print()
            else:
                print(f"{bg_rd}ERROR:{reset} No city found.\n")

        # QUIT
        elif category == "q":
            query = False
        else:
            print(f"{bg_rd}ERROR:{reset} Invalid command.\n")

    print("\nHave a wonderful day!")


if __name__ == "__main__":
    RunDashboard()
