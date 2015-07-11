#!/usr/bin/python3

if __name__ == "__main__":
  import sys, json
  from Websheet import Websheet
  student = sys.argv[2]
  ispreview = sys.argv[3]=='True'
  try:
    websheet = Websheet.from_name(sys.argv[1], ispreview, student)
    if websheet == None:
      print("Could not find " + sys.argv[1])
      sys.exit(1)
    dbslug = websheet.dbslug
    
    import config, json
    
    if not config.db_enabled: student="anonymous"
    #  websheet = Websheet.from_filesystem(classname)
    data = {"template_code":websheet.get_json_template(),
            "description":websheet.description,
            "user_code": config.load_submission(student, dbslug),
            "ever_passed": config.ever_passed(student, dbslug),
            "num_submissions": config.num_submissions(student, dbslug),
            "initial_snippets": websheet.get_initial_snippets(),            
            "lang": websheet.lang,
            "sharing": websheet.sharing,
            "attempts_until_ref": websheet.attempts_until_ref,
            "authinfo": json.loads("".join(sys.stdin))
          }
    if websheet.nocode:
      data["nocode"] = websheet.get_nocode_question()
    else:
      data["nocode"] = False
    if (ispreview or 
        data["ever_passed"] and websheet.attempts_until_ref != "never"
        or (websheet.attempts_until_ref not in ["never", "infinity"] and
            data["num_submissions"] >= websheet.attempts_until_ref)) :
      data["reference_sol"] = websheet.get_reference_snippets()
    print(json.dumps(data, indent=4, separators=(',', ': '))) # pretty!
  except FileNotFoundError:
    print("No exercise named " + sys.argv[1])
