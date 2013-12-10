#!/usr/bin/python
import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt
plt.rc('ps', usedistiller="xpdf")
plt.rc('font',**{'family':'serif','serif':['Computer Modern Serif']})
plt.rc('text', usetex=True)
plt.rc("font", size=8)

#http://www.scipy.org/Cookbook/Matplotlib/ColormapTransformations
def cmap_map(function,cmap):
    """ Applies function (which should operate on vectors of shape 3:
    [r, g, b], on colormap cmap. This routine will break any discontinuous     points in a colormap.
    """
    cdict = cmap._segmentdata
    step_dict = {}
    # Firt get the list of points where the segments start or end
    for key in ('red','green','blue'):         step_dict[key] = map(lambda x: x[0], cdict[key])
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step : np.array(cmap(step)[0:3])
    old_LUT = np.array(map( reduced_cmap, step_list))
    new_LUT = np.array(map( function, old_LUT))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i,key in enumerate(('red','green','blue')):
        this_cdict = {}
        for j,step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j,i]
            elif new_LUT[j,i]!=old_LUT[j,i]:
                this_cdict[step] = new_LUT[j,i]
        colorvector=  map(lambda x: x + (x[1], ), this_cdict.items())
        colorvector.sort()
        cdict[key] = colorvector

    return mat.colors.LinearSegmentedColormap('colormap',cdict,1024)

#GaAs GaSb AlSb CdTe Ge ZnTe InP GaP
lattice_constants_all=np.array([5.6533, 6.0959, 6.1355, 6.482, 5.64613, 6.1034, 5.8686, 5.4512])
#Remove Closely Spaced #GaAs GaSb AlSb CdTe InP GaP
lattice_constants=np.array([5.6533, 6.0959, 6.1355, 6.482, 5.8686, 5.4512])
mismatch = (lattice_constants - 5.43095)/5.43095 * 100
af_as = np.linspace(1,1.20,num=90)
tilt = np.linspace(0,4.10695300643,num=94)
x, y = np.meshgrid(tilt, af_as)
x2, y2 = np.meshgrid(tilt, (af_as - 1)*100)
strain_epi = y/np.sqrt(3)/np.sin(np.radians(19.4712 + x)) - 1/np.sqrt(3)/np.sin(np.radians(19.4712))
strain_twin = y/(2*np.sin(np.radians(74.2068 + x))) -  1/np.sqrt(3)
fig = plt.figure(1, figsize=(4,2.53))
ax = fig.add_subplot(111)

print np.amax(strain_epi)
print np.amin(strain_epi)

print "Epitaxial on Si"
print "GaAs GaSb AlSb CdTe Ge ZnTe InP GaP"
print np.degrees(np.arcsin(lattice_constants_all/5.43095 * np.sin(np.radians(19.4712)))) - 19.4712
print "Epitaxial CdTe/GaAs"
print np.degrees(np.arcsin(lattice_constants_all[3]/lattice_constants_all[0] * np.sin(np.radians(19.4712)))) - 19.4712

print "Twinned"
print "GaAs GaSb AlSb CdTe Ge ZnTe InP GaP"
print np.degrees(np.arcsin(np.sqrt(3)*lattice_constants_all/(2*5.43095))) - 74.2068

print "Test"
print np.degrees(np.arcsin(1.2 * np.sin(np.radians(19.4712)))) - 19.4712

plt.hold(True)
plt.axis([0,4.10695300643,0,20])
#plt.pcolormesh(x,y2,strain_epi, cmap=cmap_map(lambda x: x/2.0+0.4, plt.cm.RdBu))
plt.pcolormesh(x,y2,strain_epi, cmap=plt.cm.bwr, vmin=-0.32, vmax=+0.32, rasterized=True)
#plt.colorbar(use_gridspec=True, format="%+1.2f", ticks=[-0.6,-0.45,-0.3,-0.15,0,0.15,0.3,0.45,0.6] )
cb = plt.colorbar(use_gridspec=True, format="%+1.2f")
cb.solids.set_rasterized(True) 
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.5))
ax.yaxis.set_major_locator(plt.MultipleLocator(2.5))
ax.yaxis.set_minor_locator(plt.MultipleLocator(1.25))

plt.xlabel('Tilt (Degrees)')
plt.ylabel('Intrinsic Lattice Mismatch (\%)')
#plt.title('Effective Mismatch of Tilted Strained Films')

