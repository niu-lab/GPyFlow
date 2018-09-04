# GPyFLow
GPyFLow is simple and easy to run local workflow.

# Install
```angular2html
python3 setup.py install
```

# Use JSON to define a workflow
```angular2html
{
  "macros": {
    "INFILE": "",
    "CHAR": "",
    "OUTPREFIX": ""
  },
  "workflow": {
    "grep-step": {
      "pres": [
      ],
      "input": [
        "#INFILE#"
      ],
      "output": [
        "#OUTPREFIX#.grep.out"
      ],
      "command": {
        "path": "grep",
        "parameters": [
          {
            "prefix": "",
            "key": "",
            "sep": "",
            "value": "#CHAR#"
          },
          {
            "prefix": "",
            "key": "",
            "sep": "",
            "value": "#IN[0]#"
          },
          {
            "prefix": "",
            "key": ">",
            "sep": " ",
            "value": "#OUT[0]#"
          }
        ]
      }
    },
    "count-step": {
      "pres": [
        "grep-step"
      ],
      "input": [
        "#OUTPREFIX#.grep.out"
      ],
      "output": [
        "#OUTPREFIX#.count.out"
      ],
      "command": {
        "path": "wc",
        "parameters": [
          {
            "prefix": "-",
            "key": "l",
            "sep": " ",
            "value": "#IN[0]#"
          },
          {
            "prefix": "",
            "key": ">",
            "sep": " ",
            "value": "#OUT[0]#"
          }
        ]
      }
    }
  }
}
```
run command line like these:
```angular2html
grep #CHAR# #INFILE# > #OUTPREFIX#.grep.out
wc -l #OUTPREFIX#.grep.out > #OUTPREFIX#.count.out
```

- use `#MACRO#` to reference `macro`
- use `IN[i]` to reference the `ith` item in `input`
- use `OUT[i]` to reference the `ith` item in `output`

# Workflow Directory
```angular2html
workflow
  - input/
  - flow.json
```
- `flow.json` is the workflow definition。
- `input` is the workflow input include init input files or script.

# Command

1. tar workflow directory to zip file
```angular2html
flowc tar [dir]
```

2. run workflow
```angular2html
flowc run workflow.zip
```

# Example
`test/test-workflow`
```angular2html
flowc tar test/test-workflow
flowc run -i test/inputs.txt -o test/test_workflow test/test-workflow.zip
```
