from collections import defaultdict
import random 

def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i


class CFG(object):
    def __init__(self, grammar = defaultdict(list)):
        self.prod = grammar.copy()

    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def prune(self, terminal_list, level = 5):
        done = False
        l = 0
        while not done and l < level:
            done = True
            non_terminal = []
            for lhs in self.prod:
                non_terminal.append(lhs)
                
            for lhs in self.prod:
                new_rule = []
                for rhs in  self.prod[lhs]:
                    exclude = False
                    for el in rhs:
                        #print(":::  -> "+el,terminal_list,el in terminal_list)
                        if (not (el in terminal_list)) and (not (el in non_terminal)):
                            exclude = True
                            done = False
                            break
                    if not exclude:
                        new_rule.append(rhs)
                        
                self.prod[lhs] = new_rule
            
            #recreate the dictionary without empty rules
            new_prod = defaultdict(list)
            for lhs in self.prod:
                if len(self.prod[lhs]) !=0:
                    new_prod[lhs] = self.prod[lhs]
                    
            self.prod = new_prod
            l+=1
        
    def print_grammar(self):
        for lhs in self.prod:
            outstr = "{:s} ->".format(lhs)
            for rhs in  self.prod[lhs]:
                for el in rhs:
                    outstr += el+ " " 
                outstr += " | "
            print(outstr)
    
    def gen_random(self, symbol ):
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        sentence = ''
        root =[]
        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sent,node = self.gen_random(sym)
                sentence += sent
                root.append(node)
            else:
                sentence += sym + ' '
                root.append(sym)

        return sentence, root


    def gen_random_convergent(self,
          symbol,
          cfactor=0.25,
          pcount=defaultdict(int)
      ):
      """ Generate a random sentence from the
          grammar, starting with the given symbol.

          Uses a convergent algorithm - productions
          that have already appeared in the
          derivation on each branch have a smaller
          chance to be selected.

          cfactor - controls how tight the
          convergence is. 0 < cfactor < 1.0

          pcount is used internally by the
          recursive calls to pass on the
          productions that have been used in the
          branch.
      """
      sentence = ''
      root = []
      # The possible productions of this symbol are weighted
      # by their appearance in the branch that has led to this
      # symbol in the derivation
      #
      weights = []
      for prod in self.prod[symbol]:
          if prod in pcount:
              weights.append(cfactor ** (pcount[prod]))
          else:
              weights.append(1.0)

      rand_prod = self.prod[symbol][weighted_choice(weights)]

      # pcount is a single object (created in the first call to
      # this method) that's being passed around into recursive
      # calls to count how many times productions have been
      # used.
      # Before recursive calls the count is updated, and after
      # the sentence for this call is ready, it is rolled-back
      # to avoid modifying the parent's pcount.
      #
      pcount[rand_prod] += 1

      for sym in rand_prod:
          # for non-terminals, recurse
          if sym in self.prod:
              sent,node = self.gen_random_convergent(
                                  sym,
                                  cfactor=cfactor,
                                  pcount=pcount)
              sentence += sent
              root.append((sym,node))
                    
          else:
              sentence += sym + ' '
              root.append((sym,))


      # backtracking: clear the modification to pcount
      pcount[rand_prod] -= 1
      return sentence, root
