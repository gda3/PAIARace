#!/usr/bin/python
import sys, random, operator


positive_positions = []
negative_positions = []
unsat_clauses = []
unsat_lits = []
len_clauses = []

def parse(filename) :
	formula = []
	clause_position = 0
	for line in open( filename ) :
		if line.startswith( 'c' ) : continue
		if line.startswith( 'p' ) :
			nvars, nclauses = line.split()[2:4]
			for x in xrange(int(nvars)):
				positive_positions.append([])
				negative_positions.append([])
			unsat_lits = [0] * int(nclauses)
			continue
		clause = [ int(x) for x in line[:-2].split() ]
		formula.append(clause)
		len_clauses.append(len(clause))
		for literal in clause:
			if literal < 0:
				negative_positions[abs(literal) - 1].append(clause_position)
				
			else:
				positive_positions[literal - 1].append(clause_position)
		clause_position += 1
	return formula, int(nvars)

def get_counter(formula) :
	counter = {}
	for clause in formula :
		for literal in clause :
			if literal in counter :
				counter[literal] += 1
			else :
				counter[literal] = 1
	return counter

def rnd_interpretation(formula, nvars, prob = 0.5):
	interpretation = []
	for var in xrange(1, nvars + 1):
		if random.random() < prob: interpretation.append(var * -1)
		else: interpretation.append(var)
	return interpretation

def satisfies(interpretation, formula):
	del unsat_clauses[:] # Empties the list
	boolean = True
	for clause in formula:
		length = len(clause)
		for literal in clause:
			if literal == interpretation[abs(literal) - 1]:
				break
			else:
				length -= 1
		if length == 0: # Falsified clause
			boolean = False
			unsat_clauses.append(clause)
	return boolean

def unsatisfies(copy_i, formula):
	num_unsat_clauses = 0
	for clause in formula:
		if clause not in unsat_clauses:
			length = len(clause)
			for literal in clause:
				if literal == copy_i[abs(literal) - 1]:
					break
				else:
					length -= 1
			if length == 0: # Falsified clause
				num_unsat_clauses += 1
	return num_unsat_clauses

def update_unsat_lits(interpretation):
	for literal in interpretation:
		if literal < 0:
			for pos in positive_positions[abs(literal) - 1]:
				unsat_lits[pos] += 1
		else:
			for pos in negative_positions[literal - 1]:	
				unsat_lits[pos] += 1

def broken_clauses(S, interpretation):
	broken_clauses = [sys.maxint] * len(interpretation)
	for literal in S:
		if literal < 0:
			for pos in positive_positions[abs(literal) - 1]:
				if unsat_lits[pos] + 1 == len_clauses[pos]:
					broken_clauses[abs(literal) - 1] += 1
		else:
			for pos in negative_positions[literal - 1]:
				if unsat_lits[pos] + 1 == len_clauses[pos]:
					broken_clauses[literal - 1] += 1
	return broken_clauses

def walksat(formula, nvars, max_tries = sys.maxint, max_flips = 10, w = 0.5):
	interpretation = []
	C = []
	S = []
	for i in xrange(max_tries):
		interpretation = rnd_interpretation(formula, nvars)
		for j in xrange(nvars * 2):
			if satisfies(interpretation,formula):
				return interpretation
			C = random.choice(unsat_clauses)
			# S <- set of variables that appear in C
			S = list(C)
			# b <- min({broken(p,F,I) | p in S})
			update_unsat_lits(interpretation)
			bc = broken_clauses(S, interpretation)
			b = min(bc)
			if b > 0 and random.random() > w:
			# 	p <- a variable of S
				p = random.choice(S)
			else:
			# 	p <- a variable of S s.t. broken(p,F,I) = b
				p = bc.index(b) + 1
			# I <- I with the value of p flipped
			interpretation[abs(p) - 1] = -interpretation[abs(p) - 1]
	return "No solution found"


def main() :
	if len(sys.argv) != 2:
		print "Usage: "+ sys.argv[0] +" file.cnf" if "./" in sys.argv[0] else "Usage: ./"+ sys.argv[0] +" file.cnf"
		return None
	formula, nvars = parse( sys.argv[1] )
	solution = walksat( formula, nvars )
	if type(solution) == list :
		solution += [ x for x in range( 1, nvars+1 ) if x not in solution and -x not in solution ]
		solution.sort( key = lambda x : abs(x) )
		print 's SATISFIABLE'
		print 'v ' + ' '.join( [ str(x) for x in solution ] ) + ' 0'
	else :
		# This will never happen because a local search algorithm never ends if the user don't want to
		print 'This should not end if no solution is found'



if __name__ == '__main__':
	main()
