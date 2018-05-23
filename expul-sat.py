#!/usr/bin/python
import sys, random, operator

positive_positions = []
negative_positions = []
unsat_clauses = []

def parse(filename) :
	formula = []
	unsat_lits = []
	clause_position = 0
	for line in open( filename ) :
		if line.startswith( 'c' ) : continue
		if line.startswith( 'p' ) :
			nvars, nclauses = line.split()[2:4]
			for x in xrange(int(nvars)):
				positive_positions.append([])
				negative_positions.append([])
			sat_lits = [3] * int(nclauses)
			continue
		clause = [ int(x) for x in line[:-2].split() ]
		formula.append(clause)
		for literal in clause:
			if literal < 0:
				negative_positions[abs(literal) - 1].append(clause_position)

			else:
				positive_positions[literal - 1].append(clause_position)
		clause_position += 1
	return formula, int(nvars), sat_lits, int(nclauses)

def rnd_interpretation(formula, nvars, prob = 0.5):
	interpretation = []
	for var in xrange(1, nvars + 1):
		if random.random() < prob: interpretation.append(var * -1)
		else: interpretation.append(var)
	return interpretation

def satisfies(formula, sat_lits, unsat_clauses):
	unsat_clauses = [formula[pos] for pos, n in enumerate(sat_lits) if n == 0]
	return (False, unsat_clauses) if unsat_clauses else (True, unsat_clauses)

def update_sat_lits(interpretation, sat_lits, nclauses):
	sat_lits = [3] * nclauses
	for literal in interpretation:
		if literal < 0:
			for pos in positive_positions[abs(literal) - 1]:
				sat_lits[pos] -= 1
		else:
			for pos in negative_positions[literal - 1]:
				sat_lits[pos] -= 1
	return sat_lits

def broken_clauses(S, nvars, sat_lits, nclauses):
	broken_clauses = [nclauses] * nvars
	for literal in S:
		if literal < 0:
			for pos in positive_positions[abs(literal) - 1]:
				if sat_lits[pos] - 1 == 0:
					broken_clauses[abs(literal) - 1] += 1
		else:
			for pos in negative_positions[literal - 1]:
				if sat_lits[pos] - 1 == 0:
					broken_clauses[literal - 1] += 1
	return broken_clauses

def walksat(formula, nvars, sat_lits, nclauses, max_tries = sys.maxint, max_flips = 10, w = 0.5):
	interpretation = []
	C = []
	S = []
	unsat_clauses = []
	for i in xrange(max_tries):
		interpretation = rnd_interpretation(formula, nvars)
		for j in xrange(nvars * 2):
			sat_lits = update_sat_lits(interpretation, sat_lits, nclauses)
			satisfiable, unsat_clauses = satisfies(formula, sat_lits, unsat_clauses)
			if satisfiable: return interpretation
			C = random.choice(unsat_clauses)
			# S <- set of variables that appear in C
			S = list(C)
			# b <- min({broken(p,F,I) | p in S})
			bc = broken_clauses(S, nvars, sat_lits, nclauses)
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
	formula, nvars, sat_lits, nclauses = parse( sys.argv[1] )
	solution = walksat( formula, nvars, sat_lits, nclauses )
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
