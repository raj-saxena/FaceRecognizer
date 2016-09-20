import httplib, ssl,json
from base64 import b64encode


class BahmniServerHelper:
    GET_LOGIN_SESSION_URL = "/openmrs/ws/rest/v1/session?v=custom:(uuid)"
    localConn = httplib.HTTPConnection('localhost', 8080)

    def __init__(self):
        self.headers = {"Content-type": "application/json;charset=UTF-8"}
        self.authenticatedCookie = None
        self.bahmniConn = httplib.HTTPSConnection("192.168.33.10", context=ssl._create_unverified_context())

    def getAuthenticatedCookie(self, uname, pswd):
        if not self.authenticatedCookie:
            # Fire delete request to get the jsession id to authenticate later
            self.bahmniConn.request("DELETE", self.GET_LOGIN_SESSION_URL)
            resp = self.bahmniConn.getresponse()
            setCookieHeader = resp.getheader('set-cookie')
            self.bahmniConn.close()

            # Prepare login request
            self.headers['Cookie'] = setCookieHeader
            userAndPass = b64encode(bytes(uname + ':' + pswd), "utf-8").decode("ascii")
            self.headers['Authorization'] = 'Basic %s' % userAndPass
            self.bahmniConn.request("GET", self.GET_LOGIN_SESSION_URL, headers=self.headers)
            resp = self.bahmniConn.getresponse()
            self.authenticatedCookie = resp.getheader('set-cookie') + "; JSESSIONID=" + str(json.loads(resp.read())['sessionId'])
            resp.close()
        return self.authenticatedCookie


# x = BahmniServerHelper()
# print x.getAuthenticatedCookie("superman", "Admin123")
# print x.getAuthenticatedCookie("afs", "asf")
