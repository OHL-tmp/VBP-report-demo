#!/usr/bin/env python3

selected_measure = {'CHF Related Average Cost per Patient': [False, 33100, 33100, 33100, 0, 2, 0, 0.5, 0],
'CHF Related Hospitalization Rate': [False, 0.4, 0.4, 0.35, 0, 3, 0, 0.2, 0], 
'NT-proBNP Change %' : [False, 0, 0, -0.25, 0, 3, 0, 0.15, 0],
'LVEF LS Mean Change %' : [False, 0, 0, 0.03, 0, 3, 0, 0.15, 0]}

selected_domain = {"Cost & Utilization Reduction" : False, "Improving Disease Outcome" : False,
                 "Decreasing Health Disparities" : True, "Increasing Patient Safety" : True,
                 "Enhancing Care Quality" : True, "Better Patient Experience" : True}

domain_to_measure = {"Cost & Utilization Reduction" : ["All Causes Average Cost per Patient", "CHF Related Average Cost per Patient", "All Causes Average IP Cost per Patient", 
	"CHF Related Average IP Cost per Patient", "All Causes Hospitalization Rate", "CHF Related Hospitalization Rate", "All Causes ER Rate", "CHF Related ER Rate"], 
"Improving Disease Outcome" : ["NT-proBNP Change %", "LVEF LS Mean Change %", "LAVi LS Mean Change", "LVEDVi LS Mean Change", "LVESVi LS Mean Change", "E/e' LS Mean Change",
	"Change in Self-Care Score", "Change in Mobility Score", "CV Mortality Rate", "Rate of CHF Progression for 24 months"],
"Decreasing Health Disparities" : [], 
"Increasing Patient Safety" : ["Emergent care rate for medication side effect", "Hospitalization rate for medication side effect"],
"Enhancing Care Quality" : ["DOT", "PDC", "MPR"], 
"Better Patient Experience" : ["Patient Reported SOB changes", "Patient Reported Fatigue and Tiredness Changes", "Patient Reported Peripheral Oedema Changes", 
	"Patient Reported Disturbed Sleep Changes"]}

measure_to_domain = {"All Causes Average Cost per Patient" : "Cost & Utilization Reduction", "CHF Related Average Cost per Patient" : "Cost & Utilization Reduction", 
	"All Causes Average IP Cost per Patient" : "Cost & Utilization Reduction", "CHF Related Average IP Cost per Patient" : "Cost & Utilization Reduction", 
	"All Causes Hospitalization Rate" : "Cost & Utilization Reduction", "CHF Related Hospitalization Rate" : "Cost & Utilization Reduction",
	"All Causes ER Rate" : "Cost & Utilization Reduction", "CHF Related ER Rate" : "Cost & Utilization Reduction",
	"NT-proBNP Change %" : "Improving Disease Outcome", "LVEF LS Mean Change %" : "Improving Disease Outcome", "LAVi LS Mean Change" : "Improving Disease Outcome", 
	"LVEDVi LS Mean Change" : "Improving Disease Outcome", "LVESVi LS Mean Change" : "Improving Disease Outcome", "E/e' LS Mean Change" : "Improving Disease Outcome",
	"Change in Self-Care Score" : "Improving Disease Outcome", "Change in Mobility Score" : "Improving Disease Outcome", "CV Mortality Rate" : "Improving Disease Outcome", 
	"Rate of CHF Progression for 24 months" : "Improving Disease Outcome",
	"Emergent care rate for medication side effect" : "Increasing Patient Safety", "Hospitalization rate for medication side effect" : "Increasing Patient Safety",
	"DOT" : "Enhancing Care Quality", "PDC" : "Enhancing Care Quality", "MPR" : "Enhancing Care Quality",
	"Patient Reported SOB changes" : "Better Patient Experience", "Patient Reported Fatigue and Tiredness Changes" : "Better Patient Experience", 
	"Patient Reported Peripheral Oedema Changes" : "Better Patient Experience", "Patient Reported Disturbed Sleep Changes" : "Better Patient Experience"}

'''domain_no = {"Cost & Utilization Reduction" : 1, "Improving Disease Outcome" : 2,
                 "Decreasing Health Disparities" : 3, "Increasing Patient Safety" : 4,
                 "Enhancing Care Quality" : 5, "Better Patient Experience" : 6}'''
domain_no = {1:"Cost & Utilization Reduction", 2:"Improving Disease Outcome",
                 3:"Decreasing Health Disparities", 4:"Increasing Patient Safety",
                 5:"Enhancing Care Quality", 6:"Better Patient Experience"}     

measure_no = {"All Causes Average Cost per Patient" : 1, "CHF Related Average Cost per Patient" : 2, 
	"All Causes Average IP Cost per Patient" : 3, "CHF Related Average IP Cost per Patient" : 4, 
	"All Causes Hospitalization Rate" : 5, "CHF Related Hospitalization Rate" : 6,
	"All Causes ER Rate" : 7, "CHF Related ER Rate" : 8,
	"NT-proBNP Change %" : 1, "LVEF LS Mean Change %" : 2, "LAVi LS Mean Change" : 3, 
	"LVEDVi LS Mean Change" : 4, "LVESVi LS Mean Change" : 5, "E/e' LS Mean Change" : 6,
	"Change in Self-Care Score" : 7, "Change in Mobility Score" : 8, "CV Mortality Rate" : 9, 
	"Rate of CHF Progression for 24 months" : 10,
	"Emergent care rate for medication side effect" : 1, "Hospitalization rate for medication side effect" : 2,
	"DOT" : 1, "PDC" : 2, "MPR" : 3,
	"Patient Reported SOB changes" : 1, "Patient Reported Fatigue and Tiredness Changes" : 2, 
	"Patient Reported Peripheral Oedema Changes" : 3, "Patient Reported Disturbed Sleep Changes" : 4}