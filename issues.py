from pathlib import Path
from jira import JIRA
from jira2markdown import convert
import image


def searchIssues(jira:JIRA):
    fields=['key', 'summary']
    jql = 'project=KC AND resolution = Unresolved ORDER BY priority DESC, updated DESC'
    issues_in_proj = jira.search_issues(jql_str=jql, maxResults=0, fields=fields )
    print(len(issues_in_proj))
    return issues_in_proj
    # for issue in issues_in_proj:
    #     print(issue.key, issue.fields.summary)





def downloadIssue(jira, key:str, destination:Path):
    fields=['key','summary','description','comment','attachment']
    issue = jira.issue(key, fields=fields)
    filename = issue.key+'.md'
    with open(destination.joinpath(filename), 'w',encoding='utf-8') as markdown:
        markdown.write(f"# {issue.key} {issue.fields.summary}\n")
        markdown.write("## Description\n")
        if issue.fields.description:
            markdown.write(image.removeSpaces(convert(issue.fields.description)))
        markdown.write("\n\n## Comments\n")
        for comment in issue.fields.comment.comments:
            # print(dir(comment))
            markdown.write(f"### {comment.created[:10]}\n")
            markdown.write(image.removeSpaces(convert(comment.body)))
            markdown.write(f"\n\n")



        for attachment in issue.fields.attachment:
            attachmentFilename = image.removeSpaces(attachment.filename)
            with open(destination.joinpath(attachmentFilename), 'wb') as f:
                    f.write(attachment.get())




    ###########################################################

    # all_proj_issues_but_mine = jira.search_issues('project=PROJ and assignee != currentUser()')

    # # my top 5 issues due by the end of the week, ordered by priority
    # oh_crap = jira.search_issues('assignee = currentUser() and due < endOfWeek() order by priority desc', maxResults=5)

    # # Summaries of my last 3 reported issues
    # for issue in jira.search_issues('reporter = currentUser() order by created desc', maxResults=3):
    #     print('{}: {}'.format(issue.key, issue.fields.summary))

if __name__ == '__main__':
    for key in ['KC-584','KC-582']:
        downloadIssue(key)
