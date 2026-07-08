"""
Author: Valentina Matos (Johns Hopkins - Kiemen/Wirtz Lab)
Date: May , 2025

Modified: checks missing images per iteration (per resolution) and verifies existence
just before saving each image (so it doesn't rely on a single initial missing set).
"""

from PIL import Image
import numpy as np
import glob
import os
import platform
import ctypes
import time

Image.MAX_IMAGE_PIXELS = None

# Try importing OpenSlide, handle platform-specific behavior
try:
    from openslide import OpenSlide
except ImportError:
    system_platform = platform.system()

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()  # Fallback to the current working directory
    openslide_dll_path = os.path.join(script_dir, 'OpenSlide bin')

    if system_platform == "Windows":
        # Add the OpenSlide DLL manually for Windows
        dll_file = os.path.join(openslide_dll_path, 'libopenslide-1.dll')
        if hasattr(os, 'add_dll_directory'):
            # Python 3.8+
            with os.add_dll_directory(openslide_dll_path):
                ctypes.cdll.LoadLibrary(dll_file)
                from openslide import OpenSlide
        else:
            # Earlier Python versions
            if openslide_dll_path not in os.environ['PATH']:
                os.environ['PATH'] = openslide_dll_path + os.pathsep + os.environ['PATH']
            ctypes.cdll.LoadLibrary(dll_file)
            from openslide import OpenSlide

    elif system_platform == "Darwin":  # macOS
        # Load libopenslide.1.dylib for macOS
        dylib_file = os.path.join(openslide_dll_path, 'libopenslide.1.dylib')
        try:
            ctypes.cdll.LoadLibrary(dylib_file)
            from openslide import OpenSlide
        except OSError as e:
            raise ImportError(f"Failed to load {dylib_file} on macOS. Ensure it is installed.") from e
    else:
        raise ImportError(f"Unsupported platform: {system_platform}")


def process_missing_images_for_resolution(pth, resolution, umpix, missing_images):
    """
    Process the list of missing image basenames for a single resolution/umpix.
    This function checks the output file existence just before creating it, so that
    it avoids re-creating files that may have been created since the initial check.
    """
    for idx, missing_image in enumerate(sorted(missing_images)):
        start_time = time.time()
        print(f"{idx + 1} / {len(missing_images)} processing: {missing_image} (resolution: {resolution})")
        try:
            # Prepare output path for this resolution and image
            pthim = os.path.join(pth, f'{resolution}')
            if not os.path.isdir(pthim):
                os.makedirs(pthim)

            output_path = os.path.join(pthim, missing_image + '.tif')
            # Check right before doing any heavy work if the file already exists
            if os.path.exists(output_path):
                print(f"   Skipping {missing_image} for {resolution}: output already exists.")
                continue

            # Try to find either .ndpi or .svs file for the missing image
            ndpi_path = os.path.join(pth, missing_image + '.ndpi')
            svs_path = os.path.join(pth, missing_image + '.svs')
            if os.path.exists(ndpi_path):
                slide_path = ndpi_path
            elif os.path.exists(svs_path):
                slide_path = svs_path
            else:
                print(f"   Neither .ndpi nor .svs file found for {missing_image}")
                continue

            # Open the slide and read once
            wsi = OpenSlide(slide_path)
            svs_img = wsi.read_region(location=(0, 0), level=0, size=wsi.level_dimensions[0]).convert('RGB')

            # Calculate resize factors
            resize_factor_x = umpix / float(wsi.properties['openslide.mpp-x'])
            resize_factor_y = umpix / float(wsi.properties['openslide.mpp-y'])
            resize_dimension = (
                int(np.ceil(wsi.dimensions[0] / resize_factor_x)),
                int(np.ceil(wsi.dimensions[1] / resize_factor_y))
            )

            # Resize and save the image (we already ensured directory exists)
            resized_img = svs_img.resize(resize_dimension, resample=Image.NEAREST)
            # Double-check again (race conditions are rare but possible)
            if os.path.exists(output_path):
                print(f"   Skipping save for {missing_image}: output created by another process.")
            else:
                resized_img.save(output_path, resolution=1, resolution_unit=1, quality=100, compression=None)

        except Exception as e:
            print(f"Error processing {missing_image} (resolution {resolution}): {e}")
        image_time = time.time() - start_time
        print(f"   Processing time: {image_time:.2f} seconds")


def WSI2tif(pth, resolutions, umpix_list):
    if len(resolutions) != len(umpix_list):
        raise ValueError("The length of resolutions and umpix_list must match.")

    # For each resolution, compute which .tif files are missing for that resolution
    # and process only those. This re-checks the missing set per-resolution/iteration.
    for resolution, umpix in zip(resolutions, umpix_list):
        pthim = os.path.join(pth, f'{resolution}')

        # Ensure the image directory exists
        if not os.path.isdir(pthim):
            os.makedirs(pthim)

        # Get the .tif image names for this resolution
        image_files_tif = glob.glob(os.path.join(pthim, '*.tif'))
        images_names_tif = {os.path.splitext(os.path.basename(image))[0] for image in image_files_tif}

        # Get the .ndpi and .svs image names (source WSIs)
        image_files_wsi = glob.glob(os.path.join(pth, '*.ndpi')) + glob.glob(os.path.join(pth, '*.svs'))
        if not image_files_wsi:
            print("No .ndpi or .svs files found in the directory.")
            continue
        images_names_wsi = {os.path.splitext(os.path.basename(image))[0] for image in image_files_wsi}

        # Determine which images are missing for THIS resolution
        missing_images = images_names_wsi - images_names_tif

        if missing_images:
            process_missing_images_for_resolution(pth, resolution, umpix, missing_images)


if __name__ == '__main__':
    path = r'\\10.17.182.53\kiemen-lab-data\Valentina Matos\PanIn Lifespan study\2D slides michigan\Raw_GOL_07022026\renamed'
    # 8um = 1.25x #4um = 2.5x, #2um=5x, 1um=10x, 0.5um=20x, 0.25um=40x
    resolutions = ['10x']
    umpix_list = [1]
    WSI2tif(path, resolutions, umpix_list)