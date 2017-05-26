# import random
#
#
# # TODO: nie dziala na 2.7 - poprawic
# NB_POINTS = 10**5
# LENGTH = 10**5
# CENTER = [LENGTH//2,LENGTH//2]
#
# def in_circle(point):
#     x,y = point
#     center_x, center_y = CENTER
#     radius = LENGTH//2
#     return (x - center_x)**2 + (y - center_y)**2 < radius**2
#
# def compute_pi(nb_it):
#     inside_count = sum(1 for _ in range(nb_it) if in_circle((random.randint(1,LENGTH),random.randint(1,LENGTH))))
#     return (inside_count // nb_it) * 4
#
# if __name__ == "__main__":
#     num = compute_pi(NB_POINTS)
#     print num

# biblioteki:
# python2-requests
from random import *
import sys
import requests


print sys.argv
print sys.argv[1]

MAXN = 10000000

def dist(x, y):
    return (x * x + y * y)

i = 0
j = 0

seed()

while i < MAXN:
    x = random()
    y = random()
    if dist(x, y) <= 1.0:
        j += 1
    i += 1

print j * 4.0 / MAXN

# TODO: przykladowe wyslanie
#
# url = 'http://ES_search_demo.com/document/record/_search?pretty=true'
# data = '{
#   "query": {
#     "bool": {
#       "must": [
#         {
#           "text": {
#             "record.document": "SOME_JOURNAL"
#           }
#         },
#         {
#           "text": {
#             "record.articleTitle": "farmers"
#           }
#         }
#       ],
#       "must_not": [],
#       "should": []
#     }
#   },
#   "from": 0,
#   "size": 50,
#   "sort": [],
#   "facets": {}
# }'
# response = requests.post(url, data=data)