from jira import JIRA
import configparser
from pathlib import Path
import issues

config = configparser.ConfigParser()
config.sections()
config.read('settings.ini')


root = Path(config['destination']['directory'])
root.mkdir(parents=True, exist_ok=True)


url = 'https://elmtreeclinic.atlassian.net/'
basic_auth=(config['jira']['username'],config['jira']['token'])

jira = JIRA( url,basic_auth=basic_auth)
openIssues = issues.searchIssues(jira)

summary = open(root.joinpath("contents.md"), mode='w', encoding='utf-8')
summary.write("# Contents\n\n")


for issue in openIssues:
    print(issue.key)
    summary.write(f"[[{issue.key}]] {issue.fields.summary}\n")
    destination = root.joinpath("open", issue.key)
    destination.mkdir(parents=True, exist_ok=True)
    issues.downloadIssue(jira, issue.key, destination)
    
    


