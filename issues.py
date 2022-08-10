from pathlib import Path
from jira import JIRA
from jira2markdown import convert
import util


def searchIssues(jira:JIRA):
    fields=['key', 'summary']
    # jql = 'project=KC AND resolution = Unresolved ORDER BY priority DESC, updated DESC'
    jql = 'project=KC AND key=KC-108'
    issues_in_proj = jira.search_issues(jql_str=jql, maxResults=0, fields=fields )
    print(len(issues_in_proj))
    return issues_in_proj
    # for issue in issues_in_proj:
    #     print(issue.key, issue.fields.summary)





def downloadIssue(jira, key:str, destination:Path):
    fields=['key','summary','description','comment','attachment','created', 'status']
    issue = jira.issue(key, fields=fields)
    filename = issue.key+'.md'
    with open(destination.joinpath(filename), 'w',encoding='utf-8') as markdownFile:
        # YAML front matter
        markdownFile.write(f"---\n")
        markdownFile.write(f"id: {issue.key}\n")  # We're calling it an "id"
        markdownFile.write(f"status: #{issue.fields.status}\n")
        markdownFile.write(f"created: {issue.fields.created[:10]}\n")
        markdownFile.write(f"---\n")


        markdownFile.write(f"# {issue.fields.summary}\n")
        # markdown.write("# Description\n")  # Leave out this heading, it's redundant
        if issue.fields.description:
            markdownFile.write(util.removeMarkdownURLSpaces(convert(issue.fields.description)))
        

        if len(issue.fields.attachment):
            markdownFile.write("\n\n## Attachments\n")

        for attachment in issue.fields.attachment:
            attachmentFilename = attachment.filename.replace(" ","")
            markdownFile.write(f"- [{attachmentFilename}]({attachmentFilename})\n")
            with open(destination.joinpath(attachmentFilename), 'wb') as f:
                    f.write(attachment.get())

        markdownFile.write("\n\n# Comments\n")
        for comment in issue.fields.comment.comments:
            # print(dir(comment))
            markdownFile.write(f"## {comment.created[:10]}\n")

            # Comments are in Jira wiki format, need to be converted and the headings need demoting 
            comment = convert(comment.body)
            comment = util.removeMarkdownURLSpaces(comment)
            comment = util.demoteHeadings(comment)
            markdownFile.write(comment)
            markdownFile.write(f"\n\n")







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
