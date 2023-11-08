import pymongo 
from pymongo.errors import ConnectionFailure

client = "";

def getDbMongo():
    try:
        conexion = 'mongodb://10.237.5.31:27017,10.237.5.33:27017,10.237.5.166:27017/telmexApp'
        client = pymongo.MongoClient(conexion)
        print("Conexión exitosa a MongoDB")
        return client
    except Exception as e:
        print("No se pudo conectar a MongoDB", e)



getDbMongo()