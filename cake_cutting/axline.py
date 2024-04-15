from matplotlib.transforms import Bbox, BboxTransformTo
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
import numpy as np

def axline(
    ax: Axes, xy1: tuple[float, float], xy2: tuple[float, float] = None, *,
    slope: float | None = None, semi_x: bool = None, segment: bool = None, **kwargs
):
    """
    Custom axline function. Adds option for controlling which x-halfplane
    around the xy1 point to draw.

    semi_x=True uses the halfplane greater than xy1 (positive x direction),
        semi_x=False uses the halfplane less than xy1 (negative x direction)

    Ignoring semi_x (semi_x=None) preserves the default axline behavior.
    
    .

    Original docstring below:
    ----------
    Add an infinitely long straight line.

    The line can be defined either by two points *xy1* and *xy2*, or
    by one point *xy1* and a *slope*.

    This draws a straight line "on the screen", regardless of the x and y
    scales, and is thus also suitable for drawing exponential decays in
    semilog plots, power laws in loglog plots, etc. However, *slope*
    should only be used with linear scales; It has no clear meaning for
    all other scales, and thus the behavior is undefined. Please specify
    the line using the points *xy1*, *xy2* for non-linear scales.

    The *transform* keyword argument only applies to the points *xy1*,
    *xy2*. The *slope* (if given) is always in data coordinates. This can
    be used e.g. with ``ax.transAxes`` for drawing grid lines with a fixed
    slope.

    Parameters
    ----------
    xy1, xy2 : (float, float)
        Points for the line to pass through.
        Either *xy2* or *slope* has to be given.
    slope : float, optional
        The slope of the line. Either *xy2* or *slope* has to be given.

    Returns
    -------
    `.AxLine`

    Other Parameters
    ----------------
    **kwargs
        Valid kwargs are `.Line2D` properties

        %(Line2D:kwdoc)s

    See Also
    --------
    axhline : for horizontal lines
    axvline : for vertical lines

    Examples
    --------
    Draw a thick red line passing through (0, 0) and (1, 1)::

        >>> axline((0, 0), (1, 1), linewidth=4, color='r')
    """
    if slope is not None and (ax.get_xscale() != 'linear' or
                              ax.get_yscale() != 'linear'):
        raise TypeError("'slope' cannot be used with non-linear scales")

    datalim = [xy1] if xy2 is None else [xy1, xy2]
    if "transform" in kwargs:
        # if a transform is passed (i.e. line points not in data space),
        # data limits should not be adjusted.
        datalim = []

    line = _AxLine(xy1, xy2, slope, semi_x, segment, **kwargs)
    # Like add_line, but correctly handling data limits.
    ax._set_artist_props(line)
    if line.get_clip_path() is None:
        line.set_clip_path(ax.patch)
    if not line.get_label():
        line.set_label(f"_child{len(ax._children)}")
    ax._children.append(line)
    line._remove_method = ax._children.remove
    ax.update_datalim(datalim)

    #     line.set_label(f"_line{len(ax.lines)}")
    # ax.lines.append(line)
    # line._remove_method = ax.lines.remove
    # ax.update_datalim(datalim)

    ax._request_autoscale_view()
    return line

