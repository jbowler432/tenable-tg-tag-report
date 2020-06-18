import requests
import json
import sys
import time
import os
import csv
from datetime import datetime

def read_keys():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    print(fileDir)
    f=open(keys_dir+"keys.json","r")
    keys=json.load(f)
    return keys

def get_keys(key_name):
        keys=[]
        f=open("keys.csv","r")
        for line in f:
                items=line.split(",")
                name=items[0]
                ak=items[1]
                sk=items[2]
                # print name, ak, sk
                if name==key_name:
                        keys.append(ak)
                        keys.append(sk)
                        keys.append(name)
        return keys


def days_passed(ts):
	current_time=time.time()
	elapsed_time=current_time-ts
	days_since=elapsed_time/86400
	return int(days_since)


def get_asset_filters(headers):
# returns list of all target group filters
	url = "https://cloud.tenable.com/filters/workbenches/assets"
	response = requests.request("GET", url, headers=headers)
	decoded = json.loads(response.text)
	for filter in decoded['filters']:
		# print(filter)
		# print("\n")
		filter_name=filter['name']
		filter_control=filter['control']
		if filter_name=="target_group":
			control_list=filter_control['list']
			# print(filter_name)
			# print(filter_control)
			# print(control_list)
			return control_list

def get_target_groups(headers):
        url = "https://cloud.tenable.com/target-groups"
        response = requests.request("GET", url, headers=headers)
        decoded = json.loads(response.text)
        tg_lst=[]
        rtn_lst=[]
        for tg in decoded['target_groups']:
                tg_name=tg['name']
                tg_id=tg['id']
                tg_members=tg['members'].encode('utf-8')
                tg_lst=[tg_name,tg_id,tg_members]
                rtn_lst.append(tg_lst)
        return rtn_lst



def get_vuln_filters(headers):
# returns list of all target group filters
	url = "https://cloud.tenable.com/filters/workbenches/vulnerabilities"
	response = requests.request("GET", url, headers=headers)
	decoded = json.loads(response.text)
	for filter in decoded['filters']:
		# print(filter)
		# print("\n")
		filter_name=filter['name']
		filter_control=filter['control']
		if filter_name=="target_group":
			control_list=filter_control['list']
			# print(filter_name)
			# print(filter_control)
			# print(control_list)
			return control_list


def get_assets_no_tg(headers):
	# company summary - no target group
	url = "https://cloud.tenable.com/workbenches/assets"
	querystring = {"date_range":"90","filter.0.filter":"is_licensed","filter.0.quality":"eq","filter.0.value":"true","filter.search_type":"and","all_fields":"full"}
	response = requests.request("GET", url, headers=headers, params=querystring)
	decoded = json.loads(response.text)
	asset_count=decoded['total']
	return asset_count

def get_assets_filtered(querystring,headers):
	# company summary - no target group
	url = "https://cloud.tenable.com/workbenches/assets"
	response = requests.request("GET", url, headers=headers, params=querystring)
	decoded = json.loads(response.text)
	asset_count=decoded['total']
	return asset_count

def get_assets(target_group,headers):
	url = "https://cloud.tenable.com/workbenches/assets"
	querystring = {"date_range":"90","filter.0.filter":"is_licensed","filter.0.quality":"eq","filter.0.value":"true","filter.1.filter":"target_group","filter.1.quality":"eq","filter.1.value":target_group,"filter.search_type":"and","all_fields":"full"}
	response = requests.request("GET", url, headers=headers, params=querystring)
	decoded = json.loads(response.text)
	asset_count=decoded['total']
	return asset_count

def get_vulns(querystring,headers):
	url = "https://cloud.tenable.com/workbenches/vulnerabilities"
	response = requests.request("GET", url, headers=headers, params=querystring)
	decoded = json.loads(response.text)
	vuln_count=decoded['total_vulnerability_count']
	return vuln_count

