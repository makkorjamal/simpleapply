import getopt, sys
from anschreiben import Anschreiben
import copy

def usage():
    print("Usage: main.py -i <inputfile> -t <templatefile> [-v]")

def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hi:t:v",
            ["help", "input=", "template=", "verbose"]
        )
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    verbose = False
    input_data = {}
    template_data = {}
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-i", "--input"):
            if verbose:
                print("Reading input from", a)
            with open(a) as f:
                icode = compile(f.read(), a, 'exec')
                exec(icode, {}, input_data)
        elif o in ("-t", "--template"):
            if verbose:
                print("Reading template from", a)
            template_data.update(input_data)
            with open(a) as f:
                tcode = compile(f.read(), a, 'exec')
                exec(tcode, {}, template_data)
                geometry_options = {"margin":"1.0in"}
                anschreiben = Anschreiben(geometry_options = geometry_options,\
                        input_data = input_data, template = template_data)
                anschreiben.fill_document()
                anschreiben.generate_document()
        else:
            assert False, "Unhandled option"
    #process(args, output=output, verbose=verbose)

if __name__ == "__main__":
    main()
