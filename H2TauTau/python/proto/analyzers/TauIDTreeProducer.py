from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase

class TauIDTreeProducer(H2TauTauTreeProducerBase):

    # def vector(self, tree, varName, maxlen, type=float, storageType="default"):
    #     tree.vector(varName, '', maxlen=maxlen, type=type, storageType=storageType)

    # def bookJet(self, tree, p_name, fill_extra=False):
    #     super(TauIDTreeProducer, self).bookJet(tree, p_name, fill_extra=fill_extra)
        

    def declareVariables(self, setup):

        # to find the event again
        self.var(self.tree, 'run')
        self.var(self.tree, 'lumi')
        self.var(self.tree, 'event')

        # declare jet + constituents
        self.bookParticle(self.tree, 'Jet')
        self.var(self.tree, 'Jet_nconstituents')
        self.var(self.tree, 'Jet_hadronFlavour')
        self.var(self.tree, 'Jet_partonFlavour')
        for i in range(200):
            self.bookParticle(self.tree, 'ptc_{}'.format(i))
            self.var(self.tree, 'ptc_{}_pdgid'.format(i))
            self.var(self.tree, 'ptc_{}_dxy'.format(i))
            self.var(self.tree, 'ptc_{}_dz'.format(i))
            self.var(self.tree, 'ptc_{}_e'.format(i))
            self.bookParticle(self.tree, 'GenJet_ptc_{}'.format(i))
            self.var(self.tree, 'GenJet_ptc_{}_pdgid'.format(i))
            self.var(self.tree, 'GenJet_ptc_{}_dxy'.format(i))
            self.var(self.tree, 'GenJet_ptc_{}_dz'.format(i))
            self.var(self.tree, 'GenJet_ptc_{}_e'.format(i))
        self.bookParticle(self.tree, 'GenJet')
        self.var(self.tree, 'GenJet_nconstituents')
        self.var(self.tree, 'GenJet_dR')

        #eventual tau and gentau
        self.bookParticle(self.tree, 'Tau')
        self.bookParticle(self.tree, 'GenTau')
        self.var(self.tree, 'GenTau_dR')
        self.var(self.tree, 'GenTau_tau_dR')
        self.var(self.tree, 'Jet_tau_dR')
        self.var(self.tree, 'GenJet_GenTau_dR')
        self.var(self.tree, 'decayModeFinding')
        self.var(self.tree, 'Tau_leadChargedHadrCand_dz')
        self.var(self.tree, 'againstElectronVLooseMVA6')
        self.var(self.tree, 'againstMuonLoose3')
        self.var(self.tree, 'byIsolationMVArun2v1DBoldDMwLTraw')
        self.var(self.tree, 'byTightIsolationMVArun2v1DBoldDMwLT')
        self.var(self.tree, 'byVTightIsolationMVArun2v1DBoldDMwLT')
        self.var(self.tree, 'byMediumIsolationMVArun2v1DBoldDMwLT')
        self.var(self.tree, 'byLooseIsolationMVArun2v1DBoldDMwLT')
        self.var(self.tree, 'byVLooseIsolationMVArun2v1DBoldDMwLT')

        #other useful
        self.var(self.tree, 'isSignal')
        # self.var(self.tree, 'nPU')
        
        # declare taugenjet + constituents
        
    def process(self, event):
        self.readCollections(event.input)

        # self.tree.reset()
        # import pdb;pdb.set_trace()
        # self.fill(self.tree, 'event', event.eventId)
        # self.fill(self.tree, 'lumi', event.lumi)   
        # self.fill(self.tree, 'run', event.run)
        # self.fillTree(event)

        # turn over the jets of the event
        for jet in event.jets:
            isSignal = (hasattr(jet,'gen_tau') and jet.gen_tau and jet.gen_tau_dr<0.3)
            if self.cfg_comp.is_signal and (not isSignal):
                continue # skip if is a jet in signal sample
            if (not self.cfg_comp.is_signal) and isSignal:
                continue # skip if is a genuine tau in QCD sample

            self.tree.reset()

            self.fill(self.tree, 'event', event.eventId)
            self.fill(self.tree, 'lumi', event.lumi)   
            self.fill(self.tree, 'run', event.run)
            
            self.fillParticle(self.tree, 'Jet', jet)
            # import pdb;pdb.set_trace()
            ndaughter = jet.numberOfDaughters()
            self.fill(self.tree, 'Jet_nconstituents', ndaughter)
            if hasattr(jet, 'hadronFlavour') and jet.hadronFlavour():
                self.fill(self.tree, 'Jet_hadronFlavour', jet.hadronFlavour())
            if hasattr(jet, 'partonFlavour') and jet.partonFlavour():
                self.fill(self.tree, 'Jet_partonFlavour', jet.partonFlavour())
            if ndaughter>200:
                ndaughter=200
            for i in range(ndaughter):
                if jet.daughter(i):
                    self.fillParticle(self.tree, 'ptc_{}'.format(i), jet.daughter(i))
                    self.fill(self.tree, 'ptc_{}_pdgid'.format(i), jet.daughter(i).pdgId())
                    self.fill(self.tree, 'ptc_{}_dxy'.format(i), jet.daughter(i).dxy())
                    self.fill(self.tree, 'ptc_{}_dz'.format(i), jet.daughter(i).dz())
                    self.fill(self.tree, 'ptc_{}_e'.format(i), jet.daughter(i).energy())

                
            if hasattr(jet,'gen_jet') and jet.gen_jet:
                genjet = jet.gen_jet
                self.fillParticle(self.tree, 'GenJet', genjet)
                ndaughter = genjet.numberOfDaughters()
                self.fill(self.tree, 'GenJet_nconstituents', ndaughter)
                if ndaughter>200:
                    ndaughter=200
                for i in range(ndaughter):
                    if genjet.daughter(i):
                        self.fillParticle(self.tree, 'GenJet_ptc_{}'.format(i), genjet.daughter(i))
                        self.fill(self.tree, 'GenJet_ptc_{}_pdgid'.format(i), genjet.daughter(i).pdgId())
                        self.fill(self.tree, 'GenJet_ptc_{}_dxy'.format(i), genjet.daughter(i).dxy())
                        self.fill(self.tree, 'GenJet_ptc_{}_dz'.format(i), genjet.daughter(i).dz())
                        self.fill(self.tree, 'GenJet_ptc_{}_e'.format(i), genjet.daughter(i).energy())
                self.fill(self.tree, 'GenJet_dR', jet.gen_jet_dr)
            
            if hasattr(jet,'gen_tau') and jet.gen_tau:
                self.fillParticle(self.tree, 'GenTau', jet.gen_tau)
                self.fill(self.tree, 'GenTau_dR',jet.gen_tau_dr)
                if hasattr(jet,'tau_gen_reco_dr') and jet.tau_gen_reco_dr:
                    self.fill(self.tree, 'GenTau_tau_dR', jet.tau_gen_reco_dr)
                if hasattr(jet, 'gen_jet') and hasattr(jet, 'genjet_gentau_dr') and jet.genjet_gentau_dr:
                    self.fill(self.tree, 'GenJet_GenTau_dR', jet.genjet_gentau_dr)
                    
            if hasattr(jet,'tau') and jet.tau:
                self.fillParticle(self.tree, 'Tau', jet.tau)
                if hasattr(jet,'tau_dr') and jet.tau_dr:
                    self.fill(self.tree, 'Jet_tau_dR', jet.tau_dr)
                self.fill(self.tree, 'byTightIsolationMVArun2v1DBoldDMwLT', jet.tau.tauID('byTightIsolationMVArun2v1DBoldDMwLT'))
                self.fill(self.tree, 'byVTightIsolationMVArun2v1DBoldDMwLT', jet.tau.tauID('byVTightIsolationMVArun2v1DBoldDMwLT'))
                self.fill(self.tree, 'byMediumIsolationMVArun2v1DBoldDMwLT', jet.tau.tauID('byMediumIsolationMVArun2v1DBoldDMwLT'))
                self.fill(self.tree, 'byLooseIsolationMVArun2v1DBoldDMwLT', jet.tau.tauID('byLooseIsolationMVArun2v1DBoldDMwLT'))
                self.fill(self.tree, 'byVLooseIsolationMVArun2v1DBoldDMwLT', jet.tau.tauID('byVLooseIsolationMVArun2v1DBoldDMwLT'))
                self.fill(self.tree, 'byIsolationMVArun2v1DBoldDMwLTraw', jet.tau.tauID('byIsolationMVArun2v1DBoldDMwLTraw'))
                self.fill(self.tree, 'decayModeFinding', jet.tau.tauID('decayModeFinding'))
                self.fill(self.tree, 'Tau_leadChargedHadrCand_dz', jet.tau.leadChargedHadrCand().dz())
                self.fill(self.tree, 'againstElectronVLooseMVA6', jet.tau.tauID('againstElectronVLooseMVA6'))
                self.fill(self.tree, 'againstMuonLoose3', jet.tau.tauID('againstMuonLoose3'))

            if hasattr(jet,'gen_tau') and jet.gen_tau and jet.gen_tau_dr<0.3:
                self.fill(self.tree, 'isSignal', 1.)
            else:
                self.fill(self.tree, 'isSignal', 0.)

            # if hasattr(event, 'nPU') and event.nPU:
            #     self.var(self.tree, 'nPU')

            self.fillTree(event)