class _AxLine(Line2D):
    def __init__(self, xy1, xy2, slope, semi_x, segment, **kwargs):
        super().__init__([0, 1], [0, 1], **kwargs)

        if (xy2 is None and slope is None or
                xy2 is not None and slope is not None):
            raise TypeError(
                "Exactly one of 'xy2' and 'slope' must be given")

        self._slope = slope
        self._xy1 = xy1
        self._xy2 = xy2
        self._semi_x = semi_x  # handle semi-plane
        self._segment = segment

    def get_transform(self):
        ax = self.axes
        points_transform = self._transform - ax.transData + ax.transScale

        if self._xy2 is not None:
            # two points were given
            (x1, y1), (x2, y2) = \
                points_transform.transform([self._xy1, self._xy2])
            dx = x2 - x1
            dy = y2 - y1
            if np.allclose(x1, x2):
                if np.allclose(y1, y2):
                    raise ValueError(
                        f"Cannot draw a line through two identical points "
                        f"(x={(x1, x2)}, y={(y1, y2)})")
                slope = np.inf
            else:
                slope = dy / dx
        else:
            # one point and a slope were given
            x1, y1 = points_transform.transform(self._xy1)
            slope = self._slope
        (vxlo, vylo), (vxhi, vyhi) = ax.transScale.transform(ax.viewLim)
        # General case: find intersections with view limits in either
        # direction, and draw between the middle two points.
        if np.isclose(slope, 0):
            start = vxlo, y1
            stop = vxhi, y1
        elif np.isinf(slope):
            start = x1, vylo
            stop = x1, vyhi
        else:
            _, start, stop, _ = sorted([
                (vxlo, y1 + (vxlo - x1) * slope),
                (vxhi, y1 + (vxhi - x1) * slope),
                (x1 + (vylo - y1) / slope, vylo),
                (x1 + (vyhi - y1) / slope, vyhi),
            ])
        # Handle semi-plane
        if self._semi_x:
            start = (x1, y1)
        elif self._semi_x is False:
            stop = (x1, y1)
        if self._segment and self._xy2 is not None:
            start = (x1, y1)
            stop = (x2, y2)
        return (BboxTransformTo(Bbox([start, stop]))
                + ax.transLimits + ax.transAxes)

    def draw(self, renderer):
        self._transformed_path = None  # Force regen.
        super().draw(renderer)

    def get_xy1(self):
        """
        Return the *xy1* value of the line.
        """
        return self._xy1

    def get_xy2(self):
        """
        Return the *xy2* value of the line.
        """
        return self._xy2

    def get_slope(self):
        """
        Return the *slope* value of the line.
        """
        return self._slope

    def set_xy1(self, x, y):
        """
        Set the *xy1* value of the line.

        Parameters
        ----------
        x, y : float
            Points for the line to pass through.
        """
        self._xy1 = x, y

    def set_xy2(self, x, y):
        """
        Set the *xy2* value of the line.

        Parameters
        ----------
        x, y : float
            Points for the line to pass through.
        """
        if self._slope is None:
            self._xy2 = x, y
        else:
            raise ValueError("Cannot set an 'xy2' value while 'slope' is set;"
                             " they differ but their functionalities overlap")

    def set_slope(self, slope):
        """
        Set the *slope* value of the line.

        Parameters
        ----------
        slope : float
            The slope of the line.
        """
        if self._xy2 is None:
            self._slope = slope
        else:
            raise ValueError("Cannot set a 'slope' value while 'xy2' is set;"
                             " they differ but their functionalities overlap")


def example():
    """
    Example to show usage cases.
    """
    import matplotlib.pyplot as plt

    fig, ax_dict = plt.subplot_mosaic(
        [
            ["slope no semi", "semi_x true", "semi_x false"],
            ["2 points semi_x true", "2 points semi_x false", "2 points segment"],
        ],
        figsize=(12, 8),
    )
    fig.suptitle("axline semiplanes and segments")

    ax: Axes
    ax = ax_dict["slope no semi"]
    ax.set_title("plot with slope\nno semi_x or segment")
    xy1 = (0.5, 0.5)
    slope = -1
    ax.scatter(*xy1)
    axline(ax, xy1, slope=slope, c="b", semi_x=None, segment=None)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xticks([])
    ax.set_yticks([])

    ax = ax_dict["semi_x true"]
    ax.set_title("plot with slope\nsemi_x = True")
    xy1 = (0.5, 0.5)
    slope = -1
    ax.scatter(*xy1)
    axline(ax, xy1, slope=slope, c="g", semi_x=True, segment=None)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xticks([])
    ax.set_yticks([])

    ax = ax_dict["semi_x false"]
    ax.set_title("plot with slope\nsemi_x = False")
    xy1 = (0.5, 0.5)
    slope = -1
    ax.scatter(*xy1)
    axline(ax, xy1, slope=slope, c="r", semi_x=False, segment=None)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xticks([])
    ax.set_yticks([])

    ax = ax_dict["2 points semi_x false"]
    ax.set_title("plot with 2 points\nsemi_x = False")
    xy1 = (0.5, 0.5)
    xy2 = (0.75, 0.75)
    ax.scatter(*xy1)
    ax.scatter(*xy2)
    axline(ax, xy1, xy2=xy2, c="r", semi_x=False, segment=None)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xticks([])
    ax.set_yticks([])

    ax = ax_dict["2 points semi_x true"]
    ax.set_title("plot with 2 points\nsemi_x = True")
    xy1 = (0.5, 0.5)
    xy2 = (0.75, 0.75)
    ax.scatter(*xy1)
    ax.scatter(*xy2)
    axline(ax, xy1, xy2=xy2, c="g", semi_x=True, segment=None)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xticks([])
    ax.set_yticks([])

    ax = ax_dict["2 points segment"]
    ax.set_title("plot with 2 points\nsegment = True")
    xy1 = (0.5, 0.5)
    xy2 = (0.75, 0.75)
    ax.scatter(*xy1)
    ax.scatter(*xy2)
    axline(ax, xy1, xy2=xy2, c="k", semi_x=None, segment=True)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()


if __name__ == "__main__":
    example()
