
import seaborn as sns
import matplotlib.pyplot as plt


def barplot_final_list_of_labels_v001(labels_list,des="",logger=None):
    plot_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=plot_dims)

    labels_unique = list(set(labels_list))

    # This is the corresponding count for each value
    counts = [labels_list.count(value) for value in labels_unique]


    ax = sns.barplot(x = labels_unique,
                    y = counts,ax=ax)

    ##? write class value on each par
    for i in ax.containers:
        ax.bar_label(i,)

    ax.set_xlabel(f"{des} - class label")
    ax.set_ylabel("number of data item")
    fig.savefig("output.png")
    plt.show()
    logger.log_image(image_data = "output.png", name=f"dataloader_data_{des}",image_format="png",step= 0)