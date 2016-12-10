
function [m_0, m_1] = m_range_s(na, nbr, nc, d)

    nz_0 = 0;							% nz mínimo
    nz_1 = min([na, nbr, nc]);			% nz máximo

    nbi_0 = fzero(@(nbi) eq1s(na,nbr,nbi,nc,nz_0,d), [0 nbr]);	% halla nbi_0 como solución de f1 = 0 usando nz = nz_0
    nbi_1 = fzero(@(nbi) eq1s(na,nbr,nbi,nc,nz_1,d), [0 nbr]);	% halla nbi_1 como solución de f1 = 0 usando nz = nz_1

    m_0 = fzero(@(m) eq2s(na, nbr, nbi_0, nc, nz_0, m, d), 0);	% halla m_0 como solución de f2 = 0 usando nz = nz_0 y nbi = nbi_0
    m_1 = fzero(@(m) eq2s(na, nbr, nbi_1, nc, nz_1, m, d), 0);	% halla m_1 como solución de f2 = 0 usando nz = nz_1 y nbi = nbi_1
    
    m_0 = int8(ceil(m_0));	% construye la lista
    m_1 = int8(floor(m_1));	% de números enteros

end

%% Ecuación 1: igualdad de módulos, modo s
function res = eq1s(na, nbr, nbi, nc, nz, d)
    res = log(abs(ps(na, nbr, nbi, nc, nz))) + 4*pi*imag(nbx(nbr, nbi, nz))*d;
end

%% Ecuación 2: ecuación de fases, modo s
function res = eq2s(na, nbr, nbi, nc, nz, m, d)
    res = angle(ps(na, nbr, nbi, nc, nz)) - 4*pi*real(nbx(nbr, nbi, nz))*d - 2*pi*m;
end

%% rho perpendicular: ps
function res = ps(na, nbr, nbi, nc, nz)
    nnbx = nbx(nbr,nbi,nz);
    nnax = sqrt(na^2 - nz^2);
    nncx = sqrt(nc^2 - nz^2);
    res = ( (nnbx + nnax) * (nnbx + nncx) ) /...
          ( (nnbx - nnax) * (nnbx - nncx) );
end

%% nbx es la proyección del "vector" nb en la dirección x. Es complejo, parte real positiva y parte imaginaria negativa.
function res = nbx(nbr, nbi, nz)
    res = sqrt((nbr - 1i*nbi)^2 - nz^2);
end
