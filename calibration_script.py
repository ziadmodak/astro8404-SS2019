import os
import numpy as np

my_steps = np.arange(0,14)


my_vis = 'uid___A002_Xaeaf96_X515.ms' 

if 0 in my_steps :

    ## Import the asdm in .ms
    
    os.system('rm -rf '+my_vis)
    importasdm(asdm='../raw/uid___A002_Xaeaf96_X515.asdm.sdm', #.asdm.sdm',
               vis=my_vis,
               lazy=True,
               asis='*',
               bdfflags=True)
    
    ## create summary of this EB
    
    os.system('rm -rf '+my_vis+'.listobs')
    listobs(vis=my_vis,
            listfile=my_vis+'.listobs')

    ## Visualize the array configuration at the time of the observations

    os.system('rm -rf '+my_vis+'.plotants.png')
    plotants(vis=my_vis,
             figfile=my_vis+'.plotants.png')


    #####################################
    #### Summary of listobs/plotants ####
    #####################################
    

    
    # ALMA Band-3 observations at ~109GHz with 4 main SpWs (3 with 128 channels, 1 with 3840 channels).
    # 
    #       
    # CALIBRATE FLUX/AMPLI:  J0334-4008   (ID:0)   scan: 3                        SpW: 19 - 21 - 23 - 25
    # CALIBRATE BANDPASS  :  J0334-4008   (ID:0)   scan: 3                        SpW: 19 - 21 - 23 - 25
    # CALIBRATE PHASE     :  ESO358-G015J0336-3616   (ID:1)   scan: 4, 14, 24, 34, 44, 48    SpW: 19 - 21 - 23 - 25
    # TARGETS: MCG-06-08-024, ESO358-G015, FCC282, NGC1437A, 
    #          NGC1437B, ESO359-G002, NGC1386, NGC1387, 
    #          PGC013571, ESO_358-16FCC177
    # TARGET FOR EXAM     :  NGC1386      (ID:8)   scan: 11,25,38,46              SpW: 19 - 21 - 23 - 25    
    # 
    # Tsys                :  J0334-4008; NGC1387   scan: 2,12,26,39               SpW: 17 - 19 - 21 - 23 ---- 17 applies to 25 asthey are the closest in frequency!
    #                        (ID: 0)     (ID: 9)
    # 
    # WVR                 :  All Scans                                            SpW: 4 
    # 
    # 
    # Array Configuration : 42 Antennae; Longest Baseline ~307 m (PM03 -- DV13) -> Synthesize Beam ~57"
    # Reference Antenna   : DA49                   
    # 
    #
    #####################################
    #####################################
    #####################################   
 
 
 
 
 
    
if 1 in my_steps :


    #####################################
    ###  A Priori Calibration: Tsys   ###
    #####################################

    
    os.system('rm -rf '+my_vis+'.tsys')
    
    # generate of Tsys caltable (naming convention name_ms.caltable_name)
    gencal(vis=my_vis,                     
           caltable=my_vis+'.tsys',        
           caltype='tsys')                  
    

    # Tsys measurements are known to be corrupted at the edges of SpWs, hence the edges are being flagged
    flagdata(vis=my_vis+'.tsys',                      
             mode='manual',                            
             spw='17;19;21;23:0~3;124~127',            
             flagbackup = False)                       
             
    

    # plot for each antenna and each SPW, Tsys vs. Freq, overlaying all tsys scan together
    # and add the atmospheric transmission
    plotbandpass(caltable=my_vis+'.tsys',              
                 xaxis='freq',
                 yaxis='tsys',
                 antenna='',
                 spw='',
                 showatm=True,                 
                 overlay='time',
                 plotrange=[0, 0, 0, 0],               
                 figfile=my_vis+'.tsys.plots/'+my_vis, 
                 interactive=False)
                 

    # Inspect these plots and look for peculiar antennae/spw/scan
    #
    # DA46 SpW 19,21,23 YY has suspicious wigglea - NEEDS TO BE FLAGGED
    # 
    # DA57 SpW 19,23 has a weird uncalled for peak - NEEDS TO BE FLAGGED
    #
    # DV01 SpW 19 XX has suspicious wiggles - NEEDS TO BE FLAGGED
    #    
    # DV22 all SpWs XX is different from other scans - NEEDS TO BE FLAGGED

    



