Soren DeHaan and Carl Tankersley

MNIST GAN 

dependecies: TensorFlow (install on Mirage with command 'pip3 install tensorflow')

The file gan.py contains our model of a Generative Adversarial Network (GAN) to generate MNIST handwritten digits.
While we wouldn't recommend training it yourself, since it took us about five hours to do so, you can verify that 
it will train by running 'python3 gan.py', optionally adding the flag '-e <number_of_epochs>' to specify the 
number of training epochs. If you want to see results from the included saved model without training, run the 
command 'python3 gan.py -m generator_model_250.h5'. This should create a png file with 100 "handwritten" digits
generated by the network.