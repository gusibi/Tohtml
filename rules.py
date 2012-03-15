#!/usr/bin/env python
# encoding: utf-8

'''
Created on 2012-2-25

@author: goodspeedcheng
'''
__metaclass__ = type

class Rule:
    '''
        所有类的基类
    '''
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True
    
class HeadingRule(Rule):
    '''
        标题是一个最多70个字符的行，不以冒号结尾
        <h2>
    '''
    type = 'heading'   #在rule 类里被handler.start(self.type)调用
    def condition(self,block):
        #返回一个布尔值判断给定的值是否符合规则
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    '''
        题目是文档的第一个块，前提是它是大标题
        <h1>
    '''
    type = 'title'
    first = True
    
    def condition(self,block):
        if not self.first:#如果不是第一个块
            return False
        self.first = False
        #用HeadingRule.condition()判断是否符合title的规则
        return HeadingRule.condition(self, block)

class ListItemRule(Rule):
    '''
        列表是以连字符开始的段落，作为格式化的一部分，连字符会被删除
        <li></li>
    '''
    type = 'listitem'
    def condition(self,block):
        return block[0] =='-'
    def action(self,block,handler):
        #应用规则   
        handler.start(self.type)
        handler.feed(block[1:].strip())#连字符会被删除
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    '''
        列表开始于并非列表项的块和随后的列表项之间，由最后一个连续的列表项作为结束
        <ul></ul>
    '''  
    type = 'list'
    inside = False#默认文本块不在列表中
    def condition(self,block):
        return True
    def action(self,block,handler):
        if not self.inside and ListItemRule.condition(self, block):#当在列表中且符合列表项规则时调用start函数 
            handler.start(self.type)
            self.inside = True#标记为在列表中
        elif self.inside and not ListItemRule.condition(self, block):#当inside = True且不符合列表项规则时调用start函数 
            handler.end(self.type)
            self.inside =False#标记为不在列表中
        return False
    

class ParagraphRule(Rule):
    '''
        段落是不符合其它规则的块
    '''
    type = 'paragraph'
    def condition(self,block):
        return True
    