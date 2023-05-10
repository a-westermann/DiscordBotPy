import pylab
import matplotlib.pyplot as pyplot
from matplotlib_venn import venn3, venn3_circles
import discord


def get_baby_venn():
    ashley_names = set(['Evelyn', 'Heidi', 'Paytona500', 'Sophia'])
    andrew_names = set(['Evelyn', 'Heidi', 'Rosemary', 'Anya'])
    venn = venn3([ashley_names, andrew_names], ('Ashley_Names', 'Andrew_Names'))
    # pyplot.show()
    chart_file = "names_diagram.png"
    pyplot.savefig(chart_file)
    chart_image = discord.File(chart_file)
    return chart_image