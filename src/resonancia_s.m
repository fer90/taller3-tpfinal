%% res_s y res_p son celdas donde cada posición tiene una matriz con 3 filas:
 % nbi, nz, m, y con tantas columnas como soluciones.
 % ds es la lista de valores para barrer d' (x ej, para barrer d' desde 1 hasta 100, con pasos de a 5: ds = 1:5:100
 % También ds puede ser un sólo valor, x ej: ds = 1000)
function [res_s, res_p] = resonancia(na, nbr, nc, ds)
tic		% inicia cronómetro para contabilizar el tiempo total de ejecución
    nz_0 = 0;							% nz mínimo
    nz_1 = min([na, nbr, nc]);			% nz máximo
    res_s = cell(1,length(ds));			% crea celdas para los resultados del modo s. Una celda por cada valor de d.
    res_p = cell(1,length(ds));			% crea celdas para los resultados del modo p. Una celda por cada valor de d.
    i=0;
    for d = ds
        i=i+1;
        res_s{i} = resonancia_modo_s(na, nbr, nc, nz_0, nz_1, d);	% resuelve las resonancias para modo s con d fijo y lo guarda en la celda correspondiente
        res_p{i} = resonancia_modo_p(na, nbr, nc, nz_0, nz_1, d);	% resuelve las resonancias para modo p con d fijo y lo guarda en la celda correspondiente
    end
toc		% imprime el tiempo total de ejecución
end

%% resonancia_modo_s
function res = resonancia_modo_s(na, nbr, nc, nz_0, nz_1, d)
    nbi_0 = fzero(@(nbi) eq1s(na,nbr,nbi,nc,nz_0,d), [0 nbr]);	% halla nbi_0 como solución de f1 = 0 usando nz = nz_0
    nbi_1 = fzero(@(nbi) eq1s(na,nbr,nbi,nc,nz_1,d), [0 nbr]);	% halla nbi_1 como solución de f1 = 0 usando nz = nz_1
    
    m_0 = fzero(@(m) eq2s(na, nbr, nbi_0, nc, nz_0, m, d), 0);	% halla m_0 como solución de f2 = 0 usando nz = nz_0 y nbi = nbi_0
    m_1 = fzero(@(m) eq2s(na, nbr, nbi_1, nc, nz_1, m, d), 0);	% halla m_1 como solución de f2 = 0 usando nz = nz_1 y nbi = nbi_1
    
    m_0 = ceil(m_0);	% construye la lista
    m_1 = floor(m_1);	% de números enteros
    ms = m_0:1:m_1;		% ms en el intervalo
%     ms = ms(ms~=0);		% (m_0, m_1)
    
    res = zeros(3,2*length(ms));			% reserva memoria para resultados parciales res
    options=optimset('Display','off');
    
    i = 0;
	for m = ms		% barre la lista ms
        [sol0,~,exitflag0,~] = fsolve(@(y) eqs12_s(na, nbr, nc, m, d, y), [nbi_0 + 0.4*(nbi_1 - nbi_0), nz_0 + 0.4*(nz_1 - nz_0)], options);	% halla solución del sistema f1 = 0, f2 = 0 con condición inicial con r = 0.4
        if (exitflag0 > 0 && sol0(1) > 0 && sol0(1) < nbr && sol0(2) > nz_0 && sol0(2) <= nz_1)		% chequea si la solución es admisible (exitflag > 0 indica que fsolve convergió a una solución del sistema de ecuaciones). sol(1) es nbi y sol(2) es nz
            i = i+1;
            res(1:2,i) = sol0;		% guarda soluciones en la matriz de resultados parciales
            res(3,i) = m;
        end
        [sol1,~,exitflag1,~] = fsolve(@(y) eqs12_s(na, nbr, nc, m, d, y), [nbi_0 + 0.9*(nbi_1 - nbi_0), nz_0 + 0.9*(nz_1 - nz_0)], options);	% halla solución del sistema f1 = 0, f2 = 0 con condición inicial con r = 0.9
		if (norm(sol0 - sol1) > 1e-6 && exitflag1 > 0 && sol1(1) > 0 && sol1(1) < nbr && sol1(2) > nz_0 && sol1(2) <= nz_1)		% chequea si la solución es admisible (la primer condición chequea que la solución sea distinta a la encontrada con r = 0.4). sol(1) es nbi y sol(2) es nz
			i = i+1;
			res(1:2,i) = sol1;		% guarda soluciones en la matriz de resultados parciales
			res(3,i) = m;
		end
	end
	res = res(:,1:i);	% descarta el espacio no utilizado de la matriz
