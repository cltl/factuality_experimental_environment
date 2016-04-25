from KafNafParserPy import *
import sys
import os


def run_on_dir(indir, outdir):
    
    for f in os.listdir(indir):
        create_raw_from_tokens(indir +'/' + f, outdir + '/' + f + '.naf')



def create_raw_from_tokens(infile, outfile=''):
    '''
    Goes through token-layer of a naf file and creates the raw text using the token's offsets.
    Replaces the old raw text if present. Output is outfile name if provided, else stdout
    '''
    mynaf = KafNafParser(infile)
    raw = ''
    print(infile)
    current_offset = 0
    for tok in mynaf.get_tokens():
        myoffset = tok.get_offset()
        if int(myoffset) == current_offset:
            raw += tok.get_text()
        else:
            distance = int(myoffset) - current_offset
            current_offset += distance
            if distance == 1:
                raw += ' '
                raw += tok.get_text()
            elif distance == 2:
                raw += '\n\n'
                raw += tok.get_text()
            elif distance < 0:
                print >> sys.stderr, 'Problem: overlap between tokens'
            else:
                raw += ' ' * distance
                raw += tok.get_text()
                print >> sys.stderr, distance
            
      #  elif int(myoffset) > current_offset:
            #fill in whitespace for distance between word
      #      distance = 
      #      print >> sys.stderr, distance, current_offset, myoffset
      #      raw += distance * ' '
      #      raw += tok.get_text()
      #      #make up for space
      #      current_offset = int(myoffset)
      #  else:
      
        current_offset += int(tok.get_length())
    mynaf.set_raw(raw)
    
    if outfile:
        mynaf.dump(outfile)
    else:
        mynaf.dump()





def main(argv=None):
    
    argv=sys.argv
    
    if len(argv) == 3:
        run_on_dir(argv[1], argv[2])
    elif len(argv) == 1:
        infile = sys.stdin
        create_raw_from_tokens(infile)



if __name__ == '__main__':
    main()