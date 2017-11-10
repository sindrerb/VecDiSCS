import _spectrum
import hyperspy.api as hs
from ase import Atoms
import numpy as np

def saveHyperspy(signal,filename=None):
    if not filename:
        filename=signal.metadata['General']['name']
        filename+"_"

    signal.save(filename+".hspy")

def createSignal(data, eBin, mesh, units = ("eV", "a*", "b*", "c*"), names = ("Energy Loss", "q_a", "q_b", "q_c"), qOffset = (-0.5, -0.5, -0.5), metadata = None):
    """Organize and convert data and axes into a hyperspy signal 
    :param data: the resulting array from simulation
    :param eBin: the energy binning used in simulation
    :param mesh: the k-mesh used in simulation
    :returns: hyperspy signal 
    """

    # REWRITE TO USE DICTIONARIES FOR AXES!
    if not (data.shape[0] == len(eBin)):
        shape = np.asarray(data.shape)
        transposer = tuple(np.hstack([np.where(shape == len(eBin)), np.where(shape != len(eBin))]).tolist()[0])
        data = data.transpose(transposer)
        
    s = hs.signals.BaseSignal(data, metadata=metadata)

    for i in range(len(data.shape)-1):
        name = names[i+1]
        s.axes_manager[2-i].name = name
        s.axes_manager[name].scale = 1/mesh[i]
        s.axes_manager[name].units = units[i+1]
        s.axes_manager[name].offset = qOffset[i]
    i += 1
    name = names[0]
    s.axes_manager[i].name = name
    s.axes_manager[name].scale = eBin[1]-eBin[0]
    s.axes_manager[name].units = units[0]
    s.axes_manager[name].offset = eBin[0]
    s.metadata.Signal.binned = True


    p = s.as_signal1D(-1)
    return p

def createMeta(name=None, title=None, authors=None, notes=None, signal_type=None, elements=None, model=None, cell=None, fermi=None, coordinates=None, effective_masses = None, energy_levels = None):
    """ Generate and organize info into a matadata dictionary recognized by hyperspy
    :returns: nested dictionary of information
    """
    if not name:
        name = "Unnamed_simulation"
    if not title:
        title = name
    if elements:
        symbol = Atoms.get_chemical_symbols()
        for i in range(elements):
            elements[i] = symbol[i]

    description = "Simulated material system\n See 'system' for further information."
    description += "System model: {}\n".format(model)
    if fermi:
        description += "Fermi:{}".format(fermi)

    if effective_masses:
        description += "Effective masses:"
        for i in range(len(effective_masses)):
            description += "m[{}]: {}\n".format(i,effective_masses[i])

    metadata = {}
    metadata['General'] = {}

    metadata['General']['name'] = name
    metadata['General']['title'] = title
    metadata['General']['authors'] = authors
    metadata['General']['notes'] = notes

    metadata['Signal'] = {}
    metadata['Signal']['binned'] = True
    metadata['Signal']['signal_type'] = signal_type

    metadata['Sample'] = {}
    metadata['Sample']['elements'] = elements


    metadata['Sample']['system'] = {}
    metadata['Sample']['system']['model'] = model
    if not cell.any() == None:
        metadata['Sample']['system']['cell'] = {}
        axes = ['a','b','c']
        for i in range(len(cell)):
            metadata['Sample']['system']['cell'][axes[i]] = cell[i]
        
    metadata['Sample']['system']['fermi'] = fermi

    if effective_masses:
        metadata['Sample']['system']['effective_masses'] = effective_masses
    if coordinates:
        metadata['Sample']['system']['coordinates'] = coordinates
    if energy_levels:
        metadata['Sample']['system']['energy_levels'] = energy_levels
    if elements:
        metadata['Sample']['system']['elements'] = elements
    
    metadata['Sample']['description'] = description

    return metadata



def calculate_spectrum(data_structre, energy_binning, fermi_energy, brillouinZone=np.eye(3), temperature=298):
    """Calculating multi-dimensional spectrum of a band diagram
    :param data_structure: A tuple of:
                           - meshgrid (3x1 tuple with number of k-points in each dimension)
                           - k_list (nested list of equivalent k-points)
                           - Energy array (ndarray with energies for each unique k-point, one column for each band)
                           - Wave array (ndarray with wave vectors for each unique k-point and band)
    :param energy_binning: A one dimensional ndarray of energy bins. NB. must be equally binned
    :param fermi_energy: The fermi energy of the system, all final states is above, all initial states are below
    :param temperature: the themperature of the system
    :returns: A four dimensional histogram of energy transfer with corresponding moment transfer
    """

    temperature = temperature*(0.0259/298)

    A = _spectrum.calculate_spectrum(data_structre, energy_binning, brillouinZone, fermi_energy, temperature)
    return A