def get_users(headers):
	url = "https://cloud.tenable.com/users"
	response = requests.request("GET", url, headers=headers)
	decoded = json.loads(response.text)
	row=[]
	table=[]
	for x in decoded['users']:
		uname=x['username']
		try:
			lastlogin_ms=x['lastlogin']
			lastlogin=lastlogin_ms/1000
			days_since=days_passed(lastlogin)
			loginfail=x['login_fail_total']
			row=[uname,datetime.utcfromtimestamp(lastlogin).strftime('%Y-%m-%d'),days_since,loginfail]
			table.append(row)
		except:
			row=[uname,'No login info']
			table.append(row)
	return table

def get_scan_details(scan_id,hist_id,headers):
	url = "https://cloud.tenable.com/scans/"+str(scan_id)
	querystring={"history_id":str(hist_id)}
	response = requests.request("GET", url, headers=headers, params=querystring)
	decoded = json.loads(response.text)
	scan_start=decoded['info']['scan_start']
	print(scan_start)
	days_since=days_passed(scan_start)
	name=decoded['info']['name']
	owner=decoded['info']['owner']
	hostcount=decoded['info']['hostcount']
	try:
		targets=decoded['info']['targets'].replace('\n',' ').replace('\r',' ')
	except:
		targets=decoded['info']['targets']
	row=[scan_id,name,owner,hostcount,datetime.utcfromtimestamp(scan_start).strftime('%Y-%m-%d'),days_since,targets]
	return row

def get_scan_history(id,headers):
	url = "https://cloud.tenable.com/scans/"+str(id)+"/history"
	response = requests.request("GET", url, headers=headers)
	decoded = json.loads(response.text)
	history=decoded['history'][0]
	return history

def get_scans(headers):
    url = "https://cloud.tenable.com/scans"
    response = requests.request("GET", url, headers=headers)
    decoded = json.loads(response.text)
    row=[]
    table=[]
    count=0
    for x in decoded['scans']:
        try:
            name=x['name']
            id=x['id']
            enabled=x['enabled']
            owner=x['owner']
            status=x['status']
            type=x['type']
            rrules=x['rrules']
            schuuid=x['schedule_uuid']
            if status!="empty":
                count=count+1
                row=[id,name,owner,status,type,rrules,schuuid]
                print("Scan job = "+str(id)+" | "+name+" | "+owner)
                table.append(row)
        except:
            if status!="empty":
                row=[id,name,"error"]
                print(row)
    #table.append(row)
    print("Num scan jobs = "+str(count))
    return table


def write_csv(fh,lst):
    for row in lst:
        for col in row:
            if isinstance(col,str):
                myString=col.replace(","," | ")+","
            elif isinstance(col,unicode):
                myString=col.encode("utf-8").replace(","," | ")+","
            else:
                myString=str(col).replace(","," | ")+","
            fh.write(myString.replace("\n"," ").replace("\r"," "))
            print(myString)
            myTimeString2="(UTC - "+datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+")"
            fh.write(myTimeString2)
            fh.write("\n")

def write_csv_row(fh,row):
    for col in row:
        if isinstance(col,str):
            myString=col.replace(","," | ")+","
        elif isinstance(col,unicode):
            myString=col.encode("utf-8").replace(","," | ")+","
        else:
            myString=str(col).replace(","," | ")+","
        fh.write(myString.replace('\n',' ').replace('\r',' '))
        fh.write(myString)
        print(myString)
        myTimeString2="(UTC - "+datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+")"
        fh.write(myTimeString2)
        fh.write("\n")


#
# Main
#

print("\n*** in Master ***")

keys_dir="../"
results_dir="../results/"

keys=read_keys()
tio_AK=keys["tio_AK"]
tio_SK=keys["tio_SK"]

api_keys="accessKey="+tio_AK+";secretKey="+tio_SK

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'X-APIKeys': api_keys
    }



myTimeString=" (UTC,"+datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+","+str(time.time())+")"

#
asset_filters=get_asset_filters(headers)
vuln_filters=get_vuln_filters(headers)
tg_info=get_target_groups(headers)

