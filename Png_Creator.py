from astropy.io import fits
import subprocess
import os
##############################################################
Input_Folder  = 'Input/'
Output_Folder = 'Output/'

Catalogue_Name = 'Cat_Test.fits'
Contour_Field  = '_RCutout' #Without number
Image_Field    = '_Cutout' #Without number

Ra_Column  = 'RA'
Dec_Column = 'DEC'
Id_Column  = 'SourceId'

ds9 = '/Users/Astro/Documents/Software/ds9.darwinsierra.7.5/ds9'
#You also need two folders named "Contours" & "Regions"
#for the contours and regions. The files inside should
#be called CNT.lev and REG.reg (or maybe In Out: see code)!
##############################################################
Catalogue = fits.open(Input_Folder + Catalogue_Name)[1].data
ra        = Catalogue[Ra_Column]
dec       = Catalogue[Dec_Column]
id        = Catalogue[Id_Column]

for i in range(0, len(ra)):
    comm = ds9+' '+Input_Folder+str(id[i])+Contour_Field+'.fits -scale zscale' +\
           ' -contour smooth 1' +\
           ' -contour loadlevels Contours/Out.lev' +\
           ' -contour' +\
           ' -contour save Contours/png_maker.ctr wcs fk5' +\
           ' -contour no' +\
           ' '+Input_Folder+str(id[i])+Image_Field+'.fits -scale zscale -single' +\
           ' -contour load Contours/png_maker.ctr wcs fk5 blue 2 no' +\
           ' -contour close' +\
           ' -pan to '+str(ra[i])+' '+str(dec[i])+' wcs fk5 -view colorbar yes -scale zscale -geometry 800x800'+\
           ' -regions Regions/REG.reg' +\
           ' -zoom to 2 -pan to '+str(ra[i])+' '+str(dec[i])+' wcs fk5 -saveimage png '+Output_Folder+'Png_Picture'+str(id[i])+'.png' +\
           ' -exit'
    print(id[i])
    print(ra[i])
    print(dec[i])
    print(comm)
    subprocess.call(comm, shell=True)   #same as os.system but new



