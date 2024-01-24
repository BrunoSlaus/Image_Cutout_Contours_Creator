#Code that uses CASA for the creation of cutouts.
#If the image is composed of sub-images i.e.
#sub-fields, you need to provide a txt file with
#2 columns for RA and DEC centres of the subfields.
#The program will work only if all the subfields are
#THE SAME SIZE AND NEATLY ARRANGED. The columns should
#be named RA_Centres & DEC_Centres.
#The form of the names of the subfields must be as
#follows:
#Name_Prefix + RA_Centre + Name_Dash + DEC_Centre + Name_Suffix
#RA_Centre  == HHMMSS
#DEC_Centre == DDMM
#For example: I1_XXLT020631-0412_mosaic.fits

import pyfits
import numpy as np
#######################################################################
#Parameters:
#######################################################################
Input_Folder  = 'Input/'
Output_Folder = 'Output/'

#Is the map composed from subfields i.e. map-parts?
Multiple_Subfields = 'No'

#Name parameters for Multiple_Subfields == Yes
#Assumed name format is as follows:
#Name_Prefix + RA_Centre + Name_Dash + DEC_Centre + Name_Suffix
Name_Prefix = 'I1_XXLT'
Name_Dash   = '-'
Name_Suffix = '_mosaic.fits'
Ra_Dec_Centres_File_Name = 'RaDec_Centres.txt'

#Name parameters for Multiple_Subfields == No
Field_Name = 'XXL-N_GMRT610.FITS'

#Catalogue name and columns
Catalogue_Name  = 'Matched_REL.fits'
RA_Column_Name  = 'RA_1'
DEC_Column_Name = 'DEC_1'
ID_Column_Name  = 'Id'
#######################################################################
Catalogue = pyfits.core.getdata(Input_Folder + Catalogue_Name, 1) 
RA_Column  = Catalogue.field(RA_Column_Name)
DEC_Column = Catalogue.field(DEC_Column_Name)
ID_Column  = Catalogue.field(ID_Column_Name)
print('ID_Column of sources in catalogue: ', ID_Column)

if Multiple_Subfields == 'Yes':
    with open(Input_Folder + Ra_Dec_Centres_File_Name, 'r') as Ra_Dec_Centres_File:
        Ra_Dec_Centres = np.loadtxt(Ra_Dec_Centres_File, dtype=str)
    Ra_Centres_String  = Ra_Dec_Centres[:,0]
    Dec_Centres_String = Ra_Dec_Centres[:,1]

    for i in range(0,len(RA_Column)):
        h = np.zeros(len(Ra_Centres_String))
        for j in range(len(Ra_Centres_String)):
            h[j] = float(Ra_Centres_String[j][0:2])
        m = np.zeros(len(Ra_Centres_String))
        for j in range(len(Ra_Centres_String)):
            m[j] = float(Ra_Centres_String[j][2:4])
        s = np.zeros(len(Ra_Centres_String))
        for j in range(len(Ra_Centres_String)):
            s[j] = float(Ra_Centres_String[j][4:6])            
        Ra_Centres_Values  = (h + m/60 + s/3600) * 360/24
        Ra_index = (np.abs(Ra_Centres_Values-RA_Column[i])).argmin()
        Ra_Centres_Closest = str(Ra_Centres_String[Ra_index])

        h = np.zeros(len(Dec_Centres_String))
        for j in range(len(Dec_Centres_String)):
            h[j] = float(Dec_Centres_String[j][0:2])
        m = np.zeros(len(Dec_Centres_String))
        for j in range(len(Dec_Centres_String)):
            m[j] = float(Dec_Centres_String[j][2:4])
        #s = np.zeros(len(Dec_Centres_String))
        #for j in range(len(Dec_Centres_String)):
            #s[j] = float(Dec_Centres_String[j][4:6])            
        Dec_Centres_Values  = (h + m/60) # + s/3600) 
        Dec_index = (np.abs( Dec_Centres_Values-np.abs(DEC_Column[i]) )).argmin()
        Dec_Centres_Closest = str(Dec_Centres_String[Dec_index])
        
        Field_Name = Name_Prefix + Ra_Centres_Closest + Name_Dash + Dec_Centres_Closest + Name_Suffix
        print('')
        print('Opening field: ', Field_Name)
        Imagename  = Output_Folder + 'Image_Temp.image'
        importfits(fitsimage = Input_Folder + Field_Name, imagename = Imagename, overwrite=True)
        print('Output saved in: ', Output_Folder + str(ID_Column[i]) + '_Cutout.fits')       
        try:
            imsubimage(imagename = Imagename,\
                       region='centerbox[[' +str(RA_Column[i]) + 'deg, ' + str(DEC_Column[i]) + 'deg],[50arcsec,50arcsec]]',\
                       outfile = Output_Folder + 'Cutout_Image_Temp.image', overwrite=True)
            exportfits(imagename = Output_Folder + 'Cutout_Image_Temp.image',fitsimage = Output_Folder + str(ID_Column[i]) + '_Cutout.fits',\
                       overwrite=True)
        except:
            print('WARNING: Unable to create cutout ' + str(ID_Column[i]) + '!')

            
if Multiple_Subfields == 'No':
    for i in range(0,len(RA_Column)):
        print('')
        print('Opening field: ', Field_Name)
        Imagename  = Output_Folder + 'Image_Temp.image'        
        importfits(fitsimage = Input_Folder + Field_Name, imagename = Imagename, overwrite=True)
        print('Output saved in: ', Output_Folder + str(ID_Column[i]) + '_Cutout.fits')       

        try:
            imsubimage(imagename = Imagename,\
                       region='centerbox[[' +str(RA_Column[i]) + 'deg, ' + str(DEC_Column[i]) + 'deg],[50arcsec,50arcsec]]',\
                       outfile = Output_Folder + 'Cutout_Image_Temp.image', overwrite=True)
            exportfits(imagename = Output_Folder + 'Cutout_Image_Temp.image',fitsimage = Output_Folder + str(ID_Column[i]) + '_Cutout.fits',\
                       overwrite=True)
        except:
            print('WARNING: Unable to create cutout ' + str(ID_Column[i]) + '!')

os.system('rm -rf ' + Output_Folder + '*.image')
#######################################################################
#End of code:

#######################################################################
		
