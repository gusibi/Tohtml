#!/usr/bin/env python
# encoding: utf-8

'''
Created on 2012-2-25

@author: goodspeedcheng
'''
import sys,re
from handler import *
from util import *
from rules import *


__metaclass__ = type
class Parser:
    '''
    Parser(语法分析器) 读取文本文件，应用规则，控制处理程序
    '''
    def __init__(self,handler):
        self.handler = handler
        self.rules = []#规则
        self.filters = []#过滤器
        
    def addRule(self,rule):
        self.rules.append(rule)
        
    def addFilter(self,pattern,name):
        def filter(block,handler):
            return re.sub(pattern,handler.sub(name),block)
        #将过滤器添加到过滤器列表
        self.filters.append(filter)
        
    def parse(self,file):
        self.handler.start('document')#以handler.start('document')开始
        for block in blocks(r):#迭代文件内所有块
            for filter in self.filters:#过滤规则
                block = filter(block,self.handler)#使用过滤器并把结果重新绑定到块上
            for rule in self.rules:
                if rule.condition(block):#检查是否应用规则
                    if rule.action(block,self.handler):#rule.action函数返回一个布尔值 如果已经应用规则 返回True
                        break
        html = self.handler.end_document()#以handler.end('document')结束
        for li in html:
            w.write(li+'\n')
        
        
class BasicTextParser(Parser):
    '''
        在构造函数中增加规则和过滤器的具体语法分析器
    '''
    def __init__(self,handler):
        Parser.__init__(self, handler)
        #增加规则
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())
        #增加过滤器
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z]+)', 'url')
        self.addFilter(r'([\.a-zA-Z|0-9]+@[\.a-zA-Z]+[a-zA-Z])', 'mail')
    
handler = HTMLRenderer()
parser = BasicTextParser(handler)

r = open("text_input.txt",'r')
w = open('html.html','w')
parser.parse(r)    
    
    
    