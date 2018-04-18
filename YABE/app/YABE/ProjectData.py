from xml.dom import minidom
from YABE.YABE_settings import PROJECT_INFO_PATH
from datetime import datetime
from operator import itemgetter


#Extract project data from "projects.xml" and sort in desending order
__xmldoc_project=minidom.parse(PROJECT_INFO_PATH)
__raw_projectList=__xmldoc_project.getElementsByTagName("project")
projectList=[]
for project in __raw_projectList:
    newProject={}
    newProject['year']=project.attributes['year'].value
    if len(project.attributes['month'].value)<2:
        newProject['month']='0' + project.attributes['month'].value
    else:
        newProject['month']=project.attributes['month'].value
    newProject['title']=project.attributes['title'].value
    newProject['content']=project.attributes['content'].value
    if len(newProject["content"])<200:
        for num in range(0,200-len(newProject["content"])):
            newProject["content"]+=" "
    newProject['source_link']=project.attributes['source_link'].value
    newProject['detail_link']=project.attributes['detail_link'].value
    newProject['category']=project.attributes['category'].value
    projectList.append(newProject)

#sort projectList in time desending order (start at most recent one)
projectList=sorted(projectList,key=itemgetter('year','month'),reverse=True)



#methods about getting projects   
def getAllProjects():
    return projectList

def getProjectsByAttr(key,value):
    newList=[]
    for project in projectList:
        if project[key]==value:
            newList.append(project)
    return newList

def getRecentThreeProjects():
    if len(projectList) <= 3:
        return projectList
    newList=[]
    newList.append(projectList[0])
    newList.append(projectList[1])
    newList.append(projectList[2])
    return newList

#method to get value list for a certain tag
def getValueListByAttr(key):
    newList=[]
    curr=""
    for project in projectList:
        isAdded=False
        if project[key]!=curr:
            for item in newList:
                if item==project[key]:
                    isAdded=True
                    break
            if not isAdded:
                curr=project[key]
                newList.append(curr)
    return newList