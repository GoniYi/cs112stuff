from scraper import *
import pytest

prov_page = BeautifulSoup(
   requests.get("https://providence.craigslist.org/search/apa").content, 
   features="html.parser"
)

atlanta_page = BeautifulSoup(
   requests.get("https://atlanta.craigslist.org/search/apa?").content, 
   features="html.parser"
)

cityd = {"providence" : prov_page, "atlanta" : atlanta_page}

def test_cleaner():
    #case where the string has no alphabet characters
    test = "!@#$%^&*("
    assert cleaner(test) == ""
    #case where there are some alphabet characters
    test2 = "%^&*&^djd)"
    assert cleaner(test2) == "djd"
    #case where there is an emoji
    test3 = "zzz999😋"
    assert cleaner(test3) == "zzz"
    #case where it is a regular word
    test4 = "the"
    assert cleaner(test4) == "the"
    #case where there is a space in the string
    test5 = "the apple"
    assert cleaner(test5) == "the apple"

def test_scrape_data_helper():
    #case where we test if we are outputing a list of our class
    assert type(scrape_data_helper(prov_page)[0]) == Abode
    # testing if the abode objects have the right kind of data
    assert type(scrape_data_helper(prov_page)[0].rooms) == int
    assert type(scrape_data_helper(prov_page)[0].price) == float
    assert type(scrape_data_helper(prov_page)[0].description) == str
    #we cannot write any specific tests because the page can update

def test_scrape_data():
    #testing the right ouputs
    assert type(scrape_data(cityd)) == dict
    assert type(scrape_data(cityd)["providence"][0]) == Abode
    #tests done by using the summarize function

def test_avg_bednum():
    #case where take in normal data
    test = {"NY" : [Abode(10, 2000, ""), Abode(3, 1700, "")], "CA" :
     [Abode(5, 700, "")]}
    assert average_bedrooms(test) == 6
    #case where we take in an empty dictionary
    test2 = {}
    assert average_bedrooms(test2) == 0
    #no other cases to test for

def test_avg_citybedprice():
    #case where the is a room number that is not in the data at all
    test = {"NY" : [Abode(10, 2000, ""), Abode(3, 1700, "")], "CA" : 
    [Abode(5, 700, ""), Abode(3, 1699.99, "")]}
    with pytest.raises(NoCityError):
        highest_average_price(test, 0)
    #normal case where the targeted room num is in our data, but is no real work
    #to find the average
    assert highest_average_price(test, 3) == "NY"
    #case where average is being thoroughly tested
    test2 = {"NY" : [Abode(10, 2000, ""), Abode(3, 1700, ""), 
    Abode(4, 2000, ""), Abode(4, 1800, ""), Abode(4, 2100, "")], 
    "WY" :  [Abode(4, 700, ""), Abode(4, 1699.99, ""), Abode(4, 8000, ""), 
                                                            Abode(4, 6500, "")]}
    assert highest_average_price(test2, 4) == "WY"

def test_most_common_interesting_word():
    #normal case where we test
    test = {"NY" : [Abode(10, 2000, "this house is great for \
                                        playing with yo-yo's"),
     Abode(3, 1700, "i took the wok to poland"), Abode(3, 500, "im finna take \
     the wok to poland poland")], "CA" : [Abode(5, 700, "bro really took the \
     wok to poland")]}
    assert most_common_interesting_word(test, "NY") == "poland"
    #case where we do not pass in a cleaned input
    #this is fine because under normal circumstances, this function expects 
    # only cleaned data to be passed in
    # the cleaning is done in the scraper helper function
    test2 = {"NY" : [Abode(10, 2000, "this house is great for playing with \
    yo-yo's"),
     Abode(3, 1700, "i took the wok and the wok to poland"), Abode(3, 500, \
     "im finna take the wok to poland. Poland")], "CA" : [Abode(5, 700, 
     "bro really took the wok to poland")]}
    assert most_common_interesting_word(test2, "NY") == "wok"
    #regular testing case
    test3 = {"NY" : [Abode(10, 2000, "this house is great for playing with \
     yo-yo's"),
     Abode(3, 1700, "i took the wok to poland"), Abode(3, 500, "im finna take \
     the wok to poland poland")], "CA" : [Abode(5, 700, "this house is really \
     nice the house makes me happy i want to live in the house")]}
    assert most_common_interesting_word(test3, "CA") == "house"