import requests
import json
import sys
import time
import csv
import os
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


def bar_chart(labels,data,chart_id,ctx):
	chart_string='<script>var '+ctx+' = document.getElementById("'+chart_id+'").getContext("2d");var '+chart_id+' = new Chart('+ctx+', {\n'\
	' \n'\
	'    type: "bar",\n'\
	' \n'\
	'    // The data for our dataset\n'\
	'    data: {\n'\
	'        labels: '+labels+',\n'\
	'        datasets: [{\n'\
	'            label: "Asset Count",\n'\
	'            backgroundColor: "rgb(0,131,155,0.8)",\n'\
	'            borderColor: "rgb(0,0,0)",\n'\
	'            borderWidth: "1",\n'\
	'            data: '+data+'        }]\n'\
	'    },\n'\
	'    options: {\n'\
	'        scales: {\n'\
	'            yAxes: [{\n'\
	'                ticks: {\n'\
	'                    beginAtZero: true\n'\
	'                }\n'\
	'            }]\n'\
	'        }\n'\
	'    }\n'\
	'});\n'\
	'</script>\n'
	return chart_string

def line_chart2(labels,data,chart_id,ctx):
	chart_string='<script>var '+ctx+' = document.getElementById("'+chart_id+'").getContext("2d");var '+chart_id+' = new Chart('+ctx+', {\n'\
	' \n'\
	'    type: "line",\n'\
	' \n'\
	'    // The data for our dataset\n'\
	'    data: {\n'\
	'        labels: '+labels+',\n'\
	'        datasets: [{\n'\
	'            label: "Asset Count",\n'\
	'            backgroundColor: "rgb(0,131,155,0.4)",\n'\
	'            borderColor: "rgb(0,0,0)",\n'\
	'            borderWidth: "1",\n'\
	'            data: '+data+'        }]\n'\
	'    },\n'\
	'    options: {\n'\
	'        scales: {\n'\
	'            yAxes: [{\n'\
	'                ticks: {\n'\
	'                    beginAtZero: true\n'\
	'                }\n'\
	'            }]\n'\
	'        }\n'\
	'    }\n'\
	'});\n'\
	'</script>\n'
	return chart_string



def line_chart(labels,dataC,dataH,dataM,dataL,chart_id,ctx):
	chart_string='<script>var '+ctx+' = document.getElementById("'+chart_id+'").getContext("2d");var '+chart_id+' = new Chart('+ctx+', {\n'\
	'type: "line",\n'\
	' \n'\
	'    // The data for our dataset\n'\
	'    data: {\n'\
	'        labels: '+labels+',\n'\
	'        datasets: [{\n'\
	'            label: "Low",\n'\
	'	    backgroundColor: "rgba(0, 128, 0, 0.9)",\n'\
	'	    borderColor: "rgba(0, 128, 0)",\n'\
	'            borderWidth: "1",\n'\
	'            data: '+dataL+'	},{\n'\
	'            label: "Medium",\n'\
	'	    backgroundColor: "rgba(255, 215, 0, 0.9)",\n'\
	'	    borderColor: "rgba(255, 215, 0)",\n'\
	'            borderWidth: "1",\n'\
	'            data: '+dataM+'	},{\n'\
	'            label: "High",\n'\
	'	    backgroundColor: "rgba(255, 165, 0, 0.9)",\n'\
	'	    borderColor: "rgba(255, 165, 0)",\n'\
	'            borderWidth: "1",\n'\
	'            data: '+dataH+'	},{\n'\
	'            label: "Critical",\n'\
	'	    backgroundColor: "rgba(255, 0, 0, 0.9)",\n'\
	'	    borderColor: "rgba(255, 0, 0)",\n'\
	'            borderWidth: "1",\n'\
	'            data: '+dataC+'        }]\n'\
	'    },\n'\
	'    options: {\n'\
	'        scales: {\n'\
	'            yAxes: [{\n'\
	'		stacked: true,\n'\
	'                ticks: {\n'\
	'                    beginAtZero: true\n'\
	'                }\n'\
	'            }]\n'\
	'        }\n'\
	'    }\n'\
	'});\n'\
	'</script>\n'
	return chart_string



