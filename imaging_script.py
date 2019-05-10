import os

my_vis = 'uid___A002_Xaeaf96_X515.ms.split.cal'
fld = 'NGC1386'
targetname = fld


os.system('rm -rf '+str(my_vis)+'.listobs')

listobs(vis=my_vis, listfile=str(my_vis)+'.listobs')


plotms(vis=my_vis,                                
       xaxis='channel',
       yaxis='amp',
       field=fld,                                 
       avgtime='1e8',
       avgscan=True,
       iteraxis='spw')


# SpW 3:2500~3000 Line
# SpW 0~2,3:0~2350,3:3150~3839 Continuum

plotms(vis=my_vis,                                
       spw='2',
       xaxis='uvwave',                           
       yaxis='amp',
       field=fld,                                 
       avgtime='1e8',
       avgchannel='1e8',
       coloraxis='baseline')

# ~105 klambda
# Resolution of 206/105 ~ 2 arcsec
# Cellsize ~= 0.4 arcsec

# Dirty Continuum NA Image
os.system('rm -rf '+targetname+'_cont_dirty.*')
clean(vis=my_vis,
      imagename=targetname+'_cont_dirty',
      spw='0~2,3:0~2400,3:3100~3839',
      field=fld,
      mode='mfs',
      niter=0,
      imsize=256,
      cell='0.4arcsec',
      weighting='briggs',
      robust=2.0,
      interactive=False)

# rms in '170, 0, 255, 80' = 0.064 mJy/beam
stats_cont_dirty = imstat(imagename=targetname+'_cont_dirty.image', box = '170, 0, 255, 80')

rms_cont_dirty = stats_cont_dirty['rms'][0]*1e3

clthr_cont = 5*rms_cont_dirty 

clthr_cont = '%0.1f' %clthr_cont+'mJy'


# Clean Continuum NA Image
os.system('rm -rf '+targetname+'_cont.*')
clean(vis=my_vis,
      imagename=targetname+'_cont',
      spw='0~2,3:0~2400,3:3100~3839',
      field=fld,
      mode='mfs',
      niter=10000,
      threshold=clthr_cont,
      imsize=256,
      cell='0.4arcsec',
      weighting='briggs',
      robust=2.0,       # Natural weighting
      interactive=False)



#Dirty Continuum Uniform Weighting
os.system('rm -rf '+targetname+'_cont_dirty_uw*')

clean(vis=my_vis,
      imagename=targetname+'_cont_dirty_uw',
      spw='0~2,3:0~2400,3:3100~3839',
      field=fld,
      mode='mfs',
      niter=0,
      imsize=256,
      cell='0.4arcsec',
      weighting='briggs',
      robust=-2.0,
      interactive=False)


stats_cont_dirty_uw = imstat(imagename=targetname+'_cont_dirty_uw.image', box = '170, 0, 255, 80')

#0.33 mJy/beam
rms_cont_dirty_uw = stats_cont_dirty_uw['rms'][0]*1e3

clthr_cont_uw = 5*rms_cont_dirty_uw 

clthr_cont_uw = '%0.1f' %clthr_cont_uw+'mJy'

# Clean Continuum Uniform Image
os.system('rm -rf '+targetname+'_cont_uw*')
clean(vis=my_vis,
      imagename=targetname+'_cont_uw',
      spw='0~2,3:0~2400,3:3100~3839',
      field=fld,
      mode='mfs',
      niter=10000,
      threshold=clthr_cont_uw,
      imsize=256,
      cell='0.4arcsec',
      weighting='briggs',
      robust=-2.0,
      interactive=False)
#rms = 0.34 mJy/beam


# Continuum Subtraction
os.system('rm -rf '+my_vis+'.contsub')
uvcontsub(vis=my_vis,
          fitspw='0~2,3:0~2350,3:3150~3839',
          field=fld,
          solint='int',
          fitorder=1,
          combine='spw')

# CO(1-0) rest freq = 115.271GHz
# NGC4451 is at z=0.00290
# CO(1-0) freq at z = 114.936GHz

