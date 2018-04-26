import sys, random, operator

def parse(filename) :
	formula = []
	for line in open( filename ) :
		if line.startswith( 'c' ) : continue
		if line.startswith( 'p' ) :
			nvars, nclauses = line.split()[2:4]
			continue
		clause = [ int(x) for x in line[:-2].split() ]
		formula.append(clause)
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

def rnd_interpretation(formula, nvars):
	sign = ['', '-']
	interpretation = []
	for i in xrange(nvars):
		interpretation.append(random.choice(sign) + 'i')
	return interpretation

#def satisfies(interpretation, formula):


def walksat(formula, assignment, nvars, max_tries = 1000, max_flips = 1000):
	interpretation = []
	for i in xrange(max_tries):
		interpretation = rnd_interpretation(formula, nvars)
		print interpretation
		for j in xrange(max_flips):
			if satisfies(interpretation,formula):
				return interpretation

	
	return "No solution found"		


def main() :
	if len(sys.argv) != 2: 
		print "Usage: "+ sys.argv[0] +" file.cnf" if "./" in sys.argv[0] else "Usage: ./"+ sys.argv[0] +" file.cnf"  
		return None
	formula, nvars = parse( sys.argv[1] )
	solution = walksat( formula, [], nvars )
	if solution :
		solution += [ x for x in range( 1, nvars+1 ) if x not in solution and -x not in solution ]
		solution.sort( key = lambda x : abs(x) )
		print 's SATISFIABLE'
		print 'v ' + ' '.join( [ str(x) for x in solution ] ) + ' 0'
	else :
		print 's UNSATISFIABLE'



if __name__ == '__main__':
	main()
