#-*- coding:utf-8 -*-
import datetime
import json
import time as TIME
from elasticsearch import Elasticsearch
from time_utils import ts2datetime, datetime2ts,ts2date
from global_utils import es_user_portrait as es


#es = Elasticsearch(['219.224.134.213', '219.224.134.214'], timeout = 6000)

USER_RANK_KEYWORD_TASK_INDEX = 'user_rank_keyword_task'
USER_RANK_KEYWORD_TASK_TYPE = 'user_rank_task'

MAX_ITEMS = 2 ** 10

def add_task( user_name ,type = "keyword",range = "all"  ,pre ='flow_text_' , during = '1' , start_time ='2013-09-07' ,end_time ='2013-09-07', keyword = 'hello,world' , sort_norm = 'bci' , sort_scope  = 'in_limit_keyword', time = 1, isall = False  ):
    time_now = TIME.time()
        
       
    body_json = {
                'submit_user' : user_name ,
                'keyword' : keyword,
                'submit_time' : str(ts2date(time_now)) ,
                'end_time' : end_time,
                'search_type' : type,
                'status':0,
                'range' : range , 
                'user_ts' : user_name +  str(time_now),
                'pre' : pre,
                'during' : during ,
                'start_time' : start_time ,
                'sort_norm' : sort_norm ,
                'sort_scope' : sort_scope,
                'time' : time ,
                'isall' : isall
            }
    try:
        es.index(index = USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE ,  body=body_json)
        return body_json["user_ts"]
    except Exception , e1 :
        print e1

def search_user_task(user_name):
    c_result = {}
    query = {"query":{"bool":{"must":[{"term":{"user_rank_task.submit_user":user_name}}],"must_not":[],"should":[]}},"from":0,"size":MAX_ITEMS,"sort":[],"facets":{},"fields":["status","search_type","keyword","submit_user","sort_scope","sort_norm","start_time","user_ts","end_time"]}
    try:
        return_list = []
        result = es.search(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , body=query)['hits']
        c_result['flag'] = True
        for item in result['hits']:
            result_temp = {}
            result_temp['submit_user'] = item['fields']['submit_user'][0]
            result_temp['search_type'] = item['fields']['search_type'][0]
            result_temp['keyword'] = item['fields']['keyword'][0]
            result_temp['sort_scope'] = item['fields']['sort_scope'][0]
            result_temp['sort_norm'] = item['fields']['sort_norm'][0]
            result_temp['start_time'] = item['fields']['start_time'][0]
            result_temp['end_time'] = item['fields']['end_time'][0]
            result_temp['status'] = item['fields']['status'][0]
            result_temp['search_id'] = item['fields']['user_ts'][0]
            return_list.append(result_temp)
        c_result['data'] = return_list
        return c_result
    except Exception , e1 :
        c_result['flag'] = False
        c_result['data'] = e1
        print e1
        return c_result

def getResult(search_id):
    query = {"query":{"bool":{"must":[{"term":{"user_rank_task.user_ts":search_id}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"facets":{}}
    result = es.search(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , body=query)['hits']
    item = result['hits'][0]
    if item['_source']['status'] == 1:
        result_obj = {}
        result_obj['keyword'] = item['_source']['keyword']
        result_obj['sort_scope'] = item['_source']['sort_scope']
        result_obj['sort_norm'] = item['_source']['sort_norm']
        result_obj['start_time'] = item['_source']['start_time']
        result_obj['end_time'] =item['_source']['end_time']
        result_obj['result'] = json.loads(item['_source']['result'])
        return result_obj
    else :
        return []    

def delOfflineTask(search_id):
    query = {"query":{"bool":{"must":[{"term":{"user_rank_task.user_ts":search_id}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"facets":{}}
    result = es.searresult = es.search(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , body=query)['hits']['hits'][0]
    task_id = result['_id']
    es.delete(index=USER_RANK_KEYWORD_TASK_INDEX , doc_type=USER_RANK_KEYWORD_TASK_TYPE , id = task_id )
    return True


if __name__ == "__main__":
    print delOfflineTask('admin@qq.com1459089864.09')       
            
