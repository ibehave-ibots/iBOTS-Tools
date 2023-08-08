from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("workshop_id", type=int, help="Unique id of a specific workshop.")

args = parser.parse_args()
args = vars(args)

print(args)
print(args.workshop_id, type(args.workshop_id))
