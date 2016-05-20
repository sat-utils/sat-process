import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.coords import disjoint_bounds, BoundingBox


def intensity_range(image, range_values='image', clip_negative=False):
    """Return image intensity range (min, max) based on desired value type.
    Parameters
    ----------
    image : array
        Input image.
    range_values : str or 2-tuple
        The image intensity range is configured by this parameter.
        The possible values for this parameter are enumerated below.
        'image'
            Return image min/max as the range.
        'dtype'
            Return min/max of the image's dtype as the range.
        dtype-name
            Return intensity range based on desired `dtype`. Must be valid key
            in `DTYPE_RANGE`. Note: `image` is ignored for this range type.
        2-tuple
            Return `range_values` as min/max intensities. Note that there's no
            reason to use this function if you just want to specify the
            intensity range explicitly. This option is included for functions
            that use `intensity_range` to support all desired range types.
    clip_negative : bool
        If True, clip the negative range (i.e. return 0 for min intensity)
        even if the image dtype allows negative values.
    """
    if range_values == 'dtype':
        range_values = image.dtype.type

    if range_values == 'image':
        i_min = np.min(image)
        i_max = np.max(image)
    # elif range_values in DTYPE_RANGE:
    #     i_min, i_max = DTYPE_RANGE[range_values]
    #     if clip_negative:
    #         i_min = 0
    else:
        i_min, i_max = range_values
    return i_min, i_max


def rescale_intensity(image, in_range='image', out_range='dtype'):
    """Return image after stretching or shrinking its intensity levels.
    The desired intensity range of the input and output, `in_range` and
    `out_range` respectively, are used to stretch or shrink the intensity range
    of the input image. See examples below.
    Parameters
    ----------
    image : array
        Image array.
    in_range, out_range : str or 2-tuple
        Min and max intensity values of input and output image.
        The possible values for this parameter are enumerated below.
        'image'
            Use image min/max as the intensity range.
        'dtype'
            Use min/max of the image's dtype as the intensity range.
        dtype-name
            Use intensity range based on desired `dtype`. Must be valid key
            in `DTYPE_RANGE`.
        2-tuple
            Use `range_values` as explicit min/max intensities.
    Returns
    -------
    out : array
        Image array after rescaling its intensity. This image is the same dtype
        as the input image.
    See Also
    --------
    equalize_hist
    Examples
    --------
    By default, the min/max intensities of the input image are stretched to
    the limits allowed by the image's dtype, since `in_range` defaults to
    'image' and `out_range` defaults to 'dtype':
    >>> image = np.array([51, 102, 153], dtype=np.uint8)
    >>> rescale_intensity(image)
    array([  0, 127, 255], dtype=uint8)
    It's easy to accidentally convert an image dtype from uint8 to float:
    >>> 1.0 * image
    array([  51.,  102.,  153.])
    Use `rescale_intensity` to rescale to the proper range for float dtypes:
    >>> image_float = 1.0 * image
    >>> rescale_intensity(image_float)
    array([ 0. ,  0.5,  1. ])
    To maintain the low contrast of the original, use the `in_range` parameter:
    >>> rescale_intensity(image_float, in_range=(0, 255))
    array([ 0.2,  0.4,  0.6])
    If the min/max value of `in_range` is more/less than the min/max image
    intensity, then the intensity levels are clipped:
    >>> rescale_intensity(image_float, in_range=(0, 102))
    array([ 0.5,  1. ,  1. ])
    If you have an image with signed integers but want to rescale the image to
    just the positive range, use the `out_range` parameter:
    >>> image = np.array([-10, 0, 10], dtype=np.int8)
    >>> rescale_intensity(image, out_range=(0, 127))
    array([  0,  63, 127], dtype=int8)
    """
    dtype = image.dtype.type

    if in_range is None:
        in_range = 'image'
        msg = "`in_range` should not be set to None. Use {!r} instead."
        print(msg.format(in_range))

    if out_range is None:
        out_range = 'dtype'
        msg = "`out_range` should not be set to None. Use {!r} instead."
        print(msg.format(out_range))

    imin, imax = intensity_range(image, in_range)
    omin, omax = intensity_range(image, out_range, clip_negative=(imin >= 0))

    image = np.clip(image, imin, imax)

    image = (image - imin) / float(imax - imin)
    return dtype(image * (omax - omin) + omin)


def color_map_reader(path):
    """
    reads the colormap from a text file given as path.
    """

    max_value = 255
    mode = None

    try:
        i = 0
        colormap = {}
        with open(path) as cmap:
            lines = cmap.readlines()
            for line in lines:
                if not mode:
                    if 'mode = ' in line:
                        mode = float(line.replace('mode = ', ''))
                    else:
                        continue
                else:
                    str = line.split()
                    if str == []:  # when there are empty lines at the end of the file
                        break
                    colormap.update(
                        {
                            i: (int(round(float(str[0]) * max_value / mode)),
                                int(round(float(str[1]) * max_value / mode)),
                                int(round(float(str[2]) * max_value / mode)))
                        }
                    )
                    i += 1
    except IOError:
        pass

    return colormap


def adjust_bounding_box(bounds1, bounds2):
    """ If the bounds 2 corners are outside of bounds1, they will be adjusted to bounds1 corners
    @params
    bounds1 - The source bounding box
    bounds2 - The target bounding box that has to be within bounds1
    @return
    A bounding box tuple in (y1, x1, y2, x2) format
    """

    # out of bound check
    # If it is completely outside of target bounds, return target bounds
    if ((bounds2[0] > bounds1[0] and bounds2[2] > bounds1[0]) or
            (bounds2[2] < bounds1[2] and bounds2[2] < bounds1[0])):
        return bounds1

    if ((bounds2[1] < bounds1[1] and bounds2[3] < bounds1[1]) or
            (bounds2[3] > bounds1[3] and bounds2[1] > bounds1[3])):
        return bounds1

    new_bounds = list(bounds2)

    # Adjust Y axis (Longitude)
    if (bounds2[0] > bounds1[0] or bounds2[0] < bounds1[3]):
        new_bounds[0] = bounds1[0]
    if (bounds2[2] < bounds1[2] or bounds2[2] > bounds1[0]):
        new_bounds[2] = bounds1[2]

    # Adjust X axis (Latitude)
    if (bounds2[1] < bounds1[1] or bounds2[1] > bounds1[3]):
        new_bounds[1] = bounds1[1]
    if (bounds2[3] > bounds1[3] or bounds2[3] < bounds1[1]):
        new_bounds[3] = bounds1[3]

    return tuple(new_bounds)


def clip(src_path, dst_path, bounds, crs=None):

    if not isinstance(bounds, list):
        raise Exception('Bounds must be a python list')

    with rasterio.drivers():
        with rasterio.open(src_path, 'r') as src:

            if not crs:
                crs = src.crs
            bounds = transform_bounds(
                crs,
                src.crs,
                *bounds
            )

            if disjoint_bounds(bounds, src.bounds):
                bounds = adjust_bounding_box(src.bounds, bounds)

            window = src.window(*bounds)

            out_kwargs = src.meta.copy()
            out_kwargs.update({
                'height': window[0][1] - window[0][0],
                'width': window[1][1] - window[1][0],
                'transform': src.window_transform(window)
            })

            with rasterio.open(dst_path, 'w', **out_kwargs) as out:
                try:
                    # write color map if exist
                    for index in src.indexes:
                        out.write_colormap(index, src.colormap(index))
                except ValueError:
                    pass

                out.write(src.read(window=window))
