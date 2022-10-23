# https://www.vattenfall.se/api/price/spot/pricearea/2021-01-01/2021-12-31/SN3
import urllib.request
json = urllib.request.urlopen("https://www.vattenfall.se/api/price/spot/pricearea/2022-10-22/2022-10-23/SN3")
print(json.read())

