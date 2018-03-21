
from . import  EventSim
import numpy as np

class ToyExp :

	es = EventSim.EventSim()

	N_events = 0
	events = np.zeros(1)


	def setup( self, **kwargs ):
		self.es.setup( **kwargs )

	def makeArrays( self ):
		self.events = np.arange( self.N_events )
		
		self.hit_ids = []
		self.n_sig = np.zeros( self.N_events )
		self.n_uls = np.zeros( self.N_events )
		self.n_ls = np.zeros( self.N_events )
		self.n_ls_pos = np.zeros( self.N_events )
		self.n_ls_neg = np.zeros( self.N_events )
		self.n_tr_pos = np.zeros( self.N_events )
		self.n_tr_neg = np.zeros( self.N_events )

		self.avg_uls    = np.zeros( self.N_events )
		self.avg_ls     = np.zeros( self.N_events )
		self.avg_ls_pos = np.zeros( self.N_events )
		self.avg_ls_neg = np.zeros( self.N_events )
		self.avg_tr_pos = np.zeros( self.N_events )
		self.avg_tr_neg = np.zeros( self.N_events )

		self.ta_uls    = np.zeros( self.N_events )
		self.ta_ls     = np.zeros( self.N_events )
		self.ta_ls_pos = np.zeros( self.N_events )
		self.ta_ls_neg = np.zeros( self.N_events )
		self.ta_tr_pos = np.zeros( self.N_events )
		self.ta_tr_neg = np.zeros( self.N_events )

		self.t_uls    = 0
		self.t_ls     = 0
		self.t_ls_pos = 0
		self.t_ls_neg = 0
		self.t_tr_pos = 0
		self.t_tr_neg = 0

		self.n_evt_only_ls     = 0
		self.n_evt_only_ls_pos = 0
		self.n_evt_only_ls_neg = 0
		self.n_evt_has_ls      = 0
		self.n_evt_has_uls     = 0
		self.n_evt_only_uls    = 0


	def throw( self, N_events, trigger=None ) :
		self.N_events = N_events
		self.makeArrays()

		if "dimuon" == trigger:
			print( "dimuon trigger mode" )
		if "noisydimuon" == trigger:
			print( "noisy dimuon trigger mode" )
		if "muon" == trigger:
			print( "muon trigger mode" )
		if "noisymuon" == trigger:
			print( "noisy muon trigger mode" )
		self.n_thrown = 0
		for iEvt in self.events :
			self.es.reset()
			
			if "dimuon" == trigger:
				while self.es.getNPosTracks() + self.es.getNNegTracks() < 2 : # like a perfect dimuon trigger
					self.es.genEvent()
					self.n_thrown = self.n_thrown + 1
			elif "noisydimuon" == trigger:
				while (self.es.getNPosTracks() + self.es.getNNegTracks() < 2 and np.random.rand() < 0.9 ) : 
					self.es.genEvent()
					self.n_thrown = self.n_thrown + 1
			elif "muon" == trigger:
				while (self.es.getNPosTracks() + self.es.getNNegTracks() < 1 ) : # like a perfect single-muon trigger
					self.es.genEvent()
					self.n_thrown = self.n_thrown + 1
			elif "noisymuon" == trigger:
				while (self.es.getNPosTracks() + self.es.getNNegTracks() < 1 and np.random.rand() < 0.9 ) : 
					self.es.genEvent()
					self.n_thrown = self.n_thrown + 1
			else :
				self.es.genEvent()
				self.n_thrown = self.n_thrown + 1
			
			# keepEvent = False
			# if self.es.getNPosTracks() + self.es.getNNegTracks() >= 1 :
			# 	keepEvent = True
			# while False == keepEvent :
			# 	self.es.genEvent()
			# 	if self.es.getNPosTracks() + self.es.getNNegTracks() >= 1 :
			# 		keepEvent = True
			
				
			self.hit_ids.append( self.es.hit_ids )
			self.n_tr_pos [ iEvt ] = self.es.getNPosTracks()
			self.n_tr_neg [ iEvt ] = self.es.getNNegTracks()
			self.n_ls_pos [ iEvt ] = self.es.getNPosPairs()
			self.n_ls_neg [ iEvt ] = self.es.getNNegPairs()
			self.n_ls     [ iEvt ] = self.es.getNLSPairs()
			self.n_uls    [ iEvt ] = self.es.getNULSPairs()
			self.n_sig    [ iEvt ] = self.es.n_p

			self.t_tr_pos = self.t_tr_pos + self.es.getNPosTracks()
			self.t_tr_neg = self.t_tr_neg + self.es.getNNegTracks()
			self.t_ls_pos = self.t_ls_pos + self.es.getNPosPairs()
			self.t_ls_neg = self.t_ls_neg + self.es.getNNegPairs()
			self.t_ls     = self.t_ls     + self.es.getNLSPairs()
			self.t_uls    = self.t_uls    + self.es.getNULSPairs()


			self.ta_tr_pos [ iEvt ] = self.t_tr_pos
			self.ta_tr_neg [ iEvt ] = self.t_tr_neg
			self.ta_ls_pos [ iEvt ] = self.t_ls_pos
			self.ta_ls_neg [ iEvt ] = self.t_ls_neg
			self.ta_ls     [ iEvt ] = self.t_ls
			self.ta_uls    [ iEvt ] = self.t_uls

			self.avg_tr_pos [ iEvt ] = self.t_tr_pos / float( iEvt + 1 )
			self.avg_tr_neg [ iEvt ] = self.t_tr_neg / float( iEvt + 1 )
			self.avg_ls_pos [ iEvt ] = self.t_ls_pos / float( iEvt + 1 )
			self.avg_ls_neg [ iEvt ] = self.t_ls_neg / float( iEvt + 1 )
			self.avg_ls     [ iEvt ] = self.t_ls     / float( iEvt + 1 )
			self.avg_uls    [ iEvt ] = self.t_uls    / float( iEvt + 1 )

			if ( self.n_ls[ iEvt ] > 0 ) :
				self.n_evt_has_ls += 1
			if ( self.n_uls[ iEvt ] > 0 ) :
				self.n_evt_has_uls += 1

			if ( 0 == self.n_uls[ iEvt ] and self.n_ls[ iEvt ] > 0) :
				self.n_evt_only_ls += 1
				if ( 0 == self.n_ls_neg[ iEvt ] ) :
					self.n_evt_only_ls_pos += 1
				if ( 0 == self.n_ls_pos[ iEvt ] ) :
					self.n_evt_only_ls_neg += 1
			if ( 0 == self.n_ls[ iEvt ] and self.n_uls[ iEvt ] > 0 ) :
				self.n_evt_only_uls += 1
			






