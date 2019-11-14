import requests
import sys

a = sys.argv[1]

if (a==""):
   a=0


 
URL = "http://127.0.0.1:5000/predict/" + str(a)
 
r = requests.post(url = URL)
 
print (r.text)
