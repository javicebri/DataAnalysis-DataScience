import panel as pn
import holoviews as hv
import pandas as pd
import numpy as np
from scipy.optimize import minimize
#from cerberus import Validator

pn.extension()


class GraphApp:
    def __init__(self):
        self.index = 0  # Índice para el gráfico
        self.plot_pane = pn.pane.HoloViews()

        self.functions_dict = {'Cuadratic': 'x**2',
                               'Mixed': '(np.sin(1/2 * x) + 2 * np.cos(1/2 * x)) * x**2'}
        possible_functions_list = list(self.functions_dict.keys()) + ["Custom"]
        self.select_widget = pn.widgets.Select(options=possible_functions_list,
                                               name='Function')
        self.select_widget.param.watch(self.select_function, "value")
        self.selected_option = None

        self.text_title = pn.pane.Markdown("# Optimizer Viewer", style={'font-size': '16pt'})
        self.text_widget = pn.widgets.StaticText(name='Hint', value='')
        self.text_widget.value = "Select the function."
        self.text_index = pn.widgets.StaticText(value='', visible=False)
        self.text_index.value = str(self.index)

        self.custom_input_widget = pn.widgets.TextInput(name='Custom function', visible=False)
        self.lower_limit_input_widget = pn.widgets.FloatInput(name='Lower limit', visible=False)
        self.upper_limit_input_widget = pn.widgets.FloatInput(name='Upper limit', visible=False)
        self.check_function_button = pn.widgets.Button(name="Validate", button_type="primary",
                                                       visible=False, align="center")
        self.check_function_button.on_click(self.check_function)
        self.optimize_button = pn.widgets.Button(name="Optimize", button_type="primary", visible=False)
        self.optimize_button.on_click(self.start_optimization)
        self.advance_button = pn.widgets.Button(name="Advance >", button_type="primary", visible=False)
        self.advance_button.on_click(self.advance_plot)
        self.backward_button = pn.widgets.Button(name="< Backward", button_type="primary", visible=False)
        self.backward_button.on_click(self.backward_plot)

        self.x = None
        self.x0 = None
        self.y = None
        self.curve = None
        self.max_index = 0
        self.lower_limit = None
        self.upper_limit = None
        self.iteration_arr = None
        self.evaluation_arr = None
        self.function_expression = None

    def read_limits(self):
        self.lower_limit = self.lower_limit_input_widget.value
        self.upper_limit = self.upper_limit_input_widget.value

        if self.lower_limit == self.upper_limit:
            self.text_widget.value = "Limits must have different values."

    def start_optimization(self, event):
        seed = 42
        np.random.seed(seed)

        self.read_limits()

        self.x0 = np.random.uniform(self.lower_limit,
                                    self.upper_limit)
        self.x = np.linspace(self.lower_limit,
                             self.upper_limit,
                             1000)

        if self.selected_option == "Custom":
            self.function_expression = self.custom_input_widget.value
            self.check_function()
        else:
            self.function_expression = self.functions_dict[self.selected_option]

        x = self.x  # eval expression needs x value
        self.y = eval(self.function_expression)

        self.curve = self.plot_function()

        # list to save each function evaluation: x value and function value
        evaluation_list = []
        iteration_list = []

        def objetive_function(x):
            eval_result = self.evaluate_function(x)
            evaluation_list.append(np.array([x[0], eval_result[0]]))
            return eval_result

        # callback funtion to save each iteration retsult: x value and function value
        def iteration_call(x):
            function_value = self.evaluate_function(x)
            iteration_list.append(np.array([x[0], function_value[0]]))

        # apply function
        result = minimize(objetive_function, self.x0,
                          method='slsqp',
                          bounds=[(self.lower_limit, self.upper_limit)],
                          options={'disp': True},
                          callback=iteration_call)

        self.evaluation_arr = np.vstack(evaluation_list)
        self.iteration_arr = np.vstack(iteration_list)

        evaluation_df = pd.DataFrame({
            'x': self.evaluation_arr[:, 0],
            'y': self.evaluation_arr[:, 1],
            'color': "blue"
        })
        evaluation_df.iloc[-1, 2] = "red"
        self.max_index = evaluation_df.shape[0]
        self.index = evaluation_df.shape[0]


        scatter = hv.Scatter(evaluation_df).opts(color=hv.dim('color').categorize({'blue': 'blue',
                                                                                   'red': 'red'}),
                                                 title='Optimization Iteration Nº={}'.format(self.max_index))
        self.plot_pane.object = self.curve * scatter
        self.text_index.value = self.max_index
        self.text_index.visible = True
        self.backward_button.visible = True
        self.advance_button.visible = True
        self.text_widget.value = "Optimization done"

    def evaluate_function(self, x):
        return eval(self.function_expression)

    def plot_function(self):
        curve = hv.Curve((self.x, self.y)).opts(width=500, height=300)
        return curve

    def check_function(self):
        x = np.array([0, 1, 2])
        try:
            eval(self.function_expression)
        except Exception as error:
            self.text_widget.value = error

    def select_function(self, event):
        self.selected_option = event.obj.value
        self.text_widget.value = "Selected function is " + self.selected_option +\
                                 ". Now fix the limits."

        if self.selected_option == "Custom":
            self.custom_input_widget.visible = True
            self.check_function_button.visible = False
        else:
            self.custom_input_widget.visible = False
            self.check_function_button.visible = False

        self.lower_limit_input_widget.visible = True
        self.upper_limit_input_widget.visible = True
        self.optimize_button.visible = True

    def advance_plot(self, event):
        if self.index < self.max_index:
            self.index += 1
            self.text_widget.value = "Advance done"
        self.text_index.value = str(self.index)
        self.update_plot()

    def backward_plot(self, event):
        if self.index > 0:
            self.index -= 1
            self.text_widget.value = "Backward done"
        self.text_index.value = str(self.index)
        self.update_plot()

    def update_plot(self):
        evaluation_df = pd.DataFrame({
            'x': self.evaluation_arr[:self.index, 0],
            'y': self.evaluation_arr[:self.index, 1],
            'color': "blue"
        })
        evaluation_df.iloc[-1, 2] = "red"
        scatter = hv.Scatter(evaluation_df).opts(color=hv.dim('color').categorize({'blue': 'blue',
                                                                                   'red': 'red'}),
                                                 title='Optimization Nº Iteration = {}'.format(evaluation_df.shape[0]))
        self.plot_pane.object = self.curve * scatter
        self.text_index.value = evaluation_df.shape[0]

    def view(self):
        return pn.Column(
            self.text_title,
            pn.Row(
                pn.Column(self.select_widget,
                          pn.Row(self.custom_input_widget,
                                 self.check_function_button),
                          self.lower_limit_input_widget,
                          self.upper_limit_input_widget,
                          self.optimize_button,
                          self.text_widget
                          ),
                pn.Column(self.plot_pane,
                          pn.Row(self.backward_button,
                                 self.text_index,
                                 self.advance_button)
                          ),
            )
        )


app = GraphApp()
# Abrir la aplicación en el navegador predeterminado
app.view().servable(title="Optimization Viewer")
