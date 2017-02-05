"""
Gestione della lettura e scrittura delle opzioni su file criptato
Caricamento CMS su server
Autore : Federico Rinaldi
Web: http://www.federicorinaldi.com
Version : 1.0
"""
from ConfigParser import SafeConfigParser
from cryptography.fernet import Fernet
import os

class GestioneProperties():
    key = "XfiH6GYtAj9de7e6kPBOCz25UdmFlxE9u_1UlSGLSdQ="

    def leggiFile(self):
        parser = SafeConfigParser()
        parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'config/config.ini')))
        cipher_suite = Fernet(self.key)
        datiConnessione = {"nome":parser.get('connessioneftp','nome'),
                           "host": cipher_suite.decrypt(parser.get('connessioneftp', 'host')),
                           "username": cipher_suite.decrypt(parser.get('connessioneftp', 'username')),
                           "password": cipher_suite.decrypt(parser.get('connessioneftp', 'password')),
                           "port": cipher_suite.decrypt(parser.get('connessioneftp', 'port'))}
        return datiConnessione

    def scriviFile(self,datiFtp):
        parser = SafeConfigParser()
        parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'config/config.ini')))
        cipher_suite = Fernet(self.key)
        try:
            #parser.add_section("connessioneftp")
            parser.set("connessioneftp", "nome", datiFtp['nome'])
            parser.set("connessioneftp","host",cipher_suite.encrypt(datiFtp['host']))
            parser.set("connessioneftp", "username", cipher_suite.encrypt(datiFtp['username']))
            parser.set("connessioneftp", "password", cipher_suite.encrypt(datiFtp['password']))
            parser.set("connessioneftp", "port", cipher_suite.encrypt(datiFtp['port']))
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'config/config.ini')), 'wb') as configfile:
                parser.write(configfile)
        except Exception as e :
            print e
            return 0
        finally:
            return 1


    def leggiCmsDaScaricare(self):
        parser = SafeConfigParser()
        parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'config/config.ini')))
        sitidaScaricare = {}
        path_items = parser.items("cms")
        for key, path in path_items:
            sitidaScaricare[key] = path

        return sitidaScaricare