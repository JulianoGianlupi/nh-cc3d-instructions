
from cc3d import CompuCellSetup
        


from plate_growthSteppables import CellInitializerSteppable

CompuCellSetup.register_steppable(steppable=CellInitializerSteppable(frequency=1))




from plate_growthSteppables import GrowthSteppable

CompuCellSetup.register_steppable(steppable=GrowthSteppable(frequency=1))




from plate_growthSteppables import MitosisSteppable

CompuCellSetup.register_steppable(steppable=MitosisSteppable(frequency=1))


CompuCellSetup.run()
