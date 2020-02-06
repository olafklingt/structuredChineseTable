# structuredChineseTable
A python script that reads a chinese text file and outputs the text as list of words with PinYin, BoPoMoFo, and English translation
The outputfile can be used with pandoc markdown+grid_tables format'

For example:
./structuredchinesetable.py source.txt table.txt
pandoc -o table.docx -f markdown+grid_tables table.txt

Because the translation is made using Google Translate only short text can be translated before google blocks the connection.

The script uses
argparse # to parse arguments
re # to split sentences
Texttable # for output in table form
pywordseg # for chinese word spegmentation
googletrans # for english translation
pypinyin * # for pinyin and bopomofo
pinyin # for english translation (if google fails but it works quite badly)

These can be installed useing pip

On my computer (arch linux) pywordseg must be once called from superuser so that it downloads and installs its models

