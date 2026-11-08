with open(r'e:\DCCBC\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
tabs = re.findall(r'<button class="nav-tab[^"]*"[^>]*>(.*?)</button>', html)
print('Current nav tabs:', tabs)