if 2 in my_steps :

    #####################################
    ###   A Priori Calibration: WVR   ###
    #####################################

    
    ## Generation of the WVR caltable using the task WVRGCAL

    os.system('rm -rf '+my_vis+'.wvr')
    wvrgcal(vis=my_vis,                  
            caltable=my_vis+'.wvr',      
            spw=[17,19,21,23,25],        
            smooth='6.05s',              # Smooth the calibration on the given timescale from the appropriate SpWs' Average Interval
            tie=['NGC1437B,J0336-3616', 'ESO358-G015,J0336-3616', 'ESO_358-16,J0336-3616', 'MCG-06-08-024,J0336-3616', 'NGC1387,J0336-3616', 'NGC1437A,J0336-3616', 'FCC282,J0336-3616', 'NGC1386,J0336-3616', 'PGC013571,J0336-3616', 'FCC177,J0336-3616', 'ESO359-G002,J0336-3616'], # tie = ['NGC_4451,J1239+0730'],
            statsource='NGC1386')
    

    # From the Logger
    #       PWV ~ 3.6 mm
    # Seems fine


if 3 in my_steps :

    #############################################
    ###   A Priori Calibration: Application   ###
    #############################################

    

    # Generate tsysmap
    from recipes.almahelpers import tsysspwmap
    tsysmap = tsysspwmap(vis=my_vis,
                         tsystable=my_vis+'.tsys')

    applycal(vis=my_vis,                                 
             field='0',                                  
             spw='17,19,21,23,25',                       
             gaintable= [my_vis+'.tsys',my_vis+'.wvr'],  
             gainfield= ['0',''],                        
             interp ='linear,linear',                    
             calwt= True,                                
             flagbackup = False,
             spwmap=[tsysmap,[]])  



    applycal(vis=my_vis,                                 
             field='1~12',                               
             spw='17,19,21,23,25',                       
             gaintable= [my_vis+'.tsys',my_vis+'.wvr'],  
             gainfield= ['9',''],                        
             interp ='linear,linear',                    
             calwt= True,                                
             flagbackup = False,
             spwmap=[tsysmap,[]])  

    # Field 1~12 have no Tsys measurements. Tsys of field 9 is applied to these fields.


    
if 4 in my_steps :

    #############################################
    ###    A Priori Calibration: Flagging     ###
    #############################################




    # Flag auto-correlation visibilities
    flagdata(vis = my_vis,  
             mode = 'manual',                      
             spw = '0~26',                          
             autocorr = True,
             flagbackup = False)

    
    # Flag un-necessary scans (POINTING, SIDEBAND_RATIO, ATMOSPHERE) 
    flagdata(vis = my_vis,  # Name of the MS
             mode = 'manual',
             intent = '*POINTING*,*SIDEBAND_RATIO*,*ATMOSPHERE*',
             flagbackup = False)

    
    # Flag visibilities coming from antennae which are shadowed by an other one.
    flagdata(vis = my_vis,
             mode = 'shadow',
             flagbackup = False)

    # Flag antennae from Tsys plots
    flagdata(vis = my_vis,
             mode = 'manual',
             spw = '19,21,23',
             antenna = 'DA46',
             correlation = 'YY',
             flagbackup = False)

    flagdata(vis = my_vis,
             mode = 'manual',
             antenna = 'DA57',
             flagbackup = False)

    flagdata(vis = my_vis,
             mode = 'manual',
             spw = '19',
             antenna = 'DV01',
             correlation = 'XX',
             flagbackup = False)

    flagdata(vis = my_vis,
             mode = 'manual',
             antenna = 'DV22',
             correlation = 'XX',
             flagbackup = False)



if 5 in my_steps :

    ###################################################
    ###   SPLIT I: slim down data for calibration   ###
    ###################################################

    os.system('rm -rf '+my_vis+'.split') 
    split(vis = my_vis,                       
        outputvis = my_vis+'.split',          
        datacolumn = 'corrected',             
        spw = '19,21,23,25',                  
        field='0,1,8',                        
        keepflags = True)                     
    
    
    os.system('rm -rf '+my_vis+'.split.listobs')
    listobs(vis = my_vis+'.split',
        listfile = my_vis+'.split.listobs')
    

    ## Completer dataset (not required for exam)   
    os.system('rm -rf '+my_vis+'full.split') 
    split(vis = my_vis,                       
        outputvis = my_vis+'full.split',      
        datacolumn = 'corrected',             
        spw = '19,21,23,25',                  
        keepflags = True)                     

    os.system('rm -rf '+my_vis+'full.split.listobs')
    listobs(vis = my_vis+'full.split',
        listfile = my_vis+'full.split.listobs')
   


