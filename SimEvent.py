
from .SimTrack import SimTrack
import numpy as np

class SimEvent:
    B = np.random.binomial
    M = np.random.multinomial
    P = np.random.poisson

    def reset(self):
        self.tracks = []
        self.n_true_pairs = 0
        self.n_true_pos = 0
        self.n_true_neg = 0
        self.n_pairs = 0
        self.n_pos = 0
        self.n_neg = 0

    def __init__(self):
        self.reset()
    
    def gen(self, n_true_pos, n_true_neg, n_true_pairs):
        self.reset()
        self.n_true_pos = n_true_pos
        self.n_true_neg = n_true_neg
        self.n_true_pairs = n_true_pairs

        self.n_pos = self.B( n_true_pos, 0.04 )
        self.n_neg = self.B( n_true_neg, 0.04 )
        self.n_pairs = self.B(n_true_pairs, 0.04*0.04 )

        # while( self.n_pos + self.n_neg < 2 ):
        #     self.n_pos=self.B(n_true_pos, 0.04)
        #     self.n_neg=self.B(n_true_neg, 0.04 )
        #     self.n_pairs=self.B(n_true_pairs, 0.04 * 0.04)

        for i in np.arange( 0, self.n_pos ):
            self.add_track( 1 )
        for i in np.arange( 0, self.n_neg):
            self.add_track(-1)
        for i in np.arange(0, self.n_pairs):
            self.add_track( 1)
            self.add_track(-1)

        # print( "%d pos, %d neg" % ( self.n_pos, self.n_neg ) )

    def add_track(self, charge):
        hit_ids = [x.hit_id for x in self.tracks ]

        hit_id = np.random.randint(500)
        while ( hit_id in hit_ids ) :
            hit_id = np.random.randint( 500 )
        self.tracks.append( SimTrack( charge, hit_id ) )

    def n_tracks_in(self, charge, hit_id_low, hit_id_high):
        n = 0
        for t in self.tracks:
            if t.charge != charge :
                continue
            if t.hit_id < hit_id_low : 
                continue
            if t.hit_id > hit_id_high : 
                continue
            n = n + 1
        return n