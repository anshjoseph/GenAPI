from .urlEncoder import UrlEncoder
import requests
import json
class DriverUtils:
    urlencoder:UrlEncoder = None

    @staticmethod
    def handelNone(data:str)->str:
        if data == None:
            return ""
        return data

    @staticmethod
    def dictTodata(data)->str:
        if data==None:
            return str()
        result:str = ""
        flag = True
        for key in data.keys():
            if flag:
                result+=f"{key}:{data[key]}"
                flag=False
                continue
            result+=f",{key}:{data[key]}"

        return result
    @staticmethod
    def listToData(datas)->str:
        if datas == None:
            return str()
        result:str = ""
        flag = True
        for data in datas:
            if flag:
                result+=data
                flag=False
            result+=","+data
        return result
    
    @staticmethod
    def operations(url:str,oprations:dict)->dict:
        url:str = ""
        if oprations.get("feilds") == None:
            url = DriverUtils.urlencoder.setQuery(secretkey=oprations.get("secretkey"),
            opcode=oprations.get("opcode"),
            fkey=DriverUtils.handelNone(oprations.get("fkey")),
            sheetname=oprations.get("sheetname"),
            pkey=DriverUtils.handelNone(oprations.get("pkey")),
            data=DriverUtils.dictTodata(oprations.get("data"))
            )
            url = DriverUtils.urlencoder.getUrl()
        else:
            DriverUtils.urlencoder.setQuery(secretkey=oprations.get("secretkey"),
            opcode=oprations.get("opcode"),
            fkey=DriverUtils.handelNone(oprations.get("fkey")),
            sheetname=oprations.get("sheetname"),
            pkey=DriverUtils.handelNone(oprations.get("pkey")),
            data=DriverUtils.dictTodata(oprations.get("data")),
            feilds=DriverUtils.listToData(oprations.get("feilds"))
            )
            url = DriverUtils.urlencoder.getUrl()
        # print(url)
        response = requests.request("GET", url, headers={}, data={})
        # print(response.text)
        return json.loads(response.text)
        # return dict()
        