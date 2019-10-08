import requests
import bs4

class Mailnesia:
    def __init__(self, mailnesiaId):
        self.mailnesiaId = mailnesiaId
        self.mailLinks = []

    def getMailLinks(self):
        url = "http://mailnesia.com/mailbox/{}".format(self.mailnesiaId)

        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all("a", "email")
        return list(map(lambda x: x['href'], links))[::4]

    def getBirdCode(self, mailLink):
        r = requests.get("http://mailnesia.com{}".format(mailLink))
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all("a")
        magic_link = list(filter(lambda x: x['href'].find('magic_link') != -1, links))[0]
        
        return magic_link['href'].split('/')[-1]

if __name__ == '__main__':
    m = Mailnesia("this.is.a.test")
    links = m.getMailLinks()
    print(m.getBirdCode(links[0]))
