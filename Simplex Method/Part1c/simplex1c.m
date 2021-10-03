function [z, x, pi, indices, exitflag, IBmatrix] = simplex1c(A, b, c, m, n, IBmatrix, indices, phase)
% Solves min cx s.t. Ax=b, x>=0
% starting with basic variables listed in vector indices
% and basis matrix Bmatrix
% exitflag is 0 if solved successfully, -1 if unbounded
% returns optimal vector x and its value z, along with pi, and indices of basic variables

% Initialize for 1st loop

% Create vector of basic costs
cb=zeros(m,1);

for i=1:m
    if indices(i)<=n
        cb(i,1)=c(indices(i),1);
    else %artifical variable still in basis
        if phase==2
            cb(i,1)=0;
        else %phase 1
            cb(i,1)=1;
        end
    end
end
exitflag=0;


while true
    
    %calculate pi and xb
    
    
    pi=(cb'*IBmatrix)';
    xb=IBmatrix*b;
    
    
    % Entering variable
    % Only use costs of real variables
    [as,cs,s]=findenter1c(A,pi,c,indices,n,m);
    
    if s==0 %Optimal
        break
    end
    
    %Leaving variable
    p=findleave1c(IBmatrix,as,xb, indices, phase, n);
    
    if p==0 %unbounded
        exitflag=-1;
        break
    end
    
    
    
    
    % update inverse of B matrix, indices and cb
    
    [IBmatrix,indices,cb]=updateGJ(IBmatrix,indices,cb,cs,as,s,p);
    
    
end

%Once optimal solution found, find objective function

z=cb'*xb;

% Create x vector

x=zeros(n,1);

for i=1:m
    if indices(i)<=n %Do not add any remaining artifical variables to x vector
        x(indices(i),1)=xb(i);%Copy values of all basic variables
    end 
end


end