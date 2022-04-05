import argparse
import os

def parse_args():
	'''
	Parses the struc2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run struc2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	return parser.parse_args()

def main(args):
	os.mkdir(args.input)
	os.mkdir(args.output)

if __name__ == "__main__":
	args = parse_args()
	main(args)
