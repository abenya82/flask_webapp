import matplotlib.pyplot as plt
import itertools

def get_list_of_values(query_result):
    list_of_values = []
    
    for i in range(len(query_result)):
        list_of_values.append(query_result[i][0])
    return list_of_values


def get_pie_chart_of_frequencies(column,year,engine,filename='pie_chart1.png',show=False):
    '''
    Takes frequencies of first column over given year

    returns: filename of pie chart
    '''
    
    #if filename == 'pie_chart1.png':
    #    filename = str(column) + '_' + str(year)+'_'+filename

    query_str = 'SELECT DISTINCT `' + str(column) + '` FROM mastertwo;'
    res = engine.execute(query_str).fetchall()

    x_labels = get_list_of_values(res)
    x_labels

    list_yearly_frequencies = []
    for i in range(len(x_labels)):
        sum_sales_query = 'SELECT COUNT(`' + str(column) + '`) FROM mastertwo WHERE `' +str(column)+'`= \'' + str(x_labels[i])+ '\' AND Year='+str(year)
        res = engine.execute(sum_sales_query).fetchall()
        #print(res[0][0])
        list_yearly_frequencies.append(res[0][0])
    list_yearly_frequencies

    fig1, ax1 = plt.subplots()
    fig1.set_facecolor('gray')
    
    ax1.pie(list_yearly_frequencies,labels=x_labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    
    ax1.set_title(str(year)+' '+str(column) + ' Frequencies')
    #plt.savefig(filename)
    # for flask app only
    filepath = 'static' + '\pie_chart1.png'
    plt.savefig(filepath)
    if show: plt.show()
    plt.cla()
    return filename



def get_2D_freq_stacked_bar(column1,column2,engine,filename='freqBarChart.png',show=False):
    data_dict = {}
    column1 = str(column1)
    column2 = str(column2)

    query_str = 'SELECT DISTINCT `' + str(column1) + '` FROM mastertwo;'
    res = engine.execute(query_str).fetchall()

    column1_labels = get_list_of_values(res)

    query_str = 'SELECT DISTINCT `' + str(column2) + '` FROM mastertwo;'
    res = engine.execute(query_str).fetchall()

    column2_labels = get_list_of_values(res)

    #print(column1_labels)
    #print(column2_labels)

    for year in [2011,2012,2013,2014]:

        for i in range(len(column1_labels)):
            for j in range(len(column2_labels)):
        

                query = 'SELECT COUNT(`' + str(column1) + '`) FROM mastertwo WHERE `' +str(column2)+'`= \'' + str(column2_labels[j])+ '\' AND `' +str(column1)+'`= \'' + str(column1_labels[i])+ '\' AND Year='+str(year)
                #print(query)
                res = engine.execute(query).fetchall()
                #print(res[0][0])
                data_dict[ str(column1_labels[i]) + ' ' + str(column2_labels[j]) +' '+ str(year)] = res[0][0]




    lst=[]
    list_2011_2014 = []
    used=[]
    x_labels = []
    fig = plt.figure(figsize=(10,6))
    for year in [2011,2012,2013,2014]:
            for i in range(len(column1_labels)):            
                x_labels.append(str(column1_labels[i]) + ' ' + str(year))

    for j in range(len(column2_labels)):
        lst=[]
        for year in [2011,2012,2013,2014]:
            for i in range(len(column1_labels)):
                lst.append(data_dict[str(column1_labels[i]) + ' ' + str(column2_labels[j]) +' '+ str(year)])
        list_2011_2014.append(lst)

    #print(lst)
    #print(list_2011_2014)
    #print(x_labels)

    bottom = [0]*len(x_labels)
    width= 0.5 + len(x_labels)/150

    years = [2011,2012,2013,2014]
    used=[]
    for i in range(len(list_2011_2014)):
        try:
            plt.bar(x_labels,list_2011_2014[i],width=width,bottom=bottom,label=str(column2_labels[i]))
        except:
            pass
        used.append(list_2011_2014[i])
        bottom = [sum(x) for x in zip(*used)]
    #plt.set_xticklabels(x_labels, rotation = 45, ha="right")
    plt.xticks(rotation = 45, label=x_labels,ha='right') # Rotates X-Axis Ticks by 45-degrees
    #plt.ylabel(str(column2))
    plt.xlabel(str(column1)+ ' & ' + 'YEAR')
    plt.ylabel('# of Orders')
    plt.title(str(column1) +' v ' +str(column2) +' Frequencies')
    plt.legend()
    fig.subplots_adjust(bottom=0.4)
    filepath = 'static' + '\\freqBarChart1.png'
    plt.savefig(filepath)
    if show: plt.show()
    plt.cla()
    return(filepath)










def get_2D_sum_stacked_bar_graph(column1,column2,engine,filename='twoDstackedBar.png',show=False):

    '''
    makes stacked bar graph of SUM of first column v. distinct elements in column2
    seperated by year
    
    '''
    


    sales_sum_dict={}

    #want bar graph each column2-value, height is total sales, each stack is yearly sales
    query_str = 'SELECT DISTINCT `' + str(column2) + '` FROM mastertwo;'
    res = engine.execute(query_str).fetchall()

    x_labels = get_list_of_values(res)

    for i in range(len(x_labels)):

        for year in [2011,2012,2013,2014]:

            sum_sales_query = 'SELECT SUM(`' + str(column1) + '`) FROM mastertwo WHERE `' +str(column2)+'`= \'' + str(x_labels[i])+ '\' AND Year='+str(year)
            try:
                res = engine.execute(sum_sales_query).fetchall()
            except:
                return 'Bad Query'
            #print(res[0][0])
            sales_sum_dict[str(x_labels[i]) + ' ' + str(year)] = res[0][0]


    list_of_lists_of_annual_sales = []
    list_annual_sales = []
    for i in range(len(x_labels)):
        for year in [2011,2012,2013,2014]:
            res = sales_sum_dict[str(x_labels[i]) + ' ' + str(year)]
            list_annual_sales.append(res)
        list_of_lists_of_annual_sales.append(list_annual_sales)
        list_annual_sales = []

    #list_of_lists_of_annual_sales
    list_of_lists_of_annual_sales_transpose = list(map(list, itertools.zip_longest(*list_of_lists_of_annual_sales, fillvalue=None)))

    width = 0.35       # the width of the bars: can also be len(x) sequence
    ylabel= str(column1)
    title = str(column1) + ' v ' + str(column2)
    filename = 'bar_stacked_2d.png'
    used = []
    bottom = [0] * len(x_labels)
    year = 2011

    for i in range(4):
    #print(xlabels,quantities_of_values[i])
    #print(bottom,list_of_values[i])
        plt.bar(x_labels, list_of_lists_of_annual_sales_transpose[i], width,bottom=bottom,label=year)
        used.append(list_of_lists_of_annual_sales_transpose[i])
        bottom = [sum(x) for x in zip(*used)]
        year +=1
        #print(bottom)
        #ax.bar(xlabels, men_means, width, label='Men')
        #ax.bar(xlabels, women_means, width, bottom=men_means, label='Women')
        #print(i)
    plt.xticks(rotation = 45,ha='right') # Rotates X-Axis Ticks by 45-degrees
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.subplots_adjust(bottom=0.4)

    filepath = 'static' + '\chart1.png'
    plt.savefig(filepath)
    if show: plt.show()
    plt.cla()







    return filepath


def get_list_product_names(engine,list_length=10):
    '''
    if list_length is 0, ALL products are returned
    '''
    product_names=[]
    if list_length==0:
        query = 'SELECT DISTINCT `Product Name` FROM productDimension ORDER BY `Product Name` ASC'
    else:
        query = 'SELECT `Product Name`, COUNT(*) FROM productDimension Group By `Product Name` Order By COUNT(*) DESC LIMIT '+str(list_length)
    res = engine.execute(query).fetchall()
    for item in res:
        product_names.append(item[0])
    return product_names


def get_list_product_names_values(engine,list_length=5):
    '''
    if list_length is 0, ALL products are returned
    '''
    product_names=[]
    product_counts=[]
    if list_length==0:
        query = 'SELECT `Product Name`, COUNT(*) FROM productDimension Group By `Product Name` Order By COUNT(*)'
    else:
        query = 'SELECT `Product Name`, COUNT(*) FROM productDimension Group By `Product Name` Order By COUNT(*) DESC LIMIT '+str(list_length)
    res = engine.execute(query).fetchall()
    for item in res:
        product_names.append(item[0])
        product_counts.append(item[1])
    return product_names,product_counts

def get_top_items_count_graph(engine,number_of_items=10,show=False):
    top_values_names,top_values_values = get_list_product_names_values(engine=engine,list_length=number_of_items)
    fig = plt.figure(figsize=(8,6))
    plt.xticks(rotation = 35,ha='right') # Rotates X-Axis Ticks by 45-degrees
    fig.subplots_adjust(bottom=0.5)
    plt.bar(top_values_names,top_values_values)
    if show: plt.show()
    filepath = 'static' + '\\top_count_chart1.png'
    plt.savefig(filepath)
    plt.cla()
    return filepath



def get_top_country_counts_chart(product,engine):
    #query = 'SELECT `Country`, COUNT(*) FROM productDimension WHERE `Product Name`="Acco Index Tab, Clear" Group By `Country` Order By COUNT(*) DESC LIMIT 10'

    query = 'SELECT `Country`, COUNT(*) FROM productDimension WHERE `Product Name`='
    query += '\"'
    query += str(product)
    query += '\"'
    query += 'Group By `Country` Order By COUNT(*) DESC LIMIT 10'
    #query = 'SELECT COUNT(*) FROM productDimension WHERE `Product Name`=' +'"'+str(product)+'"'
    print(query)
    res = engine.execute(query).fetchall()
    res

    top_country_list = []
    top_country_values = []
    for item in res:
        top_country_list.append(item[0])
        top_country_values.append(item[1])
    #top_country_values,top_country_list


    filepath = 'static' + '\country_prod_chart1.png'
    fig = plt.figure(figsize=(10,6))
    plt.title(product)
    plt.ylabel('# of Transactions') 
    plt.xticks(rotation = 45,ha='right') # Rotates X-Axis Ticks by 45-degrees
    plt.bar(top_country_list,top_country_values)
    plt.savefig(filepath)
    plt.cla()
    return filepath






def get_2D_time_freq_stacked_bar(column1,column2,engine,tablename='timeDimension',filename='freqBarChart.png',show=False):
    data_dict = {}
    column1 = str(column1)
    column2 = str(column2)

    query_str = 'SELECT DISTINCT `' + str(column1) + '` FROM '+str(tablename)
    res = engine.execute(query_str).fetchall()

    column1_labels = get_list_of_values(res)

    query_str = 'SELECT DISTINCT `' + str(column2) + '` FROM '+str(tablename)
    res = engine.execute(query_str).fetchall()

    column2_labels = get_list_of_values(res)

    #print(column1_labels)
    #print(column2_labels)

    for year in [2011,2012,2013,2014]:

        for i in range(len(column1_labels)):
            for j in range(len(column2_labels)):
        

                query = 'SELECT COUNT(`' + str(column1) + '`) FROM mastertwo WHERE `' +str(column2)+'`= \'' + str(column2_labels[j])+ '\' AND `' +str(column1)+'`= \'' + str(column1_labels[i])+ '\' AND Year='+str(year)
                #print(query)
                res = engine.execute(query).fetchall()
                #print(res[0][0])
                data_dict[ str(column1_labels[i]) + ' ' + str(column2_labels[j]) +' '+ str(year)] = res[0][0]




    lst=[]
    list_2011_2014 = []
    used=[]
    x_labels = []
    fig = plt.figure(figsize=(10,6))
    for year in [2011,2012,2013,2014]:
            for i in range(len(column1_labels)):            
                x_labels.append(str(column1_labels[i]) + ' ' + str(year))

    for j in range(len(column2_labels)):
        lst=[]
        for year in [2011,2012,2013,2014]:
            for i in range(len(column1_labels)):
                lst.append(data_dict[str(column1_labels[i]) + ' ' + str(column2_labels[j]) +' '+ str(year)])
        list_2011_2014.append(lst)

    #print(lst)
    #print(list_2011_2014)
    #print(x_labels)

    bottom = [0]*len(x_labels)
    width= 0.5 + len(x_labels)/150

    years = [2011,2012,2013,2014]
    used=[]
    for i in range(len(list_2011_2014)):
        try:
            plt.bar(x_labels,list_2011_2014[i],width=width,bottom=bottom,label=str(column2_labels[i]))
        except:
            pass
        used.append(list_2011_2014[i])
        bottom = [sum(x) for x in zip(*used)]
    #plt.set_xticklabels(x_labels, rotation = 45, ha="right")
    plt.xticks(rotation = 45, label=x_labels,ha='right') # Rotates X-Axis Ticks by 45-degrees
    #plt.ylabel(str(column2))
    plt.xlabel(str(column1)+ ' & ' + 'YEAR')
    plt.ylabel('# of Orders')
    plt.title(str(column1) +' v ' +str(column2) +' Frequencies')
    plt.legend()
    fig.subplots_adjust(bottom=0.4)
    filepath = 'static' + '\\freqBarChart1.png'
    plt.savefig(filepath)
    if show: plt.show()
    plt.cla()
    return(filepath)




def get_time_freq_bar_chart_all(time_selection,column,engine,filename='time_chart2.png'):

    time_selection = str(time_selection)
    column = str(column)
    year = 2001



    column_values = []
    time_selection_values=[]
    query_str = 'SELECT DISTINCT `' + str(column) + '` FROM timeDimension;'
    res = engine.execute(query_str).fetchall()
    for item in res:
        column_values.append(item[0])

    query_str = 'SELECT DISTINCT `' + str(time_selection) + '` FROM timeDimension ORDER BY `' +str(time_selection) + '` ASC'
    res = engine.execute(query_str).fetchall()
    for item in res:
        time_selection_values.append(item[0])
    #print(column_values,time_selection_values)   


    column1=time_selection
    column2=column
    column1_labels=time_selection_values
    column2_labels=column_values
    data_dict = {}

    for i in range(len(column1_labels)):
        for j in range(len(column2_labels)):
            

            query = 'SELECT COUNT(`' + str(column1) + '`) '
            query += 'FROM timeDimension WHERE `' +str(column2)+'`= \'' + str(column2_labels[j])+ '\' AND `' +str(column1)+'`= \'' + str(column1_labels[i])+'\''
            #print(query)
        
            #print(query)
            res = engine.execute(query).fetchall()
            #print(res[0][0])
            data_dict[ str(column1_labels[i]) + ' ' + str(column2_labels[j])] = res[0][0]


    #print(data_dict)


    lst=[]
    list_2011_2014 = []
    list_of_lst = []
    used=[]
    x_labels = column2_labels
    #print(x_labels)
    for i in range(len(column1_labels)):
        lst=[]
        for j in range(len(column2_labels)):
            lst.append(data_dict[str(column1_labels[i]) + ' ' +str(column2_labels[j])])
        list_of_lst.append(lst)
        
        #print(lst)

    #list_of_lst




    list_of_lists_transpose = list(map(list, itertools.zip_longest(*list_of_lst, fillvalue=None)))



    bottom = [0] * len(list_of_lists_transpose[0])
    used=[]
    fig = plt.figure(figsize=(10,6))

    for i in range(len(column2_labels)):
        plt.bar(column1_labels,list_of_lists_transpose[i],bottom=bottom,label=str(column2_labels[i]))
        used.append(list_of_lists_transpose[i])
        bottom = [sum(x) for x in zip(*used)]

    plt.xlabel(str(column1))
    plt.ylabel('# of Orders')
    plt.title(str(column1) +' v ' +str(column2) +' Frequencies, ALL TIME')
    plt.legend()
    fig.subplots_adjust(bottom=0.4)
    filepath = 'static' + '\\' + filename
    plt.savefig(filepath)
    return filepath

        





