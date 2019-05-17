from bin.utils import get_page
from bs4 import BeautifulSoup
import csv
import os
import time


def crawl_one_urls(html):
    urls = []
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='s_position_list').find_all('li', 'con_list_item')
    for item in items:
        urls.append(item.find('a')['href'])
    return urls


def crawl_info(html):
    soup = BeautifulSoup(html, 'lxml')
    job = soup.find('div', class_='job-name')
    dl = soup.find('dl', class_='detail')

    # 公司，职位
    company = job.find('div', class_='company').text.replace('招聘', '')
    position = job.find('span', class_='name').text

    # 薪资，最大最小薪资，城市，工作经验，学历，工作性质(全职兼职实习)
    requests = soup.find('dd', class_='request').find_all('span')
    salary = requests[0].text.replace('/', '').strip()
    minSalary, maxSalary = salary.split('-')
    city = requests[1].text.replace('/', '').strip()
    empirical = requests[2].text.replace('/', '').replace('经验', '').strip()
    education = requests[3].text.replace('/', '').strip()
    workNature = requests[4].text.replace('/', '').replace('及以上', '').strip()

    # 公司优势
    advantage = dl.find('dd', class_='job-advantage').find('p').text

    # 具体需求
    detail = ''
    detail = detail.join(
        dl.find('div', class_='job-detail').text.replace('<br>', '').split())

    # 坐标，地址
    location = dl.find('dd', class_='job-address').find_all('input')
    eastLong = location[0].attrs['value']
    northLat = location[1].attrs['value']
    coordinate = (float(eastLong), float(northLat))
    address = location[3].attrs['value'] + location[2].attrs['value']

    return [position, company, salary, minSalary, maxSalary, city, empirical,
            education, workNature, advantage, detail, address, coordinate]


def save_info(infoFileName, info):
    print('Writing:')
    [print(item, end=' ') for item in info[:3]]
    [print(item, end=' ') for item in info[5:9]]
    print()
    with open(infoFileName, 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(info)


def save_infos(infoFileName, urlsFileName):
    if not os.path.isfile(infoFileName):
        with open(infoFileName, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Position', 'Company', 'Salary', 'Min-Salary', 'Max-Salary',
                'City', 'Empirical', 'Education', 'Work Nature', 'Advantage',
                'Detail', 'Address', 'Coordinate'
                ])
    try:
        with open(urlsFileName, 'r', encoding='utf-8') as file:
            urls = file.readlines()
            for url in urls:
                html = get_page(url.replace('\n', ''))
                info = crawl_info(html)
                save_info(infoFileName, info)
                time.sleep(12)
    except FileNotFoundError as e:
        print(e)


def save_one_urls(fileName, urls):
    with open(fileName, 'a', encoding='utf-8') as file:
        for url in urls:
            print(url)
            file.write(''.join([url]))
            file.write('\n')


def save_urls(fileName, url):
    pageSize = 30
    for i in range(1, pageSize+1):
        curUrl = url + str(i) + '/'
        print('Crawling', curUrl, '...')
        try:
            html = get_page(curUrl)
            urls = crawl_one_urls(html)
            save_one_urls(fileName, urls)
        except Exception as e:
            print(e.args[0])
        time.sleep(12)
    return urls


def main():
    url = 'https://www.lagou.com/zhaopin/C/'
    urlFileName = 'urls.txt'
    infoFileName = 'info.csv'
    # save_urls(urlFileName, url)
    save_infos(infoFileName, urlFileName)


if __name__ == '__main__':
    main()
