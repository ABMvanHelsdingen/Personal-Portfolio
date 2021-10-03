import pandas as pd
import numpy as np

'''
Python file that, given inputs that need to be calculated/estimated externally, makes forecasts
for Ireland Dail elections, which use the Single Transferable Vote (STV) voting system. 
In the STV system, voters rank candidates with number 1 being their most preferred candidate.
The aim for candidates is to reach a quota. A critical part of STV is "redistribution". A candidate
who has gone over the quota, or who has too few votes and is eliminated from contention, has votes
redistributed to other candidates based on the 2nd or subsquent preferences of each voter.
'''


# DATA IMPORTS- GLOBAL VARIABLES

# Transfers

Transfers=pd.read_csv('2021IRETransfers.csv', index_col=0, header=0)

# Set up dataframe used in redistribute function

sums=pd.DataFrame(index=['G', 'F', 'S', 'L', 'I'], columns=['votes', 'proportions'])



def main():

    # FURTHER DATA IMPORTS


    #Predicted votes (1st preferences) for each candidate

    FPV=pd.read_csv('2021IREPV.csv',index_col=0,header=0)

    #Number of seats in each constituency and previous performances

    Cons=pd.read_csv('2021IRECons.csv', index_col=0, header=0)

    # SET UP TABLES TO STORE FORECASTS

    # Set up results table to record seats won by each party in each constituency
    Results=pd.DataFrame(index=FPV.index, columns=['FG', 'FF', 'SF', 'Lab', 'Gre', 'S-PBP', 'SD', 'Renua', 'Aontu', 'Ind'])

    # Set up Count table to be used in each constituency. In the "active" row:
    # 0 means active
    # 1 means inactive (did not contest, eliminated, elected and redistributed)
    # 2 means elected but excess not yet redistributed
    Count=pd.DataFrame(index=['votes', 'active'], dtype='float64')
    for cand in FPV.columns:
        Count[cand]=0. #initialize with zeros
    
    #for each constituency:

    for cons in FPV.index:

        # table can handle 23 candidates
        active_candidates=23


        # Data into Count table and establish number of competing candidates
        for cand in FPV.columns:
           Count[cand]['votes']=FPV[cand][cons]
           if Count[cand]['votes']==0: #Inactive/non-existant candidates
               Count[cand]['active']=1
               active_candidates-=1
           else:
                Count[cand]['active']=0

        

        # ELECTION COUNTING PROCESS

        # Quota and seats avaliable
        seats_left=Cons['Seats'][cons]
        quota=(100/(seats_left+1))+0.002 # 1 vote out of around 50,000


        # Initialize Zeros in results table
        for party in Results.columns:
            Results[party][cons]=0

        while seats_left>0:

            # IF seats=candidates left: 
            #   all remaining candidates elected
            # ELSE 
            #   find highest candidate (also considering those with undistributed surpluses)
            #   IF highest exceeds quota
            #        declare all candidates over quota elected (but still with excess)
            #       The excess of the highest candidate is redistributed
            #   ELSE 
            #       eliminate lowest candidate



            if seats_left==active_candidates:
                    # Declare all remaining candidates elected
                    for cand in Count.columns:
                        if Count[cand]['active']==0:
                            Count[cand]['active']=1
                            #Record election
                            for party in Results.columns:
                                if party in cand:
                                    Results[party][cons]+=1
                
                    seats_left=0



            else: #Find active or awaiting redistribution candidate with most votes
                max_votes=0 #initialize
                for cand in Count.columns:
                    if (Count[cand]['active']==0 or Count[cand]['active']==2) and Count[cand]['votes']>max_votes:
                        max_votes=Count[cand]['votes']
                        max_cand=cand 

                
                # Declare candidates who have exceeded the quota elected
                if max_votes>quota:
                    for cand in Count.columns:
                        if Count[cand]['active']==0 and Count[cand]['votes']>quota:
                            #Record election
                            for party in Results.columns:
                                if party in cand:
                                    Results[party][cons]+=1
                            Count[cand]['active']=2
                            seats_left-=1
                            active_candidates-=1

                    # The excess of the highest candidate (who may reached quota during a previous count) will be redistributed
                    Count=redistribute(Count, max_cand, quota)
                    Count[max_cand]['active']=1


                # No candidate has reached the quota- the lowest must be eliminated
                else:
                    # Find lowest candidate
                    min_votes=100 #initialize
                    for cand in Count.columns:
                        if Count[cand]['active']==0 and Count[cand]['votes']<min_votes:
                            min_votes=Count[cand]['votes']
                            min_cand=cand


                    # Eliminate the lowest candidate and redistribute their votes
                    Count[min_cand]['active']=1
                    Count=redistribute(Count, min_cand, 0)
                    active_candidates-=1



        print(cons) # Indicate to user the progress of the script

    
    # OUTPUT OF FORECASTS

    print(Results.sum(axis=0)) # Total number of seats won by each party
    print(Results) # Seats by won each party in each constituency


    # Compare result with previous time model was run (manual editing of input csv files required between runs)

    Gains=pd.DataFrame(index=Results.index, columns=Results.columns)

    for cons in Results.index:
        for party in Results.columns:
            prev_string='Prev'+party
            Gains[party][cons]=Results[party][cons]-Cons[prev_string][cons]

    # Compare result with last election
    
    LastGains=pd.DataFrame(index=Results.index, columns=Results.columns)

    for cons in Results.index:
        for party in Results.columns:
            last_string='Last'+party
            LastGains[party][cons]=Results[party][cons]-Cons[last_string][cons]
    
    # Output to CSV files
    Results.to_csv(r'IREresults.csv') 
    Gains.to_csv(r'IREgains.csv')
    LastGains.to_csv(r'IRELastGains.csv')



                    
