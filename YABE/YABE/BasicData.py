from YABE.YABE_settings import BASIC_INFO_PATH
from xml.dom import minidom


#Extract Data from "basic.xml"
__xmldoc_basic=minidom.parse(BASIC_INFO_PATH)
  
__item=__xmldoc_basic.getElementsByTagName("host")

HOST={}
HOST["name"]=__item[0].attributes["name"].value
HOST["email"]=__item[0].attributes["email"].value
HOST["github"]=__item[0].attributes["github"].value
HOST["linkedin"]=__item[0].attributes["linkedin"].value
HOST["bio"]=__item[0].attributes["bio"].value
HOST["photoPath"]=__item[0].attributes["photopath"].value
HOST["blog"]=__item[0].attributes["blog"].value



