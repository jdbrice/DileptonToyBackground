
import numpy as np


class EventSim:
	B = np.random.binomial
	M = np.random.multinomial
	P = np.random.poisson
	def setup( self, **kwargs ):
		self.eff_pair = 1.0
		self.eff_pos = 1.0
		self.eff_neg = 1.0
		self.hit_ids = np.zeros(100)
		self.event = None
		
		
		if 'eff_pos' in kwargs:
			self.eff_pos = kwargs['eff_pos']
		if 'eff_neg' in kwargs:
			self.eff_neg = kwargs['eff_neg']

		self.eff_pair = self.eff_pos * self.eff_neg
		
		self.eff_pair_pos = self.eff_pos * (1 - self.eff_neg )
		self.eff_pair_neg = self.eff_neg * (1 - self.eff_pos )
		self.eff_pair_lost = (1 - self.eff_neg) * (1 - self.eff_pos )

		# for a given number of reconstructed pairs:
		self.norm_eff = self.eff_pair_pos + self.eff_pair_neg + self.eff_pair_lost
		self.norm_eff_pair_pos = self.eff_pair_pos / ( self.norm_eff )
		self.norm_eff_pair_neg = self.eff_pair_neg / ( self.norm_eff )
		self.norm_eff_pair_lost = self.eff_pair_lost / ( self.norm_eff )
			
		self.N_true = 10.0
		if 'N_true' in kwargs:
			self.N_true = kwargs['N_true']

		self.N_single_pos = 0.0
		if 'N_single_pos' in kwargs:
			self.N_single_pos = kwargs['N_single_pos']

		self.N_single_neg = 0.0
		if 'N_single_neg' in kwargs:
			self.N_single_neg = kwargs['N_single_neg']

		if 'quiet' in kwargs:
			return
		print("eff_pos =", self.eff_pos)
		print("eff_neg =", self.eff_neg)
		print("eff_pair =", self.eff_pair)
		print("N_true =", self.N_true)
		print("N_single_pos =", self.N_single_pos)
		print("N_single_neg =", self.N_single_neg)
			
	def genEvent( self, **kwargs ):
		self.N_real = self.P(self.N_true)
		self.genRecoPairs( )
		self.genNonRecoPairs( )
		self.genSingles()



	def reset( self):
		self.N_real = 0
		self.n_p = 0
		self.n_plus = 0
		self.n_minus = 0
		self.n_lost = 0 

	def genRecoPairs( self ) :
		# does this make sense, should each positive and neg track be a binomial eff instead of pair being binomial eff
		self.n_p = self.B( self.N_real, self.eff_pair )

	def genNonRecoPairs( self ):    
		#   it takes care of making the last element the remaing p
		m = self.M( self.N_real - self.n_p, [ self.norm_eff_pair_pos, self.norm_eff_pair_neg, self.norm_eff_pair_lost ] )
		self.n_plus = m[0]
		self.n_minus = m[1]
		self.n_lost = m[2]

	def genSingles( self ):
		self.n_plus = self.n_plus + self.B( self.N_single_pos, self.eff_pos )
		self.n_minus = self.n_minus + self.B( self.N_single_neg, self.eff_neg )

	def getSignal(self):
		return self.n_p

	
	def getNPosTracks(self) :
		return self.n_p + self.n_plus
	def getNNegTracks(self) :
		return self.n_p + self.n_minus

	def getNPosPairs(self):
		tn_pos = self.n_p + self.n_plus
		return tn_pos * ( tn_pos - 1 ) / 2.0
	
	def getNNegPairs(self):
		tn_neg = self.n_p + self.n_minus
		return tn_neg * ( tn_neg - 1 ) / 2.0
	
	def getNULSPairs(self):
		return self.n_p*self.n_p + self.n_p * self.n_plus + self.n_p * self.n_minus + self.n_plus * self.n_minus
	
	def getNLSPairs(self):
		return self.getNPosPairs() + self.getNNegPairs()

	def onlyLS(self):
		if self.getNULSPairs() <= 0 :
			return True
		return False
	def onlyPLS(self):
		if self.onlyLS() and self.getNNegPairs() <= 0 :
			return True
		return False
	def onlyNLS(self):
		if self.onlyLS() and self.getNPosPairs() <= 0 :
			return True
		return False

	def summary(self):
		print("N =", self.N_true)
		print("n_p =", self.n_p)
		print("n_plus =", self.n_plus)
		print("n_minus =", self.n_minus)
		print("n_lost =", self.n_lost)

		
def geomMean( i, j ) :
	return 2 * np.sqrt(i) * np.sqrt(j)
