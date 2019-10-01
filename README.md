# Name(s): Shahir Taj
# Course: CSCI 3725
# Assignment: M2
# Date: 09/30/2019

This program uses a Markov model to analyze the transition probabilities
between sequences of pixels in a target image, and uses these
probabilities, in combination with pictures of Mac Miller on Instagram,
to create a mosaic.

The decision to use represent states as unique sequences of pixels was
inspired by William Anderson's article "Using Machine Learning to Make
Art." The gen_mosaic(), getAverageRBG(), and getBestMatchIndex() methods
were heavily inspired by the "Implementing Photomosaics" tutorial on
GeeksforGeeks. All of the images used to create the mosaic were
downloaded from https://www.instagram.com/macmillerdivine/.
