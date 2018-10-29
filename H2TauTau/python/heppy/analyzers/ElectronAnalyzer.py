from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Electron import Electron

class ElectronAnalyzer(Analyzer):

    def declareHandles(self):
        super(ElectronAnalyzer, self).declareHandles()

        self.handles['electrons'] = AutoHandle(
            self.cfg_ana.electrons,
            'std::vector<pat::Electron>'
        )
        
    def process(self, event):
        self.readCollections(event.input)
        electrons = self.handles['electrons'].product()
        output_electrons = []
        for electron in electrons:
            helectron = Electron(electron)
            # helectron.associatedVertex = event.vertices[0]
            helectron.event = event.input.object()
            # helectron.rho = event.rho
            output_electrons.append(helectron)
        setattr(event, self.cfg_ana.output, output_electrons)
        
