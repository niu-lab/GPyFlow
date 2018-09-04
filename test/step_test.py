from flow.step import Step
import json

test_string = '''
{
  "pres": null,
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
}
'''

if __name__ == "__main__":
    test_dict = json.loads(test_string)
    test_step = Step("test_workflow", "test_step")
    test_step.load_from_dict(test_dict)
    assert (test_step.__generate() == "grep #CHAR# #INFILE# > #OUTPREFIX#.grep.out")
