# GPyFlow
GPyFlow is simple and easy engine to run local workflow.

# Install
```angular2html
python3 setup.py install
```

# Use Web Editor to Define a Workflow
[GPyFlow Visual WebSite](http://niulab.scgrid.cn/GPyFlow/). 
# Usage
- ## extract macros
```
pyflow extract -f flow.json -o input.macros
```
- ## run workflow
```angular2
pyflow run -i input.macros -o output_dir flow.json
# or
pyflow run -i input.macros -o output_dir workflow.zip
```
- ## tar workflow directory to share
```angular2html
pyflow tar workflow_dir
```
- ## more 
preview commamd lines before run a workflow
```angular2
pyflow run --preview true -i input.macros -o output_dir flow.json
```