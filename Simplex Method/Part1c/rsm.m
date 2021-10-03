function [z, x, pi, indices, exitflag] = rsm(A, b, c, m, n)
% Solves min cx s.t. Ax=b, x>=0
% exitflag is 0 if solved successfully, 1 if infeasible, and -1 if unbounded
% Performs a Phase I procedure starting with an all artificial basis
% and then calls function simplex with modified leaving variable
% criterion in Phase II


% Phase I- finding a bfs



costs=zeros(n,1); %Zero costs for real variables
indices=linspace(n+1,n+m,m)'; %All-artifical basis

IBmatrix=eye(m); %Identity matrix is initial Basis, and inverse is also identity matrix

[z,x,pi,indices,~, IBmatrix]=simplex1c(A,b,costs,m,n,IBmatrix,indices,1);


if z==0 %Indicates a feasible solution exists
    
    
    % Phase II- solving the original problem
    
    [z,x,pi,indices,exitflag, ~]=simplex1c(A,b,c,m,n,IBmatrix,indices,2);
    
    
else %Infeasible problem
    exitflag=1;
end

end