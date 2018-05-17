from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet, GenJet
from PhysicsTools.HeppyCore.utils.deltar import bestMatch, deltaR
import math

class TauIDSelector(Analyzer):
    '''Selects events containing either genjets or gen hadronictaus 
    ptThreshold = pt threshold for either hadronic taus or jets'''

    def declareHandles(self):
        super(TauIDSelector, self).declareHandles()

        # self.mchandles['genInfo'] = AutoHandle(('generator','',''), 'GenEventInfoProduct' )

        self.mchandles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')
        self.mchandles['genParticles'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle')

        self.handles['jets'] = AutoHandle('slimmedJets',
                                          'std::vector<pat::Jet>')
        self.handles['taus'] = AutoHandle('slimmedTaus', 'std::vector<pat::Tau>')
        # self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>')

    def process(self, event):
        self.readCollections(event.input)

        taus = self.handles['taus'].product()
        miniaodjets = self.handles['jets'].product()

        allJets = [Jet(jet) for jet in miniaodjets]

        jets = [jet for jet in allJets if jet.pt()>30.]
        
        genJets = map(GenJet, self.mchandles['genJets'].product())
        event.genParticles = self.mchandles['genParticles'].product()

        event.gentaus = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.pt()>30. and p.statusFlags().isPrompt() and not any(abs(self.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(self.getFinalTau(p).numberOfDaughters()))]
        
        if len(jets)==0 and len(event.gentaus)==0:
            return False

        for jet in jets:
            gen_jet, gen_jet_dr2 = bestMatch(jet, genJets)
            jet.gen_jet = gen_jet
            jet.gen_jet_dr = math.sqrt(gen_jet_dr2)

        for tau in event.gentaus:
            jet, jet_dr2 = bestMatch(tau, jets)
            if jet is not None:
                reco_tau, reco_tau_dr2 = bestMatch(tau, taus)
                if reco_tau is not None and jet is not None:
                    jet.tau_gen_reco_dr = math.sqrt(reco_tau_dr2)
                jet.gen_tau = tau
                jet.gen_tau_dr = math.sqrt(jet_dr2)
                if jet.gen_jet:
                    jet.genjet_gentau_dr = deltaR(tau, jet.gen_jet)
        for tau in taus:
            jet, jet_dr2 = bestMatch(tau, jets)
            if jet is not None:
                jet.tau = tau
                jet.tau_dr = math.sqrt(jet_dr2)
        
            
            #add old tau id
        event.jets = jets
        # import pdb;pdb.set_trace()
        
        
        # for ptc in jets:
        #     if ptc.pt()>self.cfg_ana.ptThreshold:
        #         return True
        # for ptc in event.gentaus:
        #     if ptc.pt()>self.cfg_ana.ptThreshold:
        #         return True
        # return False

    @staticmethod
    def getFinalTau(tau):
        for i_d in xrange(tau.numberOfDaughters()):
            if tau.daughter(i_d).pdgId() == tau.pdgId():
                return TauIDSelector.getFinalTau(tau.daughter(i_d))
        return tau        
