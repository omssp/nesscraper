"https://www.romstation.fr/games?game_title=mario&consoles_id%5B%5D=19%2FNES&game_players=&release_date_min=&release_date_max=&dev_edit_name=&excludes%5B%5D=demo%2FDemo&excludes%5B%5D=fangame%2FFangame&excludes%5B%5D=hack%2FHackrom&excludes%5B%5D=homebrew%2FHomebrew&order_disp=rating%2FTop+rated&rs_page=1&letter=&uploader_id="
link = "https://www.romstation.fr/games?game_title={}&consoles_id%5B%5D=19%2FNES&game_players=&release_date_min=&release_date_max=&dev_edit_name=&excludes%5B%5D=demo%2FDemo&excludes%5B%5D=fangame%2FFangame&excludes%5B%5D=hack%2FHackrom&excludes%5B%5D=homebrew%2FHomebrew&order_disp=rating%2FTop+rated&rs_page=1&letter=&uploader_id="
from requests import get
from bs4 import BeautifulSoup as bs
import os
import json
import slugify

liste = []

roms = os.listdir('roms')
i = 1
for rom in roms[2:]:
    try:
        name = rom.replace('.nes', '')
        print(name)
        
        response = get(link.format(name))
        soup = bs(response.content, 'html.parser')
        
        imageurl = f"https://www.romstation.fr{soup.select('.game_inner_row')[0].img['data-src']}".replace('mini_', '')
        
        slug = f"{i}-{slugify.slugify(name)}"
        nes = f"roms/{slug}.nes"
        image = f"roms/{slug}.jpg"
        os.rename(f"roms/{rom}", nes)
    
        
        file_object = get(imageurl)
        with open(image, 'wb') as local_file:
            local_file.write(file_object.content)
        
        liste.append({
            'slug': slug,
            'name': name,
            'nes': nes,
            'image': image,
            'imageurl': imageurl,
        })
        
        with open('gooder.json', 'w', encoding='utf-8') as f:
            json.dump(liste, f, ensure_ascii=False, indent=4)
        i += 1
        print(liste[-1])
    except Exception as e:
        print(e)


