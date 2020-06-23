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

f.write('<div class=page_heading>\n')
f.write('<h1>Target Group and Tag Report</h1>')
f.write('<table width=100%></table></div>')


#
# Company Summary
#
reader=csv.reader(open(results_dir+"company_summary.csv"),delimiter=",")
f.write('<div class=bar_chart_fl>\n')
f.write("<h1>Vulnerability Summary</h1>\n")
f.write("<table width=900px>\n")
f.write("<tr><td align=left>\n")
f.write('Current vulnerability count grouped by severity. Asset and vulnerability calculations are based on the "Last 90 Days" view from the date shown.\n')
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")

f.write('<br>')


f.write("<table class=table1 width=600px>\n")
f.write("<tr><td align=left>Licensed Asset Count</td><td>Critical</td><td>High</td><td>Medium</td><td>Low</td>\n")
for row in reader:
	f.write("<tr>\n")
	f.write("<td align=left>"+'{:,}'.format(int(row[1]))+"</td>\n")
	f.write("<td class=critical width=80px>"+'{:,}'.format(int(row[2]))+"</td>\n")
	f.write("<td class=high width=80px>"+'{:,}'.format(int(row[3]))+"</td>\n")
	f.write("<td class=medium width=80px>"+'{:,}'.format(int(row[4]))+"</td>\n")
	f.write("<td class=low width=80px>"+'{:,}'.format(int(row[5]))+"</td>\n")
	mydate=row[0]
f.write("<tr><td colspan=5 align=right>Last updated - "+mydate+"</td>\n")
f.write("</table>\n")

f.write("</div>")

#
# Target Group Report
#
reader=csv.reader(open(results_dir+"tgs_vuln_summary.csv"),delimiter=",")
sortedlist = sorted(reader, key=lambda row: int(row[6]), reverse=True)
f.write('<div class=bar_chart_fl>\n')
f.write("<h1>Target Group Report</h1>\n")
f.write("<table class=table1 width=900px>\n")
f.write("<tr><td align=left>Target Group</td><td align=center>Asset Count</td><td align=center>Critical</td><td align=center>High</td><td align=center>Medium</td><td align=center>Low</td>\n")
for row in sortedlist:
	f.write("<tr>\n")
	f.write("<td align=left>"+row[0]+"</td>\n")
	f.write("<td align=center width=100px>"+'{:,}'.format(int(row[6]))+"</td>\n")
	f.write("<td class=critical width=80px>"+'{:,}'.format(int(row[2]))+"</td>\n")
	f.write("<td class=high width=80px>"+'{:,}'.format(int(row[3]))+"</td>\n")
	f.write("<td class=medium width=80px>"+'{:,}'.format(int(row[4]))+"</td>\n")
	f.write("<td class=low width=80px>"+'{:,}'.format(int(row[5]))+"</td>\n")
f.write("</table>\n")
f.write('</div>')

#
# Tags Report
#
reader=csv.reader(open(results_dir+"tags_vuln_summary.csv"),delimiter=",")
sortedlist = sorted(reader, key=lambda row: int(row[6]), reverse=True)
f.write('<div class=bar_chart_fl>\n')
f.write("<h1>TAG Report</h1>\n")
f.write("<table class=table1 width=900px>\n")
f.write("<tr><td align=left>Tag</td><td align=center>Asset Count</td><td align=center>Critical</td><td>High</td><td align=center>Medium</td><td align=center>Low</td>\n")
for row in sortedlist:
	f.write("<tr>\n")
	f.write("<td align=left>"+row[0]+"</td>\n")
	f.write("<td align=center width=100px>"+'{:,}'.format(int(row[6]))+"</td>\n")
	f.write("<td class=critical width=80px>"+'{:,}'.format(int(row[2]))+"</td>\n")
	f.write("<td class=high width=80px>"+'{:,}'.format(int(row[3]))+"</td>\n")
	f.write("<td class=medium width=80px>"+'{:,}'.format(int(row[4]))+"</td>\n")
	f.write("<td class=low width=80px>"+'{:,}'.format(int(row[5]))+"</td>\n")
f.write("</table>\n")
f.write('</div>')

#f.write('</div>')

f.write('</html>')


f.close()
