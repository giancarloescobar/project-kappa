""" Script to run diagnostic analysis on FMRI run
The FMRI 'run' is a continuous collection of one or more 3D volumes.
A run is usually stored as a 4D NIfTI image.
In this case we are analyzing the 4D NIfTI image: "ds114_sub009_t2r1.nii"
Fill in the code necessary under the comments below.
As you are debugging, we suggest you run this script from within IPython, with
::
    run diagnosis_script.py
Remember, in IPython, that you will need to "reload" any modules that have
changed.  So, if you have imported your module like this:
    import diagnostics
Then you will need to run this before rerunning your script, to get the latest
version of the code.
    reload(diagnostics)
Before you submit your homework, don't forget to check this script also runs
correctly from the terminal, with::
    python diagnosis_script.py
"""

# import standard libraries here
import diagnostics as dg
import numpy as np
import numpy.linalg as npl
import matplotlib.pyplot as plt
import nibabel as nib


"""
* Load the image as an image object
* Load the image data from the image
* Drop the first four volumes, as we know these are outliers
"""
img = nib.load('test.nii')
data = img.get_data()


"""
data = data[...,4:]
Use your vol_std function to get the volume standard deviation values for the
remaining 169 volumes.
Write these 169 values out to a text file.
*IMPORTANT* - this text file MUST be called 'vol_std_values.txt'
"""
stds = dg.vol_std(data)
np.savetxt('vol_std_values.txt' ,stds)

"""
Use the iqr_outlier detection routine to get indices of outlier volumes.
Write these indices out to a text file.
*IMPORTANT* - this text file MUST be called 'vol_std_outliers.txt'
"""
outliers = dg.iqr_outliers(dg.vol_std(data))[0]
np.savetxt('vol_std_outliers.txt' , outliers)

"""
Plot all these on the same plot:
* The volume standard deviation values;
* The outlier points from the std values, marked on the plot with an 'o'
  marker;
* A horizontal dashed line at the lower IRQ threshold;
* A horizontal dashed line at the higher IRQ threshold;
Extra points for a good legend to the plot.
Save the figure to the current directory as ``vol_std.png``.
IMPORTANT - use exactly this name.
"""
IQR = np.percentile(stds, [75,25])[0] - np.percentile(stds, [75,25])[1]
max = np.percentile(stds, [75,25])[0]+(IQR*1.5)
min = np.percentile(stds, [75,25])[1]-(IQR*1.5)

plt.plot(stds)
plt.plot(np.arange(len(stds))[outliers],np.array(stds)[outliers],'o', color='r')
plt.axhline(y = min,color = 'g', ls = 'dashed')
plt.axhline(y = max, color = 'y', ls = 'dashed')

plt.xlabel('Voxel')
plt.ylabel('STD')
plt.title('STD of Voxels')
plt.legend(['STD','Outlier','.25','.75'], loc = 1)

plt.savefig('vol_std.png')
plt.close()

""" Next calculate and plot the RMS difference values
* Calculate the RMS difference values for the image data;
* Use the ``iqr_outlier`` function to return indices of possible outliers in
  this RMS difference vector;
On the same plot, plot the following:
* The RMS vector;
* The identified outlier points marked with an `o` marker;
* A horizontal dashed line at the lower IRQ threshold;
* A horizontal dashed line at the higher IRQ threshold;
IMPORTANT - save this plot as ``vol_rms_outliers.png``
"""

diff = dg.vol_rms_diff(data)

IQR2 = np.percentile(diff, [75,25])[0] - np.percentile(diff, [75,25])[1]
max2 = np.percentile(diff, [75,25])[0]+(IQR2*1.5)
min2 = np.percentile(diff, [75,25])[1]-(IQR2*1.5)

outliers2 = dg.iqr_outliers(diff)

plt.plot(diff)
plt.plot(np.arange(len(diff))[outliers2[0]],np.array(diff)[outliers2[0]],'o', color='r')
plt.axhline(y = min2, color = 'g', ls = 'dashed')
plt.axhline(y = max2, color = 'y', ls = 'dashed')

plt.xlabel('Voxel')
plt.ylabel('RMS')
plt.title('RMS of Voxel')
plt.legend(['STD','Outlier','.25','.75'], loc = 1)

plt.savefig('vol_rms_outliers.png')
plt.close()

""" Use the ``extend_diff_outliers`` to label outliers
Use ``extend_diff_outliers`` on the output from ``iqr_outliers`` on the RMS
difference values.  This gives you indices for labeled outliers.
On the same plot, plot the following:
* The RMS vector with a 0 appended to make it have length the same as the
  number of volumes in the image data array;
* The identified outliers shown with an `o` marker;
* A horizontal dashed line at the lower IRQ threshold;
* A horizontal dashed line at the higher IRQ threshold;
IMPORTANT - save this plot as ``extended_vol_rms_outliers.png``
"""

rms_index = dg.extend_diff_outliers(outliers2[0])

plt.plot(np.append(diff, 0))
plt.plot(np.arange(len(diff))[rms_index],np.array(diff)[rms_index],'o', color='r')
plt.axhline(y = min2, color = 'g', ls = 'dashed')
plt.axhline(y = max2, color = 'y', ls = 'dashed')

plt.xlabel('Voxel')
plt.ylabel('RMS')
plt.title('RMS of Voxel')
plt.legend(['STD','Outlier','.25','.75'], loc = 1)

plt.savefig('extended_vol_rms_outliers.png')
plt.close()

""" Write the extended outlier indices to a text file.
IMPORTANT: name the text file extended_vol_rms_outliers.txt
"""

np.savetxt('extended_vol_rms_outliers.txt' ,rms_index)

""" Show that the residuals drop when removing the outliers
Create a design matrix for the image data with the convolved neural regressor
and an intercept column (column of 1s).
Load the convolved neural time-course from ``ds114_sub009_t2r1_conv.txt``.
Fit this design to estimate the (2) betas for each voxel.
Subtract the fitted data from the data to form the residuals.
Calculate the mean residual sum of squares (MRSS) at each voxel (the sum of
squared divided by the residual degrees of freedom).
Finally, take the mean of the MRSS values across voxels.  Print this value.
convolved = np.loadtxt('ds114_sub009_t2r1_conv.txt')[4:]
design = np.ones((len(convolved), 2))
data_2d = np.reshape(data, (-1, data.shape[-1]))
betas_4d = np.reshape(betas.T, img.shape[:-1] + (-1,))
"""

"""
Next do the exactly the same, except removing the extended RMS difference
outlier volumes from the data and the corresponding rows for the design.
Print the mean of the RMSS values across voxels. Is this value smaller?
"""

""" Now save these two mean MRSS values to a text file
IMPORTANT: save to ``mean_mrss_vals.txt``
"""


# Some final checks that you wrote the files with their correct names
from os.path import exists
assert exists('vol_std_values.txt')
assert exists('vol_std_outliers.txt')
assert exists('vol_std.png')
assert exists('vol_rms_outliers.png')
assert exists('extended_vol_rms_outliers.png')
assert exists('extended_vol_rms_outliers.txt')