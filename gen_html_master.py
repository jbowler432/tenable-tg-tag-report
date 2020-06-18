import requests
import json
import sys
import time
import csv
from datetime import datetime


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

if len(sys.argv)!=2:
        print "Need to supply key name where key name is one of the names in keys.csv"
        exit(0)

key_lst=get_keys(sys.argv[1])

tio_AK=key_lst[0]
tio_SK=key_lst[1]
res_dir=key_lst[2]

api_keys="accessKey="+tio_AK+";secretKey="+tio_SK

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'X-APIKeys': api_keys
    }


input_dir="./"
output_dir=res_dir+"/"
results_dir=res_dir+"/"

f=open(output_dir+"status_report.html","w+")

html_header='<html>\n'\
		'<head>\n'\
		'<title>Tenable Status Report</title>\n'\
		'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n'\
		'<meta http-equiv="Pragma" content="no-cache" /><meta http-equiv="Expires" content="0" />\n'

f.write(html_header)
f2=open(input_dir+"style.css","r")
for line in f2:
	f.write(line)
f2.close()

f.write('<script>\n')

f2=open(input_dir+"Chart.min.js","r")
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
# Extract history data for trending graphs
#
'''
f.write("<div class=border1 id=company>\n")
f.write("<h1>Asset Count Trend Graph - License Overview</h1>\n")


reader=csv.reader(open(results_dir+"company_history.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
for row in lst:
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
		dataC="["+row[2]+","
		dataH="["+row[3]+","
		dataM="["+row[4]+","
		dataL="["+row[5]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
		dataC=dataC+row[2]+"]"
		dataH=dataH+row[3]+"]"
		dataM=dataM+row[4]+"]"
		dataL=dataL+row[5]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
		dataC=dataC+row[2]+","
		dataH=dataH+row[3]+","
		dataM=dataM+row[4]+","
		dataL=dataL+row[5]+","
	row_count=row_count+1

f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
f.write('Total licensed asset count calculated at the end of each day. Asset calculation based on "Last 90 Days" view from the date shown.\n')
f.write(' Licensed asset information can also be viewed from the "Health & Status" and the "Licensing" page of Tenable.io.')
f.write(' Licensed asset counts will always be different to the generic asset counts shown in Tenable.io vulnerability workbenches')
f.write(' as the latter will also show assets from discovery scans.')
f.write(' As scans jobs are running continuously, please note that the licensed asset counts shown below are accurate at the point in time ')
f.write('that the report was run. Please refer to the "Health and Status" page in Tenable.io for a live view of Licensed Assets.')
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart1" width=880 height=280></canvas></div>\n')
chart_string=line_chart2(labels,data,"chart1","ctx1")
f.write(chart_string)

f.write("</div>")


f.write("<div class=border1 id=company>\n")
f.write("<h1>Vulnerability Trend Graph</h1>\n")



f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
f.write('Vulnerability count grouped by severity calculated at the end of each day. Asset and vulnerability calculations are based on the "Last 90 Days" view from the date shown.\n')
f.write(' Aligns with the "Current Vulnerabilities" view shown on the Tenable.io classic interface using the "Last 90 Days" view filter.')
f.write(' Note that the "Vulnerability Trending" graph shown in the "New Interface" of Tenable.io is always based on the "All" filter and will show higher numbers')
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart2" width=880 height=280></canvas></div>\n')
chart_string=line_chart(labels,dataC,dataH,dataM,dataL,"chart2","ctx2")
f.write(chart_string)


f.write('</div>')
'''
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