end

%% resonancia_modo_p
function res = resonancia_modo_p(na, nbr, nc, nz_0, nz_1, d)
    nbi_0 = fzero(@(nbi) eq1p(na,nbr,nbi,nc,nz_0,d), [0 nbr]);
    nbi_1 = fzero(@(nbi) eq1p(na,nbr,nbi,nc,nz_1,d), [0 nbr]);
    
    m_0 = fzero(@(m) eq2p(na, nbr, nbi_0, nc, nz_0, m, d), 0);
    m_1 = fzero(@(m) eq2p(na, nbr, nbi_1, nc, nz_1, m, d), 0);
    
    m_0 = ceil(m_0);
    m_1 = floor(m_1);
    ms = m_0:1:m_1;
%     ms = ms(ms~=0);

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

%% Sistema de ecuaciones 1 y 2, modo s. y es un vector cuyas componentes son nbi y nz: y(1) = nbi, y(2) = nz.
function res = eqs12_s(na, nbr, nc, m, d, y)
    nnbx = nbx(nbr, y(1), y(2));
    pps = ps(na, nbr, y(1), nc, y(2));
    res = [log(abs(pps)) + 4*pi*imag(nnbx)*d; ...
           angle(pps) - 4*pi*real(nnbx)*d - 2*pi*m];
end

%% Sistema de ecuaciones 1 y 2, modo p. y es un vector cuyas componentes son nbi y nz: y(1) = nbi, y(2) = nz.
function res = eqs12_p(na, nbr, nc, m, d, y)
    nnbx = nbx(nbr, y(1), y(2));
    ppp = pp(na, nbr, y(1), nc, y(2));
    res = [log(abs(ppp)) + 4*pi*imag(nnbx)*d; ...
           angle(ppp) - 4*pi*real(nnbx)*d - 2*pi*m];
end

%% Ecuación 1: igualdad de módulos, modo s
function res = eq1s(na, nbr, nbi, nc, nz, d)
    res = log(abs(ps(na, nbr, nbi, nc, nz))) + 4*pi*imag(nbx(nbr, nbi, nz))*d;
end

%% Ecuación 1: igualdad de módulos, modo p
function res = eq1p(na, nbr, nbi, nc, nz, d)
    res = log(abs(pp(na, nbr, nbi, nc, nz))) + 4*pi*imag(nbx(nbr, nbi, nz))*d;
end

%% Ecuación 2: ecuación de fases, modo s
function res = eq2s(na, nbr, nbi, nc, nz, m, d)
    res = angle(ps(na, nbr, nbi, nc, nz)) - 4*pi*real(nbx(nbr, nbi, nz))*d - 2*pi*m;
end

%% Ecuación 2: ecuación de fases, modo p
function res = eq2p(na, nbr, nbi, nc, nz, m, d)
    res = angle(pp(na, nbr, nbi, nc, nz)) - 4*pi*real(nbx(nbr, nbi, nz))*d - 2*pi*m;
end

%% rho perpendicular: ps
function res = ps(na, nbr, nbi, nc, nz)
    nnbx = nbx(nbr,nbi,nz);
    nnax = sqrt(na^2 - nz^2);
    nncx = sqrt(nc^2 - nz^2);
    res = ( (nnbx + nnax) * (nnbx + nncx) ) /...
          ( (nnbx - nnax) * (nnbx - nncx) );
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
