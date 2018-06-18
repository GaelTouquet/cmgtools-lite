from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.average import Average

class TauFakeRateWeighter( Analyzer ):
    '''Gets tau decay mode efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauFakeRateWeighter,self).__init__(cfg_ana, cfg_comp, looperName)

            
    def beginLoop(self, setup):
        print self, self.__class__
        super(TauFakeRateWeighter,self).beginLoop(setup)
        self.averages.add('weight', Average('weight') )

    def process(self, event):
        self.weight = 1.

        # print 'FR weighter', self.cfg_comp.name
        sampleNames = []
        # Not strictly correct, but this is agreed upon for Summer 2013:
        for name in sampleNames:
            if self.cfg_comp.name.startswith(name):
                tauPt = event.diLepton.leg1().pt()
                if tauPt > 200.:
                    tauPt = 200.

                # self.weight =  1.15743 +  (-0.00736136) * tauPt + (4.3699e-05) * tauPt * tauPt + (-1.188e-07) * tauPt * tauPt * tauPt
                self.weight =  1. +  0. * tauPt + 0. * tauPt * tauPt + 0. * tauPt * tauPt * tauPt

        event.tauFakeRateWeightUp = self.weight + 0.5 * (1. - self.weight)
        event.tauFakeRateWeightDown = self.weight - 0.5 * (1. - self.weight)

        #event.eventWeight *= self.weight
        event.tauFakeRateWeight = self.weight

        if self.cfg_ana.verbose:
            print 'TauFakeRateWeighter', event.diLepton.leg1().pt(), self.cfg_comp.name, self.weight

        self.averages['weight'].add( self.weight )
        return True
                
