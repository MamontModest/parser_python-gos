from bs4 import BeautifulSoup as bs
import requests
from pywinauto import Application
import keyboard
import gspread
sa = gspread.service_account(filename='parser-360307-6c864aa005a9.json')
sh = sa.open("Пример парсинга")
wks = sh.worksheet("Лист1")
from threading import Thread
def f():
    print('ok')
    b=[]
    app = Application(backend='uia')
    app.connect(title_re=".*Chrome.*")
    element_name = "Address and search bar"
    dlg = app.top_window()
    url = dlg.child_window(title=element_name, control_type="Edit").get_value()
    r = requests.get('https://' + url)
    popitka=0
    while (r.status_code) != 200 and popitka<100:
        r = requests.get('https://' + url)
        popitka+=1
    #b1,b5,b6,b9
    try:
        a=[]
        b=[0]*10
        b[7] = 'https://' + url
        soup = bs(r.text, "html.parser")
        vacancies_names = soup.find_all('div',class_='common-text__value')
        for name in vacancies_names:
            a.append(name.text)
            if len(a)>10:
                break
        if len(a)>10:
            for i in range (10):
                if 'http' in a[i]:
                    b[8]=a[i+1].split('\n')
                    b[8]=b[8][1]
            m=[]
            for i in a:
                m.append(i.split("\n"))
            b[1] = m[2][1]
            b[5] = m[1][1]
            del a
            vacancies_names=soup.find_all('div',class_='price-block__value')
            for name in  vacancies_names:
                b[2]=name.text
            c=[]
            vacancies_names = soup.find_all('div', class_='data-block__value')
            for name in vacancies_names:
                c.append(name.text.split("\n"))
            b[3]=c[0][1]
            b[4]=c[2][1]
            vacancies_names=soup.find_all('div',class_='registry-entry__header-mid__number')
            for name in  vacancies_names:
                b[6]=name.text.split("\n")
                b[6]=b[6][2]
            vacancies_names=soup.find_all('div',class_='registry-entry__body-value')
            for name in vacancies_names:
                b[9]=name.text.split("\n")
                b[9]=b[9][2]
        else:
            print('ok')
            a=[]
            vacancies_names = soup.find_all('span', class_='cardMainInfo__content cost')
            for name in vacancies_names:
                b[2]=name.text
            vacancies_names = soup.find_all('div',class_='cardMainInfo__section')
            for name in vacancies_names:
                a.append(name.text.split("\n"))
            b[1]=a[0][2]
            b[4]=a[-1][-2]
            b[3]=a[3][3]
            b[9]=a[1][-3]
            a=[]
            vacancies_names = soup.find_all('span',class_="cardMainInfo__purchaseLink distancedText")
            for name in vacancies_names:
                b[6]=name.text
            vacancies_names = soup.find_all('section',class_="blockInfo__section section")
            for name in vacancies_names:
                a.append(name.text.split("\n"))
                if len(a)>10:
                    break
            b[5]=a[0][2]
            b[8]=a[1][2]




    except:
        print('Ошибка страницы')
    d=0
    for i in (str(b[2]).replace(" ","")[1:-5]):
        if i in {'0','1','2','3','4','5','6','7','8','9'}:
            d=d*10+int(i)
    b[2]=d

    while str(b[1])[0]==" ":
        b[1]=str(b[1])[1:]
    while str(b[5])[0]==" ":
        b[5]=str(b[5])[1:]
    while str(b[6])[0]==" ":
        b[6]=str(b[6])[1:]
    while str(b[9])[0] == " ":
        b[9] = str(b[9])[1:]

    try:
        for i in range(1, wks.row_count):
            if wks.acell('A' + str(i)).value == None:
                k = i
                break
        b[0]=k
        wks.insert_row(index=k, values=b)

    except:
        print('Ошибка при записи')

    return True
def run():
    keyboard.add_hotkey('alt+j', f)
    keyboard.wait("p+j")
Thread(target=run).start()
