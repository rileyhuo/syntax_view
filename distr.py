import pandas as pd
import matplotlib.pyplot as plt

def conditional(df, title, conditions, y, y_measure):
    '''
    Generate conditional distributions of thematic relations based on specified conditions,
    such as "Gender" and "Grammatical Function."
    '''

    mode = 'coarse'

    def find_condition_names(condition):
        condition_dictionary = {
            'Interactional Role': {'Maxine', 'mother', 'father', 'aunt', 'NA'},
            'Phonological Realization': {'pronounced', 'silent'},
            'Gender': {'NA', 'feminine', 'masculine'},
            'Person': {'first', 'second', 'third'},
            'Number': {'singular', 'plural'},
            # 'Case': {'nominative', 'prepositional', 'NA', 'accusative'},
            'Grammatical Function': {'subject', 'indirect object', 'direct object', 'object of preposition'}
        }
        condition_names = []

        for c in condition:
            for key, value in condition_dictionary.items():
                if c in value:
                    condition_names.append(key)

        return(condition_names)
            
    condition_names_here = find_condition_names(conditions[0])
    
    new_dfs= []
    total_counts = []

    if y == 'thematic':
        y_1 = 'Theta Role'
        y_2 = 'Thematic Relation'
    
    if  y == 'person':
        y_1 = y_2 = 'Person'

    for condition in conditions:

        if len(condition_names_here) == 1:
            old_df = df[(df[condition_names_here[0]] == condition[0])][y_1].value_counts().reset_index()
        
        if len(condition_names_here) == 2:
            old_df = df[(df[condition_names_here[0]] == condition[0]) &
                        (df[condition_names_here[1]] == condition[1])][y_1].value_counts().reset_index()
        
        if len(condition_names_here) == 3:
            old_df = df[(df[condition_names_here[0]] == condition[0]) &
                        (df[condition_names_here[1]] == condition[1]) &
                        (df[condition_names_here[2]] == condition[2]) 
                        ][y_1].value_counts().reset_index()

        counts = {}

        for index, row in old_df.iterrows():

            key = row[y_1]
            count = row['count']
            
            if mode == 'coarse':
            # Check if the key contains a "/"
                if '/' in key:
                    parts = key.split('/')
                    for part in parts:
                        counts[part] = counts.get(part , 0) + count
                else:
                    counts[key] = counts.get(key, 0) + count

            if mode == 'mixed':
                if '/' in key:
                    parts = key.split('/')
                    for part in parts:
                        part = '/' + part
                        counts[part] = counts.get(part, 0) + count
                else:
                    counts[key] = counts.get(key, 0) + count

            if mode == 'pure':
                if '/' not in key:
                    counts[key] = counts.get(key, 0) + count

            if mode == None:
                counts[key] = counts.get(key, 0) + count

        new_df = pd.DataFrame(list(counts.items()), columns=[y_2, 'count']).sort_values('count', ascending=False)
        total_count = new_df['count'].sum()
        new_df['frequency'] = new_df['count'] / total_count

        new_dfs.append(new_df)
        total_counts.append(total_count)

    # return new_dfs[2]

    if len(new_dfs) == 1:
        merged_df = new_dfs[0][[y_2, y_measure]].fillna(0).rename(
            columns={f'{y_measure}': f'{conditions[0]}'})

    # frequency df for conditions
    if len(new_dfs) == 2:
        merged_df = pd.merge(new_dfs[0][[y_2, y_measure]], 
                            new_dfs[1][[y_2, y_measure]], 
                            on=y_2, how='outer').fillna(0).rename(
                                columns={f'{y_measure}_x': f'{conditions[0]}', f'{y_measure}_y': f'{conditions[1]}'})

    if len(new_dfs) == 3:
        merged_df_0 = pd.merge(new_dfs[0][[y_2, y_measure]], 
                            new_dfs[1][[y_2, y_measure]], 
                            on=y_2, how='outer').fillna(0).rename(
                                columns={f'{y_measure}_x': f'{conditions[0]}', f'{y_measure}_y': f'{conditions[1]}'})
        merged_df = pd.merge(new_dfs[2][[y_2, y_measure]], 
                            merged_df_0[[y_2, f'{conditions[0]}', f'{conditions[1]}']], 
                            on=y_2, how='outer').fillna(0).rename(
                                columns={f'{y_measure}': f'{conditions[2]}'})
        
    len_merged_df = len(merged_df)

    # if conditional is based on 1 field
    if len(condition_names_here) == 1:

        bar_width = 0.25
        index = range(len_merged_df)
        fig_width = 5.5 + len_merged_df * .5
        plt.figure(figsize=(fig_width, fig_width * .4), dpi=2500/len_merged_df)
        
        # how many bars to plot = how many conditions
        # 1 field meaning the labeling is easy 
        if len(conditions) == 1:
            plt.bar(index, merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + f'\n(n = {total_counts[0]})', color='#ff9100')

        if len(conditions) == 2:
            plt.bar([i - 0.5 * bar_width for i in index], merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + f'\n(n = {total_counts[0]})', color='#30fbff')
            plt.bar([i + 0.5 * bar_width for i in index], merged_df[f'{conditions[1]}'], width=bar_width, label=conditions[1][0] + f'\n(n = {total_counts[1]})', color='#ff307c')

        if len(conditions) == 3:
            plt.bar([i - bar_width for i in index], merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + f'\n(n = {total_counts[0]})', color='#ff307c')
            plt.bar(index, merged_df[f'{conditions[1]}'], width=bar_width, label=conditions[1][0] + f'\n(n = {total_counts[1]})', color='#30fbff')
            plt.bar([i + bar_width for i in index], merged_df[f'{conditions[2]}'], width=bar_width, label=conditions[2][0] + f'\n(n = {total_counts[2]})', color='#ffea26')

        
        plt.xlabel(y_2)
        plt.ylabel(y_measure.capitalize())
        # plt.title(f'{title} P({y_2}|{condition_names_here[0]})')
        plt.xticks(index, merged_df[y_2], rotation=0, ha='center')

        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.show()

    # if conditional is based on 2 fields
    if len(condition_names_here) == 2:

        bar_width = 0.25
        index = range(len_merged_df)
        fig_width = 5.5 + len_merged_df * .5
        plt.figure(figsize=(fig_width, fig_width * .4), dpi=2500/len_merged_df)
        
        if len(conditions) == 1:
            plt.bar(index, merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + ', ' + conditions[0][1] + f'\n(n = {total_counts[0]})', 
                    color='#ff9100')
            
        if len(conditions) == 2:
            plt.bar([i - 0.5 * bar_width for i in index], merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + ', ' + conditions[0][1] + f'\n(n = {total_counts[0]})', 
                    color='#30fbff')
            plt.bar([i + 0.5 * bar_width for i in index], merged_df[f'{conditions[1]}'], width=bar_width, label=conditions[1][0] + ', ' + conditions[1][1] + f'\n(n = {total_counts[1]})', 
                    color='#ff307c')

        if len(conditions) == 3:
            plt.bar([i - bar_width for i in index], merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + ', ' + conditions[0][1] + f'\n(n = {total_counts[0]})', 
                    color='#ff307c')
            plt.bar(index, merged_df[f'{conditions[1]}'], width=bar_width, label=conditions[1][0] + ', ' + conditions[1][1] + f'\n(n = {total_counts[1]})', 
                    color='#30fbff')
            plt.bar([i + bar_width for i in index], merged_df[f'{conditions[2]}'], width=bar_width, label=conditions[2][0] + ', ' + conditions[2][1] + f'\n(n = {total_counts[2]})', 
                    color='#ffea26')

        plt.xlabel(y_2)
        plt.ylabel(y_measure.capitalize())
        # plt.title(f'{title} P({y_2}|{condition_names_here[0]}, {condition_names_here[1]})')
        plt.xticks(index, merged_df[y_2], rotation=0, ha='center')

        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.show()
    
    if len(condition_names_here) == 3:

        bar_width = 0.25
        index = range(len_merged_df)
        fig_width = 3.5 + len_merged_df * .5
        plt.figure(figsize=(fig_width, fig_width * .4), dpi=2500/len_merged_df)
        
        if len(conditions) == 1:
            plt.bar(index, merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + ', ' + conditions[0][1] + ', ' + conditions[0][2] + f'\n(n = {total_counts[0]})', 
                    color='#ff9100')
            
        if len(conditions) == 2:
            plt.bar([i - 0.5 * bar_width for i in index], merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + ', ' + conditions[0][1] + ', ' + conditions[0][2] + f'\n(n = {total_counts[0]})', 
                    color='#30fbff')
            plt.bar([i + 0.5 * bar_width for i in index], merged_df[f'{conditions[1]}'], width=bar_width, label=conditions[1][0] + ', ' + conditions[1][1] + ', ' + conditions[1][2] + f'\n(n = {total_counts[2]})', 
                    color='#ff307c')

        if len(conditions) == 3:
            plt.bar([i - bar_width for i in index], merged_df[f'{conditions[0]}'], width=bar_width, label=conditions[0][0] + ', ' + conditions[0][1] + ', ' + conditions[0][2] + f'\n(n = {total_counts[0]})', 
                    color='#30fbff')
            plt.bar(index, merged_df[f'{conditions[1]}'], width=bar_width, label=conditions[1][0] + ', ' + conditions[1][1] + ', ' + conditions[1][2] + f'\n(n = {total_counts[1]})', 
                    color='#ff307c')
            plt.bar([i + bar_width for i in index], merged_df[f'{conditions[2]}'], width=bar_width, label=conditions[2][0] + ', ' + conditions[2][1] + ', ' + conditions[2][2] + f'\n(n = {total_counts[2]})', 
                    color='#ffea26')
            
        
        plt.xlabel(y_2)
        plt.ylabel(y_measure.capitalize())
        # plt.title(f'{title} P({y_2}|{condition_names_here[0]}, {condition_names_here[1]}, {condition_names_here[2]})')
        plt.xticks(index, merged_df[y_2], rotation=0, ha='center')

        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.show()