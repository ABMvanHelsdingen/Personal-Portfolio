function [z, x, pi, indices, exitflag] = simplex(A, b, c, m, n, Bmatrix, indices)
% Solves min cx s.t. Ax=b, x>=0
% starting with basic variables listed in vector indices
% and basis matrix Bmatrix
% exitflag is 0 if solved successfully, -1 if unbounded
% returns optimal vector x and its value z, along with pi, and indices of basic variables

% Initialize for 1st loop
cb=c(indices);
exitflag=0;

while true
    
    % Calculate xb and pi
    
    Binv=inv(Bmatrix);
    
    pi=(cb'*Binv)';
    xb=Binv*b;
    
    
    %Entering variable
    [as,cs,s]=findenter(A,pi,c);
    
    if s==0 %Optimal
        break
    end
    
    %Leaving variable
    p=findleave(Bmatrix,as,xb);
    
    if p==0 %unbounded
        exitflag=-1;
        break
    end
    
    
    
    % update B matrix, indices and cb
    
    [Bmatrix,indices,cb]=update(Bmatrix,indices,cb,cs,as,s,p);
    
    
    
end

%Once optimal solution found, find objective function

z=cb'*xb;

% Create x vector

x=zeros(n,1);

for i=1:m
    x(indices(i),1)=xb(i); %Copy values of all basic variables
end


end





