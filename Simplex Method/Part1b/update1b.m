function [newBmatrix, newindices, newcb] = update1b(Bmatrix, indices, cb, cs, as, s, leave)
% Bmatrix is current m by m basis matrix
% indices is a column vector current identifiers for basic variables in
% order of B columns
% cb is a column vector of basic costs in the order of B columns
% as is the entering column
% s is the index of the entering variable
% leave is the column (p) of the basis matrix that must leave
% (not its variable index t)
% update replaces column leave of Bmatrix with as to give newBmatrix
% replaces row leave of indices with enter to give newindices
% replaces row leave of cb with cs to give newcb


%Column of zeros, with 1 in position (p) of leaving variable

ep=zeros(length(as),1);
ep(leave,1)=1;

%Add and subtract columns

added_column=as*ep';
removed_column=(Bmatrix*ep)*ep';

newBmatrix=Bmatrix+added_column-removed_column;

%Adjust cb vector
newcb=cb;
newcb(leave)=cs;

%Adjust indices

newindices=indices;
newindices(leave)=s;



end