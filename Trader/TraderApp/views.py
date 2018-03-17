from django.shortcuts import render
from django.http import JsonResponse
from nltk import *
from requests import get
import numpy as np
import re, requests, json, datetime
from TraderApp.models import Person,Asset,Transaction
from django.contrib.auth.models import User
from decimal import Decimal

# Create your views here.
def profile(request):
	return render(request,'trader/index.html', )

def handleCommand(request):
    text=request.GET.get("text").lower()
    current_user=request.user.get_username()
    retval=do_action(text,current_user)

    return JsonResponse(retval)

#Utility Functions
def getData(url):
    response=get(url)
    data=response.json()
    return data

def extracter(data,tags):
    extracted=[]
    for i in range(0,len(data)):
        temp=[]
        for j in range(0,len(tags)):
            temp.append(data[i][tags[j]])
        extracted.append(temp)
    return extracted

def graph_json(data):

    ret={'x':[],'open':[],'close':[],'high':[],'low':[]}

    for each in data:
        value=datetime.datetime.fromtimestamp(each[0])
        ret['x'].append(value.strftime('%Y-%m-%d %H:%M:%S'))
        ret['high'].append(each[1])
        ret['low'].append(each[2])
        ret['open'].append(each[3])
        ret['close'].append(each[4])

    ret=json.dumps(ret)
    ret=json.loads(ret)

    return ret

#API Calls
def getDataByDay(CurrencyFrom,CurrencyTarget='INR',limit='7',interval='1'):
    url="https://min-api.cryptocompare.com/data/histoday?fsym="
    url+=str(CurrencyFrom)+'&tsym='+str(CurrencyTarget)+'&limit='+str(limit)+'&aggregate='+str(interval)
    data=getData(url)
    data=data["Data"]
    extracted=extracter(data,['time','high','low','open','close'])
    return extracted

def getDataByHour(CurrencyFrom,CurrencyTarget='INR',limit='24',interval='1'):
    url="https://min-api.cryptocompare.com/data/histohour?fsym="
    url+=str(CurrencyFrom)+'&tsym='+str(CurrencyTarget)+'&limit='+str(limit)+'&aggregate='+str(interval)
    data=getData(url)
    data=data["Data"]
    extracted=extracter(data,['time','high','low','open','close'])
    return extracted

def getDataByMinutes(CurrencyFrom,CurrencyTarget='INR',limit='12',interval='5'):
    url="https://min-api.cryptocompare.com/data/histominute?fsym="
    url+=str(CurrencyFrom)+'&tsym='+str(CurrencyTarget)+'&limit='+str(limit)+'&aggregate='+str(interval)
    data=getData(url)
    data=data["Data"]
    extracted=extracter(data,['time','high','low','open','close'])
    return extracted

#Functionalities
def buy_now(text,user=None):
    mode="dollars"    #Load default mode from database

    pattern=r"dollar|dollars|rupees"
    if (re.search(pattern,text)==None):
        pattern=r"\d+\s\bbitcoin[s]\b|\d+\s\bether\b|\d+\s\bripple\b|\d+\s\bethereum\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        what=match[1]
    else:
        pattern=r"\d+\s\bdollars\b|\d+\s\bdollar\b|\d+\s\brupees\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        mode=match[1]

        pattern=r"\bbitcoin[s]\b|\bether\b|\bripple\b|\bethereum\b"
        match=re.findall(pattern,text)[0]
        what=match[0]

    print(quantity,what,mode)
    
    return {'quantity': quantity, 'what': what, 'mode': mode}


def buy_later(text,user=None):
    pattern=r"\d+\s\bhours\b|\d+\s\bminutes\b|\d+\s\bminute\b|\d+\s\bhour\b"
    match=re.findall(pattern,text)[0].split(' ')
    time=float(match[0])
    unit=match[1]

    mode="dollars"   #Load default mode from database

    pattern=r"dollar|dollars|rupees"
    if (re.search(pattern,text)==None):
        pattern=r"\d+\s\bbitcoin[s]\b|\d+\s\bether\b|\d+\s\bripple\b|\d+\s\bethereum\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        what=match[1]
    else:
        pattern=r"\d+\s\bdollars\b|\d+\s\bdollar\b|\d+\s\brupees\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        mode=match[1]

        pattern=r"\bbitcoin[s]\b|\bether\b|\bripple\b|\bethereum\b"
        match=re.findall(pattern,text)[0]
        what=match[0]

    print(time,unit,quantity,what,mode)

def sell_now(text,user=None):
    mode="dollars"    #Load default mode from database

    pattern=r"dollar|dollars|rupees"
    if (re.search(pattern,text)==None):
        pattern=r"\d+\s\bbitcoin[s]\b|\d+\s\bether\b|\d+\s\bripple\b|\d+\s\bethereum\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        what=match[1]
    else:
        pattern=r"\d+\s\bdollars\b|\d+\s\bdollar\b|\d+\s\brupees\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        mode=match[1]

        pattern=r"\bbitcoin[s]\b|\bether\b|\bripple\b|\bethereum\b"
        match=re.findall(pattern,text)[0]
        what=match[0]

    print(quantity,what,mode)

