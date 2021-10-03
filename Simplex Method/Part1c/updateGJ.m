function [IBmatrix, indices, cb] = updateGJ(IBmatrix, indices, cb, cs, as, s, leave)

% updates inverse matrix of B using Gauss-Jordan elimination


y=IBmatrix*as;

yp=y(leave,1);

%Divide pth row by yp
IBmatrix(leave,:)=IBmatrix(leave,:)/yp;

for i=1:size(IBmatrix,1) %for all rows excepth the pth
    if i~=leave
        IBmatrix(i,:)=IBmatrix(i,:)-y(i,1)*IBmatrix(leave,:); %subtract yi*pth row of Binv
    end
end

%Adjust cb vector
cb(leave)=cs;

%Adjust indices

indices(leave)=s;

end




