from manimlib.active.diffyq.part1.pendulum import Pendulum, ThetaVsTAxes
from manimlib.old.fourier import *
from manimlib.imports import *
from scipy.optimize import leastsq
import scipy.integrate

class Intro(Scene):

    def construct(self):
        title = TextMobject('BMED 2250\\\\Phase III\\\\Lecture 2')
        title1 = TextMobject('Signal Processing', color=BLUE)
        title1.scale(2)
        info = TextMobject('Raymond Biju\\\\', '\\emph{rbiju3@gatech.edu}')
        info.set_color_by_tex('\\emph', YELLOW)
        info.shift(DOWN)
        self.play(Write(title))
        self.wait()
        self.play(Transform(title, title1))
        self.wait()
        self.play(FadeInFromDown(info))

class PlotNoisySignal(GraphScene):
    CONFIG = {
        "y_max": 30,
        "y_min": 0,
        "x_max": 100,
        "x_min": 0,
        'x_tick_frequency': 10,
        "y_tick_frequency": 10,
        "axes_color": BLUE,
        "x_axis_label": "$t$",
        "y_axis_label": "$f(t)$",
        "graph_origin": ORIGIN + 5 * LEFT + 3 * DOWN
    }

    def construct(self):
        sf = 10
        f1 = 0.05
        f2 = 0.2
        data = self.getNoisyData(f1, f2, 100, sf)
        dots = VGroup()
        self.setup_axes()
        clean_sig = self.get_graph(lambda x: 6 * np.sin(2*math.pi * x * f1) + 15,
                                   color=WHITE)

        for time, dat in enumerate(data):
            ti = time / sf
            dot = Dot(color=BLUE, radius=0.03).move_to(self.coords_to_point(ti, dat))
            dots.add(dot)

        self.wait(0.5)
        self.play(ShowCreation(dots), run_time=4, rate_func=linear)
        self.wait(2)
        self.play(ShowCreation(clean_sig), run_time=4, rate_func=linear)
        self.wait(1)

    def getNoisyData(self, f1, f2, n, sf):
        times = np.linspace(0,n,n*sf + 1)
        data = 6 * np.sin(2*math.pi * times * f1) + 3 * np.sin(2*math.pi*times * f2) + 15
        for time, dat in enumerate(data):
            data[time] = dat + random.gauss(0, 3)
        return data

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parameters of labels
        #   For x
        init_label_x = 0
        end_label_x = 100
        step_x = 10
        #   For y
        init_label_y = 0
        end_label_y = 30
        step_y =10
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN  # DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
            init_label_x,
            end_label_x + step_x,
            step_x
        ))
        #   For y
        self.y_axis.add_numbers(*range(
            init_label_y,
            end_label_y + step_y,
            step_y
        ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis))
        self.wait()

class PlotReconstructedSignal(GraphScene):
    CONFIG = {
        "y_max": 30,
        "y_min": 0,
        "x_max": 100,
        "x_min": 0,
        'x_tick_frequency': 10,
        "y_tick_frequency": 10,
        "axes_color": BLUE,
        "x_axis_label": "$t$",
        "y_axis_label": "$f(t)$",
        "graph_origin": ORIGIN + 5 * LEFT + 3 * DOWN
    }
    def construct(self):
        f1 = 0.05
        f2 = 0.2
        self.setup_axes()
        graph = self.get_graph(lambda x: 6 * np.sin(2*math.pi * x * f1) + 3 * np.sin(2*math.pi*x * f2) + 15,
                               color=YELLOW)

        self.play(ShowCreation(graph), run_time=4, rate_func=linear)
        self.wait()

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parameters of labels
        #   For x
        init_label_x = 0
        end_label_x = 100
        step_x = 10
        #   For y
        init_label_y = 0
        end_label_y = 30
        step_y =10
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN  # DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
            init_label_x,
            end_label_x + step_x,
            step_x
        ))
        #   For y
        self.y_axis.add_numbers(*range(
            init_label_y,
            end_label_y + step_y,
            step_y
        ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis))
        self.wait()

class ModelingIsHard(Scene):
    def construct(self):
        f1 = TexMobject(
            "\\theta(t) =",  "\\theta_0", "\\cos(\\sqrt{\\frac{g}{L}} t)"
        )
        f1.scale(2)
        framebox1 = SurroundingRectangle(f1[1], buff=.1, color=RED)
        f2 = TexMobject(
            " (\\theta_0 <<< )", color=RED
        )
        f2.scale(2)
        self.play(Write(f1))
        self.wait(5)
        self.play(ShowCreation(framebox1))
        self.wait(5)
        self.play(FadeOut(framebox1),
                  Transform(f1,f2))
        self.wait()

