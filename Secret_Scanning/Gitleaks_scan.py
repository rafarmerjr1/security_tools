#Script to iterate over repos in various organizational projects for secrets.
# Requires the python verstion of gitleaks, installed locally.

import os
from github import Github
import sys

global api_token
api_token = 'API Token goes here'

# Function that scans for secrets of given repos
def scan_repos(repo_txt_list):
    f = open(repo_txt_list, "r")
    for i in f:
        i = i.rstrip()
        try:
            # before running, modify or remove depth flag as needed
            gitleaks = "gitleaks -f=csv --depth 5 --repo-url=https://URL_HERE/%s.git -v --access-token=%s > %s.csv" % (i, api_token,i)
            results = os.system(gitleaks)
            print(results)
        except:
            print("Error on %s" %i)

# Generates a list of all repositories matching search criteria of URL/Project_Name
# where the team name is present in the name of the repository.
def getOrgRepos(project_name, team_name):
    global repostore
    repostore = []
    g = Github(api_token, base_url='https://URL_HERE/') # include API path in URL as needed
    for i in g.get_user().get_repos():
        if project_name in i.full_name:
            if team_name in i.name:
                repostore.append(i.name)
    return repostore

# Generates a text file of repos based on the team name provided, useful to keep
# the text file for auditing and future reference.
def modular_write_to_repolist(repostore, team_name):
    global filename
    file_name = "%s.txt" % team_name
    f = open(file_name, "w")
    for i in repostore:
        if team_name in i:
            f.write(i + "\n")
            print("Prepare to scan: %s" % i)
    return filename

# main
def runnit():
    if len(sys.argv) != 3:
        print("\n*** Requirements:  Team_Name Project_Name***\n")
        print("Usage: %s TEAMNAME ORGNAME" % sys.argv[0])
        print("Example: %s team1 project1 " % sys.argv[0])
    team_name = sys.argv[1]
    project_name = sys.argv[2]

    getOrgRepos(project_name, team_name)
    if team_name:
        scan_repos(modular_write_to_repolist(repostore, team_name))

runnit()
