%% res_p es una celda donde cada posición tiene una matriz con 3 filas:
 % nbi, nz, m, y con tantas columnas como soluciones.
function [res_p] = resonancia_p(na, nbr, nc, d, m_0, m_1)
tic		% inicia cronómetro para contabilizar el tiempo total de ejecución
    nz_0 = 0;							% nz mínimo
    nz_1 = min([na, nbr, nc]);			% nz máximo
    res_p = cell(1,1);			% crea celdas para los resultados del modo p
    res_p{1} = resonancia_modo_p(na, nbr, nc, nz_0, nz_1, d, m_0, m_1);	% resuelve las resonancias para modo p con d fijo y lo guarda en la celda correspondiente
toc		% imprime el tiempo total de ejecución
end

%% resonancia_modo_p
function res = resonancia_modo_p(na, nbr, nc, nz_0, nz_1, d, m_0, m_1)
    nbi_0 = fzero(@(nbi) eq1p(na,nbr,nbi,nc,nz_0,d), [0 nbr]);
    nbi_1 = fzero(@(nbi) eq1p(na,nbr,nbi,nc,nz_1,d), [0 nbr]);

    ms = m_0:1:m_1;

    res = zeros(3,2*length(ms));
    options=optimset('Display','off');
    i = 0;
    
	for m = ms
        [sol0,~,exitflag0,~] = fsolve(@(y) eqs12_p(na, nbr, nc, m, d, y), [nbi_0 + 0.4*(nbi_1 - nbi_0), nz_0 + 0.4*(nz_1 - nz_0)], options);	% halla solución del sistema f1 = 0, f2 = 0 con condición inicial con r = 0.4
		if (exitflag0 > 0 && sol0(1) > 0 && sol0(1) < nbr && sol0(2) > nz_0 && sol0(2) <= nz_1)		% chequea si la solución es admisible (exitflag > 0 indica que fsolve convergió a una solución del sistema de ecuaciones). sol(1) es nbi y sol(2) es nz
            i = i+1;
            res(1:2,i) = sol0;	% guarda soluciones en la matriz 
            res(3,i) = m;		% de resultados parciales
		end
        [sol1,~,exitflag1,~] = fsolve(@(y) eqs12_p(na, nbr, nc, m, d, y), [nbi_0 + 0.9*(nbi_1 - nbi_0), nz_0 + 0.9*(nz_1 - nz_0)], options);	% halla solución del sistema f1 = 0, f2 = 0 con condición inicial con r = 0.9
        if (norm(sol0 - sol1) > 1e-6 && exitflag1 > 0 && sol1(1) > 0 && sol1(1) < nbr && sol1(2) > nz_0 && sol1(2) <= nz_1)		% chequea si la solución es admisible (la primer condición chequea que la solución sea distinta a la encontrada con r = 0.4). sol(1) es nbi y sol(2) es nz
			i = i+1;
			res(1:2,i) = sol1;	% guarda soluciones en la matriz 
			res(3,i) = m;		% de resultados parciales
        end
	end
	res = res(:,1:i);	% descarta el espacio no utilizado de la matriz
end

%% Sistema de ecuaciones 1 y 2, modo p. y es un vector cuyas componentes son nbi y nz: y(1) = nbi, y(2) = nz.
function res = eqs12_p(na, nbr, nc, m, d, y)
    nnbx = nbx(nbr, y(1), y(2));
    ppp = pp(na, nbr, y(1), nc, y(2));
    res = [log(abs(ppp)) + 4*pi*imag(nnbx)*d; ...
           angle(ppp) - 4*pi*real(nnbx)*d - 2*pi*m];
end

%% Ecuación 1: igualdad de módulos, modo p
function res = eq1p(na, nbr, nbi, nc, nz, d)
    res = log(abs(pp(na, nbr, nbi, nc, nz))) + 4*pi*imag(nbx(nbr, nbi, nz))*d;
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
