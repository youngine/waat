class DataContent:
    def __init__(self,):
        self.title =""
        self.category  =[]
        self.language =""
        self.target_person =""
        self.eq_grade_price = {"A":0, "B":0, "C" :0 }
        self.imagepath = ""

        self.introudce = ""
        self.backgroudContents = ""
        self.PRobject = ""

        self.developContens = ""
        self.excutePlan = ""

    def set_1Page(self,title,category):
        self.title = title
        self.category.append(category)
    