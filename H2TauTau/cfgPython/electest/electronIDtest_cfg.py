import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps

from PhysicsTools.HeppyCore.framework.event import Event
Event.print_patterns = ['*taus*', '*muons*', '*electrons*', 'veto_*', 
                        '*dileptons_*', '*jets*']



#components
from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
import CMGTools.H2TauTau.proto.samples.fall17.higgs as higgs
index=ComponentIndex(higgs)
comp = index.glob('HiggsVBF125')[0]
# comp.files = ['root://lyogrid06.in2p3.fr//dpm/in2p3.fr/home/cms/data/store/mc/RunIIFall17MiniAODv2/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/088E7A46-F442-E811-A227-A0369FD0B282.root']
comp.files = ['/home/cms/touquet/CMSSW/modular/CMSSW_9_4_11_cand1/src/CMGTools/H2TauTau/cfgPython/preproc/elecIDv2_events.root']
comp.splitFactor = 1
comp.fineSplitFactor = 1
selectedComponents = [comp]


#analyzers


from CMGTools.H2TauTau.heppy.analyzers.ElectronAnalyzer import ElectronAnalyzer
electrons = cfg.Analyzer(
    ElectronAnalyzer,
    output = 'electrons',
    electrons = 'slimmedElectrons',
)


from CMGTools.H2TauTau.heppy.analyzers.Debugger import Debugger
debugger = cfg.Analyzer(
    Debugger,
    name = 'Debugger',
    condition = lambda x: True
)

sequence = [electrons, debugger]


from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)
