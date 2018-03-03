"""Detect objects on the image."""

from __future__ import (print_function,
                        division,
                        absolute_import)

import numpy as np
import scipy.stats as st

import sep

__all__ = ['sep_detection', 'simple_convolution_kernel', 'get_gaussian_kernel',
           'sep_background']


def simple_convolution_kernel(kernel):
    """Precomputed convolution kernel for the SEP detections."""
    if kernel == 1:
        # Tophat_3.0_3x3
        convKer = np.asarray([[0.560000, 0.980000,
                               0.560000], [0.980000, 1.000000, 0.980000],
                              [0.560000, 0.980000, 0.560000]])
    elif kernel == 2:
        # Topcat_4.0_5x5
        convKer = np.asarray(
            [[0.000000, 0.220000, 0.480000, 0.220000,
              0.000000], [0.220000, 0.990000, 1.000000, 0.990000, 0.220000],
             [0.480000, 1.000000, 1.000000, 1.000000,
              0.480000], [0.220000, 0.990000, 1.000000, 0.990000, 0.220000],
             [0.000000, 0.220000, 0.480000, 0.220000, 0.000000]])
    elif kernel == 3:
        # Topcat_5.0_5x5
        convKer = np.asarray(
            [[0.150000, 0.770000, 1.000000, 0.770000,
              0.150000], [0.770000, 1.000000, 1.000000, 1.000000, 0.770000],
             [1.000000, 1.000000, 1.000000, 1.000000,
              1.000000], [0.770000, 1.000000, 1.000000, 1.000000, 0.770000],
             [0.150000, 0.770000, 1.000000, 0.770000, 0.150000]])
    elif kernel == 4:
        # Gaussian_3.0_5x5
        convKer = np.asarray(
            [[0.092163, 0.221178, 0.296069, 0.221178,
              0.092163], [0.221178, 0.530797, 0.710525, 0.530797, 0.221178],
             [0.296069, 0.710525, 0.951108, 0.710525,
              0.296069], [0.221178, 0.530797, 0.710525, 0.530797, 0.221178],
             [0.092163, 0.221178, 0.296069, 0.221178, 0.092163]])
    elif kernel == 5:
        # Gaussian_4.0_7x7
        convKer = np.asarray([[
            0.047454, 0.109799, 0.181612, 0.214776, 0.181612, 0.109799,
            0.047454
        ], [
            0.109799, 0.254053, 0.420215, 0.496950, 0.420215, 0.254053,
            0.109799
        ], [
            0.181612, 0.420215, 0.695055, 0.821978, 0.695055, 0.420215,
            0.181612
        ], [
            0.214776, 0.496950, 0.821978, 0.972079, 0.821978, 0.496950,
            0.214776
        ], [
            0.181612, 0.420215, 0.695055, 0.821978, 0.695055, 0.420215,
            0.181612
        ], [
            0.109799, 0.254053, 0.420215, 0.496950, 0.420215, 0.254053,
            0.109799
        ], [
            0.047454, 0.109799, 0.181612, 0.214776, 0.181612, 0.109799,
            0.047454
        ]])
    elif kernel == 6:
        # Gaussian_5.0_9x9
        convKer = np.asarray([[
            0.030531, 0.065238, 0.112208, 0.155356, 0.173152, 0.155356,
            0.112208, 0.065238, 0.030531
        ], [
            0.065238, 0.139399, 0.239763, 0.331961, 0.369987, 0.331961,
            0.239763, 0.139399, 0.065238
        ], [
            0.112208, 0.239763, 0.412386, 0.570963, 0.636368, 0.570963,
            0.412386, 0.239763, 0.112208
        ], [
            0.155356, 0.331961, 0.570963, 0.790520, 0.881075, 0.790520,
            0.570963, 0.331961, 0.155356
        ], [
            0.173152, 0.369987, 0.636368, 0.881075, 0.982004, 0.881075,
            0.636368, 0.369987, 0.173152
        ], [
            0.155356, 0.331961, 0.570963, 0.790520, 0.881075, 0.790520,
            0.570963, 0.331961, 0.155356
        ], [
            0.112208, 0.239763, 0.412386, 0.570963, 0.636368, 0.570963,
            0.412386, 0.239763, 0.112208
        ], [
            0.065238, 0.139399, 0.239763, 0.331961, 0.369987, 0.331961,
            0.239763, 0.139399, 0.065238
        ], [
            0.030531, 0.065238, 0.112208, 0.155356, 0.173152, 0.155356,
            0.112208, 0.065238, 0.030531
        ]])
    else:
        raise Exception("### More options will be available in the future")

    return convKer


