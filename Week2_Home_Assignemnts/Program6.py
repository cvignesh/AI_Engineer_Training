from datetime import date 

class book:
    def __init__(self,title,author,publication_year):
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def get_age(self):
        current_year = date.today().year
        return current_year - int(self.publication_year)
    
book1 = book("Book1","Bob","2010")
print(book1.get_age())