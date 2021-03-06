import traceback
import sys
import json
import argparse
import requests
from requests.api import request
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

def getIpPortDns(mesosDnsAddr, serviceMesosDns):
    
    '''[
  {
   "service": "_rfp-db-rfp._tcp.marathon.mesos.",
   "host": "rfp-db-rfp-xss9x-s1.marathon.mesos.",
   "ip": "10.0.0.13",
   "port": "31332"
  }
 ]'''
    response = requests.get(mesosDnsAddr + "/v1/services/" + serviceMesosDns, timeout = 20)
    if response.status_code == requests.codes.ok:
        #print(response.text)
        responseJson = json.loads(response.text)
        ip = responseJson[0]["ip"]
        port = responseJson[0]["port"]
        if not ip:
            print("No ip for " + serviceMesosDns)
        if not port:
            print("No port for " + serviceMesosDns)
    else:
        print("Error getting ip/port for " + serviceMesosDns)
        ip = ""
        port = ""
    return (ip, port)



if __name__ == "__main__":
    print("Running the Mesos DNS ip/port extractor")
    parser = argparse.ArgumentParser(description="Get the ip/port for various services from Mesos DNS")
    parser.add_argument('--regions_template_url', required=True, help="The template file for the regions json e.g. ftp://ftpgrycap.i3m.upv.es/public/eubrabigsea/data/regions.json")
    parser.add_argument('--regions_local_path', required=True, help="The output regions file with updated fields full path that will be used by the application")
    parser.add_argument('--mesosdns', required=True, help='Mesos DNS full address e.g. http://127.0.0.1:8123')
    parser.add_argument('--mesosdns_db', required=True, help="Mesos DNS full name for the DB e.g. '_rfp-db-rfp._tcp.marathon.mesos.'")
    parser.add_argument('--vars', required=True, help="The full path of the file which will be generated by this script. It will contain the new values for various env variables that are needed by the web-app e.g. './vars.rc'")

    args = parser.parse_args()
    regionsURL = args.regions_template_url
    regionsLocalPath = args.regions_local_path
    varsFName = args.vars
    mesosDnsAddr = args.mesosdns
    mesosDnsDb = args.mesosdns_db
    
    
    try:
        print("Load data from " + regionsURL)
        rTmp = urlopen(regionsURL)

        regions = json.load(rTmp)
        print("Get the ips/ports for all regions")
        for idxCountry in range(0, len(regions)):
            cities = regions[idxCountry]["cities"]
            for idxCity in range(0, len(cities)):
               ipPort = getIpPortDns(mesosDnsAddr, cities[idxCity]["mesosDNSBRRoutes"])
               cities[idxCity]["hostBRRoutes"] = ipPort[0]
               cities[idxCity]["portBRRoutes"] = ipPort[1]
               ipPort = getIpPortDns(mesosDnsAddr, cities[idxCity]["mesosDNSBRTrips"])
               cities[idxCity]["hostBRTrips"] = ipPort[0]
               cities[idxCity]["portBRTrips"] = ipPort[1]
            
        
        with open(regionsLocalPath, "w") as regionsF:
            json.dump(regions, regionsF)
            
        with open(varsFName, "w") as varsF:    
            ipPort = getIpPortDns(mesosDnsAddr, mesosDnsDb)
            print("PSQL_HOST ip: " + ipPort[0])
            print("PSQL_HOST port: " + ipPort[1])
            varsF.write("PSQL_HOST=" + ipPort[0] + "\n")
            varsF.write("PSQL_PORT=" + ipPort[1] + "\n")
    except Exception:
        print(traceback.format_exc())
    
    
    
