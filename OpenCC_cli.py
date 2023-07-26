import sys
from tkinter.filedialog import askopenfilenames
import opencc
import chardet
import os.path as osp

class cli_param():
    fformat = (('All','*.*'), ('Text-based', '*.txt;*.csv;*.html;*.json;*.xml;*.cfg;*.ini;*.md;*.log;*.yaml'),
            ('Subtitle','*.srt;*.ass;*.sub;*.vtt;*.lrc'))
    class conv_langs():  
        mapping = {
            's' : '簡體',
            't' : '繁體',
            'tw' : '臺灣繁體',
            'hk' : '香港繁體',
            'jp' : '日本漢字 (Kanji)',
            'sp' : '簡體 (中國大陸常用詞彙)',
            'twp' : '繁體 (臺灣常用詞彙)'
        }   
        lang_key = ['s', 't', 'tw', 'hk', 'jp', 'sp', 'twp']
        s = ['t','tw','hk','twp']
        t = ['s','tw','hk','jp']
        tw = ['s','t','sp']
        hk = ['s','t']
        jp = ['t']
        json_name = ['s2t','t2s','s2tw','tw2s','s2hk','hk2s',
                's2twp','tw2sp','t2tw','hk2t','t2hk','t2jp','jp2t','tw2t']


def opencc_converter(src_files, lang_json):       
    conv = opencc.OpenCC(lang_json)
    for file in src_files:
        out_name = osp.splitext(file)[0] + '_converted' + osp.splitext(file)[1]
        with open(file, 'rb') as fin, open(out_name, 'w', encoding='utf-8') as fout:
            content = fin.read()
            dectecting = chardet.detect(content)
            decoded_text = content.decode(dectecting['encoding'])
            for line in decoded_text.splitlines():
                fout.write(conv.convert(line) + '\n')

def opencc_CLI():
    while True:
        if len(sys.argv) > 1:
            file_path = sys.argv[1:]
        else:
            file_path = askopenfilenames(title='請選擇檔案', filetypes=cli_param.fformat)
        if file_path != '':
            break
        print('請選擇檔案')
    
    while True:
        for i, opt in enumerate(cli_param.conv_langs.lang_key[:5]):
            print(f'{i+1}. {cli_param.conv_langs.mapping[opt]}')
        original_lang_idx = int(input('原有語言： '))
        if original_lang_idx > 0 and original_lang_idx < 6:
            break
        print('\n請輸入正確選項\n')
    ori_lang = cli_param.conv_langs.lang_key[original_lang_idx - 1]
    print('-----------------------------------------------------------------------')
    while True:
        possible_out = getattr(cli_param.conv_langs, ori_lang)
        for i, member in enumerate(possible_out):
            print(f'{i+1}. {cli_param.conv_langs.mapping[member]}')
        target_lang_idx = int(input('目標語言： '))
        if (target_lang_idx > 0) and (target_lang_idx < len(possible_out) + 1):
            break
        print('\n請輸入正確選項\n')
    target_lang = cli_param.conv_langs.lang_key[target_lang_idx - 1]
    
    opt_lang = f'{ori_lang}2{target_lang}.json'
    try:
        opencc_converter(file_path, opt_lang)
        print('\n檔案轉換完成')
    except:
        print('\n檔案轉換錯誤')
        
if __name__ == "__main__":
    opencc_CLI()