'''
#
# Last Assessed Report - Seperate html file
#

f=open(output_dir+"last_assessed_report.html","w+")

html_header='<html>\n'\
		'<head>\n'\
		'<title>Last Assessed Report</title>\n'\
		'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n'\
		'<meta http-equiv="Pragma" content="no-cache" /><meta http-equiv="Expires" content="0" />\n'

f.write(html_header)
f2=open(input_dir+"style.css","r")
for line in f2:
	f.write(line)
f2.close()

f.write('<script>\n')

f2=open(input_dir+"Chart.min.js","r")
for line in f2:
	f.write(line)
f2.close()


f.write('</script>\n')


f.write('</head>\n<body>\n')

f.write('<div class=article_no_page>\n')

f.write("<h1>Last Assessed Licensing Report</h1>\n")




#
# Extract last assessed data
#
f.write("<div class=border1>\n")
reader=csv.reader(open(results_dir+"last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>All Sources</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed assets scanned during period = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart1" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart1","ctx1")
f.write(chart_string)
f.write("</div>")


#
# Extract last assessed data
# NNM only
#
f.write("<div class=border1>\n")
reader=csv.reader(open(results_dir+"pvs_exclusive_last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>NNM Exclusive</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed asset contribution detected exclusively by NNM = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart10" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart10","ctx10")
f.write(chart_string)
f.write("</div>")

#
# Extract last assessed data
# Nessus only
#
f.write("<div class=border1>\n")

reader=csv.reader(open(results_dir+"nessus_exclusive_last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>Nessus Only</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed asset contribution detected exclusively by Nessus = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart20" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart20","ctx20")
f.write(chart_string)
f.write("</div>")


#
# Extract last assessed data
# Agent only
#
f.write("<div class=border1>\n")

reader=csv.reader(open(results_dir+"agent_exclusive_last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>Agent Only</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed asset contribution detected exclusively by Agents = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart30" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart30","ctx30")
f.write(chart_string)
f.write("</div>")


#
# Extract last assessed data
# Agent and Nessus
#
f.write("<div class=border1>\n")

reader=csv.reader(open(results_dir+"agent_and_nessus_last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>Agent and Nessus</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed asset contribution detected with Nessus and Agent combined = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart40" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart40","ctx40")
f.write(chart_string)
f.write("</div>")

#
# Extract last assessed data
# Has NNM
#
f.write("<div class=border1>\n")

reader=csv.reader(open(results_dir+"has_pvs_last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>Has NNM</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed asset contribution detected where NNM is one of the sources = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart50" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart50","ctx50")
f.write(chart_string)
f.write("</div>")


#
# Extract last assessed data
# Has Nessus
#
f.write("<div class=border1>\n")

reader=csv.reader(open(results_dir+"has_nessus_last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>Has Nessus</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed asset contribution detected where Nessus is one of the sources = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart60" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart60","ctx60")
f.write(chart_string)
f.write("</div>")


#
# Extract last assessed data
# Has Agent
#
f.write("<div class=border1>\n")

reader=csv.reader(open(results_dir+"has_agent_last_assessed.csv"),delimiter=",")
row_count=0
lst=[]
for row in reader:
	lst.append(row)
	row_count=row_count+1

max_rows=row_count-1
first_row=0
row_count=0
total=0
for row in reversed(lst):
	if row_count==0:
		labels='["'+row[0]+'","'
		data="["+row[1]+","
	elif row_count==max_rows:
		labels=labels+row[0]+'"]'
		data=data+row[1]+"]"
	else:
		labels=labels+row[0]+'","'
		data=data+row[1]+","
	total=total+int(row[1])
	row_count=row_count+1

f.write("<h1>Has Agent</h1>")
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText="Total licensed asset contribution detected where Nessus is one of the sources = "+str(total)
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
f.write("<div class=bar_chart>\n")
f.write('<canvas id="chart70" width=880 height=280></canvas></div>\n')
chart_string=bar_chart(labels,data,"chart70","ctx70")
f.write(chart_string)
f.write("</div>")



f.write('</div>')

fscript=open("search_script.txt","r")
for x in fscript:
	f.write(x)

f.write('</html>')
'''

#
# Scan Report - Seperate html file
#

f=open(output_dir+"scan_report.html","w+")

html_header='<html>\n'\
		'<head>\n'\
		'<title>Tenable Scan Report</title>\n'\
		'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n'\
		'<meta http-equiv="Pragma" content="no-cache" /><meta http-equiv="Expires" content="0" />\n'

f.write(html_header)
f2=open(input_dir+"style.css","r")
for line in f2:
	f.write(line)
f2.close()

f.write('<script>\n')

f2=open(input_dir+"Chart.min.js","r")
for line in f2:
	f.write(line)
f2.close()


f.write('</script>\n')


f.write('</head>\n<body>\n')

f.write('<div class=article_no_page>\n')

f.write("<h1>Scan History Report</h1>\n")


#
# Scan Results
#

f.write("<div class=border1>\n")
f.write("<h1>Latest Scan Job Information</h1>")
'''
f.write("<table class=simple_table width=95%>\n")
f.write("<tr><td align=left width=70%>\n")
myText='Scheduled scan jobs will have many results sets, one for each scan job that has been run. This table '\
	'shows the most recent summary information for the last scan run by every scan job. '\
	'The information is ordered to show the most recently run scan jobs first to provide '\
	'clarity around what scans jobs are being running on a regular basis. It also shows the host count '\
	'so that you can see how many hosts the scan is seeing in each run. This provides a measure of how effective '\
	'the scan job is in targeting hosts.'
f.write(myText)
f.write("</td><td>&nbsp;</td>\n")
f.write("</table>\n")
'''

