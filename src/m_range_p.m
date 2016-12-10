
function [m_0, m_1] = m_range_p(na, nbr, nc, d)

    nz_0 = 0;							% nz mínimo
    nz_1 = min([na, nbr, nc]);			% nz máximo

    nbi_0 = fzero(@(nbi) eq1p(na,nbr,nbi,nc,nz_0,d), [0 nbr]);
    nbi_1 = fzero(@(nbi) eq1p(na,nbr,nbi,nc,nz_1,d), [0 nbr]);

    m_0 = fzero(@(m) eq2p(na, nbr, nbi_0, nc, nz_0, m, d), 0);
    m_1 = fzero(@(m) eq2p(na, nbr, nbi_1, nc, nz_1, m, d), 0);
    
    m_0 = int8(ceil(m_0));
    m_1 = int8(floor(m_1));

end

%% Ecuación 1: igualdad de módulos, modo p
function res = eq1p(na, nbr, nbi, nc, nz, d)
    res = log(abs(pp(na, nbr, nbi, nc, nz))) + 4*pi*imag(nbx(nbr, nbi, nz))*d;
end

%% Ecuación 2: ecuación de fases, modo p
function res = eq2p(na, nbr, nbi, nc, nz, m, d)
    res = angle(pp(na, nbr, nbi, nc, nz)) - 4*pi*real(nbx(nbr, nbi, nz))*d - 2*pi*m;
end

%% rho paralelo: pp
function res = pp(na, nbr, nbi, nc, nz)
    Na = (nbr - 1i*nbi)^2 / (na^2);
    Nc = (nbr - 1i*nbi)^2 / (nc^2);
    nnbx = nbx(nbr,nbi,nz);
    nnax = sqrt(na^2 - nz^2);
    nncx = sqrt(nc^2 - nz^2);
    res = ( (nnbx + Na*nnax) * (nnbx + Nc*nncx) ) /...
          ( (nnbx - Na*nnax) * (nnbx - Nc*nncx) );
end

%% nbx es la proyección del "vector" nb en la dirección x. Es complejo, parte real positiva y parte imaginaria negativa.
function res = nbx(nbr, nbi, nz)
    res = sqrt((nbr - 1i*nbi)^2 - nz^2);
end
