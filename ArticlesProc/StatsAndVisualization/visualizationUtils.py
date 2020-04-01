def hslToRgb(h, s, l):
    '''Converts h, s, and l values to a color code of the form #FFFFFF'''
    # print(h,s,l)
    # Apply h
    h = abs(h) % 360
    r = 255*abs(h-180)/180
    h += 120
    h = h % 360
    b = 255*abs(h-180)/180
    h += 120
    h = h % 360
    g = 255*abs(h-180)/180
    # Apply s
    mean = (r + g + b) / 3
    r = min(max(r*s + mean*(1-s), 0), 255)
    g = min(max(g*s + mean*(1-s), 0), 255)
    b = min(max(b*s + mean*(1-s), 0), 255)
    # Apply v
    if l > 0.5:
        l -= 0.5
        l *= 2
        r = r*(1 - l) + 255*l
        g = g*(1 - l) + 255*l
        b = b*(1 - l) + 255*l
    elif l < 0.5:
        l *= 2
        r = r*(l) + 0*(1 - l)
        g = g*(l) + 0*(1 - l)
        b = b*(l) + 0*(1 - l)
    #print(r,g,b)
    try:
        int(g)
    except:
        print(h,s,l)
        print(r,g,b)
    return '#' + \
        '{0:0{1}x}'.format(int(r), 2) + \
        '{0:0{1}x}'.format(int(g), 2) + \
        '{0:0{1}x}'.format(int(b), 2)
def zScoreToRGB(z):
    # Center hue at blue (120), and constrain it to within 120 (not 180) of that
    # so as to avoid wrapping around (so that very high z score does not
    # look like very low z score)
    # 1.96 is p = 0.05 if this is actually z, or for t with infinite degrees of
    # freedom
    if z is None:
        return '#FFFFFF'
    hue = 240 + max(min((z / 1.96)**3 * 120, 120), -120)
    saturation = 1
    # Zero z score is white, p < 0.05 is 0.5 (that is, 1 - 0.5) lightness.
    # lightness ranges from 0 (black) to 0.5 (no effect) to 1 (white)
    lightness = 1 - min(abs(z) / 1.96 * 0.5, 0.5)
    return hslToRgb(hue, saturation, lightness)
    