# Dirty Line NA
os.system('rm -rf '+targetname+'_line_CO_dirty.*')
clean(vis=my_vis+'.contsub',
      imagename=targetname+'_line_CO_dirty',
      field=fld,
      spw='3:2400~3100',
      mode='velocity',
      outframe='bary',
      nchan=40,
      start='-300km/s',
      width='15km/s',
      restfreq='114.936GHz',
      niter=0,
      imsize=256,
      cell='0.4arcsec',
      weighting='briggs',
      robust=2.0,
      pbcor=True,
      interactive=False)

# RMS Map
os.system('rm -rf '+targetname+'_line_CO_dirty.mom6')
immoments(imagename=targetname+'_line_CO_dirty.image',              
          moments=[6],                                               
          chans='0,1,2,3,37,38,39',                                 
          outfile=targetname+'_line_CO_dirty.mom6')                   


# rms = 5 mJy/beam over the whole image
imst=imstat(imagename=targetname+'_line_CO_dirty.mom6')

os.system('rm -rf '+targetname+'_line_CO_05_dirty.*')
clean(vis=my_vis+'.contsub',
      imagename=targetname+'_line_CO_05_dirty',
      field=fld,
      spw='3:2400~3100',
      mode='velocity',
      outframe='bary',
      nchan=40,
      start='-300km/s',
      width='15km/s',
      restfreq='114.936GHz',
      niter=0,
      imsize=256,
      cell='0.4arcsec',
      weighting='briggs',
      robust=0.5,
      pbcor=True,
      interactive=False)

os.system('rm -rf '+targetname+'_line_CO_05_dirty.mom6')
immoments(imagename=targetname+'_line_CO_05_dirty.image',              
          moments=[6],                                               
          chans='0,1,2,3,37,38,39',                                 
          outfile=targetname+'_line_CO_05_dirty.mom6')                   

imst=imstat(imagename=targetname+'_line_CO_05_dirty.mom6')

os.system('rm -rf '+targetname+'_line_autothresh*')
tclean(vis=my_vis+'.contsub',
      imagename=targetname+'_line_autothresh',
      field=fld,
      spw='3:2500~3000',
      imsize=256,
      cell='0.4arcsec',
      stokes='I',
      specmode='cube',
      nchan=55,
      start='-300km/s',
      width='10km/s',
      restfreq='114.936GHz',
      veltype='radio',
      gridder='standard',
      deconvolver='hogbom',
      restoringbeam='common',
      weighting='briggs',
      robust=0.5,
      niter=1000000,
      threshold=str(imst['rms'][0])+'Jy',
      usemask='auto-multithresh',
      pbmask=0.0,
      sidelobethreshold=2.0,
      noisethreshold=4.25,
      lownoisethreshold=1.5,
      negativethreshold=15.0,
      minbeamfrac=0.3,
      growiterations=75,
      interactive=False)


os.system('rm -rf '+targetname+'_line_autothresh.mom6')
immoments(imagename=targetname+'_line_autothresh.image',            
          moments=[6],                                               
          chans='0~3,52~54',                                          
          outfile=targetname+'_line_autothresh.mom6')                   

imst=imstat(imagename=targetname+'_line_autothresh.mom6')
print imst['rms']*1e3

os.system('rm -rf '+targetname+'_CO01_autothresh.mom0*')
immoments(imagename=targetname+'_line_autothresh.image',
          moments=[0],
          chans='4~51',
          box='80,75,175,185',
          outfile=targetname+'_CO01_autothresh.mom0')

os.system('rm -rf '+targetname+'_CO01_autothresh.mom1*')
immoments(imagename=targetname+'_line_autothresh.image', 
          moments=[1], 
          chans='4~51', 
          box='80,75,175,185',
          includepix=[imst['rms'][0]*3.0, 100000],
          outfile=targetname+'_CO01_autothresh.mom1')

os.system('rm -rf '+targetname+'_CO01_autothresh.mom2*')
immoments(imagename=targetname+'_line_autothresh.image', 
          moments=[2], 
          chans='4~51', 
          box='80,75,175,185',
          includepix=[imst['rms'][0]*5.0, 100000],
          outfile=targetname+'_CO01_autothresh.mom2')


