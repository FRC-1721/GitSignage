from github import Github

g = Github("Ah ah ah, you diden't say the magic word!")


repo = g.get_repo("FRC-1721/1721-RapidReact")
open_issues = repo.get_issues(state="open")
for issue in open_issues:
    print(issue)

open_milestones = repo.get_milestones(state="open")
for milestone in open_milestones:
    print(milestone)
    print(milestone.due_on)
