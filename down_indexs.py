from playwright.sync_api import sync_playwright
import time,os,sys
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()
def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text
def citem(h):
    a=h.split('<div class="List-item" tabindex="0">')[1:]
    return [{'act':b.split('<span class="ActivityItem-metaTitle">')[1].split('<')[0],
            'time':b.split('<span class="ActivityItem-metaTitle">')[1].split('<span>')[1].split('<')[0],
            'data-zop':eval(dehtml(b.split('data-zop="')[1].split('"')[0]))if'data-zop="'in b else None,
            'data-za-extra-module':eval(dehtml(b.split('data-za-extra-module="')[1].split('"')[0]).replace('false','False').replace('true','True').replace('null','None'))if'data-za-extra-module="'in b else None}for b in a]
if not os.path.exists('indexs'):os.makedirs('indexs')
nn=0
n2=0
with sync_playwright() as p:
    browser_type=p.firefox
    if browser_type:
        br = browser_type.launch()
        pa = br.new_page()
        pa.goto('https://www.zhihu.com/people/lao-liang-83-95')
        pa.locator('xpath=//*[@class="Button Modal-closeButton Button--plain"]').click()
        while True:
            n2+=1
            l=[]
            dn1=len((a:=pa.content()).split('<div class="List-item" tabindex="0">')[1:])
            pa.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            pa.evaluate("window.scrollTo(0, 0);")
            dn2=len((c:=pa.content()).split('<div class="List-item" tabindex="0">')[1:])
            if dn1!=dn2:
                a=citem(a)
                if n2==1:l.extend(a)
                c=citem(c)
                c2=[]
                for b in c:
                    if b not in a:
                        c2.append(b)
                c=c2
                l.extend(c)
                for n in range(len(a)):
                    pa.evaluate('document.getElementsByClassName(\'List-item\')[0].remove()')
                print(l[len(l)-1])
                nn+=len(l)
                print('已循環%d次，已抓取動態數目為%d項。'%(n2,nn))
                f=open('indexs/%d.list'%int(time.time()),'w+');f.write(repr(l));f.close()
                #break
        #pa.screenshot(path=f'example-{browser_type.name}.png')
        br.close()
