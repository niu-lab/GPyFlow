# GPyFlow
GPyFlow is simple and easy to run local workflow.

# Install
```angular2html
python3 setup.py install
```

# Use Web Interface to Define a workflow
[GPyFlow Visual WebSite](http://101.200.50.190/GPyFlow/). 
# Commands
tar workflow directory to zip file
```angular2html
pyflow tar [dir]
```
run workflow
```angular2html
pyflow run -i inputs.txt -o output_dir flow.json
pyflow run -i inputs.txt -o output_dir workflow.zip
```
