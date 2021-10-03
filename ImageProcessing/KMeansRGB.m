% This function iteratively calls the AssignToCluster and UpdateMeans functions in
% order to operate the k-means algorithim. When the clusters are no longer
% changing at each iteration, or after a specificed maximum number of iterations, 
% the process is terminated. 
% Inputs
% image: The 3D array containing the RGB values of each pixel in the image
% seedMeans: kx1x3 array containing the RGB values of the seed means
% maxIterations: the maximum number of Iterations before stopping
% Outputs
% clusters: a mxn array containing the cluster number that each pixel has been assigned
% means:  kx1x3 array containing the RGB values of the final cluster means
% Author: Alec van Helsdingen

function [clusters,means]=KMeansRGB(image,seedMeans,maxIterations)

k=size(seedMeans,1); % get value of k
means=seedMeans; % set means initially to be the seed means
oldMeans=seedMeans; % this will be the means at the prior iteration
numberIterations=0; % set up count of iterations so far

while numberIterations<maxIterations
    [clusters]=AssignToClusters(image,means);
    [means]=UpdateMeans(image,k,clusters);
    if means==oldMeans % when the clusters have converged
        disp(['Iteration ' num2str(numberIterations+1)]);
        numberIterations=maxIterations+1; % exits while loop
    else
        numberIterations=numberIterations+1;
        disp(['Iteration ' num2str(numberIterations)]);
        oldMeans=means; % oldMeans is now the means of the previous iteration
    end
end

if numberIterations==maxIterations
    disp('Maximum number of iterations reached before convergence was achieved')
end

end

    
    
        