#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse, logging
import numpy as np
import struc2vec
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from time import time
import os
import json
import graph

logging.basicConfig(filename='struc2vec.log',filemode='w',level=logging.DEBUG,format='%(asctime)s %(message)s')

def parse_args():
	'''
	Parses the struc2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run struc2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')

	parser.add_argument('--walk-length', type=int, default=80,
	                    help='Length of walk per source. Default is 80.')

	parser.add_argument('--num-walks', type=int, default=10,
	                    help='Number of walks per source. Default is 10.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--until-layer', type=int, default=None,
                    	help='Calculation until the layer.')

	parser.add_argument('--iter', default=5, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=4,
	                    help='Number of parallel workers. Default is 8.')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	parser.add_argument('--OPT1', default=False, type=bool,
                      help='optimization 1')
	parser.add_argument('--OPT2', default=False, type=bool,
                      help='optimization 2')
	parser.add_argument('--OPT3', default=False, type=bool,
                      help='optimization 3')	
	return parser.parse_args()

def read_graph():
	'''
	Reads the input network.
	'''
	logging.info(" - Loading graph...")
	G = graph.load_edgelist(args.input,undirected=False)
	if(G == None): return None
	logging.info(" - Graph loaded.")
	return G

def learn_embeddings():
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	logging.info("Initializing creation of the representations...")
	walks = LineSentence('random_walks.txt')
	model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, hs=1, sg=1, workers=args.workers, iter=args.iter)
	model.wv.save_word2vec_format(args.output)
	logging.info("Representations created.")
	
	return

def exec_struc2vec(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	if(args.OPT3):
		until_layer = args.until_layer
	else:
		until_layer = None

	G = read_graph()
	if(G == None): return None
	G = struc2vec.Graph(G, args.directed, args.workers, untilLayer = until_layer)

	if(args.OPT1):
		G.preprocess_neighbors_with_bfs_compact()
	else:
		G.preprocess_neighbors_with_bfs()

	if(args.OPT2):
		G.create_vectors()
		G.calc_distances(compactDegree = args.OPT1)
	else:
		G.calc_distances_all_vertices(compactDegree = args.OPT1)


	G.create_distances_network()
	G.preprocess_parameters_random_walk()

	G.simulate_walks(args.num_walks, args.walk_length)


	return G

def main(args):

	G = exec_struc2vec(args)

	learn_embeddings()


if __name__ == "__main__":
	args = parse_args()
	if not os.path.exists(args.input + '_input'):
		os.mkdir(args.input + '_input')
	if not os.path.exists(args.output+'_output'):
		os.mkdir(args.output + '_output')
	if not os.path.exists(args.output+'_output/feature'):
		os.mkdir(args.output+'_output/feature')
	suc = 0
	fal = 0
	with open(args.input,'r') as f_in:
		res = f_in.readlines()
		for line in res:
			try:
				dic = json.loads(line)
				suc = suc + 1
			except:
				print line
				fal = fal + 1
				continue
			fname = args.input+'_input'+ '/' + str(suc)
			with open(fname,'w') as f_out:
				json.dump(dic,f_out,ensure_ascii=False)
	input_ = args.input
	output_ = args.output	
	for i in range(0,suc):
		args.input = input_  + '_input'+ '/' + str(i+1)
		args.output= output_ + '_output' + '/' + str(i+1)
		with open(args.input,'r') as f:
			dic = json.load(f)
			if(dic['n_num'] == 1):
				for j in range(args.dimensions):
					dic['features'][0].append(0)
				with open(output_ + '_output/feature/'+str(i+1),'w') as fo:
					json.dump(dic,fo,ensure_ascii=False)

			else:
				main(args)
				with open(args.output,'r') as f1:
					data = f1.readlines()
					for m in range(1,len(data)):
						line = data[m]
						str_list = line.split(' ')
						for j in range(len(str_list)):
							if(j == 0): str_list[0] = int(str_list[0])
							else:
								str_list[j] = float(str_list[j][1:])
						for x in range(1,len(str_list)):
							dic['features'][str_list[0]].append(str_list[x])
				with open(output_ + '_output/feature/'+str(i+1),'w') as f2:
					json.dump(dic,f2,ensure_ascii=False)
								
	
