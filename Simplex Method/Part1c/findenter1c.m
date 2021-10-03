function [as, cs, s] = findenter1c(Amatrix, pi, c, indices, n, m)
% Given the complete m by n matrix Amatrix,
% the complete cost vector c with n components
% the vector pi with m components
% findenter finds the index of the entering variable and its column
% It returns the column as, its cost coefficient cs, and index s
% Returns s=0 if no entering variable can be found (i.e.  optimal)
% This will happen when minimum reduced cost> tolerance% where tolerance = -1.0E-6


%Create list of non-basic variables
non_basic=linspace(1,n,n);

% Delete all basic indices from the list
for i=1:m
    basic=indices(i);
    non_basic=non_basic(non_basic~=basic);
    
end

%Delete columns relating to basic variables from A and c
Amatrix=Amatrix(:,non_basic);
c=c(non_basic);



reduced_costs=c'-(pi'*Amatrix); % rs=cs-(pi)T*as
[min_r, index]=min(reduced_costs);

if min_r>=-0.000001 % If all reduced costs are non-negative (subject to tolerance), solution is optimal
    s=0;
    as=[]; %Empty arrays- won't be used by other functions
    cs=[];
    
else % Most negative reduced cost is entering variable
    
    as=Amatrix(:,index);
    cs=c(index);
    s=non_basic(index); %returns original index
    
    
end