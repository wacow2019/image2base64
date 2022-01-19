from PIL import Image
import sys
import base64
import uuid
import os
import re


def print_fail(msg):
    print('fail:{}'.format(msg))
# / def print_fail


def get_image_resize(path, width):
    '''轉換圖檔到指定的大小，並回傳base64字串'''
    try:
        img = Image.open(path)
    except FileNotFoundError:
        print_fail('無此檔案 {}'.format(path))
    except Exception:
        print_fail('無法開啟檔案 {}'.format(path))
    else:
        w, h = img.size
        if (w >= h):
            # 長型圖片
            dw = width
            dh = int(dw*(h/w))
        else:
            # 寬型圖片
            dh = width
            dw = int(dh*(w/h))
        # / if
        return img.resize((dw, dh), Image.ANTIALIAS)
    # /try
    return None
# /get_jpg


def pathinfo(filename, field=None):
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    try:
        filename, extension = basename.rsplit(".", 1)
    except Exception:
        filename = basename
        extension = ''
    # /try
    if(dirname == ''):
        fullname = basename
    else:
        fullname = '%s/%s' % (dirname, filename)
    # /if ---
    result = {
        "dirname": dirname,
        "basename": basename,
        "filename": filename,
        "extension": extension.lower(),
        "fullname": fullname
    }
    if(field == None):
        return result
    else:
        return result.get(field, None)
    # /if ---
# / pathinfo


def base64image(filepath):
    '''將圖檔轉成base64格式的字串，可以直接被html img src使用'''
    try:
        with open(filepath, 'rb') as imageFile:
            strimage = base64.b64encode(imageFile.read())
        # /with ---

    except Exception:
        return None
    else:
        ext = pathinfo(filepath, 'extension')
        return 'data:image/%s;base64,%s' % (ext, str(strimage, encoding='utf-8'))
    # /try ---
# /base64image


def argv_index(index):
    try:
        return sys.argv[index]
    except Exception as e:
        return None
# /def argv_index


def argv_value(prevalue=None, default=None):
    """ 取得傳入參數的後方值，如-save file.jpg 
    prevalue -save
    return file.jpg
    """
    if prevalue == None:
        return argv_index(1)

    try:
        i = sys.argv.index(prevalue)
    except Exception as e:
        return default
    else:
        return argv_index(i+1)
    if prevalue not in sys.argv:
        return None
    # / try
# / def argv_value


def data2image(data_url, filename):
    ''' data_url 存成檔案
    import re,base64

    @param string $data_url  data:image/jpg;i8adlasdff==
    @param string $filename 要儲存的檔名不含副檔名
    @return string 回傳完整檔名不含路徑
    '''
    output = re.search('^data:image\/(jpg|png|gif|jpeg);base64,(.+)', data_url, flags=re.IGNORECASE)
    #沒找到可用的資料回傳None
    if (output == None): return None
    image_type, image_data = output.groups()
    filename = '{}.{}'.format(filename, image_type.lower())
    with open(filename, 'wb') as w:
        w.write(base64.b64decode(image_data))
    #/ with close file
    #/if
#/ data2image

def main():
    '''
    主程式
    2021 -01開啟寫程式
    
    為了怕不過
    '''
    filename = argv_value()
    savename = argv_value('-save')
    try:
        size = int(argv_value('-size', 640))
    except Exception as e:
        return print_fail("-size 必須是數值")
    # 轉換圖檔的SIZE
    img = get_image_resize(filename, size)
    if img == None:
        return print_fail("轉檔失敗")
    if(savename == None):
        savename = 'temp_{}.jpg'.format(uuid.uuid4())
        delfile = True
    else:
        delfile = False
    # 存檔
    img.save(savename, quality=80)
    # 將圖檔轉換base64格式
    base64data = base64image(savename)
    if(delfile):
        os.unlink(savename)
    print(base64data)

if __name__ == "__main__":
    main()
