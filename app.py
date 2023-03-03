from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import random

app = Flask(__name__, static_folder='templates/site/static')


@app.route('/')
def start():
    return render_template('/site/index.html')


@app.route('/about')
def about():
    return render_template('/site/about.html')


@app.route('/graphics_demo', methods=['GET'])
def demo():
    months = ['Enero', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
              'Jul', 'Agosto', 'Sep', 'Oct', 'Nov', 'Dec']

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=months,
        y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
        name='Producto Primario',
        marker_color='indianred'
    ))
    fig2.add_trace(go.Bar(
        x=months,
        y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
        name='Producto Secundario',
        marker_color='lightsalmon'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig2.update_layout(barmode='group', xaxis_tickangle=-45)

    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                     size='petal_length', hover_data=['petal_width'])

    graph_html = pio.to_html(fig, full_html=False)
    graph_html2 = pio.to_html(fig2, full_html=False)

    return render_template('site/demo.html', graph_html1=graph_html, graph_html2=graph_html2)

    return render_template('site/demo.html')


@app.route('/graphics_custom', methods=['GET', 'POST'])
def graphics_custom():
    if request.method == 'POST':
        x_values = request.form['x']
        y_values = request.form['y']

        # Split the X and Y values into lists
        x_values_list = [float(x.strip()) for x in x_values.split(',')]
        y_values_list = [float(y.strip()) for y in y_values.split(',')]

        # Create a Pandas DataFrame from the X and Y values
        df = pd.DataFrame({'X': x_values_list, 'Y': y_values_list})

        # Plot the graph using plotly
        fig = px.scatter(df, x='X', y='Y')

        # Convert the plotly graph to HTML
        graph_html = pio.to_html(fig, full_html=False)

        return render_template('site/graphics_custom.html', graph_html=graph_html)

    return render_template('site/graphics_custom.html')


@app.route('/graphics', methods=['GET', 'POST'])
def graphics():
    if request.method == 'POST':
        selected_table = request.form.get('table')
        fig, table_html = create_figure1(selected_table)

        if fig is None:
            return render_template('site/graphics.html', error_message=table_html)

        graph_html = pio.to_html(fig, full_html=False)

        return render_template('site/graphics.html', graph_html=graph_html, table_html=table_html)

    return render_template('site/graphics.html')


def create_figure1(selected_table=None):
    try:
        if selected_table == 'sm_hist':
            df = pd.read_csv(r'templates/files/sm_hist.csv', encoding='ISO-8859-1', delimiter=',')
            rounded_data = df.round({"sm_pa": 2})
            rounded_data = rounded_data.rename(
                columns={"anio": "Año", "sm_pa": "Salario mínimo (Pesos diarios)", "NPSM": "NPSM"})

            data = px.bar(rounded_data, x='Año', y="Salario mínimo (Pesos diarios)", color="NPSM",
                          color_discrete_sequence=["#691c32", "#bc955c"],
                          labels=dict(sm_pa="Salario mínimo (Pesos diarios)", anio="Año", NPSM="NPSM"))
            fig = go.Figure(data=data)
            fig.update_traces(showlegend=False)
            table_html = rounded_data.to_html(classes='table table-success table-striped table-hover', index=None)
            return fig, table_html
        elif selected_table == 'sbc_zona':

            df = pd.read_csv(r'templates/files/sbc_zona.csv', encoding='ISO-8859-1', delimiter=',')
            rounded_data = df.round({"SBC": 2})
            rounded_data = rounded_data.rename(
                columns={"year": "Año", "month": "Mes"})
            concat_day = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

            data = px.line(rounded_data, x=concat_day, y="SBC", color="Zona",
                           color_discrete_sequence=["#bc955c", "#235b4e"],
                           labels={
                               "x": "Año",
                               "SBC": "Pesos diarios",
                           })
            fig = go.Figure(data=data)
            table_html = rounded_data.to_html(classes='table table-success table-striped table-hover', index=None)
            return fig, table_html
        elif selected_table == 'smg18_actual':
            df = pd.read_csv(r'templates/files/smg18_actual.csv', encoding='ISO-8859-1', delimiter=',')

            rounded_data = df.round({"SMG": 2})
            data = px.line(rounded_data, x="fecha", y="SMG", color="zona",
                           color_discrete_sequence=["#235b4e", "#bc955c"],
                           labels={
                               "SMG": "Porcentaje",
                               "fecha": "Año",
                           })

            fig = go.Figure(data=data)
            table_html = rounded_data.to_html(classes='table table-success table-striped table-hover', index=None)
            return fig, table_html

        else:
            print("Invalid table selected")
            return None, None
    except Exception as e:
        print("Error:", str(e))
        return None, None


if __name__ == '__main__':
    app.run(debug=True)
