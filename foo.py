from pathlib import Path

report_path = (Path.cwd()/'resource'/'report'/'draft.txt').as_posix()
def write_report(): 
    content = {}
    with open(report_path, 'r') as f:
        lines = f.readlines()
        current_title: str

        for line in lines:
            if line.startswith('#'):
                current_title = line 
                content[current_title] = '' 
            else:
                content[current_title] += line
    
    print(content['#Numeric Stats:\n'])

write_report()
