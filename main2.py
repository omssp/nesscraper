import os
import json
import glob
import pandas
from requests import get
import patoolib
import shutil



uniq = pandas.read_json('data.json')

uniq = uniq.drop_duplicates(subset='rom', keep="last")

goodwithimgs = uniq[
    uniq.image != "https://www.retrostic.com/img/no-image-thumb.png"]

print(goodwithimgs)
goodwithimgs.to_json('sorted.json', orient='table', index=False)


lists = []
if not os.path.exists('downloads'):
    os.mkdir('downloads')
roms = pandas.read_json('sorted.json', orient='table')

for rom in roms.iterrows():
    slug = f"{rom[0]}-{rom[1]['url'].split('/')[-1]}"
    fileurl = rom[1]['rom']
    title = rom[1]['title']
    imageurl = rom[1]['image']
    dir = f'downloads/{slug}'
    imagename = f"{dir}{os.path.splitext(imageurl)[-1]}"
    filename = f"{dir}{os.path.splitext(fileurl)[-1]}"
    
    
    try:
        file_object = get(fileurl)
        with open(filename, 'wb') as local_file:
            local_file.write(file_object.content)
    
        patoolib.extract_archive(filename, outdir=dir)

        nesfile = glob.glob(f'{dir}/*.nes')[0]

        shutil.move(nesfile, f"{dir}.nes")
        shutil.rmtree(dir)
        os.remove(filename)
        
        
        file_object = get(imageurl)
        with open(imagename, 'wb') as local_file:
            local_file.write(file_object.content)

        lists.append({
            'slug': slug,
            'title': title,
            'imagename': imagename,
            'imageurl': imageurl,
            'filename': filename,
            'fileurl': fileurl,
        })
        with open('good.json', 'w', encoding='utf-8') as f:
            json.dump(lists, f, ensure_ascii=False, indent=4)
        print(lists[-1])
    except Exception as e:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        files = glob.glob(f'{dir}*')
        for file in files:
            os.remove(file)
        print(str(e))


for x in os.listdir('downloads'):
    x = 'downloads/' + x
    print(x)
    if os.path.isdir(x):
        shutil.rmtree(x)

zips = glob.glob('downloads/*.zip')
for zip in zips:
    os.remove(zip)
        
shutil.make_archive('downloads', 'zip', 'downloads')

exit()
import re
import json
from requests import get, post
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs

homeurl = "https://www.retrostic.com/roms/nes/page/"

regex = re.compile(r"window\.location\.href\s=\s\"(.+)\";")

listLinks = []


def getListGames1Page(url):
    resp = get(url)
    top = bs(resp.content, 'html.parser')
    items = top.select("#romstable tr td a")
    for item in items:
        print(item)
        try:
            page_link = urljoin(url, item['href'], 'download')
            page_title = item['title']
            page_img_url = urljoin(url, item.img['data-src'])
            resp = get(page_link)
            soup = bs(resp.content, 'html.parser')
            form = soup.select('#dl input')
            sessno = form[-1]['value']
            resp = post(f"{page_link}/download",
                        data={
                            'rom_url': page_link.split('/')[-1],
                            'console_url': 'nes',
                            'session': sessno
                        })

            page_zip = regex.findall(str(resp.content))[0]
            listLinks.append({
                'url': page_link,
                'title': page_title,
                'image': page_img_url,
                'rom': page_zip
            })

            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(listLinks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(str(e))


for i in range(1, 87):
    getListGames1Page(f"{homeurl}{i}")

print(listLinks)
