
def handle_time(ttime):
    """
        Converts seconds to appropriate unit
    """
    if ttime >= 60: # Minutes
        return (ttime / 60, "min")
    elif (ttime / 60) >= 60: # Hours
        return (ttime / 3600, "hrs")
    elif (ttime / 3600) >= 24: # days
        return (ttime / 86400, "d")
    elif (ttime / 86400) >= 7: # Weeks
        return (ttime / 604800, "w")
    else: # No sane person will run this bokk for a week
        return (ttime, "s")

class Utils:
    def __init__(self, width, height):
        self.reso_16 = [
            { "width": 1280, "height": 720 },
            { "width": 1920, "height": 1080 },
            { "width": 2560, "height": 1440 },
            { "width": 3840, "height": 2160 }
        ]
        self.width, self.height = width, height


    def padding(self):
        """
            Get's width and height of current resolution
            we iterate through reso_16 for heights, if current resolution height matches one of the entires 
            then it will calulate the difference of the width's between current resolution and 16:9 (reso_16) resolution
            divides by 2 for each side of padding

            Variables Used
            width -- used to referance current resolution width
            height -- used to referance current resolution height
            pad -- used to output how much padding we expect in different resolutions
            reso_16 -- list that  
        """
        pad = 0
        for resolution in self.reso_16: 
            if self.height == resolution['height']:
                pad = (self.width - resolution['width']) / 2

        return pad

    def scaling(self, pos_list):
        """
            This function will dynamically calculate the differance between the current resolution
            and the one that the application is designed for (2560x1440) 

            It will also add any padding needed to positions to account for 21:9

            do_padding -- this is used during start 
        """

        reso_21 = False
        for resolution in self.reso_16: 
            if self.height == resolution['height']:
                if self.width != resolution['width']:
                    reso_21 = True
                    resolution = pos_list[0]
                    break

        if reso_21 != True:
            x = pos_list[0] / 2560 
            x = x * self.width

        y = pos_list[1] / 1440

        y *= self.height
        x += self.padding() # Add padding to x

        return (x, y)
    
    def template_matching(self):
        pass