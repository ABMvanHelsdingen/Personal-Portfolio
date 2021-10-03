function [leave] = findleave1b(Bmatrix, as, xb, indices, phase, n)
% Given entering column as and vector xb of basic variables
% findleave finds a leaving column of basis matrix Bmatrix
% It returns leave=0 if no column can be found (i.e. unbounded)
% leave=p indicates that the pth column of B leaves basis



    

m=size(Bmatrix,1);
ratios=NaN(m,1);

%Calculate Binv*as first
denom=inv(Bmatrix)*as;

% Calculate xb/Binv*as ratios

artifical=false; %Boolean for if an artifical variable is to be removed

for i=1:m
    if phase==2 && indices(i)>n % artifical variable remaining in basis in phase 2
        if denom(i,1)~=0
            leave=i;
            artifical=true;
            break %No need to check the other variables
        end
    end
    if denom(i,1)>0 %Only calculate if denominator is positive
        ratios(i,1)=xb(i,1)/denom(i,1);
    end
end

if ~artifical %Only if leaving variable is not artifical
    
    [min_ratio,index]=min(ratios); % Get index of minimum ratio
    
    if isnan(min_ratio) % No positive denominator=unbounded problem
        leave=0;
    else
        leave=index;
    end
    
end

end
    