def sell_later(text,user=None):
    pattern=r"\d+\s\bhours\b|\d+\s\bminutes\b|\d+\s\bminute\b|\d+\s\bhour\b"
    match=re.findall(pattern,text)[0].split(' ')
    time=float(match[0])
    unit=match[1]

    mode="dollars"   #Load default mode from database

    pattern=r"dollar|dollars|rupees"
    if (re.search(pattern,text)==None):
        pattern=r"\d+\s\bbitcoin[s]\b|\d+\s\bether\b|\d+\s\bripple\b|\d+\s\bethereum\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        what=match[1]
    else:
        pattern=r"\d+\s\bdollars\b|\d+\s\bdollar\b|\d+\s\brupees\b"
        match=re.findall(pattern,text)[0].split(' ')
        quantity=float(match[0])
        mode=match[1]

        pattern=r"\bbitcoin[s]\b|\bether\b|\bripple\b|\bethereum\b"
        match=re.findall(pattern,text)[0]
        what=match[0]

    print(time,unit,quantity,what,mode)

def plot_graph_week(text,user=None):
    print("Weeks Graph Plotting")
    pattern=r"\bbitcoin\b|\bbitcoins\b|\bether\b|\bripple\b|\bethereum\b"
    match=re.findall(pattern,text)[0]

    #get list of currencies from file
    currencies=get_from_file('currencies.txt')
    currencies=[x.split('\n')[0] for x in currencies]

    for each in currencies:
        each=each.split(' ')
        if (each[0]==match):
            currencyFrom=each[1]

    pattern=r"\d+"
    duration=float(re.findall(pattern,text)[0])

    pattern=r"\bINR\b|\bUSD\b|\bXRP\b|\bBTC\b|\bETH\b"
    currencyTo=re.findall(pattern,text)
    if (len(currencyTo)==0):
        currencyTo='INR'
    else:
        currencyTo=currencyTo[0]

    print(currencyFrom,currencyTo,duration)
    
    data=getDataByDay(currencyFrom,currencyTo,duration*7)
    return graph_json(data)

def plot_graph_day(text,user=None):
    print("Days Graph Plotting")
    pattern=r"\bbitcoin\b|\bbitcoins\b|\bether\b|\bripple\b|\bethereum\b"
    match=re.findall(pattern,text)[0]

    #get list of currencies from file
    currencies=get_from_file('currencies.txt')
    currencies=[x.split('\n')[0] for x in currencies]

    for each in currencies:
        each=each.split(' ')
        if (each[0]==match):
            currencyFrom=each[1]

    pattern=r"\d+"
    duration=float(re.findall(pattern,text)[0])

    pattern=r"\bINR\b|\bUSD\b|\bXRP\b|\bBTC\b|\bETH\b"
    currencyTo=re.findall(pattern,text)
    if (len(currencyTo)==0):
        currencyTo='INR'
    else:
        currencyTo=currencyTo[0]

    print(currencyFrom,currencyTo,duration)
    
    data=getDataByHour(currencyFrom,currencyTo,duration*24) 
    return graph_json(data)

def compare():
    pass

def show_transactions():
    pass

def send(text,sender=None):

    pattern=r"\d+"
    match=re.findall(pattern,text)[0]
    amount=float(match)

    pattern=r"\bbitcoin\b|\bbitcoins\b|\bether\b|\bripple\b|\bethereum\b"
    match=re.findall(pattern,text)[0]

    #get list of currencies from file
    currencies=get_from_file('currencies.txt')
    currencies=[x.split('\n')[0] for x in currencies]

    for each in currencies:
        each=each.split(' ')
        if (each[0]==match):
            coin=each[1]

    users=get_from_file('users.txt')
    print(users)

    for each in users:
        each=each.split('\n')[0]
        if (each in text):
            target=each

    server="http://localhost:5000/txion"
    post_data={'from':sender,'to':target,'amount':amount, 'coin':coin}

    print(post_data)
    r=requests.post(server,data=post_data)

    user_from=User.objects.get(username=sender)
    user_to=User.objects.get(username=target)

    person_from=Person.objects.get(user=user_from)
    person_to=Person.objects.get(user=user_to)

    asset=Asset.objects.get(asset_id=coin)

    amount=Decimal(str(amount))

    txn=Transaction.objects.create(user_from=person_from,
                                    user_to=person_to,
                                    asset=asset,
                                    units=amount)

    txn.save()

    return post_data

def get_transactions(text,user=None):

    # transactions=Transaction.objects.all()
    user=User.objects.get(username=user)
    person=Person.objects.get(user=user)
    
    transactions={}
    key=0

    try:
        debit=Transaction.objects.filter(user_from=person)
        for d in debit:
            transactions[key]=[str(d.user_from),str(d.user_to),str(d.asset),str(d.units),str(d.date),'debit']
            key=key+1
    except:
        print("No Debit Transactions")

    try:
        credit=Transaction.objects.filter(user_to=person)
        for c in credit:
            transactions[key]=[str(c.user_from),str(c.user_to),str(c.asset),str(c.units),str(c.date),'credit']
            key=key+1
    except:
        print("No Credit Transactions")

    transactions["transactions"] = True;
    transactions["size"] = key
    return transactions

#Match Predefined actions
def do_action(text,user,type='relation', corpus='webbase'):
    url="http://swoogle.umbc.edu/SimService/GetSimilarity"

    possible_actions=get_from_file('predefined_actions.txt')  #Get all sentences from database

    result=[]
    func=[]
    for each in possible_actions:
        each=each.split('@')
        sample=each[0]
        response=get(url, params={'operation':'api','phrase1':text,'phrase2':sample,'type':type,'corpus':corpus})
        result.append(float(response.text.strip()))
        func.append((each[1].split('\n'))[0])

    action=np.argmax(np.array(result))

    possibles=globals().copy()
    possibles.update(locals())
    caller=possibles.get(func[action])

    return caller(text,user)

#Get all predefined actions
def get_from_file(filename):
    return list(open(filename))