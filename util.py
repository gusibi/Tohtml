#!/usr/bin/env python
# encoding: utf-8

'''
util.py

Created by goodspeed on 2012-03-11.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.


    lines生成器只是在文件的最后追加一个空行
    block生成器实现--当生成一个块后，里面的行会被连起来 并且后得的字符串会被删掉，得到一个代表快的字符串
'''


def lines(file):
    for line in file:
        yield line
        yield '\n'
        
def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []