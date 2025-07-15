"""
U-Net architecture components for image colorization.
"""

import tensorflow as tf
from typing import Tuple

class UNetBlocks:
    """
    Building blocks for U-Net architecture.
    """
    
    @staticmethod
    def down(filters: int, k: Tuple[int, int], bn: bool = True):
        """
        Create a downsampling block for the U-Net encoder.
        
        This block performs convolution with stride 2 to reduce spatial dimensions
        while increasing the number of feature channels.
        
        Args:
            filters (int): Number of output feature channels
            k (Tuple[int, int]): Kernel size for convolution
            bn (bool): Whether to apply batch normalization
            
        Returns:
            tf.keras.Sequential: Downsampling block
        """
        layer = tf.keras.Sequential([
            tf.keras.layers.Conv2D(filters, k, strides=2, padding="same"),
            tf.keras.layers.BatchNormalization() if bn else tf.keras.layers.Layer(),
            tf.keras.layers.LeakyReLU(),
        ])
        return layer

    @staticmethod
    def up(filters: int, k: Tuple[int, int], dropout: bool = False):
        """
        Create an upsampling block for the U-Net decoder.
        
        This block performs transposed convolution to increase spatial dimensions
        while reducing the number of feature channels.
        
        Args:
            filters (int): Number of output feature channels
            k (Tuple[int, int]): Kernel size for transposed convolution
            dropout (bool): Whether to apply dropout regularization
            
        Returns:
            tf.keras.Sequential: Upsampling block
        """
        seq = tf.keras.Sequential([
            tf.keras.layers.Conv2DTranspose(filters, k, strides=2, padding="same"),
            tf.keras.layers.Dropout(0.2) if dropout else tf.keras.layers.Layer(),
            tf.keras.layers.LeakyReLU(),
        ])
        return seq

class UNetModel:
    """
    U-Net model builder for image colorization.
    """
    
    def __init__(self, img_size: int = 256):
        """
        Initialize the U-Net model builder.
        
        Args:
            img_size (int): Size of input images
        """
        self.img_size = img_size
        self.input_shape = (img_size, img_size, 3)
        self.blocks = UNetBlocks()
    
    def build_model(self) -> tf.keras.Model:
        """
        Build and compile the U-Net model for image colorization.
        
        The U-Net architecture consists of:
        - Encoder: Downsampling path that captures context
        - Decoder: Upsampling path that enables precise localization
        - Skip connections: Direct connections between encoder and decoder layers
        
        Returns:
            tf.keras.Model: Compiled U-Net model ready for training
        """
        # Input layer: expects RGB images (grayscale will be fed as 3-channel)
        inputs = tf.keras.layers.Input(shape=self.input_shape)

        # Encoder (Downsampling path)
        # Each downsampling block reduces spatial dimensions by 2x
        d1 = self.blocks.down(128, (3, 3), bn=False)(inputs)      # 256x256 -> 128x128
        d2 = self.blocks.down(128, (3, 3), bn=False)(d1)          # 128x128 -> 64x64
        d3 = self.blocks.down(256, (3, 3), bn=True)(d2)           # 64x64 -> 32x32
        d4 = self.blocks.down(512, (3, 3), bn=True)(d3)           # 32x32 -> 16x16
        d5 = self.blocks.down(512, (3, 3), bn=True)(d4)           # 16x16 -> 8x8

        # Decoder (Upsampling path) with skip connections
        # Skip connections help preserve fine-grained details
        u1 = self.blocks.up(512, (3, 3), dropout=False)(d5)       # 8x8 -> 16x16
        u1 = tf.keras.layers.concatenate([u1, d4])                # Concatenate with d4
        
        u2 = self.blocks.up(256, (3, 3), dropout=False)(u1)       # 16x16 -> 32x32
        u2 = tf.keras.layers.concatenate([u2, d3])                # Concatenate with d3
        
        u3 = self.blocks.up(128, (3, 3), dropout=False)(u2)       # 32x32 -> 64x64
        u3 = tf.keras.layers.concatenate([u3, d2])                # Concatenate with d2
        
        u4 = self.blocks.up(128, (3, 3), dropout=False)(u3)       # 64x64 -> 128x128
        u4 = tf.keras.layers.concatenate([u4, d1])                # Concatenate with d1
        
        u5 = self.blocks.up(3, (3, 3), dropout=False)(u4)         # 128x128 -> 256x256
        u5 = tf.keras.layers.concatenate([u5, inputs])            # Concatenate with input

        # Final output layer: produces RGB color image
        outputs = tf.keras.layers.Conv2D(3, (2, 2), strides=1, padding="same")(u5)
        
        # Create the model
        model = tf.keras.Model(inputs, outputs, name="u-net_colorizer")

        # Compile with appropriate loss function and optimizer
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="mean_absolute_error",  # L1 loss works well for image colorization
            metrics=["acc"],
        )
        return model 