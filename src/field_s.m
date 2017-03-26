
function [e_2_4, e_5_3] = field_s(na, nbr, nbi, nc, nz, d)

	nbx = nbr - i * nbi
	nz_2 = nz^2
	nax = sqrt(na^2 - nz_2)
	ncx = sqrt(nc^2 - nz_2)
	alpha = exp(2 * pi * i * nbx * d)

	numerador = (2 * alpha * nbx)
	e_2_4 = numerador / (nbx + nax)
	e_5_3 = numerador / (nbx + ncx)

end