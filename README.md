# Mac Miller Markov Mosaic
The Mac Miller Markov Mosaic uses a Markov model to analyze the transition
probabilities between sequences of pixels in a target image, and uses these
probabilities, in combination with pictures of Mac Miller on Instagram,
to create a mosaic.

## Credits
- The decision to represent states as unique sequences of pixels was
inspired by William Anderson's article "Using Machine Learning to Make
Art."
- The gen_mosaic(), get_average_rbg(), and get_best_match_index() functions
were heavily inspired by the "Implementing Photomosaics" tutorial on
GeeksforGeeks.
- All of the images used to create the mosaic were
downloaded from https://www.instagram.com/macmillerdivine/.

## License
This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.
