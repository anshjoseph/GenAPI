# from urllib.request import Request

import re
import uvicorn
from fastapi import FastAPI, Request
from APIinterface.APIdriver import AsyncAPIdriver
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import Fernet
import hashlib 

#   App Constant
app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth = "dhfiueiu983uy4903ki,p[3i[0ikmlkv3409uvjkej9843yuhv5984ythin93ry8vvolr3oinj"
async def checkAuth(request:Request)->bool:
    _request = await request.json()
    if _request.get('auth')!= None:
        if _request.get('auth') == auth:
            return True
    return False

url = "https://script.google.com/macros/s/AKfycbzI8OmV18j2NbH-_gOFpcZkRsdTgD44Qp92a4zrRDpJSCrY-4jJ6JuogRTUmCurHUFITw/exec"
apiKey = "2b7b59b169085f9ce798a181b7446fe64ed7b77f542fb66559e0aa2d1688d80e"
encodeKey = 'B-508--xebRcKnnXRM_KsGy8q2d3osFQISOs574Svj8='
APIdriver = AsyncAPIdriver(url,apiKey,encodeKey)
Tables = {
    "passwords"   : ["uuid","password","menomin","login_uuid","website","username"],
    "MasterLogin" : ["uuid" , "username" ,"password"]
}
encrypt = Fernet(encodeKey)

async def checkLogin(authKey:str)->bool:
    try:
        key = encrypt.decrypt(authKey.encode()).decode()
    except:
        return False
    _out = await APIdriver.Search("MasterLogin","uuid",key)
    if _out.get("Error_code") != None:
        return False
    if len(_out.get("Output"))==0:
        return False
    return True

async def checkUsername(username:str):
    _out = await APIdriver.Search("MasterLogin","username",username)
    if _out.get("Error_code") != None:
        return False
    if len(_out.get("Output"))==0:
        return False
    return True






@app.get("/")
async def getStatus(request:Request):
    # print(request)
    if not (await checkAuth(request)):
        return {"out":"hmmmmm"}
    _request = await request.json()
    loginornot = await checkLogin(_request.get("authkey"))
    if not loginornot:
        return {"out":"login first"}
    _key = encrypt.decrypt(_request.get("authkey").encode()).decode()
    out = await APIdriver.Search("passwords","login_uuid",_key)
    return {"out": out}


@app.post("/setpassword")
async def setpassword(request:Request):
    if not (await checkAuth(request)):
        return {"out":"hmmmmm"}
    _request = await request.json()
    if _request.get('authkey') is None:
        return {"out":"not login"}
    loginornot = await checkLogin(_request.get("authkey"))
    if not loginornot:
        return {"out":"not login"}
    _username = str(_request.get('username'))
    _password = str(_request.get('password'))
    _menonic = str(_request.get('menonic'))
    _website = str(_request.get('website'))
    _key = encrypt.decrypt(_request.get("authkey").encode()).decode()

    await APIdriver.Insert("passwords",{
        "uuid":str(uuid4()),
        "password":_password,
        "username":_username,
        "menomin":_menonic,
        "login_uuid":_key,
        "website":_website
    })
    return {"out":"new password is added"}







@app.post("/user")

async def user(request:Request):
    if not (await checkAuth(request)):
        return {"out":"hmmmmm"}
    _request = await request.json()
    if not await checkUsername(_request.get("username")):
        await APIdriver.Insert("MasterLogin",{
            "uuid": str(uuid4()),
            "username": _request.get("username"),
            "password": hashlib.sha512(_request.get("password").encode()).hexdigest()
            })
        return {"out":"user api is make"}
    return {"out":"user another username"}

@app.post("/login")
async def getLogin(request:Request):
    if not (await checkAuth(request)):
        return {"out":"hmmmmm"}
    _data = await request.json()
    _username = _data.get('username')
    _password = hashlib.sha512(_data.get('password').encode()).hexdigest()
    dataOut = await APIdriver.Search("MasterLogin","username",_username)
    try:
        print(dataOut.get("Output")[-1].get("password"))
        if dataOut.get("Output")[-1].get("password") == _password:
            return {"authkey":encrypt.encrypt(dataOut.get("Output")[-1].get("uuid").encode())}
    except:
        pass
    return {"authkey": "0"}



if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, port=8000, host='127.0.0.1')