from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from ROOT import TFile, TTree
import numpy as np
import random

class TestTreeProducer(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TestTreeProducer,self).__init__(cfg_ana, cfg_comp, looperName)
        self.outservicename = getattr(cfg_ana,"outservicename","outputfile")

    def beginLoop(self, setup):
        super(TestTreeProducer, self).beginLoop(setup)
        fileName = '/'.join([self.dirName,
                             'tree.root'])
        isCompressed = self.cfg_ana.isCompressed if hasattr(self.cfg_ana,'isCompressed') else 1
        print 'Compression', isCompressed
        self.file = TFile( fileName, 'recreate', '', isCompressed )
        self.file.cd()
        self.tree = TTree('tree',self.name)
        self.p4varlist = ['px','py','pz','energy','pdgId','charge']#,'p','pt','mass','rapidity','eta','theta','phi'] ###add hadronflavour and partonflavor for jets !!!
        self.genericjetvarlist = ['numberOfDaughters']
        self.jetvarlist = ['hadronFlavour','partonFlavour']
        if hasattr(self.cfg_ana, 'nptcs') and self.cfg_ana.nptcs:
            self.nptcs = self.cfg_ana.nptcs
        else:
            self.nptcs = 200
        self.ptcvarlist = ['dxy','dz']
        self.branchdict = {'Jet':np.zeros((1,9)),'RawJet':np.zeros((1,6)),'GenJet':np.zeros((1,7)),'ptcs':np.zeros((self.nptcs,8)),'genptcs':np.zeros((self.nptcs,8)),'Tau':np.zeros((1,6)),'GenTau':np.zeros((1,6))}
        self.singlevarBranchDict = {'event':np.zeros(3),'dRs':np.zeros(4),'standardID':np.zeros(6)}
        for name in self.branchdict:
            self.tree.Branch(name, self.branchdict[name], name+'['+str(len(self.branchdict[name]))+']['+str(len(self.branchdict[name][0]))+']/D')
        for name in self.singlevarBranchDict:
            self.tree.Branch(name, self.singlevarBranchDict[name], name+'['+str(len(self.singlevarBranchDict[name]))+']/D')

    def process(self, event):
        
        for jet in event.jets:
            self.reset()
            i = 0
            for index ,var in enumerate(self.p4varlist):
                self.branchdict['Jet'][0,i] = eval('jet.'+var+'()')
                for j in range(self.nptcs):
                    if jet.daughter(j):
                        self.branchdict['ptcs'][j,i] = eval('jet.daughter('+str(j)+').'+var+'()')
                self.branchdict['RawJet'][0,i] = eval('jet.correctedJet(0).'+var+'()')
                if hasattr(jet,'gen_jet') and jet.gen_jet:
                    self.branchdict['GenJet'][0,i] = eval('jet.gen_jet.'+var+'()')
                    for j in range(self.nptcs):
                        if jet.gen_jet.daughter(j):
                            self.branchdict['genptcs'][j,i] = eval('jet.gen_jet.daughter('+str(j)+').'+var+'()')
                if hasattr(jet,'gen_tau') and jet.gen_tau:
                    self.branchdict['GenTau'][0,i] = eval('jet.gen_tau.'+var+'()')
                if hasattr(jet,'tau') and jet.tau:
                    self.branchdict['Tau'][0,i] = eval('jet.tau.'+var+'()')
                i += 1
            iptc = i
            for index, var in enumerate(self.ptcvarlist):
                 for j in range(self.nptcs):
                    if jet.daughter(j):
                        self.branchdict['ptcs'][j,iptc] = eval('jet.daughter('+str(j)+').'+var+'()')
                    if hasattr(jet,'gen_jet') and jet.gen_jet:
                        if jet.gen_jet.daughter(j):
                            self.branchdict['genptcs'][j,iptc] = eval('jet.gen_jet.daughter('+str(j)+').'+var+'()')
                 iptc+=1
            ijets = i
            for index, var in enumerate(self.genericjetvarlist):
                self.branchdict['Jet'][0,ijets] = eval('jet.'+var+'()')
                if hasattr(jet,'gen_jet') and jet.gen_jet:
                    self.branchdict['GenJet'][0,ijets] = eval('jet.gen_jet.'+var+'()')
                ijets+=1
            ijet = ijets
            for index, var in enumerate(self.jetvarlist):
                self.branchdict['Jet'][0,ijet] = eval('jet.'+var+'()')
                ijet+=1
            self.singlevarBranchDict['event'][0] = event.eventId
            self.singlevarBranchDict['event'][1] = event.lumi
            self.singlevarBranchDict['event'][2] = event.run
            if hasattr(jet,'gen_tau') and jet.gen_tau:
                self.singlevarBranchDict['dRs'][0] = jet.gen_tau_dr
                if hasattr(jet,'tau_gen_reco_dr') and jet.tau_gen_reco_dr:
                    self.singlevarBranchDict['dRs'][1] = jet.tau_gen_reco_dr
                if hasattr(jet, 'gen_jet') and hasattr(jet, 'genjet_gentau_dr') and jet.genjet_gentau_dr:
                    self.singlevarBranchDict['dRs'][2] = jet.genjet_gentau_dr
            if hasattr(jet,'tau_dr') and jet.tau_dr:
                self.singlevarBranchDict['dRs'][3] = jet.tau_dr
            if hasattr(jet,'tau') and jet.tau:
                self.singlevarBranchDict['standardID'][0] = jet.tau.tauID('byIsolationMVArun2v1DBoldDMwLTraw')
                self.singlevarBranchDict['standardID'][1] = jet.tau.tauID('decayModeFinding')
                self.singlevarBranchDict['standardID'][2] = jet.tau.leadChargedHadrCand().dz()
                self.singlevarBranchDict['standardID'][3] = jet.tau.tauID('againstElectronVLooseMVA6')
                self.singlevarBranchDict['standardID'][4] = jet.tau.tauID('againstMuonLoose3')
                self.singlevarBranchDict['standardID'][5] = jet.tau.decayMode()
            # import pdb;pdb.set_trace()
            self.tree.Fill()
        

    def write(self, setup):
        super(TestTreeProducer, self).write(setup)
        if self.outservicename not in setup.services:
            self.file.Write() 

    def reset(self):
        for name in self.branchdict:
            self.branchdict[name].fill(0.)
        for name in self.singlevarBranchDict:
            self.singlevarBranchDict[name].fill(0.)
            