if 6 in my_steps :        


    ######################################################
    ###   Calibration: Inspection, Editing, Flagging   ###
    ######################################################

    # Amplitudes vs. UVDistances    
    plotms(vis=my_vis+'.split',            
        xaxis='uvdist',
        yaxis='amp', 
        field='0',                          
        avgchannel='1000',                  
        avgtime='1e8', 
        avgscan=True,
        iteraxis='spw',                     
        coloraxis='antenna1',               
        showgui=True,                       
        plotfile='fields-0-1-3-amp-uvdist.png',  
        overwrite=True)



    # Amplitudes vs. Channels   
    plotms(vis=my_vis+'.split', 
        xaxis='frequency',
        yaxis='amp', 
        field='0',                         
        avgtime='1e8', 
        avgscan=True,
        coloraxis='corr',
        showgui=True, 
        plotfile='field-0-1-3-amp-channel.png', 
        overwrite=True)
        
    # TDMs have edge-roll-off: FLAG EDGES OF SpWs 0,1,2
 
 
 
    ## Amplitudes vs. Time
    plotms(vis=my_vis+'.split', 
        xaxis='time',
        yaxis='amp', 
        avgchannel='1e8',
        iteraxis='spw', 
        coloraxis='field',
        showgui=True, 
        plotfile='field-0-1-3-amp-time.png',
        overwrite=True)

    # DA55 in spw 2 has lower amplitude: FLAGGED
    # DA59 in all SpWs has lower amplitude: FLAGGED


    ## Phase vs. Time   
    plotms(vis=my_vis+'.split', 
        xaxis='time',
        yaxis='phase', 
        field='0',
        spw='0',
        antenna='DA49&*',      # Refernce Antenna
        avgchannel='1e8',
        iteraxis='baseline', 
        coloraxis='corr',
        showgui=True, 
        #plotfile='field-0-1-3-phase-time.png',
        overwrite=True)

   # All plots look good, no weird scatter. Other than some plots with a phase shift of 360 deg. Problematic?

    
    ## Flagging based on the previous plots
    flagdata(vis = my_vis+'.split',
        mode = 'manual',
        spw='0;1;2:0~3;124~127',            
        flagbackup = False)
  
  
    flagdata(vis = my_vis+'.split',
        mode = 'manual',
        antenna='DA55',
        spw='2',             
        flagbackup = False)
  
    flagdata(vis = my_vis+'.split',
        mode = 'manual',
        antenna='DA59',        
        flagbackup = False)
  
  
    
    
    

if 7 in my_steps :    
    
    
    #####################################
    ###     Calibration: Bandpass     ###
    #####################################
   

    os.system('rm -rf '+my_vis+'.split.ap_pre_bandpass')

    gaincal(vis = my_vis+'.split',                     
        caltable = my_vis+'.split.ap_pre_bandpass',    
        field = '0',        # bandpass calibrator
        spw = '',
        scan = '3',
        solint = 'int',                                
        refant = 'DA49',	                           
        calmode = 'p')		                           # calibrate phase


    os.system('rm -rf '+my_vis+'.split.ap_pre_bandpass.plots')  
    os.system('mkdir '+my_vis+'.split.ap_pre_bandpass.plots')   
    
    ## little tweak to get all antenna names 
    tb.open(my_vis+'.split/ANTENNA')
    antList = tb.getcol('NAME')
    tb.close()
    
    ## iterate plots over antenna names
    for i in antList:
        plotcal(caltable=my_vis+'.split.ap_pre_bandpass',     
            xaxis='time',                                     
            yaxis='phase',                                    
            field='0',                                        # bandpass calibrator
            antenna=i,                                        # needed to plot per antenna
            iteration='antenna, spw',                         
            subplot=411,                                      
            plotrange=[0, 0, -180, 180],                      
            figfile=my_vis+'.split.ap_pre_bandpass.plots/'+my_vis+'.split.ap_pre_bandpass.field0.'+i+'.png')
    
     
    
    
    os.system('rm -rf '+my_vis+'.split.bandpass')       
    
    bandpass(vis = my_vis+'.split',                     
        caltable = my_vis+'.split.bandpass',            
        field = '0',                     # bandpass calibrator
        scan = '3',
        solint = 'inf',                                 # solution interval (time interval) set to infinite = entire scan
        combine = 'scan',                               # extend 'infinite' beyond scan limits ---> one solution per observation and channel
        refant = 'DA49',                                
        solnorm = True,                                 
        bandtype = 'B',                                 
        gaintable = my_vis+'.split.ap_pre_bandpass')   

		
    plotbandpass(caltable=my_vis+'.split.bandpass',     
        xaxis='freq',                                   
        yaxis='both',                                   
        antenna='',                                     
        spw='',                                         
        overlay='',                                     
        showatm=True,                                   
        pwv='auto',                                     
        field='0',                                      # bandpass calibrator
        plotrange=[0, 0, 0, 0],                         
        figfile=my_vis+'.split.bandpass.plots-B/'+my_vis+'.split.bandpass.field0', 
        interactive=False)




