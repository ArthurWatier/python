import random
import unicodecsv as csv
import urllib
import bs4
import requests
import time


start_url = 'https://syntec-numerique.fr'
annuaire = '/annuaire-des-adherents?'
file = 'donnees.csv'
i = 1
k = 149


def make_soup(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html5lib")
    return soup


def get_links(url):
    soup = make_soup(url)
    block_societe = soup.find_all("div", {"class": "cadre"})
    links = []

    for div in block_societe:
        a_tags = div.find('a')['href']
        link = start_url + a_tags
        print(link)
        links.append(link)
    return links


def get_nom_societe(link):
    soup = make_soup(link)
    nom_societe = soup.find('h1')
    if nom_societe is not None:
        return nom_societe.text
    else:
        return ''


def get_mail(link):
    soup = make_soup(link)
    mail = soup.find('div',  class_="field-name-field-couriel")
    if mail is not None:
        return mail.text
    else:
        return ''


def get_telephone(link):
    soup = make_soup(link)
    numero = soup.find('div', class_="field-name-field-telephone-std")
    if numero is not None:
        return numero.text
    else:
        return ''


def add_in_csv(infos):
    with open(file, 'ab') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(infos)


if __name__ == '__main__':
    start = time.time()
    url_societes = []
    while i < k:
        var = {
            'page': str(i)
        }
        url = start_url + annuaire + urllib.urlencode(var)
        url_societes = url_societes + get_links(url)
        i += 1
    for url in url_societes:
        infos = [get_nom_societe(url), get_mail(url), get_telephone(url)]
        print([get_nom_societe(url), get_mail(url), get_telephone(url)])
        add_in_csv(infos)
        time.sleep(random.uniform(0.0, 6.9))
    end = time.time()
    print(end - start)