CS = plt.contour(x,y2,strain_epi,levels=[0], colors='black', linestyles='dashdot', zorder=100)
#Change dash-dot pattern, on, off, on, off
for c in CS.collections:
    c.set_dashes([(0, (4.0, 3.0, 1.0, 3.0))])
    
ax.annotate('Zero Projected Strain', xy=(1.55, 7.45), xytext=(1.75, 5.5),
            arrowprops=dict(facecolor='black', shrink=0.1,width=0.05,headwidth=2),
            )
plt.tight_layout(pad=0)
plt.savefig('step1.pdf', bbox_inches='tight', dpi=600, pad_inches=0, transparent=True)


#Ours 916
plt.scatter(2.65, mismatch[1], color='red', marker='x', s=21, facecolors='none', zorder=500, lw=0.75)
#Ours 1046
plt.scatter(2.55, mismatch[1], color='red', marker='x', s=21, facecolors='none', zorder=500, lw=0.75)
#Ours 1300
plt.scatter(2.40, mismatch[1], color='red', marker='x', s=21, facecolors='none', zorder=500, lw=0.75)

plt.savefig('step2.pdf', bbox_inches='tight', dpi=600, pad_inches=0, transparent=True)


#Plot all the mismatch lines
for item in mismatch:
    plt.plot([0.02, 5], [item, item], linestyle='dashed', color='white')

#Plot one not on silicon (CdTe on GaAs)
plt.plot([0.02, 5], [(6.482 - 5.6533)/5.6533 * 100, (6.482 - 5.6533)/5.6533 * 100], linestyle='dashed', color='white')

plt.text(0.1, 18.4, 'CdTe/Si')
plt.text(0.1, 13.2, 'AlSb/Si')
plt.text(0.1, 11.2, 'GaSb\&ZnTe/Si')
plt.text(0.1, 7, 'InP/Si')
plt.text(0.1, 4.4, 'GaAs\&Ge/Si')
plt.text(0.1, 0.6, 'GaP/Si')
plt.text(0.1, 15, 'CdTe/GaAs')


plt.savefig('step3.pdf', bbox_inches='tight', dpi=600, pad_inches=0, transparent=True)


#Others
plt.scatter(3.5, mismatch[3], marker='o', s=30, color='black', facecolors='none', zorder=500, lw=0.75)
plt.scatter(3.5, mismatch[3], marker='.', s=4, edgecolor='none', facecolors='black', zorder=500)

plt.scatter(2.66, mismatch[1], marker='s', s=30, color='black', facecolors='none', zorder=500, lw=0.75)
plt.scatter(2.66, mismatch[1], marker='.', s=4, edgecolor='none', facecolors='black', zorder=500)

#From referees Johnson GaAs on Si
plt.scatter(0.781, mismatch[0], marker=(3, 0, 0), s=40, color='black', facecolors='none', zorder=500, lw=0.75)
plt.scatter(0.781, mismatch[0], marker='.', s=4, edgecolor='none', facecolors='black', zorder=500)

#From referees Johnson CdTe on GaAs
plt.scatter(4.098-0.835, (6.482 - 5.6533)/5.6533 * 100, marker='D', s=30, color='black', facecolors='none', zorder=500, lw=0.75)
plt.scatter(4.098-0.835, (6.482 - 5.6533)/5.6533 * 100, marker='.', s=4, edgecolor='none', facecolors='black', zorder=5)

#From David Smith at II-VI Conference ZnTe-Si
plt.scatter(2.24, (6.1034 - 5.43095)/5.43095 * 100, marker='p', s=40, color='black', facecolors='none', zorder=500, lw=0.75)
plt.scatter(2.24, (6.1034 - 5.43095)/5.43095 * 100, marker='.', s=4, edgecolor='none', facecolors='black', zorder=500)

#From David Smith at II-VI Conference CdTe-GaAs
plt.scatter(2.6, (6.482 - 5.6533)/5.6533 * 100, marker='h', s=40, color='black', facecolors='none', zorder=500, lw=0.75)
plt.scatter(2.6, (6.482 - 5.6533)/5.6533 * 100, marker='.', s=4, edgecolor='none', facecolors='black', zorder=500)

plt.savefig('step4.pdf', bbox_inches='tight', dpi=600, pad_inches=0, transparent=True)

#plt.savefig('tiltmap_epitaxial.eps', bbox_inches='tight', dpi=600, pad_inches=0, transparent=True)
#plt.savefig('tiltmap_epitaxial.png', bbox_inches='tight', dpi=600, pad_inches=0, transparent=True)
#plt.show()
