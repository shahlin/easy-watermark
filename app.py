from PIL import Image
import sys, math, argparse, os


IMAGE_IS_FILE = 1
IMAGE_IS_DIR = 2

def setup_parser():
    """
    Creates ArgumentParser and adds necessary arguments
    """
    parser = argparse.ArgumentParser(description='Add watermark to your images')
    parser.add_argument('images_path',
                        type=str,
                        help='Path to the image (or images folder) to add watermark to.')
    
    parser.add_argument('-w', '--watermark',
                        metavar='watermark',
                        type=str,
                        nargs='?',
                        help='Watermark image path. Only .png images are allowed.')

    parser.add_argument('-p', '--position',
                        metavar='position',
                        type=str.lower,
                        nargs='?',
                        help='Position of the watermark to be placed. Can be "topleft", "topright", "bottomleft" or "bottomright".')

    parser.add_argument('-s', '--size',
                        metavar='size',
                        type=int,
                        nargs='*',
                        help='Size of the watermark. Width x Height. Example: 128 128')
    
    parser.add_argument('-o', '--output',
                        metavar='output',
                        type=str,
                        nargs='?',
                        help='Folder to save the images to')
    
    return parser

def get_position_offset(main_img, watermark_img, position):
    """
    Gets the offset (x, y) where the watermark is to be placed
    """
    main_img_w, main_img_h = main_img.size
    watermark_img_w, watermark_img_h = watermark_img.size

    if position == 'topleft':
        offset_x = 20
        offset_y = 0
    elif position == 'topright':
        offset_x = main_img_w - watermark_img_w
        offset_y = 0
    elif position == 'bottomleft':
        offset_x = 20
        offset_y = main_img_h - watermark_img_h
    else:
        # Take the width of the main image and remove
        # the width of the watermark along with the main image's width divided by 20
        # 20 just seemed to work
        # offset_x = main_img_w - (watermark_img_w + (main_img_w // 20))
        offset_x = main_img_w - watermark_img_w
        offset_y = main_img_h - watermark_img_h
    
    return offset_x, offset_y

def get_scale_size(main_img, size):
    """
    Gets the size of the watermark (width, height)
    Either calculate automatically or use the one provided by user
    """
    # Scale the watermark into given size by default
    # 15% of the width of the image
    scale_size = (main_img.size[0] * 0.15,) * 2

    if size is None:
        return scale_size

    if size[0] < 0 or size[1] < 0:
        print('Negative number given for size. Defaulting to fallback...')
        return scale_size

    if len(size_arg) == 1:
        scale_size = (size_arg[0],) * 2
    elif len(size_arg) >= 2:
        scale_size = (size_arg[0], size_arg[1])

    return scale_size

def image_file_or_dir(image_path):
    """
    Checks if the image is a file or a directory
    """
    if os.path.isfile(image_path):
        return IMAGE_IS_FILE

    if os.path.isdir(image_path):
        return IMAGE_IS_DIR

    exit(image_path + " is invalid or doesn't exist. Quitting now...")

def get_images_list(image_path):
    """
    If image_path is a single image, it returns a list with one image
    If it is a folder, adds all the images in the folder to a list
    """
    image_type = image_file_or_dir(image_path)
    supported_formats = ('png', 'jpg', 'jpeg')

    if image_type == IMAGE_IS_FILE:
        if image_path.endswith(supported_formats):
            return [image_path]
    elif image_type == IMAGE_IS_DIR:
        images_in_dir = os.listdir(image_path)
        images = []

        for image in images_in_dir:
            if image.endswith(supported_formats):
                images.append(image)
        
        return images

def validate_watermark(image_path):
    """
    Check if the specified watermark is a valid file and a .png image
    """
    exit_msg = image_path + " is invalid or doesn't exist. Quitting now..."

    if not os.path.isfile(image_path):
        exit(exit_msg)

    if not image_path.endswith('.png'):
        exit(exit_msg)

def place_watermark(image_path, watermark_path, watermark_pos, watermark_size):
    """
    Place the watermark onto the image
    """
    # Open the image specified
    main_img = Image.open(image_path, 'r')

    # Open the watermark photo
    watermark_img = Image.open(watermark_path, 'r')

    scale_size = get_scale_size(main_img, watermark_size)
        
    watermark_img.thumbnail(scale_size)

    # Get their sizes
    main_img_w, main_img_h = main_img.size
    watermark_img_w, watermark_img_h = watermark_img.size

    offset = get_position_offset(main_img, watermark_img, watermark_pos)

    # Put watermark into the main image at the location specified by the offset
    main_img.paste(watermark_img, offset, watermark_img)

    # Split by slashes in case its a long path
    # Take the last one (supposedly the image name)
    image_name = image_path.split("/")[-1]
    save_img_to_disk(main_img, image_name)

def save_img_to_disk(img, name):
    """
    Save image to an output folder
    """
    # Create new output folder if not exists
    try:
        os.makedirs('output')
    except FileExistsError:
        pass

    # Save image
    if output_arg is None:
        img.save('output/' + name)
    else:
        img.save(output_arg + "/" + name)

parser = setup_parser()
args = vars(parser.parse_args())

# Get command line arguments
image_arg = args['images_path']  # Required
watermark_arg = args['watermark'] if args['watermark'] else 'watermark.png'
position_arg = args['position'] if args['position'] else 'bottomright'
size_arg = args['size']
output_arg = args['output']

# Make sure the watermark specified is valid, else quit program
validate_watermark(watermark_arg)

# Get the list of images from the given path (Can also be just one image)
image_list = get_images_list(image_arg)

# Get the type of image - File or Dir
image_type = image_file_or_dir(image_arg)

# Loop through each image and place watermark on it
for image in image_list:
    if image_type == IMAGE_IS_FILE:
        image_path = image_arg
    elif image_type == IMAGE_IS_DIR:
        image_path = image_arg + "/" + image

    place_watermark(image_path, watermark_arg, position_arg, size_arg)

print("Done! Check the output folder!")