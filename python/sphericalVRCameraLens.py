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
    fm = (ew * m.sin((urh+m.pi)*eye/2) / 2,ew * m.cos((urh+m.pi)*eye/2) / 2) # far movement value
    rn0, rn1, rf0, rf1 = [], [], [], []
    rv = urv
    for pv in range(iv-1): # pixel width count
        cosv = m.cos(rv-m.pi/2)
        rn0.append(rn + ln * gb0 * cosv) # point radius near #0
        rn1.append(rn + ln * gb1 * cosv) # point radius near #1
        rf0.append(rf + lf * gb1 * cosv) # point radius far #0
        rf1.append(rf + lf * gb0 * cosv) # point radius far #1
        rv += urv
    cosh0, cosh1 = 1, m.cos(urh)
    sinh0, sinh1 = 0, m.sin(urh)
    pn = [ (0, -rn, 0),
        (sinh0 * m.cos(urv-m.pi/2) * rn0[0], m.sin(urv-m.pi/2) * rn0[0], cosh0 * m.cos(urv-m.pi/2) * rn0[0]),
        (sinh1 * m.cos(urv-m.pi/2) * rn1[0], m.sin(urv-m.pi/2) * rn1[0], cosh1 * m.cos(urv-m.pi/2) * rn1[0]),
    ]
    lensvn = cmds.polyCreateFacet(ch=0,p=pn)[0]
    rv = 2*urv
    for pv in range(iv-2): # pixel virtical count
        cosv, sinv = m.cos(rv-m.pi/2), m.sin(rv-m.pi/2)
        pn = [ 3*pv+1,
            (sinh0 * cosv * rn0[pv+1], sinv * rn0[pv+1], cosh0 * cosv * rn0[pv+1]),
            (sinh1 * cosv * rn1[pv+1], sinv * rn1[pv+1], cosh1 * cosv * rn1[pv+1]),
        ]
        cmds.polyAppend(ch=0,a=pn)
        rv += urv
    pn = [ 3*(iv-2)+1, (0, rn, 0)]
    cmds.polyAppend(ch=0,a=pn)
    pf = [ (fm[0], -rf, fm[1]),
        (sinh1 * m.cos(urv-m.pi/2) * rf0[0] + fm[0], m.sin(urv-m.pi/2) * rf0[0] + fm[1], cosh1 * m.cos(urv-m.pi/2) * rf0[0] + fm[1]),
        (sinh0 * m.cos(urv-m.pi/2) * rf1[0] + fm[0], m.sin(urv-m.pi/2) * rf1[0] + fm[1], cosh0 * m.cos(urv-m.pi/2) * rf1[0] + fm[1]),
    ]
    lensvf = cmds.polyCreateFacet(ch=0,p=pf)[0]
    rv = 2*urv
    for pv in range(iv-2): # pixel virtical count
        cosv, sinv = m.cos(rv-m.pi/2), m.sin(rv-m.pi/2)
        pf = [ 3*pv+1,
            (sinh1 * cosv * rf0[pv+1] + fm[0], sinv * rf0[pv+1] + fm[1], cosh1 * cosv * rf0[pv+1] + fm[1]),
            (sinh0 * cosv * rf1[pv+1] + fm[0], sinv * rf1[pv+1] + fm[1], cosh0 * cosv * rf1[pv+1] + fm[1]),
        ]
        cmds.polyAppend(ch=0,a=pf)
        rv += urv
    pf = [ 3*(iv-2)+1, (fm[0], rf, fm[1])]
    cmds.polyAppend(ch=0,a=pf)
    lensh = [cmds.polyUnite([lensvn, lensvf], ch=0)[0]]
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
sphericalVRCameraLens(3,20,60,40,40,1.1,1)
