import json
import os
import pandas as pd
import psycopg2
import time
import re  
from pydash import py_
import datetime as dt
from datetime import datetime
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import boto3
from boto3.dynamodb.types import TypeDeserializer


lambda_client = boto3.client('lambda')

dynamodb =  boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')
fssycnrequest = dynamodb.Table('fs-sync-requests-db')
fs_sync_requests_db = os.environ.get("fs-sync-requests-db","fs-sync-requests-db")


def lambda_handler(event, context):
    print(event)
    events = os.environ.get("requests", '[{"testing":"2022-09-14T08:00:41.067Z-o7D89"}]')
    events = json.loads(events) 
    print('events: ', events)
    connection = psycopg2.connect(user='appuserpostgres', password='fsdbauprod#rsa@641011', host='c.fspostgresprod.postgres.database.azure.com', database='citus')
    # connection = psycopg2.connect(user='citus', password='forcesight@123', host='c.forcesightpostgres.postgres.database.azure.com', database='citus')
    events =  [{'createdAt': '2023-05-18T11:19:35.828Z', 'createdBy': 'cron', 'requestId': '2023-05-18T11:19:35.828Z-S5IA7', 'channel': 'Myntra', 'orgId': 955, 'updatedAt': '2023-05-18T11:19:35.938Z', 'config': {'ecs': {'cpu': 512, 'memory': 2048}}, 'key': '0'}]
    cursor = connection.cursor() 
    # event = events[0] if events else []
    
    # print(events)
    for event in events:
        status = 'COMPLETED'
        try:
            # print(event)
            # org_id = event['orgId']
            org_id = event['orgId']
            response = dynamodb_client.query(
                TableName=fs_sync_requests_db,
                KeyConditionExpression="orgId = :org_id and requestId = :requestId",
                ExpressionAttributeValues={
                    ":org_id": {"N": "{}".format(event['orgId'])},
                    ":requestId": {"S": "{}".format(event['requestId'])}
                }
            )
            print('response: ', response)
            requestId = event['requestId']
            key = event['key']
            source_data = response['Items'][0] if response != [] and response['Items'] != [] else []
            source_data = TypeDeserializer().deserialize({"M": source_data})
            
            
            # bucket = event['bucket']
            # file_name = event['file_name']
        except Exception as ex: 
            print('error: ', ex) 
            print('Not workinng')
            
    try:       
        shopify_details = ' select dashboard from "fs-organisations-channels-db" where orgid = {} and channel = \'TechnoSport\' limit 1 '.format(org_id)
        print(shopify_details)
        shopify_details = cursor.execute(shopify_details)
        shopify_details = [dict((cursor.description[i][0], value) \
            for i, value in enumerate(row)) for row in cursor.fetchall()]
        
        # if shopify_details:
        #     domain_url = shopify_details[0]['dashboard']['domainURL']
        # else:
        #     domain_url = None
            
        # print('domain_url: ', domain_url)

        domain_url = 'https://www.technosport.in/product/'
                
        organisation_details = ' select * from "fs-organisations-channels-db" where orgid = {} and channel = \'Facebook-Ads\'  limit 1 '.format(org_id)
        print(organisation_details)
        organisation_details = cursor.execute(organisation_details)
        organisation_details = [dict((cursor.description[i][0], value) \
            for i, value in enumerate(row)) for row in cursor.fetchall()]
        
        for fb in organisation_details:
            # print(fb['dashboard'])
            FACEBOOK_CLIENT_ID = fb['dashboard']['facebookClientId'] if 'dashboard' in fb and 'facebookClientId' in fb['dashboard'] else ''
            ACCOUNT_ID = fb['dashboard']['facebookAccountId'] if 'dashboard' in fb and 'facebookAccountId' in fb['dashboard'] else ''
            FACEBOOK_CLIENT_SECRET = fb['dashboard']['facebookSecret'] if 'dashboard' in fb and 'facebookSecret' in fb['dashboard'] else ''
            FACEBOOK_ACCESS_TOKEN = fb['dashboard']['facebookToken'] if 'dashboard' in fb and 'facebookToken' in fb['dashboard'] else ''
            
            
            print('test: ', FACEBOOK_CLIENT_ID,ACCOUNT_ID,FACEBOOK_CLIENT_SECRET,FACEBOOK_ACCESS_TOKEN)
            # Initialize Facebook Ads API
            
            currentupdatedat = datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            currentupdatedat = currentupdatedat.strftime('%Y-%m-%d %H:%M:%S+00')
            current_date = datetime.today()
            start_date = current_date - timedelta(days=67)
            end_date = current_date - timedelta(days=16)
            
            # sync_start,sync_end = start_date,end_date
            sync_start = (start_date - timedelta(days=1)).strftime('%Y-%m-%d') + 'T18:30:00Z'
            # sync_end = str(end_date - timedelta(days=1)) + 'T18:30:00Z'
            sync_end = (end_date).strftime('%Y-%m-%d') + 'T18:29:59Z'
                
            print(org_id,sync_start,sync_end)
            update_orders_based_date = 'UPDATE orders SET productadsspent = null, fbfees = \'{}\'::jsonb,updatedat = now() WHERE orgid = %s and channel = \'Shopify\' and orderdate  between %s and %s '
            # .format(org_id,min_date,max_date)
            update_values = (org_id,sync_start,sync_end)
            # print('update_orders_based_date: ', update_orders_based_date,update_values)
            cursor.execute(update_orders_based_date,update_values)
            connection.commit()
            
            # acc_id = 'sdfs'  # or acc_id = ['tets', 'dfs']

            if isinstance(ACCOUNT_ID, str):
                ACCOUNT_ID = [ACCOUNT_ID]
            
            for account_id in ACCOUNT_ID:
            
                FacebookAdsApi.init(FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, FACEBOOK_ACCESS_TOKEN)

                start_date = current_date - timedelta(days=67)
                end_date = current_date - timedelta(days=16)
                
                # sync_start,sync_end = start_date,end_date
                sync_start = (start_date - timedelta(days=1)).strftime('%Y-%m-%d') + 'T18:30:00Z'
                # sync_end = str(end_date - timedelta(days=1)) + 'T18:30:00Z'
                sync_end = (end_date).strftime('%Y-%m-%d') + 'T18:29:59Z'
                # print('start_date: ', start_date)
                ads_info_based_on_date = []
                # time.sleep(2)
                while start_date <= end_date:
                    time.sleep(2)
                    # print('start_date: ', start_date)
                    sync_date = start_date.strftime('%Y-%m-%d')
                    start_date += timedelta(days=1)
                    print('sync_date: ', sync_date)
                    fields = ['ad_name', 'ad_id', 'spend']
                    params = {
                        'time_range': {
                            'since': sync_date,
                            'until': sync_date
                        },
                        'level': 'ad',
                        'limit': 100000
                    }

                    ad_account = AdAccount(account_id)
                    # print('ad_account: ', ad_account)
                    ad_insights = ad_account.get_insights(fields, params)
                    
                    

                    for ad_insight in ad_insights:
                        ad_id = ad_insight.get('ad_id')
                        ad_name = ad_insight.get('ad_name')
                        spend = ad_insight.get('spend')
                        date_start = ad_insight.get('date_start')
                        date_stop = ad_insight.get('date_stop')
                        info = {
                            'ad_id': ad_id,
                            'ad_name': ad_name,
                            'spend': spend,
                            'date_start': date_start,
                            'date_stop': date_stop
                        }
                        ads_info_based_on_date.append(info)

                # print('ads_info_based_on_date:',(ads_info_based_on_date))
                ads_info_based_on_date1 = ads_info_based_on_date
                if ads_info_based_on_date:
                    time.sleep(30)
                    ad_account = AdAccount(account_id)

                    fields = [
                        'adcreatives'
                    ]
                    ads_info = []
                    ads = ad_account.get_ads(fields)
                    # print('ads: ', ads,len(ads))
                    
                    for ad in ads:
                        # print(ad)
                        time.sleep(2)
                        ad_id = ad.get('id')
                        print('ad_id: ', ad_id)
                        if 'adcreatives' in ad:
                            for ad_cre_id in ad['adcreatives']['data']:
                                ad_creative_id = ad_cre_id['id']
                                ads_info.append({'id': ad_id,'ad_creative_id': ad_creative_id})
                        # print('Ad ID:', ad_id,ad_creative_id)
                    # print('ads_info: ', (ads_info))
                    # ads_info.append({'id': '23855252029870038','ad_creative_id': '23856255996390038'})
                    
                    time.sleep(5)
                    
                    fields = [
                        'ad_id',
                        'object_story_spec'
                    ]

                    adscreatives = ad_account.get_ad_creatives(fields)

                    adscreatives_info = []
                    for ad_creative in adscreatives:
                        # print('ad_creative: ', ad_creative)
                        ad_id = ad_creative.get('id')
                        # if ad_id == '23858956883930723' or ad_id == 23858956883930723:
                        #     print('ad_creative: ', ad_creative)
                        links = []
                        # object_story_spec = ad_creative.get('object_story_spec')
                        if 'object_story_spec' in ad_creative:
                            # for ad_cre in ad_creative['object_story_spec']['link_data']:
                                # print('tested: ', ad_cre)
                            if 'link_data' in ad_creative['object_story_spec']:
                                if 'child_attachments' in ad_creative['object_story_spec']['link_data']:
                                    for link in ad_creative['object_story_spec']['link_data']['child_attachments']:
                                        # print('link: ', link)
                                        links.append(link['link'])
                                        # time.sleep(55)
                                else:
                                    link = ad_creative['object_story_spec']['link_data']['link']
                                    links.append(link)
                            elif 'video_data' in ad_creative['object_story_spec'] and 'call_to_action' in ad_creative['object_story_spec']['video_data'] and 'link' in ad_creative['object_story_spec']['video_data']['call_to_action']['value']:
                                # print(ad_creative['object_story_spec'])
                                link = ad_creative['object_story_spec']['video_data']['call_to_action']['value']['link']
                                links.append(link)
                            elif 'template_data' in ad_creative['object_story_spec'] and 'link' in ad_creative['object_story_spec']['template_data']:  
                                link = ad_creative['object_story_spec']['template_data']['link']
                                links.append(link)
                            else:
                                # print('sjdfhks: ')
                                links = [domain_url]
                                # time.sleep(25)
                            adscreatives_info.append({'ad_creative_node_id': ad_id,'link': links})
                        else:
                            # print('tested: ', domain_url)
                            links = [domain_url]
                            adscreatives_info.append({'ad_creative_node_id': ad_id,'link': links})
                            
                    # print('adscreatives_info:', adscreatives_info,len(adscreatives_info))
                    # print('ads_info_based_on_date: ', ads_info_based_on_date)
                    # print('ads_info: ', ads_info)
                    ads_info_based_on_date=pd.DataFrame(ads_info_based_on_date) 
                    ads_info=pd.DataFrame(ads_info)
                    first_two_res = pd.merge(ads_info_based_on_date, ads_info, how='right', left_on = 'ad_id', right_on = 'id')
                    first_two_res = json.dumps(json.loads(first_two_res.reset_index().to_json(orient='records')))
                    first_two_res = json.loads(first_two_res)
                    first_two_res = [entry for entry in first_two_res if entry.get('spend') is not None]
                    # first_two_res = (ad for ad in first_two_res if ad['spend'])
                    # print('first_two_res: ', first_two_res, len(first_two_res))
                    
                    
                    first_two_res=pd.DataFrame(first_two_res)
                    adscreatives_info=pd.DataFrame(adscreatives_info)
                    combined_res = pd.merge(first_two_res, adscreatives_info, how='right', left_on = 'ad_creative_id', right_on = 'ad_creative_node_id')
                    combined_res = json.dumps(json.loads(combined_res.reset_index().to_json(orient='records')))
                    combined_res = json.loads(combined_res)
                    combined_res = [entry for entry in combined_res if entry.get('spend') is not None]
                    # print('combined_res: ', combined_res,len(combined_res))
                    
                    
                    # for item in combined_res:
                    #     if not item['link']:
                    #         item['link'] = [domain_url]
                    # print('ads_info_based_on_date: ', ads_info_based_on_date)
                    
                    not_matched_res = []
                    combined_res_set = {(ad['ad_name'], ad['spend'], ad['date_start']) for ad in combined_res}

                    for data in ads_info_based_on_date1:
                        if (data['ad_name'], data['spend'], data['date_start']) not in combined_res_set:
                            links = [domain_url]
                            data['link'] = links
                            not_matched_res.append(data)

                    
                    combined_res.extend(not_matched_res)
                    
                    
                    
                    
                    
                    final_res = []
                    for res in combined_res:
                        # print('res: ', res)
                        if len(res['link']) > 0:
                            spend = round(float(res['spend']) / len(res['link']),2)
                            date = res['date_start']
                            for link in res['link']:
                                final_res.append({'date': date,'link': link,'spend': spend})
                                # time.sleep(55)
                        
                    
                    
                    # print('final_res: ', final_res)
                    
                    # time.sleep(65)
                    final_res = pd.DataFrame(final_res)
                    # json.dumps(json.loads(combined_res.reset_index().to_json(orient='records')))
                    grouped_data = json.dumps(json.loads(final_res.groupby(['link', 'date'])['spend'].sum().reset_index().to_json(orient='records')))
                    grouped_data = json.loads(grouped_data)
                    grouped_data = sorted(grouped_data, key=lambda x: x['date'])
                    print('grouped_data: ', grouped_data,len(grouped_data))
                    
                    camp_res = []    
                    for res in combined_res:
                        if len(res['link']) > 0:
                            date = res['date_start']
                            spend = round(float(res['spend']) / len(res['link']),2)
                            ad_name = res['ad_name']
                            for link in res['link']:
                                camp_res.append({'name': ad_name,'link': link,'spend': spend,'date': date})
                    
                    
                    # print('camp_res: ', camp_res)
                    camp_res = pd.DataFrame(camp_res)
                    # json.dumps(json.loads(combined_res.reset_index().to_json(orient='records')))
                    camp_grouped_data = json.dumps(json.loads(camp_res.groupby(['link', 'name','date'])['spend'].sum().reset_index().to_json(orient='records')))
                    camp_grouped_data = json.loads(camp_grouped_data)
                    camp_grouped_data = sorted(camp_grouped_data, key=lambda x: x['date'])
                    
                    print('camp_grouped_data: ', len(camp_grouped_data))
                    
                    
                    # time.sleep(30)
                    
                    
                    for prod in grouped_data:
                        # print('prod: ', prod)
                        date = datetime.strptime(prod['date'], '%Y-%m-%d').date()
                        start_date = str(date - timedelta(days=1)) + 'T18:30:00Z'
                        end_date = str(date) + 'T18:29:59Z'
                        # print('start_date: ', start_date,end_date)
                        landing_page = prod['link']
                        cost = prod['spend']
                        # print(landing_page)
                        # time.sleep(55)
                        domain_url = domain_url.replace("https://","").replace("www.","").replace("/","")
                        if 'products' in landing_page and domain_url in landing_page:
                            category = landing_page.split('products')[1].split('?')[0]
                            # print(category)
                            # time.sleep(2)
                            variant = 'variant=' + str(landing_page.split('variant=')[1].split('&')[0]) if 'variant=' in landing_page else ''
                            search_url = '%'+ domain_url +'%' + 'products' +  category + '?' + variant + '%'
                        elif 'collections' in landing_page and domain_url in landing_page:
                            category = landing_page.split('collections')[1].split('?')[0]
                            search_url = '%'+ domain_url +'%' + 'collections' +  category + '%'
                            # time.sleep(55)
                        elif domain_url in landing_page:
                            category = 'Not Available'
                            search_url = '%'
                        else:
                            category = 'Not Available'
                            search_url = ''    # print('category: ', category,search_url)
                        # time.sleep(45)
                        
                        # time.sleep(2)
                        get_inventory = 'SELECT distinct(sku) as sku FROM inventory where OrgId = {} and Channel = \'TechnoSport\' and ( url like \'{}\' or collection::text like \'{}\')  '.format(org_id,search_url,search_url)
                        # print('get_inventory: ', get_inventory)
                        results = cursor.execute(get_inventory)
                        results = [dict((cursor.description[i][0], value) \
                                for i, value in enumerate(row)) for row in cursor.fetchall()]
                        
                        skus = py_.pluck(results, 'sku')
                        print('sku_len: ', len(skus))
                        if skus:
                            skus.extend(['999999','999999'])
                            skus = tuple(e for e in skus)
                            sku_query = 'and sku in {}'.format(skus)
                        else:
                            sku_query = ''
                            # print('tested: ', category)
                            # time.sleep(2)
                        
                        get_orders_qty = 'SELECT sum(quantityshipped) as qty FROM orders where OrgId = {} and Channel = \'TechnoSport\' and orderid not like \'%temp%\' and orderdate between \'{}\' and \'{}\'  {}  '.format(org_id,start_date,end_date,sku_query)
                        # get_orders_qty = 'SELECT sum(quantityshipped) as qty FROM orders where Channel = \'Shopify\' and OrgId = {}  and orderdate between \'{}\' and \'{}\'  {}  '.format(org_id,start_date,end_date,sku_query)
                        # print('get_orders_qty: ', get_orders_qty)
                        results = cursor.execute(get_orders_qty)
                        results = [dict((cursor.description[i][0], value) \
                                for i, value in enumerate(row)) for row in cursor.fetchall()]
                        if results:
                            total_qty = results[0]['qty']
                        else:
                            total_qty = 0
                        
                        matching_entries = [entry for entry in camp_grouped_data if entry['link'] == prod['link'] and entry['date'] == prod['date']] 
                
                
                        print('total_qty: ', total_qty,matching_entries)   
                        campaign_details = {}
                        avg_cost = 0    
                        if total_qty and total_qty != 0:
                            # print('tested')
                            for item in matching_entries:
                                key = str(account_id) + item['name'].replace("'","''") + '--' + landing_page + '--' + item['date']
                                cost_inside_for  = item['spend'] / total_qty
                                campaign_details[key] = cost_inside_for 
                            print('campaigndetails: ', campaign_details)
                            campaign_details = json.dumps(campaign_details)
                            
                            avg_cost = round((float(cost) / total_qty),2)
                            new_landing_page = {str(account_id) + landing_page + start_date: avg_cost }                      
                            new_landing_page = json.dumps(new_landing_page)
                            orderupdation = """ UPDATE orders SET updatedat = \'{}\',adslastsyncat = \'{}\',fbfees = CASE WHEN fbfees IS NULL OR jsonb_typeof(fbfees) <> 'object' THEN \'{}\'::jsonb ELSE fbfees || \'{}\'::jsonb END,campaigndetails = CASE WHEN campaigndetails IS NULL OR jsonb_typeof(campaigndetails) <> 'object' THEN \'{}\'::jsonb ELSE campaigndetails || \'{}\'::jsonb END WHERE OrgId = {}  and Channel = \'TechnoSport\' and orderid not like \'%temp%\' and  orderdate between \'{}\' and \'{}\'  {}; """.format(currentupdatedat,currentupdatedat,campaign_details,campaign_details,campaign_details,campaign_details,org_id,start_date,end_date,sku_query)
                            # orderupdation = """ UPDATE orders SET adslastsyncat = \'{}\',fbfees = CASE WHEN fbfees IS NULL OR jsonb_typeof(fbfees) <> 'object' THEN \'{}\'::jsonb ELSE fbfees || \'{}\'::jsonb END WHERE Channel = \'Shopify\' and OrgId = {}  and orderdate between \'{}\' and \'{}\'  {}; """.format(currentupdatedat,new_landing_page,new_landing_page,org_id,start_date,end_date,sku_query)
                            # update_values = (landing_page,productadsspent,org_id,skus)
                            # print('orderupdation1: ', orderupdation)
                            cursor.execute(orderupdation)
                            connection.commit()
                            
                            
                            productadsspenttotalsum = """ WITH order_totals AS (SELECT o.order_id,max(o.quantityshipped) as quantityshipped, SUM(CAST(kv.value AS numeric)) as total FROM orders o, LATERAL jsonb_each_text(o.fbfees::jsonb) kv WHERE  o.orgid = {} {} and orderdate between \'{}\' and \'{}\' and orderid not like \'%temp%\'  GROUP BY o.order_id ) UPDATE orders o SET productadsspent = ot.total * ot.quantityshipped FROM order_totals ot WHERE o.order_id = ot.order_id; """.format(org_id,sku_query,start_date,end_date)
                            # print('productadsspenttotalsum1: ', productadsspenttotalsum)
                            cursor.execute(productadsspenttotalsum)
                            connection.commit()
                        
                        else:
                            print('skus: ', len(skus))
                            temp_skus = [x for x in skus if x != '999999']
                            if len(temp_skus) > 0:
                                avg_cost = round((float(cost)/ len(temp_skus)),2)
                                # print('temp_skus: ', temp_skus)
                                order_info = []
                                for temp in temp_skus:
                                    # print('temp: ', temp)
                                    new_cat = re.sub('[^a-zA-Z0-9 \n\.]', '', category)
                                    order_id = end_date + temp +'-temp'
                                    # order_id = end_date + temp + new_cat +'-temp'
                                    channel = 'Shopify'
                                    id = channel + order_id
                                    sku = temp
                                    productadsspent = avg_cost
                                    order_date = end_date
                                    # print(org_id,id,order_id,channel,sku,productadsspent,order_date)
                                    order_info.append((org_id,id,order_id,channel,sku,productadsspent,order_date))
                                # print('order_info: ', order_info)
                                # time.sleep(10)
                                if order_info:   
                                    order_info = str(order_info)[1:-1]
                                    temp_orders = """insert into orders(orgid,id,orderid,channel,sku,productadsspent,orderdate)
                                    values {}
                                    on conflict(orgid,id) 
                                    do update set productadsspent = EXCLUDED.productadsspent;""".format(order_info)
                                    # print('temo_orders: ', temp_orders)
                                    cursor.execute(temp_orders)
                                    connection.commit()
                                    
                                    for item in matching_entries:
                                        key = str(account_id) + item['name'].replace("'","''") + '--' + landing_page + '--' + item['date']
                                        cost = round((float(item['spend'])/ len(temp_skus)),2)
                                        campaign_details[key] = cost
                                    campaign_details = json.dumps(campaign_details) 
                            
                                    
                                    new_landing_page = {str(account_id) + landing_page + start_date: avg_cost }                      
                                    new_landing_page = json.dumps(new_landing_page)
                                    orderupdation = """ UPDATE orders SET updatedat = \'{}\',adslastsyncat = \'{}\',fbfees = CASE WHEN fbfees IS NULL OR jsonb_typeof(fbfees) <> 'object' THEN \'{}\'::jsonb ELSE fbfees || \'{}\'::jsonb END,campaigndetails = CASE WHEN campaigndetails IS NULL OR jsonb_typeof(campaigndetails) <> 'object' THEN \'{}\'::jsonb ELSE campaigndetails || \'{}\'::jsonb END WHERE orgid = {} AND sku in {} and orderdate between \'{}\' and \'{}\'; """.format(currentupdatedat,currentupdatedat,campaign_details,campaign_details,campaign_details,campaign_details,org_id,skus,start_date,end_date)
                                    # update_values = (landing_page,productadsspent,org_id,skus)
                                    # print('orderupdation2: ', orderupdation)
                                    cursor.execute(orderupdation)
                                    connection.commit()

                                    productadsspenttotalsum = """ WITH order_totals AS (SELECT o.order_id,max(o.quantityshipped) as quantityshipped, SUM(CAST(kv.value AS numeric)) as total FROM orders o, LATERAL jsonb_each_text(o.fbfees::jsonb) kv WHERE o.sku in {} and o.orgid = {} and orderdate between \'{}\' and \'{}\' GROUP BY o.order_id ) UPDATE orders o SET productadsspent = ot.total * coalesce(ot.quantityshipped,1) FROM order_totals ot WHERE o.order_id = ot.order_id; """.format(skus,org_id,start_date,end_date)
                                    # print('productadsspenttotalsum2: ', productadsspenttotalsum)
                                    cursor.execute(productadsspenttotalsum)
                                    connection.commit()
                            
                        print('search_url:', search_url,total_qty,avg_cost,len(skus))
            
            
        if 'requestId' in event:
            # print(source_data)
            sources = source_data['sources']
            sources[event['key']]['0']["status"] = status
            sources[event['key']]["status"] = status
            # print('source: ', sources)
            # print('environments: ', os.environ)
            response = fssycnrequest.update_item(
                    Key={"orgId": event['orgId'],
                        "requestId": event['requestId']},
                    UpdateExpression="set sources = :sources",
                    # ExpressionAttributeNames={"#statement": "status"},
                    ExpressionAttributeValues={":sources": sources})
    except Exception as ex:
        print(ex)
        status = 'FAILED'
        if 'requestId' in event:
            print(source_data)
            sources = source_data['sources']
            sources[event['key']]['0']["status"] = status
            sources[event['key']]["status"] = status
            # print('source: ', sources)
            # print('environments: ', os.environ)
            response = fssycnrequest.update_item(
                    Key={"orgId": event['orgId'],
                        "requestId": event['requestId']},
                    UpdateExpression="set sources = :sources",
                    # ExpressionAttributeNames={"#statement": "status"},
                    ExpressionAttributeValues={":sources": sources})                    

print("start")
lambda_handler({}, None)
print("finished")
