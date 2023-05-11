import pylab
import matplotlib.pyplot as pyplot
from matplotlib_venn import venn2, venn3, venn3_circles
import discord
import discord.ext


def get_baby_venn():
    pyplot.figure()
    subsets = (1, 1, 1)
    ashley_names = set(['Evelyn', 'Heidi', 'Paytona500', 'Sophia'])
    andrew_names = set(['Evelyn', 'Heidi', 'Rosemary', 'Anya'])
    venn = venn2(subsets=(ashley_names, andrew_names), set_labels=('Andrew', 'Ashley', 'Shared'))

    # labels =  ['Ashley_Names', 'Andrew_Names']
    # labels = ['Andrew', 'Ashley', 'Shared']
    # for label in labels:
    #     venn.get_label_by_id(label).set_text(label)
    # venn.get_label_by_id('100').set_text('andrew')

    pyplot.title("Baby Names")
    chart_file = "names_diagram.png"
    pyplot.savefig(chart_file) # could pass in dpi to savefig as chart's dpi to increase resolution
    chart_image = discord.File(chart_file)
    return chart_image