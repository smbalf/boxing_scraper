import re

links = ['<a class="personLink" href="/en/box-pro/354380">Adrian Rajkai</a>','<a class="personLink" href="/en/box-pro/18447">Laszlo Komjathi</a>', '<a class="personLink" href="/en/box-pro/449854">Daniel Regi</a>']

for a_tag_text in links:
    grab_url = re.search('href="(.*)">', a_tag_text)
    grab_name = re.search('>(.*)</a>', a_tag_text)
    print(grab_url.group(1))
    print(grab_name.group(1))