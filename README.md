# GPyFlow
GPyFlow is simple and easy to run local workflow.

# Install
```angular2html
python3 setup.py install
```

# Use Web Interface to Define a workflow
[GPyFlow Visual WebSite](http://niulab.scgrid.cn/GPyFlow/). 
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
