import py7zr
import glob
import os


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


rom_path = './roms-gba/*.gba'

roms = set(glob.glob(rom_path))
roms_remove = set([x.replace('.7z', '') for x in glob.glob(f'{rom_path}.7z')])

roms = list(roms - roms_remove)

for rom in roms:
    zFile = f'{rom}.7z'
    rom_size = os.path.getsize(rom)
    print(f"{sizeof_fmt(rom_size)} ", end='')
    with py7zr.SevenZipFile(zFile, 'w') as archive:
        archive.write(rom, os.path.basename(rom))
    zFile_size = os.path.getsize(zFile)
    print(f"--> {sizeof_fmt(zFile_size)} : {rom}")
