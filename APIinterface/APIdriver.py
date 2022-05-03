from unittest import result
from .driverUtils import DriverUtils
from .urlEncoder import UrlEncoder
from .encrypting import Enc
 
# url = "https://script.google.com/macros/s/AKfycbwD4s4b62VBPChxedR2VZgw1JpTZM6kckO9XaVorriMPCjgBrurKnBIToiadwhNEecDcA/exec?secretkey=2b7b59b169085f9ce798a181b7446fe64ed7b77f542fb66559e0aa2d1688d80e&opcode=1&fkey=1&sheetname=studentData&pkey=id&data=loginid:1,token:jhsegdnl"
 
# payload={}
# headers = {}
 
# response = requests.request("GET", url, headers=headers, data=payload)
 
# print(response.text)


class APIdriver:
    def __init__(self,url:str,secretKey:str,enckey:str) -> None:
        # self.url:str = "https://script.google.com/macros/s/AKfycbz7z-dUskmlAh2VEPILFqygKYh4a2k-dE4_3dP1SHemZZs1CVM8wND3ACZW9mQoqBzeUw/exec"
        # self.secretKey:str = "2b7b59b169085f9ce798a181b7446fe64ed7b77f542fb66559e0aa2d1688d80e"
        self.url:str = url
        self.secretKey:str = secretKey
        self._enc = Enc(enckey)
        DriverUtils.urlencoder = UrlEncoder(self.url)
   
    def Insert(self,tableName:str,data:dict):
        data = self._enc.encryptDict(data)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "0",
            "sheetname": tableName,
            "data":data
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    def Search(self,tableName:str,columnName:str,findkeyName:str):
        findkeyName = self._enc._encrypt(findkeyName)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "1",
            "sheetname": tableName,
            "pkey":columnName,
            "fkey":findkeyName,
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        try:
            result['Output'] = [self._enc.decryptDict(out) for out in result['Output']]
        except:
            pass
        return result

    def Update(self,tableName:str,columnName:str,findkeyName:str,data:dict)->dict:
        findkeyName = self._enc._encrypt(findkeyName)
        data = self._enc.encryptDict(data)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "2",
            "sheetname": tableName,
            "pkey":columnName,
            "fkey":findkeyName,
            "data":data
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    def Delete(self,tableName:str,columnName:str,findkeyName:str):
        findkeyName = self._enc._encrypt(findkeyName)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "3",
            "sheetname": tableName,
            "pkey":columnName,
            "fkey":findkeyName,
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    def FetchAll(self,tableName:str):
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "4",
            "sheetname": tableName
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        try:
            result['Output']['res'] = [self._enc.decryptList(out) for out in result['Output']['res']]
        except Exception as e:
            print(e)
        return result
    def FetchAllcols(self,tableName:str):
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "5",
            "sheetname": tableName
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    def GetTablesNames(self):
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "6"
        }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result


class AsyncAPIdriver:
    def __init__(self,url:str,secretKey:str,enckey:str) -> None:
        # self.url:str = "https://script.google.com/macros/s/AKfycbz7z-dUskmlAh2VEPILFqygKYh4a2k-dE4_3dP1SHemZZs1CVM8wND3ACZW9mQoqBzeUw/exec"
        # self.secretKey:str = "2b7b59b169085f9ce798a181b7446fe64ed7b77f542fb66559e0aa2d1688d80e"
        self.url:str = url
        self.secretKey:str = secretKey
        self._enc = Enc(enckey)
        DriverUtils.urlencoder = UrlEncoder(self.url)
   
    async def Insert(self,tableName:str,data:dict):
        data = self._enc.encryptDict(data)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "0",
            "sheetname": tableName,
            "data":data
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    async def Search(self,tableName:str,columnName:str,findkeyName:str):
        findkeyName = self._enc._encrypt(findkeyName)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "1",
            "sheetname": tableName,
            "pkey":columnName,
            "fkey":findkeyName,
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        try:
            result['Output'] = [self._enc.decryptDict(out) for out in result['Output']]
        except:
            pass
        return result

    async def Update(self,tableName:str,columnName:str,findkeyName:str,data:dict)->dict:
        findkeyName = self._enc._encrypt(findkeyName)
        data = self._enc.encryptDict(data)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "2",
            "sheetname": tableName,
            "pkey":columnName,
            "fkey":findkeyName,
            "data":data
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    async def Delete(self,tableName:str,columnName:str,findkeyName:str):
        findkeyName = self._enc._encrypt(findkeyName)
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "3",
            "sheetname": tableName,
            "pkey":columnName,
            "fkey":findkeyName,
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    async def FetchAll(self,tableName:str):
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "4",
            "sheetname": tableName
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        try:
            result['Output']['res'] = [self._enc.decryptList(out) for out in result['Output']['res']]
        except Exception as e:
            print(e)
        return result
    async def FetchAllcols(self,tableName:str):
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "5",
            "sheetname": tableName
            }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result
    async def GetTablesNames(self):
        oprations = {
            "secretkey":self.secretKey,
            "opcode": "6"
        }
        result =  DriverUtils.operations(url=self.url,oprations=oprations)
        return result