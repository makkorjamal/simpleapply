import getopt, sys
import yaml
from collections import namedtuple
from anschreiben import Anschreiben
from lebenslauf import Lebenslauf
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
            if ".py" in a:
                with open(a) as f:
                    template_data.update(input_data)
                    tcode = compile(f.read(), a, 'exec')
                    exec(tcode, {}, template_data)
                    geometry_options = {"margin":"1.0in"}
                    anschreiben = Anschreiben(geometry_options = geometry_options,\
                            input_data = input_data, template = template_data)
                    anschreiben.fill_document()
                    anschreiben.generate_document()
                    _ = anschreiben.dumps()
            if ".yaml" in a:
                with open(a, 'r') as file:
                    data = yaml.safe_load(file)
                    geometry_options = {"margin":"1.0in"}
                    lebenslauf =Lebenslauf(geometry_options = geometry_options,\
                            input_data = input_data, template_data = data)
                    lebenslauf.fill_document()
                    lebenslauf.generate_document()
                    _ = lebenslauf.dumps()
        else:
            assert False, "Unhandled option"

if __name__ == "__main__":
    main()
