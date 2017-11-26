def pack_values(mesh,k_grid, e_array,w_array):
	if (mesh.shape[0] != 3):
		raise IndexError("Mesh must be 3x1")
		return None
	grid_length = k_grid.len()
	if (e_array.shape[0] != grid_length):
		if(e_array.shape[1] == grid_length):
			e_array = e_array.T
		else:
			raise IndexError("No dimension in e_array match length of k_grid")
			return None
	if (w_array.shape[0] != grid_length or w_array.shape[1] != grid_length or w_array.shape[2] != grid_length):
			raise IndexError("No dimension in w_array match length of k_grid")
			return None
	return (mesh, k_grid, e_array, w_array)
