# tenable-tg-tag-report
```
*** This tool is not an officially supported Tenable project ***

Uses the public APIs for tenable.io to generate licensed asset count and vuln counts grouped by target groups
and tags. Useful to understand the breakdown of licensing and vulns across groups

run with

python3 master.py
python3 gen_html_master.py

Keys should be placed in a file called keys.json. Format of file is
{"tio_AK":"your access key","tio_SK":"your secret key"}

Directory location for the keys file is controlled by the variable keys_dir

html reports will be written to the directory reports_dir

```
