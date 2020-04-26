import numpy as np
import pandas as pd
from scipy import interpolate



Gross_Revenue=6960000/1000000
Recom_Pt_cohort='Cohort1 (Recommended)'
Performance_assumption=pd.read_csv('data/performance_assumption.csv')
Performance_assumption.set_index(['Cohort','Measure'],inplace=True)
Recom_Measure=pd.read_csv('data/recom_measure.csv')

def Contract_Calculation(Recom_Contract, UD_Measure,UD_Contract,UD_Pt_Cohort,Rebate_noVBC, Rebate_VBC):    
  
    import numpy as np
    import pandas as pd
    from scipy import interpolate

    # Pre-determined input
    
    
    #Recom_Contract=pd.read_csv('C:\\Users\\wuyabo\\Recom_contract.csv')
    
    # Recommended Scenario Calculation
    
    Recom_Performance_assumption=Performance_assumption.loc[Recom_Pt_cohort]
    
    Recom_Merge=Recom_Measure.merge(Recom_Performance_assumption, left_on='Measure', right_on='Measure', suffixes=(False, False))

    #Recommended Scenario: Performance calculation for individual measure 
    
    Recom_Merge['Worse_Diff']=Recom_Merge['Worse'].astype(float)-Recom_Merge['Target'].astype(float)
    Recom_Merge['Worse_Perc']=np.where(Recom_Merge['Scoring Method']==1,1+Recom_Merge['Worse_Diff']/Recom_Merge['Target'],1-Recom_Merge['Worse_Diff']/Recom_Merge['Target'])
    Recom_Merge['Mid_Diff']=Recom_Merge['Mid'].astype(float)-Recom_Merge['Target'].astype(float)
    Recom_Merge['Mid_Perc']=np.where(Recom_Merge['Scoring Method']==1,1+Recom_Merge['Mid_Diff']/Recom_Merge['Target'],1-Recom_Merge['Mid_Diff']/Recom_Merge['Target'])
    Recom_Merge['Better_Diff']=Recom_Merge['Better'].astype(float)-Recom_Merge['Target'].astype(float)
    Recom_Merge['Better_Perc']=np.where(Recom_Merge['Scoring Method']==1,1+Recom_Merge['Better_Diff']/Recom_Merge['Target'],1-Recom_Merge['Better_Diff']/Recom_Merge['Target'])

    #Recommended Scenario: Overall performance % calculation
    
    Worse_Performance=Recom_Merge['Weight'].dot(Recom_Merge['Worse_Perc'])
    Mid_Performance=Recom_Merge['Weight'].dot(Recom_Merge['Mid_Perc'])
    Better_Performance=Recom_Merge['Weight'].dot(Recom_Merge['Better_Perc'])
    
    #Recommended Scenario: Rebate adjustment interpolation
    
    x=[0,Recom_Contract.iloc[0][4],Recom_Contract.iloc[0][3],Recom_Contract.iloc[0][0],Recom_Contract.iloc[0][1],999]
    y=[Recom_Contract.iloc[0][5],Recom_Contract.iloc[0][5],0,0,Recom_Contract.iloc[0][2],Recom_Contract.iloc[0][2]]
    f = interpolate.interp1d(x, y)
    Recom_Rebate_Adj_Perc=[f(Mid_Performance),Recom_Contract.iloc[0][5],Recom_Contract.iloc[0][2],f(Worse_Performance),f(Better_Performance)]
    
    # User Defined Scenario Calculation
    
    UD_Performance_assumption=Performance_assumption.loc[UD_Pt_Cohort]
    
    UD_Merge=UD_Measure.merge(UD_Performance_assumption, left_on='Measure', right_on='Measure', suffixes=(False, False))
   
    #User Defined Scenario: Performance calculation for individual measure 
    
    UD_Merge['Worse_Diff']=UD_Merge['Worse'].astype(float)-UD_Merge['Target'].astype(float)
    UD_Merge['Worse_Perc']=np.where(UD_Merge['Scoring Method']==1,1+UD_Merge['Worse_Diff']/UD_Merge['Target'],1-UD_Merge['Worse_Diff']/UD_Merge['Target'])
    UD_Merge['Mid_Diff']=UD_Merge['Mid'].astype(float)-UD_Merge['Target'].astype(float)
    UD_Merge['Mid_Perc']=np.where(UD_Merge['Scoring Method']==1,1+UD_Merge['Mid_Diff']/UD_Merge['Target'],1-UD_Merge['Mid_Diff']/UD_Merge['Target'])
    UD_Merge['Better_Diff']=UD_Merge['Better'].astype(float)-UD_Merge['Target'].astype(float)
    UD_Merge['Better_Perc']=np.where(UD_Merge['Scoring Method']==1,1+UD_Merge['Better_Diff']/UD_Merge['Target'],1-UD_Merge['Better_Diff']/UD_Merge['Target'])
     
    #User Defined Scenario: Overall performance % calculation
    
    Worse_Performance=UD_Merge['Weight'].dot(UD_Merge['Worse_Perc'])
    Mid_Performance=UD_Merge['Weight'].dot(UD_Merge['Mid_Perc'])
    Better_Performance=UD_Merge['Weight'].dot(UD_Merge['Better_Perc'])
    
    #User Defined Scenario: Rebate adjustment interpolation
    
    x=[0,UD_Contract.iloc[0][4],UD_Contract.iloc[0][3],UD_Contract.iloc[0][0],UD_Contract.iloc[0][1],999]
    y=[UD_Contract.iloc[0][5],UD_Contract.iloc[0][5],0,0,UD_Contract.iloc[0][2],UD_Contract.iloc[0][2]]
    f = interpolate.interp1d(x, y)
    UD_Rebate_Adj_Perc=[f(Mid_Performance),UD_Contract.iloc[0][5],UD_Contract.iloc[0][2],f(Worse_Performance),f(Better_Performance)]
    
    #Produce output table - Pharma's net revenue
    
    data = {'Scenario': ['Best Estimate', 'Worst', 'Best', 'Lower End', 'Higher End'], 
                'NoVBC Gross Revenue': [Gross_Revenue, 'NA', 'NA','NA','NA'], 
                'NoVBC Base Rebate Payout': [Gross_Revenue*Rebate_noVBC, 'NA', 'NA','NA','NA'], 
                'NoVBC Outcome Based Rebate Adjustment': [0, 'NA', 'NA','NA','NA'], 
                'NoVBC Net Rebate Payout': [Gross_Revenue*Rebate_noVBC, 'NA', 'NA','NA','NA'], 
                'NoVBC Net Revenue': [Gross_Revenue-Gross_Revenue*Rebate_noVBC, 'NA', 'NA','NA','NA']} 
    Output_Pharma_Net_Revenue = pd.DataFrame(data) 
    
    Output_Pharma_Net_Revenue['RecomVBC Gross Revenue']=Gross_Revenue
    Output_Pharma_Net_Revenue['RecomVBC Base Rebate Payout']=Gross_Revenue*Rebate_VBC
    Output_Pharma_Net_Revenue['RecomVBC Outcome Based Rebate Adjustment']=Output_Pharma_Net_Revenue['RecomVBC Gross Revenue']*Recom_Rebate_Adj_Perc
    Output_Pharma_Net_Revenue['RecomVBC Net Rebate Payout']=Output_Pharma_Net_Revenue['RecomVBC Base Rebate Payout']-Output_Pharma_Net_Revenue['RecomVBC Outcome Based Rebate Adjustment']
    Output_Pharma_Net_Revenue['RecomVBC Net Revenue']=Output_Pharma_Net_Revenue['RecomVBC Gross Revenue']-Output_Pharma_Net_Revenue['RecomVBC Net Rebate Payout']
    
    Output_Pharma_Net_Revenue['UDVBC Gross Revenue']=Gross_Revenue
    Output_Pharma_Net_Revenue['UDVBC Base Rebate Payout']=Gross_Revenue*Rebate_VBC
    Output_Pharma_Net_Revenue['UDVBC Outcome Based Rebate Adjustment']=Output_Pharma_Net_Revenue['UDVBC Gross Revenue']*UD_Rebate_Adj_Perc
    Output_Pharma_Net_Revenue['UDVBC Net Rebate Payout']=Output_Pharma_Net_Revenue['UDVBC Base Rebate Payout']-Output_Pharma_Net_Revenue['UDVBC Outcome Based Rebate Adjustment']
    Output_Pharma_Net_Revenue['UDVBC Net Revenue']=Output_Pharma_Net_Revenue['UDVBC Gross Revenue']-Output_Pharma_Net_Revenue['UDVBC Net Rebate Payout']
    
    Output_Pharma_Net_Revenue=Output_Pharma_Net_Revenue.T
    header=Output_Pharma_Net_Revenue.iloc[0]
    Output_Pharma_Net_Revenue=Output_Pharma_Net_Revenue[1:]
    Output_Pharma_Net_Revenue.columns=header
    
    Output_Pharma_Net_Revenue.insert(0, 'Contract Type', ['Contract w/o VBC Payout']*5+['Contract with VBC Payout (Recommended)']*5+['Contract with VBC Payout (Payor Contract)']*5)
    Output_Pharma_Net_Revenue.insert(1, 'Item', ['Gross Revenue','Base Rebate Payout','Outcome Based Rebate Adjustment','Net Rebate Payout','Net Revenue']*3)
    
    #Produce output table - Pharma's rebate payout
    
    Output_Rebate = Output_Pharma_Net_Revenue[Output_Pharma_Net_Revenue['Item'].str.contains('Rebate')]
    Output_Pharma_Net_Revenue.reset_index()
    pos=[1,2,6,7,11,12]
    Output_Pharma_Net_Revenue.drop(Output_Pharma_Net_Revenue.index[pos], inplace=True)
    Output_Pharma_Net_Revenue.set_index(['Contract Type'],inplace=True)
    Output_Rebate.set_index(['Contract Type'],inplace=True)
    
    return Output_Pharma_Net_Revenue, Output_Rebate