import requests
import json
import time

class CNPJ:

    def getDados(cnpj):

        while True:

            link=f'https://open.cnpja.com/office/{cnpj}'
            response=requests.get(link)            

            if response.status_code==200:

                break

            else:

                time.sleep(10)

                pass

            pass

        js=response.json()

        return js

        pass

    def getValidarCep(cep):

        try:

            while True:

                link=f'https://viacep.com.br/ws/{cep}/json/'

                response=requests.get(link)

                js=response.json()

                if response.status_code==200:

                    break

                time.sleep(10)

                pass
            
            try:

                if js['erro']:

                    retorno=True

                    pass

                pass
            
            except:

                retorno=False

                pass

            return retorno
        
        except:

            CNPJ.getValidarCep(cep)

            pass

        pass

    pass