def get_gaussian_kernel(size, sig):
    """Return a 2D Gaussian kernel array.

    Based on https://stackoverflow.com/questions/29731726
    """
    interval = (2 * size + 1.) / size
    x = np.linspace(-size - interval / 2.,
                    size + interval / 2., size + 1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw/kernel_raw.sum()

    return kernel


def sep_background(img, mask=None, bw=None, bh=None, fw=None, fh=None,
                   subtract=False, bkgsize_min=10, **sep_kwargs):
    """Background measurement using SEP."""
    if bw is None:
        bw = img.shape[0] / 5
        bw = bw if bw >= bkgsize_min else bkgsize_min
    if bh is None:
        bh = img.shape[0] / 5
        bh = bh if bh >= bkgsize_min else bkgsize_min
    if fw is None:
        fw = bw / 2.
    if fh is None:
        fh = bh / 2.

    mask = mask if mask is None else mask.astype(bool)

    bkg = sep.Background(img, mask=mask, bw=bw, bh=bh,
                         fw=fw, fh=fh, **sep_kwargs)

    if subtract:
        # Subtract the Background off
        bkg.subfrom(img)
        return bkg, img

    return bkg


def sep_detection(img, threshold, kernel=4, err=None, use_sig=True,
                  subtract_bkg=True, return_bkg=True, return_seg=True,
                  bkg_kwargs=None, **det_kwargs):
    """Object detection using SEP.

    Example of bkg_kwargs:
        {'mask': None, 'bw': 100, 'bh': 100, 'fw': 100, 'fh': 100 }

    Example of det_kwargs:
        {'minarea': 10, 'deblend_nthreshs': 32,
         'deblend_conts': 0.0001, 'filter_type': 'matched'}

    """
    # Determine the kernel used in detection
    if isinstance(kernel, int):
        filter_kernel = simple_convolution_kernel(kernel)
    elif isinstance(kernel, (list, tuple, np.ndarray)):
        filter_kernel = get_gaussian_kernel(kernel[0], kernel[1])
    else:
        raise Exception("Wrong choice for convolution kernel")

    # Estimate background, subtract it if necessary
    if subtract_bkg:
        if bkg_kwargs is not None:
            bkg, img = sep_background(img, subtract=True, **bkg_kwargs)
        else:
            bkg, img = sep_background(img, subtract=True)
    else:
        if bkg_kwargs is not None:
            bkg = sep_background(img, subtract=False, **bkg_kwargs)
        else:
            bkg = sep_background(img, subtract=False)

    # If no error or variance array is provided, use the global rms of sky
    if err is None:
        threshold *= bkg.globalrms

    # Make the detection using sigma or variance array
    if use_sig:
        results = sep.extract(img, threshold, err=err,
                              filter_kernel=filter_kernel,
                              segmentation_map=return_seg, **det_kwargs)
    else:
        results = sep.extract(img, threshold, var=err,
                              filter_kernel=filter_kernel,
                              segmentation_map=return_seg, **det_kwargs)

    if return_seg:
        obj, seg = results
        if return_bkg:
            return obj, seg, bkg
    else:
        if return_bkg:
            return results, bkg