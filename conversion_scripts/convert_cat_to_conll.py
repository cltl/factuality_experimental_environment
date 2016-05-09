from KafNafParserPy import *
from lxml import etree
import sys
import os




def create_id2event_dict(events):

    tokid2events = {}
    eventId = 0
    for event in events:
        eventId += 1
        first = True
        evids = event.pop(0)
        for tid in sorted(evids):
            myevent = [event[0],event[1],event[2]]
            if first:
                myevent.append('B')
                first = False
            else:
                myevent.append('I')
            myevent.append(str(eventId))
            if not tid in tokid2events:
                tokid2events[tid] = myevent
            else:
                updatedevlist = tokid2events.get(tid) + myevent
                tokid2events[tid] = updatedevlist
    return tokid2events

def create_conll(cattree, conllf):

    markables = cattree.find('Markables')
    events = []
    for mark in markables.findall('EVENT_MENTION'):
        certainty = mark.get('certainty')
        polarity = mark.get('polarity')
        time = mark.get('time')
        terms=[]
        for tanch in mark.findall('token_anchor'):
            #original input naf generated from CAT, token numbers match
            tid = tanch.get('t_id')
            terms.append(tid)
        myevent = [terms, certainty, polarity, time]
        if not '' in myevent and not None in myevent:
            events.append(myevent)
    #convert so we can have look-up for tokens
    tok2events= create_id2event_dict(events)

    myout = open(conllf, 'w')
    sentence = '0'
    meantime_included = True
    for token in cattree.findall('token'):
        t_id = token.get('t_id')
        sent = token.get('sentence')
        #add additional line if new sentence
        if sent != sentence:
            myout.write('\n')
            sentence = sent
        if sentence == '6':
            meantime_included == False
        myline = t_id + '\t' + token.text + '\t'
        if t_id in tok2events and meantime_included:
            info = tok2events.get(t_id)
            if len(info) == 5 or info[3] == 'B':
                #adding event
                myline += info[3] + '-E-' + info[4] + '\t'
                #adding certainty
                myline += info[3] + '-' + info[0] + '-' + info[4] + '\t'
                #adding polarity
                myline += info[3] + '-' + info[1] + '-' + info[4] + '\t'
                #adding time
                myline += info[3] + '-' + info[2] + '-' + info[4] + '\n'
            elif len(info) == 10 or info[8] == 'B':
                #adding event
                myline += info[8] + '-E-' + info[9] + '\t'
                #adding certainty
                myline += info[8] + '-' + info[5] + '-' + info[9] + '\t'
                #adding polarity
                myline += info[8] + '-' + info[6] + '-' + info[9] + '\t'
                #adding time
                myline += info[8] + '-' + info[7] + '-' + info[9] + '\n'
            else:
                print(t_id, ' is part of too many events or something else is wrong', info)
        else:
            myline += '_\t_\t_\t_\n'
        myout.write(myline)

def convert_cat_to_conll(catdir, conlldir):

    parser = etree.XMLParser(ns_clean=True)
    for f in os.listdir(catdir):
        if f.endswith('.xml'):
            cattree = etree.parse(catdir + f, parser)
            create_conll(cattree, conlldir + f + '.conll')





def main(argv=None):
    
    
    if argv==None:
        argv = sys.argv
    
    if len(argv) < 3:
        print('USAGE: python convert_cat_to_conll.py CATdir OUTdir')
    else:
        convert_cat_to_conll(argv[1], argv[2])

if __name__ == '__main__':
    main()




