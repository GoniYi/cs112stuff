import requests
from bs4 import BeautifulSoup

"""
Place your answers to the Design check questions here:

1.The information is found in all in one class but there are subclasses that
 we need to get info for. For each given class
we need to go in it again. 

2.Yes, but we need to clean it up for it to be usable for queries. 
ex: dict = ("bedroom": 1, "price": 750, "description": "big bedroom", 
                "location": NYC)
ex: class listing:
   def init(self, numrooms : int, price: float, description : str, location: 
                str):
      self.numrooms = numrooms
      self.price = price
      self.description = description
      self.location = location

3. Dictionaries should cover all cases but we have our class listing just in 
            case. 

4. def avg_bednum(listings : list) -> int:
   def avg_citybedprice(listings: list, bednum: int) -> str:       
   def most_interesting(listings: list, cityname: str) -> str:

"""

class Abode:
    def __init__(self, rooms : int, price: float, description : str):
        self.rooms = rooms
        self.price = price
        self.description = description
    
    def __repr__(self) -> str: #we use this to print the class obj
        return "Abode(rooms=" + str(self.rooms) + ", price=" + str(self.price) \
                                    + ", description="+ self.description +")"

CITIES = [
    "providence",
    "atlanta",
    "austin",
    "boston",
    "chicago",
    "dallas",
    "denver",
    "detroit",
    "houston",
    "lasvegas",
    "losangeles",
    "miami",
    "minneapolis",
    "newyork",
    "philadelphia",
    "phoenix",
    "portland",
    "raleigh",
    "sacramento",
    "sandiego",
    "seattle",
    "washingtondc",
]

class NoCityError(Exception):
    pass

def craigslist_get_city(city_name) -> BeautifulSoup:
    """Returns a BeautifulSoup object for a given city from Craigslist"""
    url_template = "https://{}.craigslist.org/search/apa"
    try:
        resp = requests.get(url_template.format(city_name))
        return BeautifulSoup(resp.content, "html.parser")
    except:
        raise NoCityError("No city named {} found".format(city_name))

def local_get_city(city_name) -> BeautifulSoup:
    """Returns a BeautifulSoup object for a given city from the local 
    filesystem"""
    file_template = "localdata/{}.html"
    try:
        with open(file_template.format(city_name), "r") as f:
            return BeautifulSoup(f.read(), "html.parser")
    except:
        raise NoCityError("No city named {} found".format(city_name))

alphabet = {"q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j",
                                    "k","l","z","x","c","v","b","n","m", " "}
def cleaner(s : str) -> str:
    for character in s:
        if character not in alphabet:
            s = s.replace(character, "")
    return s

def scrape_data_helper(page: BeautifulSoup) -> list:
    listing = []
    desc = []
    room = []
    price = []
    div_list = page.find_all("div", "result-info")
    for div in div_list:
        
        if div.find("h3") == None:
            desc.append("")
        else:
            desc.append(cleaner(div.find("h3").text.strip().lower()))
    
        if div.find("span", "result-price") == None:
            price.append(0)
        else:    
            price.append(float(div.find("span", "result-price").
            text.strip().replace("$", "").replace(",", "")))

        if div.find("span", "housing") == None:
            room.append(0)
        else:    
            room.append(int(div.find("span", "housing").text.split("-")
                                                            [0].strip()[0]))
            
    for i in range(len(desc)):
        listing.append(Abode(room[i], price[i], desc[i]))

    return listing

def scrape_data(city_pages: dict) -> dict:
    """Scrapes data from a collection of pages.
    The keys of city_pages are city names. The values are BeautifulSoup objects
    ."""
    d = {}
    for city in city_pages:
        d[city] = scrape_data_helper(city_pages[city])
    return d

def scrape_craigslist_data():
    """Scrape data from Craigslist"""
    return scrape_data({city: craigslist_get_city(city) for city in CITIES})

def summarize_local_data():
    """Scrape data from the local filesystem"""
    return scrape_data({city: local_get_city(city) for city in CITIES})

def interesting_word(word: str) -> bool:
    """Determines whether a word in a listing is interesting"""
    return word.isalpha() and word not in [
        "to",
        "at",
        "your",
        "you",
        "and",
        "for",
        "in",
        "the",
        "with",
        "bedroom",
        "bed",
        "bath",
        "unit",
    ]

def average_bedrooms(cities : dict) -> float:
    numerator = 0
    denominator = 0
    for city in cities:
        for abode in cities[city]:
            numerator += abode.rooms
            denominator += 1
    if denominator == 0:
        return 0
    return numerator/denominator

def highest_average_price(cities: dict, bednum: int) -> str:
    pricedict = {}
    num_counter = 0
    for city in cities:
        pricedict[city] = 0
        count = 0
        for abode in cities[city]:
            if abode.rooms == bednum:
                pricedict[city] += abode.price
                num_counter += 1
                count += 1
        if count != 0:
            pricedict[city] /= count
        else:
            pricedict[city] = 0
    if num_counter == 0:
        raise NoCityError
    else:
        return max(pricedict, key=pricedict.get)

def most_common_interesting_word(cities: dict, cityname: str) -> str:
    if cityname not in cities:
        raise NoCityError
    word_dict = {}
    for abode in cities[cityname]:
        word_list = abode.description.split(" ")
        for word in word_list:
            if word not in word_dict:# and interesting_word(word):
                word_dict[word] = 1
            else:
                word_dict[word] += 1
    for word in word_dict:
        if not interesting_word(word):
            word_dict[word] = 0
    return max(word_dict, key=word_dict.get)