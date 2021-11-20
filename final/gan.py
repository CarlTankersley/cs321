import numpy as np
import matplotlib as mp
import tensorflow.keras as ks
import matplotlib.pyplot as plt
import argparse


(trainX, trainy), (testX, testy) = ks.datasets.mnist.load_data()


def define_discriminator(in_shape=(28, 28, 1)):
    model = ks.models.Sequential()
    model.add(ks.layers.Conv2D(64, (3, 3), strides=(
        2, 2), padding='same', input_shape=in_shape))
    model.add(ks.layers.LeakyReLU(alpha=0.2))
    model.add(ks.layers.Dropout(0.4))
    model.add(ks.layers.Conv2D(64, (3, 3), strides=(2, 2), padding='same'))
    model.add(ks.layers.LeakyReLU(alpha=0.2))
    model.add(ks.layers.Dropout(0.4))
    model.add(ks.layers.Flatten())
    model.add(ks.layers.Dense(1, activation='sigmoid'))
    opt = ks.optimizers.Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy',
                  optimizer=opt, metrics=['accuracy'])
    return model


# load and prepare mnist training images
def load_real_samples():
    # expand to 3d, e.g. add channels dimension
    gray_scale = np.expand_dims(trainX, axis=-1)
    # convert from unsigned ints to floats
    gray_scale = gray_scale.astype('float32')
    # scale from [0,255] to [0,1]
    gray_scale = gray_scale / 255.0
    return gray_scale


def generate_real_samples(dataset, n_samples):
    # choose random instances
    random_ints = np.random.randint(0, dataset.shape[0], n_samples)
    # retrieve selected images
    selected_images = dataset[random_ints]
    # generate 'real' class labels (1)
    class_labels = np.ones((n_samples, 1))
    return selected_images, class_labels


# generate n fake samples with class labels
def generate_fake_samples(generator_model, latent_dim, n_samples):
    # generate uniform random numbers in [0,1]
    list_of_random = generate_latent_points(latent_dim, n_samples)
    # list_of_random = np.random.rand(28 * 28 * n_samples)
    # reshape into a batch of grayscale images
    list_of_random = generator_model.predict(list_of_random)
    # list_of_random = list_of_random.reshape((n_samples, 28, 28, 1))
    # generate 'fake' class labels (0)
    class_labels = np.zeros((n_samples, 1))
    return list_of_random, class_labels


def define_generator(latent_dim):
    model = ks.models.Sequential()
    # foundation for 7x7 image
    n_nodes = 128 * 7 * 7
    model.add(ks.layers.Dense(n_nodes, input_dim=latent_dim))
    model.add(ks.layers.LeakyReLU(alpha=0.2))
    model.add(ks.layers.Reshape((7, 7, 128)))
    # upsample to 14x14
    model.add(ks.layers.Conv2DTranspose(
        128, (4, 4), strides=(2, 2), padding='same'))
    model.add(ks.layers.LeakyReLU(alpha=0.2))
    # upsample to 28x28
    model.add(ks.layers.Conv2DTranspose(
        128, (4, 4), strides=(2, 2), padding='same'))
    model.add(ks.layers.LeakyReLU(alpha=0.2))
    model.add(ks.layers.Conv2D(1, (7, 7), activation='sigmoid', padding='same'))
    return model


def generate_latent_points(latent_dim, n_samples):
    # generate points in the latent space
    random_points = np.random.randn(latent_dim * n_samples)
    # reshape into a batch of inputs for the network
    random_points = random_points.reshape(n_samples, latent_dim)
    return random_points


# define the combined generator and discriminator model, for updating the generator
def define_gan(generator, discriminator):
    # make weights in the discriminator not trainable
    discriminator.trainable = False
    # connect them
    model = ks.models.Sequential()
    # add generator
    model.add(generator)
    # add the discriminator
    model.add(discriminator)
    # compile model
    opt = ks.optimizers.Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer=opt)
    return model