reader=csv.reader(open(results_dir+"tgs_scan_details.csv"),delimiter=",")
sortedlist = sorted(reader, key=lambda row: int(row[3]), reverse=True)
f.write("<table class=table1>\n")
f.write("<tr><td align=left>Scan Name</td><td>Owner</td><td>Host Count</td><td>Last Scan Date</td><td>Days Since Scan</td>\n")
for row in sortedlist:
	f.write("<tr>\n")
	f.write("<td align=left>"+row[1]+"</td>\n")
	f.write("<td>"+row[2]+"</td>\n")
	f.write("<td>"+row[3]+"</td>\n")
	f.write("<td>"+row[4]+"</td>\n")
	f.write("<td>"+row[5]+"</td>\n")
f.write("</table>\n")
f.write('</div>')

f.write('</div>')

f.write('</div></html>')


#
# Main - Reference html
#

f=open(output_dir+"status_report_ref.html","w+")


html_header='<html>\n'\
		'<head>\n'\
		'<title>Tenable Reference</title>\n'\
		'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n'\
		'<meta http-equiv="Pragma" content="no-cache" /><meta http-equiv="Expires" content="0" />\n'



f.write(html_header)
f2=open(input_dir+"style.css","r")
for line in f2:
	f.write(line)
f2.close()


f.write('</head>\n<body>\n')


f.write('<div class=article_no_page>\n')
f.write("<h1>Tenable Status Report - Reference</h1>\n")
myhtml='<table class=table2 width=800px>\n'\
	'<td width=200px><a href="#tgs">Target Group Definitions</a></td>\n'\
	'<td>Shows the IP ranges defined for each target group</td>\n'\
	'<tr><td><a href="#scans">Scan Job Targets</a></td>\n'\
	'<td>Shows the targets configured for each scheduled scan job</td>\n'\
	'</table>\n'
f.write(myhtml)

#
# Target Group Details Reference
#
reader=csv.reader(open(results_dir+"tgs_details.csv"),delimiter=",")
# sortedlist = sorted(reader, key=lambda row: int(row[6]), reverse=True)
f.write("<div class=border1 id=tgs>\n")
f.write("<h1>Target Group Definitions</h1>\n")
f.write('<p>\n')
f.write('<input type="text" id="tg_search" onkeyup="myFunction()" placeholder="Search.." title="Type in a name">')
f.write('</p>\n')
f.write("<table class=table1 width=100% id=tg_table>\n")
f.write("<tr><td>Target Group</td><td>Members</td>\n")
for row in reader:
        f.write("<tr>\n")
        f.write("<td align=left class=hideme>"+row[0]+" "+row[2]+"</td>\n")
        f.write("<td align=left width=400>"+row[0]+"</td>\n")
        f.write("<td>"+row[2]+"</td>\n")
f.write("</table>\n")
f.write('</div>')


#
# Scan Job Details Reference
#
reader=csv.reader(open(results_dir+"tgs_scan_details.csv"),delimiter=",")
# sortedlist = sorted(reader, key=lambda row: int(row[6]), reverse=True)
f.write("<div class=border1 id=scans>\n")
f.write("<h1>Scan Job Targets</h1>\n")
f.write('<p>\n')
f.write('<input type="text" id="scan_search" onkeyup="myFunction2()" placeholder="Search.." title="Type in a name">')
f.write('</p>\n')
f.write("<table class=table1 width=100% id=scan_table>\n")
f.write("<tr><td>Scan Job (owner)</td><td>Scan Targets</td>\n")
for row in reader:
        f.write("<tr>\n")
        f.write("<td align=left class=hideme>"+row[1]+" "+row[2]+" "+row[6].replace(',',' ')+"\n")
        f.write("<td align=left width=400>"+row[1]+"\n")
        f.write("<br>("+row[2]+")</td>\n")
        f.write("<td>"+row[6].replace(',',' ')+"</td>\n")
f.write("</table>\n")
f.write('</div>')


f.write('</div>')

f.write('</div>')

fscript=open("search_script.txt","r")
for x in fscript:
	f.write(x)

f.write('</html>')

