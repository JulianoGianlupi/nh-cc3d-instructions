from cc3d.core.PySteppables import *
import plate_growth_inputs as pgi
import numpy as np

rng = np.random


class CellInitializerSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        self.init_wall()
        seeded = 0

        while seeded < pgi.inital_number_of_cells:
            self.seed_cell_random_location(volume=pgi.cell_volume, randomize_cell_volume=False, fixed_z=1)
            seeded += 1

    def seed_cell_at(self, type, location, volume, randomize_volume=False):
        cell = self.new_cell(type)
        self.cell_field[location[0], location[1], location[2]] = cell
        if not volume:  # assume the volume is to be randomized
            cell.volume = rng.randint(5, 20)

        else:
            cell.targetVolume = volume
            if randomize_volume:
                cell.targetVolume *= (1 + rng.normal(0, 0.5))
        cell.lambdaVolume = pgi.healthy_lambda_volume

    def seed_cell_random_location(self, type=None, volume=0, randomize_cell_volume=False,
                                  fixed_x=False, fixed_y=False, fixed_z=False):

        if type is None:
            type = self.HEALTHY

        location = self.get_random_empty_location()

        if fixed_x or isinstance(fixed_x, int):
            location[0] = fixed_x
        if fixed_y or isinstance(fixed_z, int):
            location[1] = fixed_y
        if fixed_z or isinstance(fixed_z, int):
            location[2] = fixed_z

        self.seed_cell_at(type, location, volume, randomize_volume=randomize_cell_volume)

    def get_random_location(self):
        return [rng.randint(0, self.dim.x), rng.randint(0, self.dim.y), rng.randint(0, self.dim.z)]

    def get_random_empty_location(self):
        occupied = True
        while occupied:
            loc = self.get_random_location()
            occupied = self.cell_field[loc[0], loc[1], loc[2]]
        return loc

    def init_wall(self):
        wall = self.new_cell(self.WALL)
        self.cell_field[:, :, 0] = wall


class GrowthSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        pass
        # for cell in self.cell_list:
        #     cell.targetVolume += 1

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        # field = self.field.CHEMICAL_FIELD_NAME

        # for cell in self.cell_list:
        # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

        # # you can use here any fcn of concentrationAtCOM
        # cell.targetVolume += 0.01 * concentrationAtCOM


class MitosisSteppable(MitosisSteppableBase):
    def __init__(self, frequency=1):
        MitosisSteppableBase.__init__(self, frequency)

    def step(self, mcs):

        cells_to_divide = []
        # for cell in self.cell_list:
        #     if cell.volume>50:
        #         cells_to_divide.append(cell)
        #
        # for cell in cells_to_divide:
        #
        #     self.divide_cell_random_orientation(cell)
        # Other valid options
        # self.divide_cell_orientation_vector_based(cell,1,1,0)
        # self.divide_cell_along_major_axis(cell)
        # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0

        self.clone_parent_2_child()

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 

        if self.parent_cell.type == 1:
            self.child_cell.type = 2
        else:
            self.child_cell.type = 1
