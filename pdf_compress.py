import os
import io
import time
import PyPDF4
import argparse
from PIL import Image
__author__ = 'Dmytro Pavliuk'

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DESTINATION = "OPTIMIZED" #destination directory for results


def mkdir_results() -> None:
    """Make destination dir with subdirs"""
    for root, dirs, files in os.walk(CURRENT_PATH):
        if DESTINATION not in root:
            path = root.replace(CURRENT_PATH, CURRENT_PATH + os.sep + DESTINATION)
            path = os.path.normpath(path)
            if not os.path.exists(path):
                os.mkdir(path)


def get_filenames():
    """Get fullpath of with source pdf files"""
    for root, dirs, files in os.walk(CURRENT_PATH):
        for file in files:
            if file.endswith(".pdf") and DESTINATION not in root:
                yield os.path.join(root, file)


def get_pages(filename: str) -> list or "Error":
    """Get pages from pdf and extract images from it
    RETURN: list of images in bytes
    """
    print(filename)
    try:
        pdf_in = PyPDF4.PdfFileReader(filename)
    except BaseException as err:
        print('Error: ', err)
        return "Error"
    imgs = []
    # every pages
    for pg in range(pdf_in.getNumPages()):
        page = pdf_in.getPage(pg)
        xObject = page['/Resources']['/XObject'].getObject()
        # every images
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                try:
                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"
                except KeyError: 
                    return "Error"

                if xObject[obj]['/Filter'] == '/FlateDecode':
                    img = Image.frombytes(mode, size, data)
                    imgs.append(img)
                else:
                    imgs.append(xObject[obj].getData())
    return imgs


def save_resuts(filename: str, pdf_out: object, pilobjects: list, quality: int) -> str:
    """Compress and save file ti destination dir"""
    fileout = filename.replace(CURRENT_PATH, CURRENT_PATH + os.sep + DESTINATION)
    fileout = os.path.normpath(fileout)
    pdf_out.save(fileout, 'pdf', save_all=True, optimize=True, quality=quality, append_images=pilobjects)
    return fileout


def main():
    """Compress images in .pdf files using PIL"""
    parser = argparse.ArgumentParser(description='Compress .pdf files')
    parser.add_argument('--q', default=50, help='quality percent, provide integer (default: 50)')
    args = parser.parse_args()
    quality = int(args.q)
    count = 0
    wrongfiles = []
    start_prog = time.time()
    print("---------------------- Start --------------------- ")
    print("Compress quality: {}%".format(quality))
    mkdir_results()
    for filename in get_filenames():
        start = time.time()
        size_in = round(os.path.getsize(filename) / 1000, 2)
        imgs = get_pages(filename)
        if imgs == "Error" or not imgs:
            wrongfiles.append(filename)
            continue
        pilobjects = []
        pdf_out = Image.open(io.BytesIO(imgs[0]))
        for img in imgs[1:]:
            pilobjects.append(Image.open(io.BytesIO(img)))
        try:
            fileout = save_resuts(filename, pdf_out, pilobjects, quality)
        except Exception as err:
            print('Error: ', err)
            wrongfiles.append(filename)
            continue
        size_out = round(os.path.getsize(fileout) / 1000, 2)
        count += 1
        print("Count: {}, \ttime: {} sec".format(count, round(time.time() - start, 2)))
        print("Input size: {} Kb, \toutput size: {} Kb".format(size_in, size_out))
        print('-'*50)        
    print("\nFinished {} files in {} sec".format(count, round(time.time() - start_prog, 2)))
    if wrongfiles:
        print(f"\n!!!-----Catched some problems with:-----!!!")
        for i in wrongfiles:
            print(i)


if __name__ == '__main__':

    main()
    # input("\n=== Presss ENTER to exit the program ===")