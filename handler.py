#!/usr/bin/env python
# encoding: utf-8

'''
Created on 2012-2-25

@author: goodspeedcheng
'''
import collections
__metaclass__ = type


class Handler:
    '''
    处理从Parser调用的方法的对象
        
    这个解析器会在每个块的开始部分调用start()和end()方法，使用合适的块名作为参数，
    sub()方法会用于正则表达式替换中，
        当使用了‘emphasis’这样的名字调用时，它会返回合适的替换函数
    '''
    def callback(self,prefix,name,*args):#参数前加*表示收集多个参数   如果想收集关键字参数 加**
        method = getattr(self,prefix+name,None)
        if callable(method):        #3.X 用 isinstance(method, collections.Callable)         
            return method(*args)
            
    def start(self,name):
        self.callback('start_', name)
        
    def end(self,name):
        self.callback('end_', name)
        
    def sub(self,name):
        def substitution(match):
            result = self.callback('sub_', name,match)
            if result is None:
                match.group(0)
            return result
        return substitution
 
lihtml = []     
class HTMLRenderer(Handler):
    '''
    用于生成HTML的具体处理程序
        
    HTMlRenderer内的方法都可以通过超类处理程序的start()、end()和sub()
        方法来访问，他们实现了用于HTML文档的基本标签
    '''
    def start_document(self): 
        lihtml.append('<!DOCType html><html><head><title>...</title><meta charset="utf-8"><head><body>')
    def end_document(self):
        lihtml.append('</body></html>')
        return lihtml
    def start_paragraph(self):
        lihtml.append('<p>')
    def end_paragraph(self):
        lihtml.append('</p>')
    def start_heading(self):
        lihtml.append('<h2>')
    def end_heading(self):
        lihtml.append('</h2>')
    def start_list(self):
        lihtml.append('<ul>')
    def end_list(self):
        lihtml.append('</ul>')
    def start_listitem(self):
        lihtml.append('<li>')
    def end_listitem(self):
        lihtml.append('</li>')
    def start_title(self):
        lihtml.append('<h1>')
    def end_title(self):
        lihtml.append('</h1>')
    def sub_emphasis(self,match):       
        return '<em>%s</em>' % match.group(1)
    def sub_url(self,match):
        return '<a href="%s">%s</a>' %(match.group(1) ,match.group(1))
    def sub_mail(self,match):      
        return '<a href="mailto:%s">%s</a>' %(match.group(1), match.group(1))
    def feed(self,data):
        lihtml.append(data)