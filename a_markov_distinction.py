"""
# Name(s): Shahir Taj
# Course: CSCI 3725
# Assignment: M2
# Date: 09/30/2019

The Mac Miller Markov Mosaic uses a Markov model to analyze the
transition probabilities between sequences of pixels in a target
image, and uses these probabilities, in combination with pictures
of Mac Miller on Instagram, to create a mosaic.

The decision to represent states as unique sequences of pixels was
inspired by William Anderson's article "Using Machine Learning to Make
Art." The gen_mosaic(), getAverageRBG(), and getBestMatchIndex() methods
were heavily inspired by the "Implementing Photomosaics" tutorial on
GeeksforGeeks. All of the images used to create the mosaic were
downloaded from https://www.instagram.com/macmillerdivine/.
"""

import glob, random, numpy
from PIL import Image

INPUT_IMAGE_WIDTH = 10
INPUT_IMAGE_HEIGHT = 10


class MarkovModel:
    """ MarkovModel class.
    Instance Variables: num_states of type int, input_data of type list,
                        order of type int, transition_probabilities of type
                        dict, output_data of type list
    Methods: gen_transition_probabilities(), gen_output_data() __str__(),
             __repr__()
    """
    
    def __init__(self, num_states, input_data, order):
        self.num_states = num_states
        self.input_data = input_data
        self.order = order
        self.transition_probabilities = {}
        self.output_data = []
    
    def gen_transition_probabilities(self):
        """ (markovmodel) -> dict
        
        Return the transition probabilities between states in the state space.
        """
        
        for i in range(self.num_states - self.order):
            # in an n-order model, a state is a unique sequence of n states
            cur_state = tuple(self.input_data[i:i + self.order])
            # the last state can transition to any state in the state space
            if i == (self.num_states - self.order - 1):
                next_state = random.choice(list(self.transition_probabilities))
            else:
                # states can only transition to states that succeed them
                next_state = self.input_data[i + 1:i + self.order + 1]
            
            # if a state has not been seen, add it to the state space
            if cur_state not in self.transition_probabilities:
                self.transition_probabilities[cur_state] = []
            # add the next state as a transition from the current state
            self.transition_probabilities[cur_state].append(next_state)
        
        return self.transition_probabilities
    
    def gen_output_data(self):
        """ (markovmodel) -> list
        
        Return a list of new state transitions, using transition probabilities.
        """
        
        # start with a random state in the state space
        start_state = random.choice(list(self.transition_probabilities))
        self.output_data = list(start_state)
        
        cur_state = tuple(start_state)
        # while size of the ouput data is less than size of the input data
        while (len(self.output_data) < self.num_states):
            # transition to a possible state
            next_state = random.choice(self.transition_probabilities[cur_state])
            # add the last item of the next state to the output data
            self.output_data.append(next_state[-1])
            cur_state = tuple(next_state)
        
        return self.output_data
    
    def __str__(self):
        """ (markovmodel) -> string
        
        Return a formatted string representation of this Markov Model.
        """
        
        return ("A Markov Model of order " + order + " with " + num_states +
                " states in its state space.")
    
    def __repr__(self):
        """ (markovmodel) -> markovmodel
        
        Return a Markov Model of the same value.
        """
        
        return "MarkovModel({0}, {1}, {2})".format(self.num_states,
                                                   self.input_data, self.order)


def gen_mosaic(input_images, output_data, target_size):
    """ (list, list, tuple) -> image
        
    Return a photomosaic of the target image using the input images.
    
    This function was heavily inspired by the "Implementing Photomosaics"
    tutorial on GeeksforGeeks.
    """
    
    image_colors = []
    # resize and get the average rgb value of each input image
    for image in input_images:
        image.thumbnail((INPUT_IMAGE_WIDTH, INPUT_IMAGE_HEIGHT))
        image_colors.append(getAverageRGB(image))
    
    image_matches = []
    # find the best input image for each pixel in the target image
    for pixel_color in output_data:
        match_index = getBestMatchIndex(pixel_color, image_colors) 
        image_matches.append(input_images[match_index])
    
    # initialize the mosaic
    max_width = max([img.size[0] for img in image_matches]) 
    max_height = max([img.size[1] for img in image_matches])     
    mosaic = Image.new('RGB', (target_size[0] * max_width, target_size[1] *
                               max_height))
    
    # paste the input images onto the mosaic
    for i in range(len(image_matches)): 
        cur_row = int(i / target_size[0])
        cur_col = i - target_size[0] * cur_row 
        mosaic.paste(image_matches[i], (cur_col * max_width, cur_row *
                                        max_height))
    
    return mosaic
    

def getAverageRGB(image): 
    """ (image) -> tuple
        
    Return the average RGB value of all of the colors in an image.
    
    This function was copied from the "Implementing Photomosaics"
    tutorial on GeeksforGeeks.
    """
    
    image_array = numpy.array(image) 
    w,h,d = image_array.shape
    
    return tuple(numpy.average(image_array.reshape(w*h, d), axis=0))


def getBestMatchIndex(pixel_color, image_colors): 
    """ (tuple, list) -> int
        
    Return the index of the image that is the best color match with
    the given pixel.
    
    This function was copied from the "Implementing Photomosaics"
    tutorial on GeeksforGeeks.
    """
    
    cur_index = 0
    min_index = 0
    min_dist = float("inf")
    # compare the r, g, and b values of each input image with the given pixel
    for color in image_colors:
        dist = ((color[0] - pixel_color[0])*(color[0] - pixel_color[0]) +
                (color[1] - pixel_color[1])*(color[1] - pixel_color[1]) +
                (color[2] - pixel_color[2])*(color[2] - pixel_color[2])) 
        if dist < min_dist: 
            min_dist = dist 
            min_index = cur_index 
        cur_index += 1
    
    return min_index


def main():
    # open target image
    target_filepath = input("Enter the filepath of the target image: ")
    # input/target_images/mac_miller.jpg
    target_file = target_filepath[20:].split(".")[0]
    try:
        target_image = Image.open(target_filepath)
    except FileNotFoundError:
        print("The file " + target_filepath + " was not found.")
    
    # read input images
    input_images = []
    input_filepath = input("Enter the filepath of the input images: ")
    # input/input_images/*.jpg
    for infile in glob.glob(input_filepath):
        try:
            image = Image.open(infile)
        except FileNotFoundError:
            print("The file " + infile + " was not found.")
        else:
            input_images.append(image)
    
    if input_images == []: 
        print("No input images found in " + input_filepath + ". Exiting.") 
        exit() 
 
    target_image.show()
    target_size = target_image.size
    target_num_pixels = target_size[0] * target_size[1]
    target_data = list(target_image.getdata())
    n = int(input("Enter the order of the Markov chain (must be less than " +
                  str(target_num_pixels) + "): "))
    if n >= target_num_pixels: # order must be less than total number of pixels
        print("Order is too large. Exiting.") 
        exit()
    
    print("building markov model...")
    markov_model = MarkovModel(target_num_pixels, target_data, n)
    markov_model.gen_transition_probabilities()
    
    print("generating output data...")
    output_data = markov_model.gen_output_data()
    
    print('creating mosaic...')
    output_image = gen_mosaic(input_images, output_data, target_size)
    
    # show and save generated mosaic image
    output_image.show()
    output_filepath = "output/" + target_file + "_mosaic" + ".jpeg"
    output_image.save(output_filepath)
    print("saved output to " + output_filepath) 
    print("done.")


if __name__ == "__main__":
    main()
