function [leave] = findleave(Bmatrix, as, xb)
% Given entering column as and vector xb of basic variables
% findleave finds a leaving column of basis matrix Bmatrix
% It returns leave=0 if no column can be found (i.e. unbounded)
% leave=p indicates that the pth column of B leaves basis



m=size(Bmatrix,1);
ratios=NaN(m,1);

%Calculate Binv*as first, the denominator of the ratios
denom=inv(Bmatrix)*as;

% Calculate xb/Binv*as ratios

for i=1:m
    if denom(i,1)>0 %Only calculate if denominator is positive
        ratios(i,1)=xb(i,1)/denom(i,1);
    end
end


[min_ratio,index]=min(ratios); % Get index of minimum ratio

if isnan(min_ratio) % No positive denominator=unbounded problem
    leave=0;
else
    leave=index;
end



end
    