class Digitization(GraphScene):
    CONFIG = {
        "y_max": 11,
        "y_min": 0,
        "x_max": 25,
        "x_min": 0,
        'x_tick_frequency': 2,
        "y_tick_frequency": 2,
        "axes_color": BLUE,
        "x_axis_label": "$t$",
        "y_axis_label": "$f(t)$",
        "graph_origin": ORIGIN + 5 * LEFT + 3 * DOWN
    }
    def construct(self):
        sf = 10
        tStep = 100
        tEnd = 25
        numBins = 16
        coeff = 5
        digiX, digiY = self.digitizer(sf, tStep, tEnd, numBins, coeff)
        self.setup_axes()
        dots = VGroup()
        for i in range(0,len(digiX)):
            dot = Dot(color=RED, radius=0.03).move_to(self.coords_to_point(digiX[i], digiY[i]))
            dots.add(dot)

        lines = VGroup()
        for j in range(0,len(dots)-1):
            line = Line(dots[j].get_center(), dots[j+1].get_center(), color=RED)
            lines.add(line)
        self.wait(0.5)
        graph1 = self.get_graph(lambda x: coeff * np.sin(x) + coeff)
        self.play(ShowCreation(graph1, run_time=8, color=BLUE, rate_func=linear),
                  ShowCreation(lines, run_time=8, rate_func=linear))


    def digitizer(self, sf, tStep, tEnd, numBins, coeff):
        x = np.linspace(0, tEnd, tEnd * tStep + 1)
        y = coeff * np.sin(x) + coeff
        bins = np.linspace(0, np.amax(y), numBins)
        inds = np.digitize(y, bins)
        xDig = np.arange(0, len(x), int(tStep / sf))
        yDig = inds[xDig]
        yDig = bins[yDig - 1]
        xDig = xDig / tStep
        digiX = np.repeat(xDig, 2)
        digiY = np.repeat(yDig, 2)
        digiX = digiX[1:]
        digiY = digiY[0:-1]
        return (digiX, digiY)

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parameters of labels
        #   For x
        init_label_x = 0
        end_label_x = 25
        step_x = 5
        #   For y
        init_label_y = 0
        end_label_y = 10
        step_y =5
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN  # DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
            init_label_x,
            end_label_x + step_x,
            step_x
        ))
        #   For y
        self.y_axis.add_numbers(*range(
            init_label_y,
            end_label_y + step_y,
            step_y
        ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis))
        self.wait()

class Amplification(GraphScene):
    CONFIG = {
        "y_max": 11,
        "y_min": 0,
        "x_max": 25,
        "x_min": 0,
        'x_tick_frequency': 2,
        "y_tick_frequency": 2,
        "axes_color": BLUE,
        "x_axis_label": "$t$",
        "y_axis_label": "$f(t)$",
        "graph_origin": ORIGIN + 5 * LEFT + 3 * DOWN
    }
    def construct(self):
        self.setup_axes()
        graph1 = self.get_graph(lambda x: np.sin(0.5 * 2*math.pi * x) + 2.5, color=WHITE)
        graph2 = self.get_graph(lambda x: 2.5 * np.sin(0.5 * 2*math.pi * x) + 2.5, color=YELLOW)

        self.play(ShowCreation(graph1))
        self.wait(3)
        self.play(Transform(graph1, graph2))
    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parameters of labels
        #   For x
        init_label_x = 0
        end_label_x = 20
        step_x = 5
        #   For y
        init_label_y = 0
        end_label_y = 10
        step_y =5
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN  # DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
            init_label_x,
            end_label_x + step_x,
            step_x
        ))
        #   For y
        self.y_axis.add_numbers(*range(
            init_label_y,
            end_label_y + step_y,
            step_y
        ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis))
        self.wait()

class Swing(Scene):
    CONFIG = {
        "pendulum_config": {
            "initial_theta": 20 * DEGREES,
            "length": 5,
            "gravity": 49.348,
            "weight_diameter": 0.3,
            "damping": 0,
            "top_point": ORIGIN,
        },
        "axes_config": {
            "y_axis_config": {"unit_size": 0.75},
            "x_axis_config": {
                "unit_size": 0.5,
                "numbers_to_show": range(2, 10, 2),
                "number_scale_val": 0.5,
            },
            "x_max": 10,
            "axis_config": {
                "tip_length": 0.3,
                "stroke_width": 2,
            }
        },
        "axes_corner": UL,
    }
    def construct(self):
        pendulum = Pendulum(**self.pendulum_config)
        pendulum.shift(2 * UP + 4 * RIGHT)
        axes = ThetaVsTAxes(**self.axes_config)
        axes.center()
        axes.to_corner(self.axes_corner, buff=LARGE_BUFF)
        axes.scale(1.5)
        axes.shift(DOWN + RIGHT)
        graph = axes.get_live_drawn_graph(pendulum)
        graph.scale(1.5)
        graph.shift(DOWN + RIGHT)

        prediction_formula = TexMobject(
            "\\theta_0", "\\cos(\\sqrt{g / L} \\cdot t)"
        )


        self.add(pendulum)
        self.wait()
        pendulum.start_swinging()
        self.wait(1.7)
        self.play(ShowCreation(axes))
        self.add(graph)
        self.wait(10)

