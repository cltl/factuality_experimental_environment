from KafNafParserPy import *
from lxml import etree
import sys
import os




def create_tok_to_term_dict(nafobj):

    tok2term = {}
    for term in nafobj.get_terms():
        tspan = term.get_span().get_span_ids()
        #spans of terms almost always have length 1 and tokens are only part of one term
        tok2term[tspan[0]] = term.get_id()

    return tok2term

def integrate_catevents_into_naf(nafobj, cattree, nafout):

    tok2term = create_tok_to_term_dict(nafobj)
    markables = cattree.find('Markables')
    events = []
    for mark in markables.findall('EVENT_MENTION'):
        terms=[]
        for tanch in mark.findall('token_anchor'):
            #original input naf generated from CAT, token numbers match
            tid = tanch.get('t_id')
            termId = tok2term['w' + tid]
            terms.append(termId)
        events.append(terms)

    #remove old coreferences (FIXME: this includes entity coreference)
    #nafobj.remove_coreference_layer()
    coref_count = 1
    for event in events:
        mycoref = Ccoreference()
        mycoref.set_id('coevent' + str(coref_count))
        coref_count += 1
        mycoref.add_span(event)
        mycoref.set_type('newevent')
        nafobj.add_coreference(mycoref)
    nafobj.dump(nafout)


def create_gold_event_nafs_from_cat(nafin, catin, nafout):

    parser = etree.XMLParser(ns_clean=True)
    for f in os.listdir(nafin):
        nafobj = KafNafParser(nafin + f)
        cfn = f.rstrip('.naf')
        cattree = etree.parse(catin + cfn, parser)
        integrate_catevents_into_naf(nafobj, cattree, nafout + f)





def main(argv=None):
    
    
    if argv==None:
        argv = sys.argv
    
    if len(argv) < 4:
        print('USAGE: python integrate_cat_gold_events_in_naf.py NAFdir CATdir OUTdir')
    else:
        create_gold_event_nafs_from_cat(argv[1], argv[2], argv[3])

if __name__ == '__main__':
    main()




