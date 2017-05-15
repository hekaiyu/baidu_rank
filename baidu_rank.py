#coding=utf-8
#工作：根据软件发布的标题查询是否有收录
import requests,codecs,urllib,time
import re
from bs4 import BeautifulSoup
import sys  
reload(sys)
sys.setdefaultencoding( "utf-8" )
class UnicodeStreamFilter:  
	def __init__(self, target):  
		self.target = target  
		self.encoding = 'utf-8'  
		self.errors = 'replace'  
		self.encode_to = self.target.encoding  
	def write(self, s):  
		if type(s) == str:  
			s = s.decode("utf-8")  
		s = s.encode(self.encode_to, self.errors).decode(self.encode_to)  
		self.target.write(s)  
		  
if sys.stdout.encoding == 'cp936':  
	sys.stdout = UnicodeStreamFilter(sys.stdout)  

#以上为cmd下utf-8中文输出的终极解决方案！
headers={
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate, sdch, br",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Connection":"keep-alive",
	"Cookie":"BAIDUID=E7A1C8BA54ADFDA307B663C356C33F5B:FG=1; BIDUPSID=E7A1C8BA54ADFDA307B663C356C33F5B; PSTM=1470026780; sugstore=1; ispeed_lsm=0; BD_UPN=12314353; BD_CK_SAM=1; PSINO=3; BDSVRTM=89; H_PS_PSSID=22164_1444_21102_22157",
	"Host":"www.baidu.com",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}
headers1={
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate, sdch, br",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

def s_word(word):
	word = word.strip()
	word = word.replace(' ', '+').replace('\n', '')
	wordtitle = word.decode("utf8")
	wordtitle = re.sub("[\s+\.\-\!\?\/_,$%^*(+\"\']+|[+——！，。？、~@—【】#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),wordtitle)#去除标点符号，前英文后中文
	return wordtitle
def baidu_html(baiduURL):
	x=1
	while x<5:
		try:
			print "第%s次查询"%x,baiduURL
			html= requests.get(baiduURL, headers = headers,timeout=30)
			r=html.json()
			break
		except:
			x=x+1
			continue
	if x>=5:
		r={"feed":{"all": "1","entry":[{"title":(word.strip()),"url":"超时，请重查"}]}}
	return r
def baidu_title():
	if url=='超时，请重查':
		rt=str(word.strip())+'\t'+str(url)+'\n'
	else:
		rt=str(word.strip())+'\t'+str(url)+'\n'
	return rt

cxtime=time.strftime("%Y%m%d", time.localtime()) 
words=open('xiala.txt','r').readlines()
for word in words:
	sword=s_word(word)
	baiduURL = 'http://www.baidu.com/s?wd=intitle:%s&tn=json&rn=20' % word.strip()
	r = baidu_html(baiduURL)
	all=r.get('feed').get ('all')
	if all==0:
		rt=str(word.strip())+'\t'+'未收'+'\n'
		print rt
		f=open(cxtime+'baiducluded.txt','a')
		f.write(str(rt))
		f.close()
	else:
		for i in r.get('feed').get('entry'): 
			if 'title' in i:
				url=i.get ('url')
				title=i.get ('title')
				ititle=s_word(title)
				if sword in ititle:
					rt=baidu_title()
					print rt
					f=open(cxtime+'baiducluded.txt','a')
					f.write(str(rt))
					f.close()
#so开始，百度以上
	soURL = 'http://www.so.com/s?q=intitle:%s' % word.strip()
	print soURL
	html= requests.get(soURL, headers = headers1,timeout=30)
	html=html.text
	soup = BeautifulSoup(html, 'lxml')
	soup=soup.find_all("h3",class_="res-title ")
	for i in soup:
		soup=i.find_all('a')
		for i in soup:
			sotitle=i.getText()
			sourl=i.get('href')
			r=re.findall("so.com\/link\?url=(.*)?&q",sourl)
			for url in r:
				url = urllib.unquote(url)
				sotitle=s_word(sotitle)
				if sword in sotitle :#对关键词、网站标题同时去除标点，如果网站标题含有关键词，则视为收录
					print sotitle,url
					f=open(cxtime+'socluded.txt','a')
					f.write(str(word.strip())+'\t'+str(url)+'\n')
					f.close()