class JustPendulum(Scene):
    CONFIG = {
        "pendulum_config": {
            "initial_theta": 20 * DEGREES,
            "length": 5,
            "gravity": 49.348,
            "weight_diameter": 0.3,
            "damping": 0,
            "top_point": ORIGIN,
        },
        "axes_config": {
            "y_axis_config": {"unit_size": 0.75},
            "x_axis_config": {
                "unit_size": 0.5,
                "numbers_to_show": range(2, 10, 2),
                "number_scale_val": 0.5,
            },
            "x_max": 10,
            "axis_config": {
                "tip_length": 0.3,
                "stroke_width": 2,
            }
        },
        "axes_corner": UL,
    }
    def construct(self):
        pendulum = Pendulum(**self.pendulum_config)
        pendulum.shift(2*UP)
        self.add(pendulum)
        self.wait()
        pendulum.start_swinging()
        self.wait(30)

class Nyquist(Scene):
    CONFIG = {
        "pendulum_config": {
            "initial_theta": 10 * DEGREES,
            "length": 5,
            "gravity": 49.348,
            "weight_diameter": 0.3,
            "damping": 0,
            "top_point": ORIGIN,
            "include_theta_label": False
        },
        "axes_config": {
            "y_axis_config": {"unit_size": 0.75},
            "x_axis_config": {
                "unit_size": 0.5,
                "numbers_to_show": range(2, 12, 2),
                "number_scale_val": 0.5,
            },
            "x_max": 12,
            "axis_config": {
                "tip_length": 0.3,
                "stroke_width": 2,
            }
        },
        "axes_corner": UL,
    }
    def construct(self):
        #double frequency is 0.95 Hz
        self.sample(0.7)

    def sample(self, sf):
        l = 5
        g = 49.348
        first_zero = 1 / 2 * math.pi * math.sqrt(l / g)
        total_time = 12
        pendulum = Pendulum(**self.pendulum_config)
        pendulum.shift(2 * UP + 4 * RIGHT)
        axes = ThetaVsTAxes(**self.axes_config)
        axes.center()
        axes.to_corner(self.axes_corner, buff=LARGE_BUFF)
        axes.scale(1.5)
        axes.shift(DOWN + RIGHT)
        graph = axes.get_live_drawn_graph(pendulum)
        graph.scale(1.5)
        graph.shift(DOWN + RIGHT)

        times = np.arange(first_zero, total_time, 1/sf)

        time_tracker = ValueTracker(0)

        flash_rect = FullScreenRectangle(
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2,
        )
        flash = FadeOut(
            flash_rect,
            rate_func=squish_rate_func(smooth, 0, 0.1)
        )

        self.add(pendulum)
        self.play(ShowCreation(axes))
        self.wait(2)
        dot = Dot(color=RED, radius=0.05)
        dot.move_to(graph.get_center())
        dot.shift(UP + LEFT)
        pendulum.start_swinging()
        self.wait(first_zero + 0.032)
        self.add(graph)
        dot_copies = VGroup()
        pendulum_copies = VGroup()
        thetas = np.array([])
        for t1, t2 in zip(times, times[1:]):
            dot_copy = dot.copy()
            dot_copy.clear_updaters()
            dot_copies.add(dot_copy)
            pendulum_copy = pendulum.copy()
            pendulum_copy.clear_updaters()
            pendulum_copy.set_opacity(0.2)
            pendulum_copies.add(pendulum_copy)
            thetas = np.append(thetas, pendulum.get_theta())

            self.add(dot_copy)
            self.add(pendulum_copy)

            # graph.save_state()
            kw = {
                "rate_func": lambda alpha: interpolate(
                    t1,
                    t2,
                    alpha
                )
            }
            anims = [
                # ShowCreation(graph, **kw),
                MoveAlongPath(dot, graph, **kw),
                ApplyMethod(
                    time_tracker.increment_value, 1/sf,
                    rate_func=linear
                ),
            ]
            anims.append(flash)
            self.play(*anims, run_time=1/sf)

        est_amp, est_freq, est_phase, est_mean = self.get_reconstruction(thetas[2:], times[2:-1])
        print(thetas[1:])
        print(times[1:-1])
        graph1 = axes.get_graph(lambda x: est_amp * np.sin(2 * math.pi * est_freq * (x - est_phase)) + est_mean, color=RED)
        print(est_amp, est_freq, est_phase, est_mean)

        self.wait(4)
        self.play(FadeOut(graph))
        self.wait(1)
        self.play(ShowCreation(graph1, run_time=5))
        self.wait(3)

    def get_reconstruction(self,thetas, times):
        optimize_func = lambda x: ((x[0] * np.sin(2 * math.pi * x[1] * (times - x[2])) + x[3]) - thetas)
        est_amp, est_freq, est_phase, est_mean = leastsq(optimize_func, [0.3, 0.2, 1, 0])[0]
        return est_amp, est_freq, est_phase, est_mean

