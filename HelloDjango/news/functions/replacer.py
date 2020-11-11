import re


def get_slug_en(title):
    dic = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v',
           'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
           'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
           'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
           'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
           'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'yi',
           'э': 'e', 'ю': 'yu', 'я': 'ya'}

    alphabet = ['Ь', 'ь', 'Ъ', 'ъ', 'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё',
                'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о',
                'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч',
                'Ш', 'ш', 'Щ', 'щ', 'Ы', 'ы', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']
    len_str = len(title)
    result = str()
    title = title.lower()
    for i in range(0, len_str):
        if title[i] in alphabet:
            simb = dic[title[i]]
        else:
            simb = title[i]
        result = (result + simb).replace(' ', '_').replace("'", '').replace('(', '').replace(')', '').replace('+', '').replace(',', '').replace('-', '').replace('«', '').replace('»', '').replace('%', 'percent').replace('.', '').replace('’', '').replace(':', '').replace('"', '').replace('$', 'usd').replace('қ', 'k').replace('ө', 'o').replace('і', 'i').replace('ә', 'a').replace('ғ', 'g').replace('ң', 'n').replace('ұ', 'u').replace('ү', 'y').replace('h', 'h').replace('.', '').replace('–', '').replace('&', 'and').replace('“', '').replace('”', '').replace('ø', 'o').replace('—', '').replace('&nbsp;', '')
        clean_result = re.sub('[^A-Za-z0-9]+', '_', result)
    return clean_result[:49]