def redistribute(Table, eliminated, votes_after):
    '''
    redistributes the votes of an eliminated candidate, as part of the STV electoral system

    Note:
    ----
    Ensure that active status of eliminated candidate has already been set to 1

    Parameters:
    -------
    Table: pd.DataFrame
        columns are candidates, rows for current votes, whether active, whether elected
    eliminated: str
        candidate to be eliminated
    votes_after: float
        votes that eliminated candidate retains


    Outputs:
    --------
    Table: pd.DataFrame
        inputted Table with modifications made

    '''

    # GET TRANSFER SCENARIO
    # Present in form, e.g. G-GFS, which means that a candidate of code G is having votes transferred
    # and the options are candidates with codes G, F and S. 


    # Clear data from last use of function
    sums['votes']=np.zeros(5)
    sums['proportions']=np.zeros(5)


    transfer_string=''
    
    # Set up transfer string
    # Eliminated Party

    cand_code=GetCode(eliminated)
    transfer_string=transfer_string+cand_code
    transfer_string=transfer_string+'-'

    
    # Remaining codes available for redistribution

    # Get List of active codes
    active_codes=[]
    for cand in Table.columns:
        if Table[cand]['active']==0:
            cand_code=GetCode(cand)
            active_codes.append(cand_code)
    
    for code in sums.index:
        if code in active_codes:
            transfer_string=transfer_string+code
    





    # add up votes per code
    # quicker to run and more concise code by using GetCode function again rather than extracting codes
    # from list active_codes

    for cand in Table.columns: #for each candidate
        if Table[cand]['active']==0:
            cand_code=GetCode(cand)
            sums['votes'][cand_code]+=Table[cand]['votes']
            




    # Retrieve redistribution proportions (NOT percentages)

    for code in sums.index:
        sums['proportions'][code]=Transfers[transfer_string][code]

    




    #  redistribute votes to candidates

    # votes available for redistribution is current votes of eliminated- votes_after
    # proprtion of those to be given to each active candidate is current votes/code sum * code proportion

    for cand in Table.columns:
        if Table[cand]['active']==0:
            code=GetCode(cand)
            redistribute_factor=(sums['proportions'][code]*Table[cand]['votes'])/(sums['votes'][code]+0.001)
            Table[cand]['votes']+=redistribute_factor*(Table[eliminated]['votes']-votes_after)
    
    # reduce eliminated candidates' votes to vote_after
    Table[eliminated]['votes']=votes_after



    return Table

def GetCode(cand):
    '''
    Converts a candidate abbreviation into the code for the purpose of redistribution

    Parameters:
    -----------
    cand: str
        abbreviation for the candidate
    
    Outputs:
    --------
    code: str
        single letter code for the candidate (G, F, S, L or I)

    '''
    # The 10 parties are grouped together in 5 codes for the purposes for transfers
    parties={
        'FG': 'G', 
        'FF': 'F', 
        'SF': 'S', 
        'Lab': 'L',
        'Gre': 'L',
        'S-PBP': 'L',
        'SD': 'L',
        'Renua': 'I',
        'Aontu': 'L',
        'Ind': 'I',
    }


    for party in parties:
        if party in cand:
            code=parties[party]
            break

    return code


if __name__ == "__main__":
    main()