#
# Main
#
keys_dir="../"
results_dir="../results/"
reports_dir="../reports/"

keys=read_keys()
tio_AK=keys["tio_AK"]
tio_SK=keys["tio_SK"]

results_dir="../results/"

api_keys="accessKey="+tio_AK+";secretKey="+tio_SK

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'X-APIKeys': api_keys
    }


f=open(reports_dir+"status_report.html","w+")

html_header='<html>\n'\
		'<head>\n'\
		'<title>Tenable Status Report</title>\n'\
		'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n'\
		'<meta http-equiv="Pragma" content="no-cache" /><meta http-equiv="Expires" content="0" />\n'

f.write(html_header)
f2=open("style.css","r")
for line in f2:
	f.write(line)
f2.close()

f.write('<script>\n')

f2=open("Chart.min.js","r")
for line in f2:
	f.write(line)
f2.close()


f.write('</script>\n')


f.write('</head>\n<body>\n')

f.write('<div class=article_no_page>\n')


f.write("<h1>Tenable Status Report</h1>\n")

myhtml='<table class=table2 width=800px>\n'\
	'<td width=150px><a href="#tgs">Target Group Report</a></td>\n'\
	'<td>Shows the licensed asset count and vulnerability severity per target group. Organised in reverse order of asset count (90 day view)</td>\n'\
	'<tr><td><a href="#scans">Scan Job Report</a></td>\n'\
	'<td>Shows all the scheduled scan jobs, how many hosts were discovered and the last time the scan was run. Organised in reverse order of host count.</td>\n'\
	'</table>\n'
# f.write(myhtml)

#
# Company Summary
#
reader=csv.reader(open(results_dir+"company_summary.csv"),delimiter=",")
f.write("<div class=border1 id=company>\n")
f.write("<h1>Current Vulnerabilities</h1>\n")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left>\n")
f.write('Current vulnerability count grouped by severity. Asset and vulnerability calculations are based on the "Last 90 Days" view from the date shown.\n')
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")

f.write("<table class=table_vs width=95%>\n")
f.write("<tr><td align=left><b>Licensed Asset Count</b></td><td><b>Critical</b></td><td><b>High</b></td><td><b>Medium</b></td><td><b>Low</b></td>\n")
for row in reader:
	f.write("<tr>\n")
	f.write("<td align=left width=50%>"+'{:,}'.format(int(row[1]))+"</td>\n")
	f.write("<td class=critical>"+'{:,}'.format(int(row[2]))+"</td>\n")
	f.write("<td class=high>"+'{:,}'.format(int(row[3]))+"</td>\n")
	f.write("<td class=medium>"+'{:,}'.format(int(row[4]))+"</td>\n")
	f.write("<td class=low>"+'{:,}'.format(int(row[5]))+"</td>\n")
	mydate=row[0]
f.write("<tr><td colspan=5 align=right>Last updated - "+mydate+"</td>\n")
f.write("</table>\n")

f.write("</div>")

#
# Target Group Report
#
reader=csv.reader(open(results_dir+"tgs_vuln_summary.csv"),delimiter=",")
sortedlist = sorted(reader, key=lambda row: int(row[6]), reverse=True)
f.write("<div class=border1 id=tgs>\n")
f.write("<h1>Target Group Report</h1>\n")
f.write("<table class=table_vs width=95%>\n")
f.write("<tr><td align=left>Target Group</td><td>Asset Count</td><td>Critical</td><td>High</td><td>Medium</td><td>Low</td>\n")
for row in sortedlist:
	f.write("<tr>\n")
	f.write("<td align=left width=40%>"+row[0]+"</td>\n")
	f.write("<td width=8%>"+'{:,}'.format(int(row[6]))+"</td>\n")
	f.write("<td class=critical>"+'{:,}'.format(int(row[2]))+"</td>\n")
	f.write("<td class=high>"+'{:,}'.format(int(row[3]))+"</td>\n")
	f.write("<td class=medium>"+'{:,}'.format(int(row[4]))+"</td>\n")
	f.write("<td class=low>"+'{:,}'.format(int(row[5]))+"</td>\n")
f.write("</table>\n")
f.write('</div>')


f.write('</div>')

f.write('</div></html>')


f.close()
