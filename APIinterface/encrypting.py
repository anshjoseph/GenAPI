from cryptography.fernet import Fernet
from sklearn.decomposition import dict_learning
from . import enc


class Enc:
    @staticmethod
    def genrate_key()->str:
        key = Fernet.generate_key()
        return key


    def __init__(self,key) -> None:
        # self._fernet = Fernet(key)
        self._edcoder = enc.EncBase64withPass(key)

    def _encrypt(self,source:str)->str:
        # return self._fernet.encrypt(source.encode())
        return self._edcoder.encode(source)

    def _decrypt(self,source:str)->str:
        # return self._fernet.decrypt(source)
        return self._edcoder.decode(source)


    def encryptDict(self,source:dict)->dict:
        for key in source.keys():
            source[key] = self._encrypt(source[key])
        return source
    def decryptDict(self,source:dict)->dict:
        for key in source.keys():
            source[key] = self._decrypt(source[key])
        return source


    def encryptList(self,source:list)->list:
        for index,value in enumerate(source):
            source[index] = self._encrypt(value)
        return source
    def decryptList(self,source:list)->list:
        for index,value in enumerate(source):
            source[index] = self._decrypt(value)
        return source
    