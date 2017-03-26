
function [h_2_4, h_5_3] = field_s(na, nbr, nbi, nc, nz, d)

	nbx = nbr - i * nbi
	na_2 = na^2
	nc_2 = nc^2
	nbx_2 = nbx^2
	nz_2 = nz^2
	nax = sqrt(na_2 - nz_2)
	ncx = sqrt(nc_2 - nz_2)
	alpha = exp(2 * pi * i * nbx * d)
	epsilon_b_a = nbx_2 / na_2
	epsilon_b_c = nbx_2 / nc_2

	numerador = (2 * alpha * nbx)
	h_2_4 = numerador / (nbx + nax)
	h_5_3 = numerador / (nbx + ncx)

end