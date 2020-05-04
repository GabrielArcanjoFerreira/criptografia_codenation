#coding: utf-8

import requests
import json
import hashlib

class Decifrar:
    def __init__(self):
        self.session = requests.session()

    def decifra_json(self, url):
        self.response = self.session.get(url, timeout=None)
        json_response = json.loads(self.response.content)
        cifrado = json_response["cifrado"]
        decifrado = ""
        salto = int(json_response["numero_casas"])
        alfabeto = [letra for letra in "abcdefghijklmnopqrstuvwxyz"]

        #Decifra o texto
        for letra in cifrado:
            try:
                letra = int(letra)
                decifrado += str(letra)

            except ValueError:
                letra = letra.lower()

                if letra in alfabeto:
                    if ord(letra) - salto < 97:
                        letra = chr(123 - (97 - (ord(letra) - salto)))
                    else:
                        letra = chr(ord(letra) - salto)

                decifrado += letra

        resumo = hashlib.sha1(decifrado.encode("utf-8")).hexdigest()

        json_response["resumo_criptografico"] = resumo
        json_response["decifrado"] = decifrado

        #Salva arquivo
        with open("answer.json", "w") as answer:
            json.dump(json_response, answer)
            answer.close()

        #Realiza POST na url
        url = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=65e88c349594bc3cd199b23ed00a08c536250ea2"
        files = [
          ('answer', open('answer.json', 'rb'))
        ]
        self.response = self.session.post(url,files=files)

        print(self.response.text.encode('utf8'))


if __name__ == "__main__":
    http = Decifrar()
    http.decifra_json("https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=65e88c349594bc3cd199b23ed00a08c536250ea2")
