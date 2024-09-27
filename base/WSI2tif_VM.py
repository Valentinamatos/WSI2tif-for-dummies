"""

Author: Valentina Matos (Johns Hopkins - Kiemen/Wirtz Lab)
Date: September 11, 2024
"""

from PIL import Image
import numpy as np
import os
import glob
import time

# Add the OpenSlide DLL directory
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()  # Fallback to the current working directory
openslide_path = os.path.join(script_dir, 'OpenSlide bin')

if hasattr(os, 'add_dll_directory'):
    # Python 3.8+
    with os.add_dll_directory(openslide_path):
        from openslide import OpenSlide
else:
    # Earlier Python versions
    if openslide_path not in os.environ['PATH']:
        os.environ['PATH'] = openslide_path + os.pathsep + os.environ['PATH']
    from openslide import OpenSlide


def process_missing_images(pth, resolutions, umpix_list, missing_images):
    """Process missing images by converting .ndpi or .svs files to .tif."""
    for idx, missing_image in enumerate(sorted(missing_images)):
        start_time = time.time()
        print(f"{idx + 1} / {len(missing_images)} processing: {missing_image}")
        try:
            # Open the slide
            slide_path = os.path.join(pth, missing_image + '.ndpi')
            wsi = OpenSlide(slide_path)

            # Read the slide region once
            svs_img = wsi.read_region(location=(0, 0), level=0, size=wsi.level_dimensions[0]).convert('RGB')

            for resolution, umpix in zip(resolutions, umpix_list):
                # Calculate resize factors
                resize_factor_x = umpix / float(wsi.properties['openslide.mpp-x'])
                resize_factor_y = umpix / float(wsi.properties['openslide.mpp-y'])
                resize_dimension = (
                    int(np.ceil(wsi.dimensions[0] / resize_factor_x)),
                    int(np.ceil(wsi.dimensions[1] / resize_factor_y))
                )

                # Resize and save the image
                resized_img = svs_img.resize(resize_dimension, resample=Image.NEAREST)
                pthim = os.path.join(pth, f'{resolution}')
                if not os.path.isdir(pthim):
                    os.makedirs(pthim)
                output_path = os.path.join(pthim, missing_image + '.tif')
                resized_img.save(output_path, resolution=1, resolution_unit=1, quality=100, compression=None)
        except Exception as e:
            print(f"Error processing {missing_image}: {e}")
        image_time = time.time() - start_time
        print(f"   Processing time: {image_time:.2f} seconds")

def WSI2tif(pth, resolutions, umpix_list):
    if len(resolutions) != len(umpix_list):
        raise ValueError("The length of resolutions and umpix_list must match.")

    for resolution, umpix in zip(resolutions, umpix_list):
        pthim = os.path.join(pth, f'{resolution}')

        # Ensure the image directory exists
        if not os.path.isdir(pthim):
            os.makedirs(pthim)

        # Get the .tif image names
        image_files_tif = glob.glob(os.path.join(pthim, '*.tif'))
        images_names_tif = {os.path.splitext(os.path.basename(image))[0] for image in image_files_tif}

        # Get the .ndpi and .svs image names
        image_files_wsi = glob.glob(os.path.join(pth, '*.ndpi')) + glob.glob(os.path.join(pth, '*.svs'))
        if not image_files_wsi:
            print("No .ndpi or .svs files found in the directory.")
            continue
        images_names_wsi = {os.path.splitext(os.path.basename(image))[0] for image in image_files_wsi}

        # Compare image names and process missing images
        if images_names_tif != images_names_wsi:
            missing_images = images_names_wsi - images_names_tif
            process_missing_images(pth, resolutions, umpix_list, missing_images)


if __name__ == '__main__':
    path = r'\\10.99.68.52\Kiemendata\Valentina Matos\tissues for methods paper\slides scanned from bispecific study'
    # 8um = 1.25x #4um = 2.5x, #2um=5x, 1um=10x, 0.5um=20x, 0.25um=40x
    resolutions = ['10x', '5x', '1x']
    umpix_list = [1, 2, 4]
    WSI2tif(path, resolutions, umpix_list)







