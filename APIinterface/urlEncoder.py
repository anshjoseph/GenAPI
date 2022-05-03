class UrlEncoder:
    def __init__(self,url:str) -> None:
        self.url:str = url
    def setQuery(self,**kwargs)->None:
        self.parameters:dict = kwargs
    
    def getUrl(self)->str:
        url=f'{self.url}?'
        flag = True
        for key in self.parameters.keys():
            if flag:
                if self.parameters.get(key) != None and len(self.parameters.get(key))!=0:
                    url+=f"{key}={self.parameters[key]}"
                    flag=False
                    continue
            if self.parameters.get(key) != None and len(self.parameters.get(key))!=0:
                url+=f"&{key}={self.parameters[key]}"
        print(url)
        return url