# train the generator and discriminator
def train(generator, discriminator, gan_model, dataset, latent_dim, n_epochs=100, batch_size=256):
    batches_per_epoch = int(dataset.shape[0] / batch_size)
    half_batch = int(batch_size / 2)
    # manually enumerate epochs
    for i in range(n_epochs):
        # enumerate batches over the training set
        for j in range(batches_per_epoch):
            # get randomly selected 'real' samples
            images_real, class_labels_real = generate_real_samples(
                dataset, half_batch)
            # generate 'fake' examples
            images_fake, class_labels_fake = generate_fake_samples(
                generator, latent_dim, half_batch)
            # create training set for the discriminator via vertical stacking
            all_images, all_class_labels = np.vstack((images_real, images_fake)), np.vstack(
                (class_labels_real, class_labels_fake))
            # update discriminator model weights
            discriminator_loss, _ = discriminator.train_on_batch(
                all_images, all_class_labels)
            # prepare points in latent space as input for the generator
            random_points = generate_latent_points(latent_dim, batch_size)
            # create inverted labels for the fake samples
            class_labels_random = np.ones((batch_size, 1))
            # update the generator via the discriminator's error
            generator_loss = gan_model.train_on_batch(
                random_points, class_labels_random)
            # summarize loss on this batch
            print('>%d, %d/%d, d=%.3f, g=%.3f' % (i+1, j+1,
                  batches_per_epoch, discriminator_loss, generator_loss))
        # evaluate the model performance, sometimes
        if (i+1) % 10 == 0:
            summarize_performance(
                i, generator, discriminator, dataset, latent_dim)


# create and save a plot of generated images (reversed grayscale)
def save_plot(examples, epoch='Testing', n=10):
    # plot images
    for i in range(n * n):
        # define subplot
        plt.subplot(n, n, 1 + i)
        # turn off axis
        plt.axis('off')
        # plot raw pixel data
        plt.imshow(examples[i, :, :, 0], cmap='gray_r')
    # save plot to file
    filename = 'generated_plot_e{}.png'.format(epoch+1 if isinstance(epoch, int) else epoch)
    print(filename)
    plt.savefig(filename)
    plt.close()


# evaluate the discriminator, plot generated images, save generator model
def summarize_performance(epoch, generator, discriminator, dataset, latent_dim, n_samples=100):
    # prepare real samples
    images_real, class_labels_real = generate_real_samples(dataset, n_samples)
    # evaluate discriminator on real examples
    _, accuracy_real = discriminator.evaluate(
        images_real, class_labels_real, verbose=0)
    # prepare fake examples
    images_fake, class_labels_fake = generate_fake_samples(
        generator, latent_dim, n_samples)
    # evaluate discriminator on fake examples
    _, accuracy_fake = discriminator.evaluate(
        images_fake, class_labels_fake, verbose=0)
    # summarize discriminator performance
    print('>Accuracy real: %.0f%%, fake: %.0f%%' %
          (accuracy_real*100, accuracy_fake*100))
    # save plot
    save_plot(images_fake, epoch)
    # save the generator model tile file
    filename = 'generator_model_%03d.h5' % (epoch + 1)
    generator.save(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('-m', '--model', type=str, help='Pretrained model save to load')
    args = parser.parse_args()

    if args.model is not None: 
        saved_model = ks.models.load_model(args.model)
        images_fake, _ = generate_fake_samples(saved_model, 50, 100)
        save_plot(images_fake, )
    else:
        # define the size of the latent space
        latent_dim = 50
        # define discriminator
        discriminator = define_discriminator()
        # define generator
        generator = define_generator(latent_dim)
        # create the gan
        gan_model = define_gan(generator, discriminator)
        # load samples
        dataset = load_real_samples()

        train(generator, discriminator, gan_model, dataset, latent_dim, args.epochs)


if __name__ == '__main__':
    main()