if 8 in my_steps :    

       
    ##########################################################
    ###     Calibration: set model for flux calibrator     ###
    ##########################################################
   
    # Using ALMA Source Catalog query from 07/11/15 -- 0.7/03/16 in freq range of 90--130 GHz
    # and then taking the mean of all the flux values at 91.5 GHz (0.86533 Jy) and 103.5 GHz (0.82364 Jy)
    # gives a spectral index of -0.400837. Using this spectral index, the flux at the 
    # central frequency of 107.771 GHz was found to be 0.810382 Jy.
 
    setjy(vis = my_vis+'.split',
      standard = 'manual',
      field = 'J0334-4008',
      fluxdensity = [0.810382, 0, 0, 0],
      spix = -0.400837,
      reffreq = '107.771GHz')
    
    
 
    
    
 
if 9 in my_steps :
   
   
    ############################################################
    ###     Calibration: Phase, Amplitude, Flux transfer     ###
    ############################################################



    ## Phase corrections (shorter timescales) for the calibrators
    os.system('rm -rf '+my_vis+'.split.phase_int')     
    gaincal(vis = my_vis+'.split',                     
        caltable = my_vis+'.split.phase_int',          
        field = '0~1', 
        solint = 'int',                                # solving for fast variations
        refant = 'DA49',                               
        gaintype = 'G',                                
        calmode = 'p',                                 
        gaintable = my_vis+'.split.bandpass')          
 
 

 
    os.system('rm -rf '+my_vis+'.split.phase_int.plots')       
    os.system('mkdir '+my_vis+'.split.phase_int.plots')       
   
    tb.open(my_vis+'.split/ANTENNA')
    antList = tb.getcol('NAME')
    tb.close()
    
    ## iterate plots over antenna names
    for i in antList:
        plotcal(caltable=my_vis+'.split.phase_int',            
            xaxis='time',                                      
            yaxis='phase',                                     
            field='0,1',                                       
            antenna=i,                                         
            iteration='antenna, spw',                          
            subplot=411,                                       
            plotrange=[0, 0, -180, 180],                       
            figfile=my_vis+'.split.phase_int.plots/'+my_vis+'.split.phase_int.field0-1.'+i+'.png')  
    
 
 
 
 
      
      
    ## Amplitude corrections for the calibrators
    os.system('rm -rf '+my_vis+'.split.ampli_inf')    
    gaincal(vis = my_vis+'.split',                     
        caltable = my_vis+'.split.ampli_inf',          
        field = '0~1', 
        solint = 'inf',                                # solving for slower, scan block long variations
        refant = 'DA49',                               
        gaintype = 'G',                                
        calmode = 'a',                                 
        gaintable = [my_vis+'.split.bandpass', my_vis+'.split.phase_int']) 
 
 

    os.system('rm -rf '+my_vis+'.split.ampli_inf.plots')       
    os.system('mkdir '+my_vis+'.split.ampli_inf.plots')        
     
     
    tb.open(my_vis+'.split/ANTENNA') 
    antList = tb.getcol('NAME') 
    tb.close() 
     
    ## iterate plots over antenna names 
    for i in antList: 
        plotcal(caltable=my_vis+'.split.ampli_inf',            
            xaxis='time',                                      
            yaxis='amp',                                       
            field='0,1',                                       
            antenna=i,                                         
            iteration='antenna, spw',                          
            subplot=411,                                       
            plotrange=[0, 0, 0, 0],                            
            figfile=my_vis+'.split.ampli_inf.plots/'+my_vis+'.split.ampli_inf.field0-1.'+i+'.png')   
     
 
 
 
 
 
 
    ## Phase corrections (slow varying) for the calibrators
    os.system('rm -rf '+my_vis+'.split.phase_inf')     
   
    gaincal(vis = my_vis+'.split',                     
        caltable = my_vis+'.split.phase_inf',         
        field = '0~1', 
        solint = 'inf',                                # solving for slower, scan block long variations
        refant = 'DA49',                              
        gaintype = 'G',                                
        calmode = 'p',                                 
        gaintable = my_vis+'.split.bandpass')          




    os.system('rm -rf '+my_vis+'.split.phase_inf.plots')       
    os.system('mkdir '+my_vis+'.split.phase_inf.plots')        
   
    tb.open(my_vis+'.split/ANTENNA')
    antList = tb.getcol('NAME')
    tb.close()
    
    ## iterate plots over antenna names
    for i in antList:
        plotcal(caltable=my_vis+'.split.phase_inf',            
            xaxis='time',                                      
            yaxis='phase',                                     
            field='0,1',                                       
            antenna=i,                                         
            iteration='antenna, spw',                          
            subplot=411,                                       
            plotrange=[0, 0, -180, 180],                       
            figfile=my_vis+'.split.phase_inf.plots/'+my_vis+'.split.phase_inf.field0-1.'+i+'.png')  
            
            
            



