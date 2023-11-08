import sys
import logging
sys.path.insert(0,"/Users/cpcarriz/Documents/merakipruebas")
import querysMongoDB

#print(querysMongoDB)

if __name__ == '__main__':
    querysMongoDB.saveApsByOrganization()