class UncertaintyPrinciple(Scene):
    CONFIG = {
        "pendulum_config": {
            "initial_theta": 10 * DEGREES,
            "length": 5,
            "gravity": 49.348,
            "weight_diameter": 0.3,
            "damping": 0,
            "top_point": ORIGIN,
            "include_theta_label": False
        },
        "axes_config": {
            "y_axis_config": {"unit_size": 0.75},
            "x_axis_config": {
                "unit_size": 0.5,
                "numbers_to_show": range(1, 12, 2),
                "number_scale_val": 0.5,
            },
            "x_max": 2,
            "axis_config": {
                "tip_length": 0.3,
                "stroke_width": 2,
            }
        },
        "axes_corner": UL,
    }
    def construct(self):
        #half frequency is 0.95 Hz
        self.sample(4)

    def sample(self, sf):
        l = 5
        g = 49.348
        first_zero = 1 / 2 * math.pi * math.sqrt(l / g)
        total_time = 2
        pendulum = Pendulum(**self.pendulum_config)
        pendulum.shift(2 * UP + 4 * RIGHT)
        axes = ThetaVsTAxes(**self.axes_config)
        axes.center()
        axes.to_corner(self.axes_corner, buff=LARGE_BUFF)
        axes.scale(1.5)
        axes.shift(DOWN + RIGHT)
        graph = axes.get_live_drawn_graph(pendulum)
        graph.scale(1.5)
        graph.shift(DOWN + RIGHT)

        times = np.arange(first_zero, total_time, 1/sf)

        time_tracker = ValueTracker(0)

        flash_rect = FullScreenRectangle(
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2,
        )
        flash = FadeOut(
            flash_rect,
            rate_func=squish_rate_func(smooth, 0, 0.1)
        )

        graph1 = axes.get_graph(lambda x: 0.17 * np.sin(2 * math.pi * 0.7 * (x - 0.5 - math.pi)),
                                color=RED, opacity=0.3)
        graph2 = axes.get_graph(lambda x: 0.17 * np.sin(2 * math.pi * 0.9 * (x - 0.5 - math.pi - 0.4)),
                                color=YELLOW, opacity=0.3)

        self.add(pendulum)
        self.play(ShowCreation(axes))
        self.wait(2)
        dot = Dot(color=RED, radius=0.05)
        dot.move_to(graph.get_center())
        dot.shift(UP + LEFT)
        pendulum.start_swinging()
        self.wait(first_zero + 0.032)
        self.add(graph)
        dot_copies = VGroup()
        pendulum_copies = VGroup()
        for t1, t2 in zip(times, times[1:]):
            dot_copy = dot.copy()
            dot_copy.clear_updaters()
            dot_copies.add(dot_copy)
            pendulum_copy = pendulum.copy()
            pendulum_copy.clear_updaters()
            pendulum_copy.set_opacity(0.2)
            pendulum_copies.add(pendulum_copy)

            self.add(dot_copy)
            self.add(pendulum_copy)

            # graph.save_state()
            kw = {
                "rate_func": lambda alpha: interpolate(
                    t1,
                    t2,
                    alpha
                )
            }
            anims = [
                # ShowCreation(graph, **kw),
                MoveAlongPath(dot, graph, **kw),
                ApplyMethod(
                    time_tracker.increment_value, 1/sf,
                    rate_func=linear
                ),
            ]
            anims.append(flash)
            self.play(*anims, run_time=1/sf)
        self.wait(2)
        self.play(FadeOut(graph))
        self.play(ShowCreation(graph1),
                  ShowCreation(graph2))
        self.wait(3)

class WaveletTransform(GraphScene):
    