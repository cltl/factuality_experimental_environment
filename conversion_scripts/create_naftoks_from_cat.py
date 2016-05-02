from KafNafParserPy import *
from lxml import etree
import sys
import os



def create_naffiles(CATdir, NAFdir):


    parser = etree.XMLParser(ns_clean=True)
    for f in os.listdir(CATdir):
        if not f.endswith('xml'):
            continue
        cattree = etree.parse(CATdir + f, parser)
        nafobj = KafNafParser(type='NAF')
        nafobj.set_language('en')
        nafobj.set_version('3.0')
        offset = 0
        quotes = False
        for tok in cattree.findall('token'):
            #collecting info
            tokId = 'w' + tok.get('t_id')
            #TODO: check if this needs to be + 1
            sent_nr = tok.get('sentence')
            token = tok.text
            length = len(token)
            #check if space needed
            if not token in [')','.',';',',',':','?']:
                offset += 1
            if token == '"':
                quotes = False
            elif token == "''" and quotes:
                offset -= 1
                quotes = False
            #setting info on naf token obj
            naftok = Cwf()
            naftok.set_id(tokId)
            naftok.set_text(token)
            naftok.set_offset(str(offset))
            naftok.set_length(str(length))
            naftok.set_sent(sent_nr)
            nafobj.add_wf(naftok)
            #update offset
            offset += length
            if token in ['(']:
                offset -= 1
            if (token == '"' and not quotes):
                quotes = True
            if token == '``':
                offset -= 1
                quotes = True
        nafobj.dump(NAFdir + f)


def main(argv=None):
    
    
    if argv==None:
        argv = sys.argv
    
    if len(argv) < 3:
        print('USAGE: python create_naftoks_from_cat.py CATdir NAFdir')
    elif len(argv) < 4:
        create_naffiles(argv[1], argv[2])

if __name__ == '__main__':
    main()