if 10 in my_steps :
   
   
    ##########################################
    ###     Calibration: FLUX TRANSFER     ###
    ##########################################

          
    os.system('rm -rf '+my_vis+'.split.flux_inf')      
    fluxscale(vis = my_vis+'.split',                   
        caltable = my_vis+'.split.ampli_inf',          
        fluxtable = my_vis+'.split.flux_inf',          
        reference = '0') 








if 11 in my_steps :
	
	
    ############################################################
    ###     Calibration: Apply the gaintables to the data    ###
    ############################################################


    ## Apply the solutions for the phase calibrator to its data
    applycal(vis = my_vis+'.split',                         
          field = '1',             # Phase calibrator
          gaintable = [my_vis+'.split.bandpass', my_vis+'.split.phase_int', my_vis+'.split.flux_inf'],  
          gainfield = ['', '1', '1'],                       
          interp = 'linear,linear',
          calwt = True,                                    
          flagbackup = False)


    ## Apply the solutions for the flux calibrator to its data 
    applycal(vis = my_vis+'.split',                        
        field = '0',                 # Flux Calibrator		    
        gaintable = [my_vis+'.split.bandpass', my_vis+'.split.phase_int', my_vis+'.split.flux_inf'],  
        gainfield = ['', '0', '0'],                         
        interp = 'linear,linear', 
        calwt = True,                                       
        flagbackup = False)


    ## Apply the solutions for the phase calibrator to the target data
    applycal(vis = my_vis+'.split',                         
        field = '2',                  # target source
        gaintable = [my_vis+'.split.bandpass', my_vis+'.split.phase_inf', my_vis+'.split.flux_inf'], 
        interp = 'linear,linear',
        calwt = True,                                      
        flagbackup = False)


       
       

if 12 in my_steps :
	
	

    ######################################################
    ###   Calibration: Post-Calibration Inspection     ###
    ######################################################
                
    ## Amplitudes/Phase vs. UVDistances (repeat for all fields)   

    plotms(vis=my_vis+'.split',                                
        xaxis='uvdist',                                        
        yaxis='phase',                                           # redo for phase (interactively)
        ydatacolumn='corrected',                               
        field='0',                                             
        avgchannel='1e8',                                      
        avgtime='1e8',                                         
        avgscan=True,                                          
        iteraxis='spw',                                       
        coloraxis='antenna1',                                 
        showgui=True,                                         
        #plotfile='field-0-amp-uvdist.png',                    
        overwrite=True)    

    # Seems fine, phase and amplitudes for the calibrators are constant across different 
    # baseline lengths (expected from point sources). Also, the amplitudes of the flux calibrator 
    # are at the level of the flux scales from ALMA SC


    ## Amplitudes/Phase vs. Channels (repeat for all fields)   
    plotms(vis=my_vis+'.split',
        xaxis='frequency',
        yaxis='amp',                                          
        field='0',                                            
        ydatacolumn='corrected',                              
        avgtime='1e8',                                         
        avgscan=True,                                          
        coloraxis='corr',                                      
        showgui=True,                                          
        overwrite=True)
        
 
 
 
    ## Amplitudes/Phase vs. Time (repeat for all fields)   
          
    plotms(vis=my_vis+'.split', 
        xaxis='time',
        yaxis='amp',                                           # redo for phase (interactively, iteration over baselines to reference antenna should be enough for phase)
        ydatacolumn='corrected',                               
        avgchannel='1e8',
        iteraxis='spw',
        coloraxis='field',
        showgui=True, 
        overwrite=True)

    
    
    




if 13 in my_steps :


    ###########################################
    ###   SPLIT II: your calibrated data !  ###
    ###########################################
    
    os.system('rm -rf '+my_vis+'.split.cal')                   
                                                               
    split(vis = my_vis+'.split',                               
        outputvis = my_vis+'.split.cal',                       
        datacolumn = 'corrected',                              
        keepflags = True)                                      

