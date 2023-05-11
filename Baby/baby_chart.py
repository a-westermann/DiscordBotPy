import pylab
import matplotlib.pyplot as pyplot
from matplotlib_venn import venn3, venn3_circles
import discord


def get_baby_venn():
    subsets = (1, 1, 1)
    ashley_names = set(['Evelyn', 'Heidi', 'Paytona500', 'Sophia'])
    andrew_names = set(['Evelyn', 'Heidi', 'Rosemary', 'Anya'])
    venn = venn3(subsets=subsets)

    # labels =  ['Ashley_Names', 'Andrew_Names']
    labels = ['100', '110', '010']
    for label in labels:
        venn.get_label_by_id(label).set_text(label)
    venn.get_label_by_id('100').set_text('andrew')
    # pyplot.show()
    chart_file = "names_diagram.png"
    pyplot.savefig(chart_file)
    chart_image = discord.File(chart_file)
    return chart_image