company_summary=1
tg_summary=1
asset_summary=1
vuln_summary=1

#
# company summary - no target group
#
if company_summary==1:
    f=open(results_dir+"company_summary.csv","w+")
    fcsv=csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # all licensed
    asset_count=get_assets_no_tg(headers)
    time.sleep(1)
    # nnm exclusive
    querystring = {"date_range":"90","filter.0.filter":"is_licensed","filter.0.quality":"eq","filter.0.value":"true","filter.1.filter":"sources","filter.1.quality":"set-hasonly","filter.1.value":"PVS","filter.search_type":"and","all_fields":"full"}
    pvs_count=get_assets_filtered(querystring,headers)
    time.sleep(1)
    # nessus exclusive
    querystring = {"date_range":"90","filter.0.filter":"is_licensed","filter.0.quality":"eq","filter.0.value":"true","filter.1.filter":"sources","filter.1.quality":"set-hasonly","filter.1.value":"NESSUS_SCAN","filter.search_type":"and","all_fields":"full"}
    nessus_count=get_assets_filtered(querystring,headers)
    time.sleep(1)
    # agent exclusive
    querystring = {"date_range":"90","filter.0.filter":"is_licensed","filter.0.quality":"eq","filter.0.value":"true","filter.1.filter":"sources","filter.1.quality":"set-hasonly","filter.1.value":"NESSUS_AGENT","filter.search_type":"and","all_fields":"full"}
    agent_count=get_assets_filtered(querystring,headers)
    time.sleep(1)
    # has agent
    querystring = {"date_range":"90","filter.0.filter":"is_licensed","filter.0.quality":"eq","filter.0.value":"true","filter.1.filter":"sources","filter.1.quality":"set-has","filter.1.value":"NESSUS_AGENT","filter.search_type":"and","all_fields":"full"}
    has_agent_count=get_assets_filtered(querystring,headers)
    time.sleep(1)
    # has nessus
    querystring = {"date_range":"90","filter.0.filter":"is_licensed","filter.0.quality":"eq","filter.0.value":"true","filter.1.filter":"sources","filter.1.quality":"set-has","filter.1.value":"NESSUS_SCAN","filter.search_type":"and","all_fields":"full"}
    has_nessus_count=get_assets_filtered(querystring,headers)
    time.sleep(1)
    print("Total Licensed Asset Count = "+str(asset_count))
    print("NNM Exclusive = "+str(pvs_count))
    print("Agent Exclusive = "+str(agent_count))
    print("Nessus Exclusive = "+str(nessus_count))
    print("Has Agent = "+str(has_agent_count))
    print("Has Nessus = "+str(has_nessus_count))
    time.sleep(1)
    querystringC = {"date_range":"90","filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"Critical","filter.search_type":"and","all_fields":"full"}
    querystringH = {"date_range":"90","filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"High","filter.search_type":"and","all_fields":"full"}
    querystringM = {"date_range":"90","filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"Medium","filter.search_type":"and","all_fields":"full"}
    querystringL = {"date_range":"90","filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"Low","filter.search_type":"and","all_fields":"full"}
    vuln_countC=get_vulns(querystringC,headers)
    vuln_countH=get_vulns(querystringH,headers)
    vuln_countM=get_vulns(querystringM,headers)
    vuln_countL=get_vulns(querystringL,headers)
    print("\n*** Company Summary ***")
    print("Asset Count="+str(asset_count)+" Criticals="+str(vuln_countC)+" Highs="+str(vuln_countH)+" Med="+str(vuln_countM)+" Low="+str(vuln_countL))
    myTimeString2=datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d')
    row=[myTimeString2, asset_count, vuln_countC, vuln_countH, vuln_countM, vuln_countL]
    fcsv.writerow(row)
    f.close()
    # append to history file
    f=open(results_dir+"company_history.csv","a+")
    fcsv=csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    myTimeString2=datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d')
    row=[myTimeString2,asset_count, vuln_countC, vuln_countH, vuln_countM, vuln_countL]
    fcsv.writerow(row)
    f.close()


#
# Target Group Summary
#
if tg_summary==1:
	print("\n** Target Group Summary **")
	f=open(results_dir+"tgs_details.csv","w+")
	fcsv=csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for row in tg_info:
		print(row[0])
		fcsv.writerow(row)
	f.close()


#
# Asset Count by Target Group
#
if asset_summary==1:
    print("\n** Asset Count per Target Group **")
    f=open(results_dir+"tgs_asset_count_hist.csv","w+")
    row=[]
    table_data=[]
    for x in asset_filters:
        tg_id=x['value']
        fname=str(tg_id)+"_asset_count_hist.csv"
        f.write(fname+","+x['name']+"\n")
        asset_count=get_assets(x['value'],headers)
        time.sleep(0.500)
        row=[x['name'],x['value'],asset_count]
        print(x['name'], x['value'], asset_count)
        table_data.append(row)
    f2=open(results_dir+fname,"a+")
    myTimeString2=datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d')
    f2.write(myTimeString2+","+str(asset_count)+","+str(x['name'])+"\n")
    f2.close()
    f.close()
    f=open(results_dir+"tgs_asset_count.csv","w+")
    fcsv=csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in table_data:
    #print row
        fcsv.writerow(row)
    f.close()

#
# Vuln Count by Target Group and Severity
#
if vuln_summary==1:
	print("\n** Vuln Count by Target Group **")
	f=open(results_dir+"tgs_vuln_count_hist.csv","w+")
	row=[]
	table_data=[]
	for x in vuln_filters:
	   tg_name=x['name']
	   tg_value=x['value']
	   fname=str(tg_value)+"_vuln_count_hist.csv"
	   f.write(fname+","+x['name']+"\n")
	   querystringC = {"date_range":"90","filter.0.filter":"target_group","filter.0.quality":"eq","filter.0.value":str(tg_value),"filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"Critical","filter.search_type":"and","all_fields":"full"}
	   querystringH = {"date_range":"90","filter.0.filter":"target_group","filter.0.quality":"eq","filter.0.value":str(tg_value),"filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"High","filter.search_type":"and","all_fields":"full"}
	   querystringM = {"date_range":"90","filter.0.filter":"target_group","filter.0.quality":"eq","filter.0.value":str(tg_value),"filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"Medium","filter.search_type":"and","all_fields":"full"}
	   querystringL = {"date_range":"90","filter.0.filter":"target_group","filter.0.quality":"eq","filter.0.value":str(tg_value),"filter.1.filter":"severity","filter.1.quality":"eq","filter.1.value":"Low","filter.search_type":"and","all_fields":"full"}
	   vuln_countC=get_vulns(querystringC,headers)
	   time.sleep(0.500)
	   vuln_countH=get_vulns(querystringH,headers)
	   time.sleep(0.500)
	   vuln_countM=get_vulns(querystringM,headers)
	   time.sleep(0.500)
	   vuln_countL=get_vulns(querystringL,headers)
	   time.sleep(0.500)
	   asset_count=get_assets(tg_value,headers)
	   row=[tg_name,tg_value,vuln_countC,vuln_countH,vuln_countM,vuln_countL,asset_count]
	   print(tg_name, tg_value, vuln_countC, vuln_countH, vuln_countM, vuln_countL,asset_count)
	   table_data.append(row)
	   f2=open(results_dir+fname,"a+")
	   myTimeString2=datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d')
	   f2.write(myTimeString2+","+str(vuln_countC)+","+str(vuln_countH)+","+str(vuln_countM)+","+str(vuln_countL)+","+str(x['name'])+"\n")
	   f2.close()
	f.close()
	f=open(results_dir+"tgs_vuln_summary.csv","w+")
	fcsv=csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for row in table_data:
		if row[1]!=2746: #exclude corrupt record
			print(row)
			fcsv.writerow(row)
	f.close()
