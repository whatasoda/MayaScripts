import maya.cmds as cmds
import math as m
import sys

def sphericalVRCameraLens(ew, ln, lf, ih, iv, ior, eye):
    ## (width between eyes, near radius of lens, far radius of lens,
    ## image horizonal count, image virtical count, index of refraction, left eye or right eye)
    theta = m.atan2(lf - ln, ew / 2)
    lfr = m.atan(ior * m.sin(theta) / (ior * m.cos(theta) - 1)) # lens face radian
    urh = 2 * m.pi / ih # horizonal unit radian
    udh = m.degrees(urh) # horizonal unit degree
    urv = m.pi / iv # vertical unit radian
    rn = ln / m.cos(urh / 2) # point radius near
    rf = lf / m.cos(urh / 2) # point radius far
    gb0 = -eye * m.tan(urh / 2) / m.sin((m.pi + urh) / 2 - lfr) * m.sin(lfr) # point radius gap base #0
    gb1 = eye * m.tan(urh / 2) / m.sin((m.pi - urh) / 2 - lfr) * m.sin(lfr) # point radius gap base #1
    rn0, rn1, rn2, rn3, rf0, rf1, rf2, rf3 = [], [], [], [], [], [], [], []
    rv0, rv1 = 0, urv
    for pv in range(iv): # pixel width count
        cosv0, cosv1 = m.cos(rv0-m.pi/2), m.cos(rv1-m.pi/2)
        rn0.append(rn + ln * gb0 * cosv0) # point radius near #0
        rn1.append(rn + ln * gb0 * cosv1) # point radius near #1
        rn2.append(rn + ln * gb1 * cosv1) # point radius near #2
        rn3.append(rn + ln * gb1 * cosv0) # point radius near #3
        rf0.append(rf + lf * gb1 * cosv0) # point radius far #0
        rf1.append(rf + lf * gb1 * cosv1) # point radius far #1
        rf2.append(rf + lf * gb0 * cosv1) # point radius far #2
        rf3.append(rf + lf * gb0 * cosv0) # point radius far #3
        rv0 += urv
        rv1 += urv
    rv0, rv1 = 0, urv
    lensh, lensv = [], []
    cosh0, cosh1 = 1, m.cos(urh)
    sinh0, sinh1 = 0, m.sin(urh)
    for pv in range(iv): # pixel virtical count
        cosv0, cosv1 = m.cos(rv0-m.pi/2), m.cos(rv1-m.pi/2)
        sinv0, sinv1 = m.sin(rv0-m.pi/2), m.sin(rv1-m.pi/2)
        pn = [
            (sinh0 * cosv0 * rn0[pv], sinv0 * rn0[pv], cosh0 * cosv0 * rn0[pv]),
            (sinh0 * cosv1 * rn1[pv], sinv1 * rn1[pv], cosh0 * cosv1 * rn1[pv]),
            (sinh1 * cosv1 * rn2[pv], sinv1 * rn2[pv], cosh1 * cosv1 * rn2[pv]),
            (sinh1 * cosv0 * rn3[pv], sinv0 * rn3[pv], cosh1 * cosv0 * rn3[pv]),
        ]
        lensv.append(cmds.polyCreateFacet(ch=0,p=pn)[0])
        pf = [
            (sinh1 * cosv0 * rf0[pv], sinv0 * rf0[pv], cosh1 * cosv0 * rf0[pv]),
            (sinh1 * cosv1 * rf1[pv], sinv1 * rf1[pv], cosh1 * cosv1 * rf1[pv]),
            (sinh0 * cosv1 * rf2[pv], sinv1 * rf2[pv], cosh0 * cosv1 * rf2[pv]),
            (sinh0 * cosv0 * rf3[pv], sinv0 * rf3[pv], cosh0 * cosv0 * rf3[pv]),
        ]
        lensv.append(cmds.polyCreateFacet(ch=0,p=pf)[0])
        cmds.move(ew * m.sin((urh+m.pi)*eye/2) / 2,0,ew * m.cos((urh+m.pi)*eye/2) / 2)
        rv0 += urv
        rv1 += urv
    lensh.append(cmds.polyUnite(lensv, ch=0)[0])
    prog = 0
    print "[" + ("----@" * 20) + "]"
    sys.stdout.write("[")
    for ph in range(ih-1): # pixel horizonal count
        lensh.append(cmds.duplicate(lensh[ph])[0])
        cmds.rotate(0,str(udh*(ph+1))+"deg",0)
        if prog != int(m.floor(100 * ph / ih)):
            for n in range(int(m.floor(100 * ph / ih)) - prog):
                prog += 1
                sys.stdout.write("@" if prog%5 == 0 else "#")
    cmds.polyUnite(lensh, ch=0,n='sphericalVRCameraLens01')
    print "]"
sphericalVRCameraLens(3,20,60,960,540,1.1,1)
