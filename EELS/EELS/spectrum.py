import _spectrum
import hyperspy.api as hs
import numpy as np

def saveHyperspy(filename, data, eBin, mesh, units = ("eV", "a*", "b*", "c*"), names = ("Energy Loss", "q_a", "q_b", "q_c"), qOffset = (-0.5, -0.5, -0.5)):

    # Force energy axis as zero axis

    if not (data.shape[0] == len(eBin)):
        shape = np.asarray(data.shape)
        transposer = tuple(np.hstack([np.where(shape == len(eBin)), np.where(shape != len(eBin))]).tolist()[0])
        data = data.transpose(transposer)
        
    s = hs.signals.BaseSignal(data)



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
    p.save(filename+".hspy")


def calculate_spectrum(data_structre, energy_binning, fermi_energy):
    """Calculating multi-dimensional spectrum of a band diagram
    :param data_structure: A tuple of:
                           - meshgrid (3x1 tuple with number of k-points in each dimension)
                           - k_list (nested list of equivalent k-points)
                           - Energy array (ndarray with energies for each unique k-point, one column for each band)
                           - Wave array (ndarray with wave vectors for each unique k-point and band)
    :param energy_binning: A one dimensional ndarray of energy bins. NB. must be equally binned
    :param fermi_energy: The fermi energy of the system, all final states is above, all initial states are below
    :returns: A four dimensional histogram of energy transfer with corresponding moment transfer
    """
    A = _spectrum.calculate_spectrum(data_structre, energy_binning, fermi_energy)
    return A
