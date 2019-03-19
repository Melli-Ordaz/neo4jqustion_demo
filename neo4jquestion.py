# -*- coding: utf-8 -*-
#author:827852966@qq.com
import aiml
import os,sys
from py2neo import Graph,Node,Relationship
#备注：这是演示小程序，主要用来演示功能的调用关系，而非工程实践
#检索知识图谱
def kgquery( input):
    # 连接数据库
    test_graph = Graph("http://localhost:7474", username="neo4j", password="123456")
    # 查找节点
    find_code_1 = test_graph.find_one("歌手", property_key="name", property_value= input)
    return find_code_1

if __name__ == '__main__':
    #切换到语料库所在工作目录
    mybot_path = './resource'
    os.chdir(mybot_path)
    #
    mybot = aiml.Kernel()
    mybot.learn("startup.xml")
    mybot.respond('load neo4jquestion')
    #处理响应
    while True:
        input_message = raw_input("Enter your message >> ")
        if len(input_message) > 60:
            print mybot.respond("input is too long > 60")
            continue
        elif input_message.strip() == '':
            print mybot.respond("空")
            continue

        if input_message == 'q':
            exit()
        else:
            response = mybot.respond(input_message)
            if response == "":
                ans = mybot.respond('找不到答案')
                print ans
            #通过知识图谱查询
            elif response[0] == '#':
                if response.__contains__("neo4j"):
                    #获取用户输入的变量
                    res = response.split(':')
                    #实体
                    entity = str(res[1]).replace(" ","")
                    #属性
                    attr = str(res[2]).replace(" ","")
                    print entity+'<---->'+attr
                    ans = kgquery(entity)
                    print ans
                # 匹配不到模版，通用查询
                elif response.__contains__("NoMatchingTemplate"):
                    print "NoMatchingTemplate"
                    print "搜索引擎查询，此功能暂不支持"

                #多答案选项选择的策略：
                if len(ans) == 0:
                    ans = mybot.respond('找不到答案')
                    print 'neo4jquestion：' + ans
                elif len(ans) >1 and  type(ans) == list:
                    print "不确定候选答案"
                    print 'neo4jquestion: '
                    for a in ans:
                        print a.encode("utf8")
                else:
                    print ans
            # 匹配模版
            else:
                print 'neo4jquestion：' + response

        #print mybot.respond(raw_input("Enter your message >> "))