# Image_Cutout_Contours_Creator
A code that uses ds9 and topcat and CASA to create optical cutouts with radio contours



These codes were created in IDL by Mladen and Vernesa
and modified to python by me.

Together they create cutouts from the optical field and then save the
png images of the cutouts. The png images will have the 
radio contours visible to indicate radio emission.

The program now works in CASA (Cut_Universal.py) and
python3 (Png_Creator.py). It no longer requires IDL. 
It does, however, require Topcat and ds9 to work.

It was also modified to handle a field divided into 
subfields. The name of the subfields must be uniform.
For example: I1_XXLT020631-0412_mosaic.fits.
For more details see the beginning of the code.
This feature can be deactivated with the "Multiple_Subfields"
parameter in case you have only one complete field.

The folder contains:
1) Cut_Universal.py: This is the code used to create the cutouts.
                     It must be run with CASA.

2) Png_Creator.py  : This code creates the png images by using
                     the created radio and optical cutouts. It
                     now works in python3.
