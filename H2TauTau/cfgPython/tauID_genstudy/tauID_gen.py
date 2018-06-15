import os
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption as _getHeppyOption
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer


from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner

def getHeppyOption(option, default):
    opt = _getHeppyOption(option, default)
    if opt in ['False', 'false']:
        opt = False
    return opt


# Get all heppy options; set via '-o production' or '-o production=True'

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production', False)
pick_events = getHeppyOption('pick_events', False)


# Just to be sure
if production:
    pick_events = False




fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True
)

# vertexAna = cfg.Analyzer(
#     VertexAnalyzer,
#     name='VertexAnalyzer',
#     fixedWeight=1,
#     keepFailingEvents=True,
#     verbose=False
# )


from CMGTools.H2TauTau.proto.analyzers.TauIDSelector import TauIDSelector

tauIDSelector = cfg.Analyzer(
    TauIDSelector,
    name='tauIDSelector')

from CMGTools.H2TauTau.proto.analyzers.TauIDTreeProducer import TauIDTreeProducer

tauIDTreeProducer = cfg.Analyzer(
    TauIDTreeProducer,
    name='tauIDTreeProducer'
)

from CMGTools.H2TauTau.proto.analyzers.TestTreeProducer import TestTreeProducer

testTreeProducer = cfg.Analyzer(
    TestTreeProducer,
    name='TestTreeProducer'
)

from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

###################################################
### CONNECT SAMPLES TO THEIR ALIASES AND FILES  ###
###################################################
from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.tauID.tauID_samples import mc_higgs_susy_gg, mc_higgs_susy_bb, QCDPt, DY

# QCD[0].files = QCD[0].files[:4]
for s in mc_higgs_susy_gg + mc_higgs_susy_bb + DY:
    s.is_signal = True

for s in QCDPt:
    s.is_signal = False

samples = mc_higgs_susy_gg#[x for x in  if x.name=='QCD_Pt15to30']#mc_higgs_susy_gg + mc_higgs_susy_bb + DY## [x for x in mc_higgs_susy_gg + mc_higgs_susy_bb if x.name in ['HiggsSUSYBB'+y for y in ['1000','130','1500','2000','2300','250','2900','3200','800']]+['HiggsSUSYGG'+y for y in ['1200','1600','2600','2900','500','80','800']]]# +QCD

# # import pdb;pdb.set_trace()
# from CMGTools.RootTools.samples.test import QCD_Pt300to470_ext
# QCD_Pt300to470_ext.is_signal=False
# samples = [QCD_Pt300to470_ext]

for s in samples:
    s.files = [s.files[0]]

split_factor = 1e4


for sample in samples:
    sample.splitFactor = splitFactor(sample, split_factor)

###################################################
###              ASSIGN PU to MC                ###
###################################################
# for mc in samples:
#     mc.puFileData = puFileData
#     mc.puFileMC = puFileMC
#     if 'PUSpring16' in mc.dataset:
#         print 'Attaching Spring 16 pileup to sample', mc.dataset
#         # mc.puFileData = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/data_pu_25-07-2016_69p2mb_60.root'
#         mc.puFileMC = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Spring16_PU25_Startup_800.root'

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples
# selectedComponents = samples_susy

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = [jsonAna,
            pileUpAna,
            tauIDSelector,
            # tauIDTreeProducer]
            testTreeProducer]
# VertexAna,


# sequence = commonSequence
# if calibrateTaus:
#     sequence.insert(sequence.index(httGenAna), tauP4Scaler)
# sequence.insert(sequence.index(httGenAna)+1, tauTauAna)
# # sequence.insert(sequence.index(genAna), l1Ana)
# # sequence.append(tau1Calibration)
# # sequence.append(tau2Calibration)
# sequence.append(tauDecayModeWeighter)
# sequence.append(tau1Weighter)
# sequence.append(tau2Weighter)
# if syncntuple:
#     sequence.append(tauIDWeighter)
# sequence.append(tauTauMT2Ana)
# sequence.append(metFilter)
# if doSUSY:
#     sequence.insert(sequence.index(mcWeighter) + 1, susyScanAna)
#     sequence.insert(sequence.index(susyScanAna) + 1, susyCounter)
# if computeSVfit:
#     sequence.append(svfitProducer)
# sequence.append(treeProducer)
# if syncntuple:
#     sequence.append(syncTreeProducer)
# if not cmssw:
#     mcWeighter.activate = False

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
if pick_events:
    evtsToPick = [88930, 26229, 66496, 30256, 57121, 75121, 61113]

    eventSelector.toSelect = evtsToPick
    sequence.insert(0, eventSelector)

# # output histogram
outputService = []


###################################################
###            SET BATCH OR LOCAL               ###
###################################################
# if production:
#     # selectedComponents = [selectedComponents[-1]]
#     for comp in selectedComponents:
#         comp.files = [comp.files[0]]
#         comp.files = ['root://cms-xrd-global.cern.ch/'+f[30:] for f in comp.files]
#         # comp.splitFactor = 1
#         # comp.fineSplitFactor = 1

if not production:
    for comp in selectedComponents:
        comp.files = [comp.files[0]]
        # comp.files = ['root://cms-xrd-global.cern.ch/'+f[30:] for f in comp.files]
    selectedComponents = [selectedComponents[-1]]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
    # comp.files = comp.files[13:20]

# preprocessor = None
# if cmssw:
#     sequence.append(fileCleaner)
#     cfg_name = "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_data_cfg.py" if data else "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_cfg.py"
#     preprocessor = CmsswPreprocessor(cfg_name, addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=outputService,
                    preprocessor=None,#preprocessor,
                    events_class=Events
                    )

printComps(config.components, True)
