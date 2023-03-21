
class fatSecret:
    def __init__(self):
        self.url = "https://www.fatsecret.com.tr/kaloriler-beslenme/search?q=Yo%c4%9furt"
        self.domain = 'https://www.fatsecret.com.tr'
    def get_html(self, url):
        import requests
        from bs4 import BeautifulSoup
        html = requests.get(url).text
        return BeautifulSoup(html, 'html.parser')   
    def get_data(self):
        import pandas as pd
        products = {}
        while True:
            soup = self.get_html(self.url)
            try:
                next_page_link = soup.find('span', {"class":"next"}).contents[0]["href"]
            except:
                break
            for link in soup.find_all('a', attrs={"class": 'prominent'}):
                complete_link = self.domain + link['href']
                _soup = self.get_html(complete_link)
                name = _soup.find('h1', attrs={'style': 'text-transform:none'}).get_text()
                manif = _soup.find('h2', attrs={'class': 'manufacturer'})
                if manif is None:
                    _name = f'{name}'
                else:
                    _name = f'{manif.get_text()} {name}'
                products[_name] = {}
                info = _soup.find_all('table', attrs={"class": 'spaced'})[0]
                titles = [i.get_text() for i in info.find_all('div', attrs={"class": 'factTitle'})]
                values = [i.get_text() for i in info.find_all('div', attrs={"class": 'factValue'})]
                for index in range(len(titles)):
                    products[_name][titles[index]] = values[index]
                self.url = self.domain + next_page_link
            print("done")
            df = pd.DataFrame.from_dict(products).transpose()
            df.to_csv('products.csv')
ft = fatSecret()
ft.get_data()
 
        
    
    



    
