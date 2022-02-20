#https://stackoverflow.com/questions/22229796/choose-at-random-from-combinations

# Problemstellung: Prüfern sollen Prüflinge zugeordent werden, sodass die Arbeit eines jeden Prüflings eine bestimmte Anzahl oft gelesen wird
# inter rater reliabilität soll optimiert werden, daher mögichst zufällige Zuordnung um Cluster zu vermeiden
# möglicherweise geht das auch deterministisch, hier wird zunächst die Zufällige Zuordnung probeirt

import random
import numpy as np
random.seed(42)

def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)

# todo: examiners könnten noch namentlich bleiben
def random_fair_assignment(candidates=20, examiners=4, examiners_per_candidate=2):
	# opt = np.floor(candidates/examiners*examiners_per_candidate) + 1
	unfairness = 2 # Unterschied der maximalen und minimalen Arbeitslast
	combinations = list()
	while unfairness > 1:
		# wähle für jeden Prüfling eine zufällige Auswahl aus den Prüfern
		combinations = np.array([list(random_combination(range(examiners), examiners_per_candidate)) for i in range(candidates)])
		# zähle, wie oft jeder Examiner arbeiten muss
		counts = np.unique( combinations.ravel(), return_counts=True )[1]
		# falls einer zu viel arbeitet -> nochmal ( ein Unterschied von 1 ist möglich, wenn die Parameter nicht passen)
		unfairness = counts.max() - counts.min()
	return combinations

# Idee: ändere nur die Zuordnungen, die den unfairen Effekt verstärken
def almost_random_fair_assignment(candidates=20, examiners=4, examiners_per_candidate=2):
	combinations = np.array([list(random_combination(range(examiners), examiners_per_candidate)) for i in range(candidates)])
#
	# unfair?
	counts = np.unique( combinations.ravel(), return_counts=True )[1]
	unfairness = counts.max() - counts.min()
	unfair = unfairness > 1
	while unfair:
		n = counts.argmax()
		ind = random.sample( list(np.where(combinations == n)[0]), 1)	# must succeed, since it's unfair
		combinations[ind[0]] = random_combination(range(examiners), examiners_per_candidate)
		counts = np.unique( combinations.ravel(), return_counts=True )[1]
		#print(counts, ind)
		unfairness = counts.max() - counts.min()
		unfair = unfairness > 1
	return combinations


# todo: update several at once
def efficient_almost_random_fair_assignment(candidates=20, examiners=4, examiners_per_candidate=2):
	combinations = np.array([list(random_combination(range(examiners), examiners_per_candidate)) for i in range(candidates)])
#
	# unfair?
	counts = np.unique( combinations.ravel(), return_counts=True )[1]
	unfairness = counts.max() - counts.min()
	unfair = unfairness > 1
	while unfair:
		n = counts.argmax()
		ind = np.where(combinations == n)[0]
		#print(ind)
		combinations[ind] = np.array([list(random_combination(range(examiners), examiners_per_candidate)) for i in range(len(ind))])
		counts = np.unique( combinations.ravel(), return_counts=True )[1]
		#print(counts, ind)
		unfairness = counts.max() - counts.min()
		unfair = unfairness > 1
	return combinations


# Wenn ich darüber nachdenke, sollte sowas gehen, obwohl ich nicht weiß, ob das die Idee von Maurice ist:
# 1. Wenn die Aufteilung nicht genau augehen sollte (also nicht jeder aus B gleich viel bekommt), würfle aus, welche Teilmenge von B 1 mehr bekommt als die anderen. Anschließend weiß man also für jede Person in B, wie oft sie zugeordnet wird.
# 2. Erstelle eine Liste mit je 2 Kopien jeder Person in A und permutiere zufällig.
# 3. Erstelle eine Liste mit k_i Kopien jeder Person i in B, wobei k_i die Anzahl der Zuordnungen für Person i sind.
# 4. Diese Listen haben gleichviele Einträge. Ordne die entsprechenden Einträge der Listen einander zu.
# 5. Wenn eine Person aus A zweimal derselben Person zugeordnet ist, verwerfe und wiederhole.

def rene_random_fair_assignment(candidates=20, examiners=4, examiners_per_candidate=2):
	unfair = True
	k_opt = candidates * examiners_per_candidate // examiners
	#while unfair:
	canarr = np.random.permutation( list(range(candidates)) * examiners_per_candidate)	
	examinarr = np.random.permutation( list(range(examiners)) * k_opt)
	# sort by row
	both = np.array( (canarr,examinarr))
	sort = both[:, both[0, :].argsort()]
	arr = sort[1].reshape(-1,2)
	print(sort)
	# jetzt sollte in jeder Zeile nichts doppelt vorkommen
	unfair = np.apply_along_axis(
        lambda x: len(set(x)) != len(x), axis=1, arr=foo[1].reshape(-1, 2)
    ).any()
	return ( sort)



