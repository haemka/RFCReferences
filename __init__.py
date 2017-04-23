import sys, getopt
from RFC import RFC

def main(argv):
    try:
        opts, args = getopt.getopt(argv,'hr:x:',['rfc=','xep='])
    except getopt.GetoptError as e:
        print(e)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-r', '--rfc'):
            rfc = RFC(arg)
        else:
            assert False, 'unhandled option'
            usage()

    rfc = RFC("3921")
    print(rfc.getTitle())
    print(rfc.getURL())
    print(rfc.getReferenceTitles())


if __name__ == "__main__":
    main(sys.argv[1:])
