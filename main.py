from sanic import Sanic
from sanic.response import json, text
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DHT"]
mycol = mydb["DHT"]

app = Sanic('myapp')

@app.route("/")
async def test(request):
  
  return json({"hello": "sonic"})

@app.route('/addDHT', methods=['POST'])
async def post_handler(request):
  post=request.json
  postT=post['T']
  postH=post['H']
  mydict = { "T":postT , "H":postH}
  mycol.insert_one(mydict) 
  return text('POST request - {}'.format(request.json))

@app.route('/DHT')
async def test(request):
  dht = mycol.find({}).sort("_id",-1).limit(1)
  for obj in dht:
    h=obj['H']
    t=obj['T']
    return json({"H":h,"T":t})
  
  

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)

