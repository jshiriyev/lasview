import plotly.graph_objects as go
import plotly.io as pio

# Create a Plotly figure
fig = go.Figure()

# Add a trace to the figure
fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[6, 7, 2, 4, 5], mode='lines+markers', name='Line'))

# Define the layout
fig.update_layout(
    title="Simple Plotly Plot",
    xaxis_title='X-Axis',
    yaxis_title='Y-Axis',
    autosize=True,
)

fig.show()

# Generate the HTML for the plot
# html = pio.to_html(fig, full_html=False)

# # Save the HTML file
# with open("centered_plotly_plot.html", "w") as f:
#     f.write(html)