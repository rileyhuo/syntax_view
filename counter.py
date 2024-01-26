import matplotlib.pyplot as plt

def temporal(df, observations):

    def find_observation_names(observation):
        observation_dictionary = {
            'Interactional Role': {'Maxine', 'mother', 'father', 'aunt', 'NA'},
            'Gender': {'NA', 'feminine', 'masculine'},
            'Person': {'first', 'second', 'third'},
            'Number': {'singular', 'plural'},
            'Grammatical Function': {'subject', 'indirect object', 'direct object', 'object of preposition'}
        }
        observation_names = []

        for o in observation:
            for key, value in observation_dictionary.items():
                if o in value:
                    observation_names.append(key)

        return(observation_names)
            
    observation_names_here = find_observation_names(observations[0])
    

    i_role_colors = {
    'Maxine': '#ffd500',
    'aunt': '#ff9100',
    'mother': '#ff0080',
    'parents': '#bc00c9',
    'father': '#0018f0'
    }

    gender_colors = {
    'feminine': '#ff0080',
    'masculine': '#00e0e0',
    'NA': '#ffdd00',
    }

    person_number_colors = {
    ('first', 'singular'): '#eb462d',
    ('first', 'plural'): '#b31e39',
    ('second', 'singular'): "#fff200",
    # ('second', 'plural'): 'pink',
    ('third', 'singular'): '#00d130',
    ('third', 'plural'): '#00a326'
    }

    if observation_names_here == ['Interactional Role']:
        colors = i_role_colors
        
    if observation_names_here == ['Gender']:
        colors = gender_colors
    
    if observation_names_here == ['Person', 'Number'] or observation_names_here == ['Number', 'Person']:
        colors = person_number_colors

    # Creating the figure and axis with a specific plot size

    fig, ax = plt.subplots(figsize=(9.5, 4))  # Set your desired figure size here (width, height)
    fig.set_dpi(250)

    # Initializing x-position for blocks
    x_pos = 0

    # Plotting the first set of blocks based on Person-Gender combination
    for index, row in df.iterrows():
    
        if len(observations[0]) == 1:
            color_here = colors.get(row[observation_names_here[0]], 'white')
        
        if len(observations[0]) == 2:
            color_here = colors.get((row[observation_names_here[0]], row[observation_names_here[1]]), 'white')
        
        # Plotting rectangular blocks for the first set with y = 2
        rect = plt.Rectangle((x_pos, 3), 1, 1, color=color_here, edgecolor=color_here, linewidth=0)
        ax.add_patch(rect)
        
        # Incrementing x-position for the next block
        x_pos += 1

    # Resetting x-position for the next set of blocks
    x_pos = 0

    # Plotting the second set of blocks based on "Theta Role" for 'agent'
    for index, row in df.iterrows():
        if len(observations[0]) == 1:
            key = row[observation_names_here[0]]
            if any(part.strip() == 'agent' for part in row['Theta Role'].split('/')):
                if key in colors.keys():
                    color_here = colors[key]
                    # Plotting rectangular blocks for the second set with y = 1
                    rect = plt.Rectangle((x_pos, 2), 1, 1, color=color_here, edgecolor=color_here, linewidth=0)
                    ax.add_patch(rect)

        if len(observations[0]) == 2:
            key_0, key_1 = row[observation_names_here[0]], row[observation_names_here[1]]
            if any(part.strip() == 'agent' for part in row['Theta Role'].split('/')):
                if (key_0, key_1) in colors.keys():
                    color_here = colors[(key_0, key_1)]
                    # Plotting rectangular blocks for the second set with y = 1
                    rect = plt.Rectangle((x_pos, 2), 1, 1, color=color_here, edgecolor=color_here, linewidth=0)
                    ax.add_patch(rect)
        
        # Incrementing x-position for the next block
        x_pos += 1

    x_pos = 0

    for index, row in df.iterrows():
        if len(observations[0]) == 1:
            key = row[observation_names_here[0]]
            if any(part.strip() == 'theme' for part in row['Theta Role'].split('/')):
                if key in colors.keys():
                    color_here = colors[key]
                    # Plotting rectangular blocks for the second set with y = 1
                    rect = plt.Rectangle((x_pos, 1), 1, 1, color=color_here, edgecolor=color_here, linewidth=0)
                    ax.add_patch(rect)

        if len(observations[0]) == 2:
            key_0, key_1 = row[observation_names_here[0]], row[observation_names_here[1]]
            if any(part.strip() == 'theme' for part in row['Theta Role'].split('/')):
                if (key_0, key_1) in colors.keys():
                    color_here = colors[(key_0, key_1)]
                    # Plotting rectangular blocks for the second set with y = 1
                    rect = plt.Rectangle((x_pos, 1), 1, 1, color=color_here, edgecolor=color_here, linewidth=0)
                    ax.add_patch(rect)
        
        # Incrementing x-position for the next block
        x_pos += 1

    x_pos = 0

    for index, row in df.iterrows():
        if len(observations[0]) == 1:
            key = row[observation_names_here[0]]
            if any(part.strip() == 'experiencer' for part in row['Theta Role'].split('/')):
                if key in colors.keys():
                    color_here = colors[key]
                    # Plotting rectangular blocks for the second set with y = 1
                    rect = plt.Rectangle((x_pos, 0), 1, 1, color=color_here, edgecolor=color_here, linewidth=0)
                    ax.add_patch(rect)

        if len(observations[0]) == 2:
            key_0, key_1 = row[observation_names_here[0]], row[observation_names_here[1]]
            if any(part.strip() == 'experiencer' for part in row['Theta Role'].split('/')):
                if (key_0, key_1) in colors.keys():
                    color_here = colors[(key_0, key_1)]
                    # Plotting rectangular blocks for the second set with y = 1
                    rect = plt.Rectangle((x_pos, 0), 1, 1, color=color_here, edgecolor=color_here, linewidth=0)
                    ax.add_patch(rect)
        
        # Incrementing x-position for the next block
        x_pos += 1



    if len(observations[0]) == 1:

        legend_patches = [
            plt.Rectangle((0, 0), 1, 1, color=color, label=f'{r}')
            for r, color in colors.items()
        ]
    
    if len(observations[0]) == 2:

        legend_patches = [
            plt.Rectangle((0, 0), 1, 1, color=color, label=f'{j}, {k}')
            for (j, k), color in colors.items()
        ]
    
    

    ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1))

    # Setting labels and title
    ax.set_xlabel('Order of Appearance')
    # ax.set_title('Apperances of Person Arguments and Their Fulfillment of Thematic Relations')

    # Setting x-axis limits
    ax.set_xlim(0, len(df))

    # Setting y-axis limits
    ax.set_ylim(0, 4)  # Adjust the y-axis limit to accommodate all sets of blocks

    # Removing y-axis ticks and labels
    ax.set_yticks([])
    ax.set_ylabel('')  # Clearing the y-axis label

    # Adjusting the positions of text labels for each linear formation
    ax.text(-1.8, 3.5, 'Appearance', fontsize=10, ha='center', va='center')
    ax.text(-1.8, 2.5, 'Fulfillment of\n"agent"', fontsize=10, ha='center', va='center')
    ax.text(-1.8, 1.5, 'Fulfillment of\n"theme"', fontsize=10, ha='center', va='center')
    ax.text(-1.8, 0.5, 'Fulfillment of\n"experiencer"', fontsize=10, ha='center', va='center')

    plt.scatter(10, -1, marker='^', color='black', label='Triangle Marker')

    # Displaying the plot
    plt.show()
