
import http.server
import socketserver
import json
import http.client



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    OPENFDA_API_URL= "api.fda.gov"
    OPENFDA_API_EVENT= "/drug/event.json"
    OPENFDA_API_LYRICA= "search=patient.drug.medicinalproduct:" "LYRICA""&limit=10"

    def get_lyrica(self):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_LYRICA)

        r1=conn.getresponse()
        print(r1.status,r1.reason)
        data1 = r1.read()


        data=data1.decode("utf8")
        events=json.loads(data)
        return events
    def get_main_page(self):

        html = """
        <html>

            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1>Open FDA Client </h1>
                <form method="get" action="receive">
                    <input type= "text" name = "drug"> </input>
                    <input type= "submit" value= "Drug List"></input>
                </form>
                <form method="get"action="search">
                    <input type= "text" name = "companynumb"> </input>
                    <input type= "submit" value= "Company Search"></input>
                </form>
            </body>
        </html>
        """
        return html
    def get_med(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?search=patient.drug.medicinalproduct:"+drug+"&limit=10")
        r1 = conn.getresponse()
        print(r1.status,r1.reason)
        data1 = r1.read()
        data=data1.decode("utf8")
        events=json.loads(data)
        return events

    def get_event(self): #ESTA DEFINIENDO LA CLASE QUE ACOGE TO LO QUE VA DENTRO DEL GET EVENT
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #clase dentro de la biblioteca http.client que gestiona la conexion con la pagina
        #de la biblioteca coge httpsconection que permite establecer conexcionex con https con una url. crea un puto cliente
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10")
        r1 = conn.getresponse()
        #consigue una respuesta y la aloja o guarda en r1.
        print(r1.status,r1.reason)
        data1 = r1.read()


        data=data1.decode("utf8")
        events=json.loads(data)
        return events

    def get_drugs(self,events):

        medicamentos=[]
        for event in events["results"]:
            medicamentos+=[event["patient"]["drug"][0]["medicinalproduct"]]
        return medicamentos

    def get_company_numb(self,events):
        com_numb=[]
        for event in events["results"]:
            com_numb+= [event["companynumb"]]
        return com_numb



    def drug_page(self,medicamentos):
        s=""
        for med in medicamentos:
            s += "<li>" +med+ "</li>"
        html="""
        <html>
            <head></head>
                <body>
                    <ul>
                        %s
                    </ul>
                </body>
        <html>""" %(s)
        return html
    def do_GET(self):

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        #h1 es el tamañconn = http.client.HTTPSConnection("api.fda.gov") #clase dentro de la biblioteca http.client que gestiona la conexion con la pagina

        # Send message back to client

        # Write content as utf-8 data


        if self.path =="/":
            html= self.get_main_page()
            self.wfile.write(bytes(html, "utf8")) #envia al navegador lo alojado en la variable del cliente html en este caso
        elif self.path == "/receive": #DE ESTA MANERA, LA PAGINA SE ABRE CUANDO SE EJECUTA EL BOTON
            events= self.get_event()
            medicamentos= self.get_drugs(events)
            html= self.drug_page(medicamentos)
            self.wfile.write(bytes(html, "utf8"))
        elif self.path== "/search?":
            events = self.get.event()
            com_num=self.get_company_numb(events)
            html= self.drug_page(com_num)
            self.wfile.write(bytes(html,"utf8"))
        elif self.path== "/drugs":
            events = self.get.event()
            com_num=self.get_company_numb(events)
            html= self.drug_page(com_num)
            self.wfile.write(bytes(html,"utf8"))
        elif self.path.find ("search"):
            s=self.path
            print (s)
            d=s.split("=")
            print (d)
            drug=d[1]
            print (drug)

            events=self.get_med(drug)
            com_numb= self-get_company_numb(events)
            html=self.drug_page(com_num)
            self.wfile.write(bytes(html,"utf8"))
        return
#Copyright [yyyy] [name of copyright owner]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
