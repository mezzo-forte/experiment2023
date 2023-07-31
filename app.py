from flask import Flask, render_template, session, request, redirect, url_for
from dotenv import load_dotenv
import os
import files_folders as paths
import settings
import json
import random
import string
from itertools import chain
import tools 


def id_generator():
    return "".join([random.choice(string.ascii_letters
            + string.digits) for n in range(10)])



def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_if_not_exists(path, default_content):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(json.dumps(default_content))

def group_assigner(group_counter, current_group_number, group_size):
    if group_counter == 0:
        group_counter = 1
        current_group_number = 1

    elif group_counter < group_size:
        group_counter += 1

    elif group_counter == group_size:
        group_counter = 1
        current_group_number += 1
    # returns a tuple
    return group_counter, current_group_number


# ======================================================================================================

app = Flask(__name__)
load_dotenv()
app.secret_key=os.getenv('TOKEN')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route("/")
def home():
    # checking and creating subject id, setting cookie 
    if 'Subject' not in session:
        session['Subject'] = id_generator()
        
        path_subject_file=os.path.join(paths.path_subjects_folder, f'{session["Subject"]}.json') 
        tools.save_data(path_subject_file, {'Subject':session['Subject']})
    return render_template('index.html')


@app.route('/description')
def description():
    return render_template('description.html')
 

@app.route('/model')
def model_assigner():
        # assigning the model based on group size 
    if 'Last_task' not in session:
        session['Last_task']=""
    if 'Income1' not in session:
        session['Income1']={'Total_earned_income':0, 'Earned_income':0, 'Total_gross_income':0, 'Gross_income':0, 'Total_net_income':0, 'Total_taxable_income':0, 'Total_tax_amount':0}
    if 'Income2' not in session:
        session['Income2']={'Total_earned_income':0, 'Earned_income':0, 'Total_gross_income':0, 'Gross_income':0, 'Total_net_income':0, 'Total_taxable_income':0, 'Total_tax_amount':0}
    if 'Total_income' not in session:
        session['Total_income']={'Total_earned_income':0, 'Total_gross_income':0, 'Total_taxable_income':0, 'Total_net_income':0, 'Total_tax_amount':0}    
    if 'Correct' not in session:
        session['Correct']= ""
    if 'Model' not in session:
        loaded_info=tools.load_data(paths.path_info)
        group_number = 0 if 'Group_number' not in loaded_info else loaded_info['Group_number']         
        current_group_number = 0 if 'Current_group_number' not in loaded_info else loaded_info['Current_group_number']        
        group_number, current_group_number = group_assigner(group_number, current_group_number, settings.group_size)
        loaded_info['Group_number']=group_number
        loaded_info['Current_group_number']=current_group_number
        tools.save_data(paths.path_info, loaded_info)
        session['Group_number_for_model']=current_group_number
    # for separated sessions use this with a proper model name:
        # session['Model'] = ""
        if (session['Group_number_for_model'] + 2) % 3 == 0:
            session['Model']="UBI"
        elif (session['Group_number_for_model']+ 1) % 3 == 0:
            session['Model']="WS"
        else: 
            session['Model']="UBIWS"    
        print (f"Model assigned:{session['Model']}")
    else:
        print (f"Model set already:{session['Model']}")
    return render_template('model.html', \
    model=session['Model'], \
    group_size = settings.group_size, \
    wage_high=settings.wage_high, \
    wage_low=settings.wage_low, \
    flat_tax_rate=settings.flat_tax_rate, \
    cutoff_income_low=settings.cutoff_income_low, \
    subsidy_rate_WS=settings.subsidy_rate_WS, \
    number_of_questions_per_stage=settings.number_of_questions_per_stage, \
    amount_UBIWS=settings.amount_UBIWS, \
    subsidy_rate_UBIWS=settings.subsidy_rate_UBIWS, \
    amount_UBI=settings.amount_UBI)

@app.route('/choice', methods=['POST', 'GET'])
def work_choice():
    if request.method=="GET":
        path_subject_file=os.path.join(paths.path_subjects_folder, f'{session["Subject"]}.json')
        subject_dict = tools.load_data(path_subject_file)
        if 'Active_part' not in session:
            session['Active_part'] = 1
            session['Task_id'] = 0
            subject_dict['Task_id'] = 0
        # session['Task_id'] = 0
        subject_dict.update(session)
        tools.save_data(path_subject_file, subject_dict)  
        return render_template ('choice.html', \
        wage_high=settings.wage_high, \
        wage_low=settings.wage_low, \
        task_id=session['Task_id'], \
        active_part = session['Active_part'], \
        last_task = session['Last_task'], \
        correctness = session['Correct'], \
        amount_UBI=settings.amount_UBI, \
        amount_UBIWS=settings.amount_UBIWS, \
        subsidy_rate_WS = settings.subsidy_rate_WS, \
        subsidy_rate_UBIWS = settings.subsidy_rate_UBIWS, \
        flat_tax_rate = settings.flat_tax_rate, \
        progressive_tax_rate_high = settings.progressive_tax_rate_high, \
        progressive_tax_rate_low = settings.progressive_tax_rate_low, \
        model = session['Model'], \
        cutoff_income_high = settings.cutoff_income_high, \
        cutoff_income_low = settings.cutoff_income_low, \
        total_net_income = session[f'Income{session["Active_part"]}']["Total_net_income"], \
        total_tax_amount = session[f'Income{session["Active_part"]}']["Total_tax_amount"], \
        total_taxable_income = session[f'Income{session["Active_part"]}']["Total_taxable_income"], \
        total_gross_income = session[f'Income{session["Active_part"]}']["Total_gross_income"], \
        # total_earned_income = session[f'Income{session["Active_part"]}']["Total_earned_income"], \
        earned_income = session[f'Income{session["Active_part"]}']["Earned_income"])

    elif request.method=='POST':
        if 'Task_loaded' not in session:
            session['Task_loaded'] = next((name for name in settings.button_names if name in request.form), None)
            # session['Task_loaded']=request.form.get('name')
            session_key = f'{session["Task_loaded"]}_part{session["Active_part"]}'
            session[session_key] = session.get(session_key, 0) + 1
        # session.pop('Task_loaded')    
        
        return redirect (f'/{session["Task_loaded"]}'.lower())
     

@app.route('/complex', methods=['POST', 'GET'])
def complex_paid():
    if request.method =='GET':
        
        current_work_units = session['Task_id'] + 1 
        total_work_units = settings.number_of_questions_per_stage 
        if 'Task_loaded' in session:
            if session['Task_loaded'] == 'Complex':
                task_content = settings.complex_content1 if session['Active_part'] == 1 else settings.complex_content2
            else: 
                return redirect(f'/{session["Task_loaded"].lower()}')
        else: 
            return redirect('/choice')

        return render_template('complex.html', \
        task_id=session['Task_id'], \
        current_work_units=current_work_units, \
        total_work_units=total_work_units, \
        task_content = task_content[session['Task_id']])

    elif request.method=='POST' and 'Task_loaded' in session:
        if session ['Task_loaded'] == 'Complex':

            session[f'Complex_part_{session["Active_part"]}_{session["Task_id"]}']=request.form['answer_given']
        else:
            return redirect('/choice')  
    
        return redirect(url_for('check', task_id=session['Task_id']))  

@app.route('/simple', methods=['POST', 'GET'])
def simple_paid():
    if request.method =='GET':
        current_work_units = session['Task_id'] + 1 
        total_work_units = settings.number_of_questions_per_stage 
        if 'Task_loaded' in session:
            if session['Task_loaded'] == 'Simple':
                task_content = settings.simple_content1 if session['Active_part'] == 1 else settings.simple_content2
            else: 
                return redirect(f'/{session["Task_loaded"].lower()}')
        else: 
            return redirect('/choice')

        return render_template('simple.html', \
        task_id=session['Task_id'], \
        current_work_units=current_work_units, \
        total_work_units=total_work_units, \
        task_content = task_content[session['Task_id']])

    elif request.method=='POST' and 'Task_loaded' in session:
        if session ['Task_loaded'] == 'Simple':
            session[f'Simple_part_{session["Active_part"]}_{session["Task_id"]}']=request.form['answer_given']
        else:
            return redirect('/choice')  
    
        return redirect(url_for('check', task_id=session['Task_id']))

@app.route('/unpaid', methods=['POST', 'GET'])
def unpaid():
    if request.method =='GET':
        current_work_units = session['Task_id'] + 1 
        total_work_units = settings.number_of_questions_per_stage 
        if 'Task_loaded' in session:

            task1 = settings.unpaid_assignment[session['Task_id']][0]
            task2 = settings.unpaid_assignment[session['Task_id']][1]
                        
            task1_text = tools.load_data(paths.path_unpaid1)[str(task1)] if session['Active_part']==1 else tools.load_data(paths.path_unpaid2)[str(task1)]
            
            task2_text = tools.load_data(paths.path_unpaid1)[str(task2)] if session['Active_part']==1 else tools.load_data(paths.path_unpaid2)[str(task2)]

        return render_template('unpaid.html', \
        task_id=session['Task_id'], \
        current_work_units=current_work_units, \
        total_work_units=total_work_units, \
        task1 = int(session['Task_id']),
        task2 = int(session['Task_id'])+1,
        task1_text=task1_text, \
        task2_text=task2_text, )

    elif request.method=='POST' and 'Task_loaded' in session:
        session[f'Unpaid_part_{session["Active_part"]}_{session["Task_id"]}']=request.form['unpaid_choice']
        return redirect(url_for('check', task_id=session['Task_id']))  


@app.route('/nowork', methods=['POST', 'GET'])
def nowork():
    if request.method=='GET':
        current_work_units = session['Task_id'] + 1 
        print(session['Task_id']) 
        total_work_units = settings.number_of_questions_per_stage 
        # if 'Task_loaded' in session:
        #     current_work_units += 1 
         
        return render_template('nowork.html', \
        task_id=session['Task_id'] if session["Active_part"] == 1 else session["Task_id"] + settings.number_of_questions_per_stage, \
        current_work_units=current_work_units, \
        total_work_units=total_work_units) 

    elif request.method=='POST' and 'Task_loaded' in session:
        session[f'Nowork_part_{session["Active_part"]}_{session["Task_id"]}'] = 1
        return redirect(url_for('check', task_id=session['Task_id']))


@app.route('/check/<int:task_id>')
def check(task_id):
    if 'Task_loaded' in session:
        session['Last_task']=session['Task_loaded']
        if session['Task_loaded'] == 'Complex':
            correct_answer = settings.complex_answers1[task_id] if session['Active_part'] == 1 else settings.complex_answers2[task_id]
            
            if int(session[f'Complex_part_{session["Active_part"]}_{task_id}']) == correct_answer:
                
                session[f'Income{session["Active_part"]}']['Earned_income'] = settings.wage_high
                session['Correct']="Correct!" 
            
            else:
                session[f'Income{session["Active_part"]}']["Earned_income"] = int(settings.wage_high / 2)
                session['Correct']="Incorrect!"            # correct_answer = settings.
         
        # Income calculations
            # session[f'Income{session["Active_part"]}'] = 0

        elif session['Task_loaded'] == 'Simple':
            correct_answer = settings.simple_answers1[task_id] if session['Active_part'] == 1 else settings.simple_answers2[task_id]
            if int(session[f'Simple_part_{session["Active_part"]}_{task_id}']) == correct_answer:
                session[f'Income{session["Active_part"]}']['Earned_income'] = settings.wage_low
                session['Correct']="Correct!" 
            else:
                session[f'Income{session["Active_part"]}']['Earned_income'] = settings.wage_low / 2
                session['Correct']="Incorrect!"
            
        elif session['Task_loaded'] == 'Unpaid' or 'Nowork':
            session[f'Income{session["Active_part"]}']['Earned_income'] = 0

        else: 
            try: 
                raise ValueError('Error 11. Unknown Task type')
            except ValueError as err:
                return f"{str(err)}"

    # Income calculation and totals
    # Earned income and totals
        session[f'Income{session["Active_part"]}']['Total_earned_income'] += session[f'Income{session["Active_part"]}']['Earned_income']
    # Gross income and totals
        session[f'Income{session["Active_part"]}']['Gross_income'] = tools.calculate_gross_income(session[f'Income{session["Active_part"]}']['Earned_income'], session['Model'])
        session[f'Income{session["Active_part"]}']['Total_gross_income'] += session[f'Income{session["Active_part"]}']['Gross_income']
    # Taxable income
        session[f'Income{session["Active_part"]}']['Total_taxable_income'] = tools.calculate_taxable_income(session[f'Income{session["Active_part"]}']['Total_earned_income'], session['Model'])
        # session[f'Income{session["Active_part"]}']['Total_taxable_income'] += session[f'Income{session["Active_part"]}']['Taxable_income']
    #Tax amount
        session[f'Income{session["Active_part"]}']['Total_tax_amount'] = tools.calculate_tax_amount(session[f'Income{session["Active_part"]}']['Total_taxable_income'], session['Model'], session['Active_part'])
    # Net income
        session[f'Income{session["Active_part"]}']['Total_net_income'] = session[f'Income{session["Active_part"]}']['Total_gross_income'] - session[f'Income{session["Active_part"]}']['Total_tax_amount']
        # session[f'Income{session["Active_part"]}']['Total_net_income'] = tools.calculate_net_income(session[f'Income{session["Active_part"]}']['Total_taxable_income'], session['Model'], session['Active_part']) 
    # Amount of subsidy

        print(task_id)
        if task_id < settings.number_of_questions_per_stage-1:
            session['Task_id']+= 1
            session.pop('Task_loaded')
            return redirect ('/choice') 

        elif session['Active_part']==1:
            session['Task_id']=0
            session.pop('Task_loaded')
            session['Active_part']=2
            return redirect('/preliminary')

        elif session['Active_part']==2:
            session['Task_id']=0
            session.pop('Task_loaded')
            session['Active_part']=0

            # total incomes
        session['Total_income']["Total_net_income"] = session['Income1']["Total_net_income"] + session['Income2']["Total_net_income"]
        session['Total_income']["Total_gross_income"] = session['Income1']["Total_gross_income"] + session['Income2']["Total_gross_income"]
        session['Total_income']["Total_earned_income"] = session['Income1']["Total_earned_income"] + session['Income2']["Total_earned_income"]
        session['Total_income']["Total_taxable_income"] = session['Income1']["Total_taxable_income"] + session['Income2']["Total_taxable_income"]
        session['Total_income']["Total_tax_amount"] = session['Income1']["Total_tax_amount"] + session['Income2']["Total_tax_amount"]

        # session.pop('Active_part')
        return redirect('/final')            
      

@app.route('/preliminary')
def preliminary_results():
    session['Income1']["Total_subsidy_amount"] = tools.calculate_subsidy_amount(session['Model'], session['Income1']["Total_earned_income"])
    session['Income1']["Total_transfer_amount"] = tools.calculate_transfer_amount(session['Model'], session['Income1']["Total_earned_income"])    
    path_subject_file=os.path.join(paths.path_subjects_folder, f'{session["Subject"]}.json')
    subject_dict = tools.load_data(path_subject_file)
    subject_dict.update(session)
    tools.save_data(path_subject_file, subject_dict)    
    return render_template('preliminary.html', \
    model = session['Model'], \
    total_net_income1 = session['Income1']['Total_net_income'], \
    total_subsidy_amount1 = session['Income1']["Total_subsidy_amount"], \
    total_transfer_amount1 = session['Income1']["Total_transfer_amount"], \
    total_tax_amount1 = session['Income1']["Total_tax_amount"], \
    total_gross_income1 = session['Income1']["Total_gross_income"], \
    total_earned_income1 = session['Income1']["Total_earned_income"], \
    earned_income1 = session['Income1']["Earned_income"])



@app.route('/model2')
def progressive_tax():
    return render_template('model2.html', model=session['Model'], \
    group_size = settings.group_size, \
    flat_tax_rate=settings.flat_tax_rate, \
    wage_high=settings.wage_high, \
    wage_low=settings.wage_low, \
    progressive_tax_rate_high=settings.progressive_tax_rate_high,\
    progressive_tax_rate_low=settings.progressive_tax_rate_low, \
    cutoff_income_high=settings.cutoff_income_high, \
    cutoff_income_low=settings.cutoff_income_low, \
    subsidy_rate_WS=settings.subsidy_rate_WS, \
    number_of_questions_per_stage=settings.number_of_questions_per_stage, \
    amount_UBIWS=settings.amount_UBIWS, \
    subsidy_rate_UBIWS=settings.subsidy_rate_UBIWS, \
    amount_UBI=settings.amount_UBI, \
    diff_cutoff_income_high_to_wage_high=settings.diff_cutoff_income_high_to_wage_high)


@app.route('/final')
def final_results():
    session['Income2']["Total_subsidy_amount"] = tools.calculate_subsidy_amount(session['Model'], session['Income2']["Total_earned_income"])
    session['Income2']["Total_transfer_amount"] = tools.calculate_transfer_amount(session['Model'], session['Income2']["Total_earned_income"])
    session['Income1']["Total_subsidy_amount"] = tools.calculate_subsidy_amount(session['Model'], session['Income1']["Total_earned_income"])
    session['Income1']["Total_transfer_amount"] = tools.calculate_transfer_amount(session['Model'], session['Income1']["Total_earned_income"])
    path_subject_file=os.path.join(paths.path_subjects_folder, f'{session["Subject"]}.json')
    subject_dict = tools.load_data(path_subject_file)
    subject_dict.update(session)
    tools.save_data(path_subject_file, subject_dict)
    return render_template('final.html', \
    model= session['Model'], \
    total_net_income2 = session['Income2']['Total_net_income'], \
    total_subsidy_amount2 = session['Income2']["Total_subsidy_amount"], \
    total_transfer_amount2 = session['Income2']["Total_transfer_amount"], \
    total_tax_amount2 = session['Income2']["Total_tax_amount"], \
    total_gross_income2 = session['Income2']["Total_gross_income"], \
    total_earned_income2 = session['Income2']["Total_earned_income"], \
    earned_income2 = session['Income2']["Earned_income"], \
    total_net_income1 = session['Income1']['Total_net_income'], \
    total_subsidy_amount1 = session['Income1']["Total_subsidy_amount"], \
    total_transfer_amount1 = session['Income1']["Total_transfer_amount"], \
    total_tax_amount1 = session['Income1']["Total_tax_amount"], \
    total_gross_income1 = session['Income1']["Total_gross_income"], \
    total_earned_income1 = session['Income1']["Total_earned_income"], \
    earned_income1 = session['Income1']["Earned_income"])
    # total_tax_amount = session['Total_income']["Total_tax_amount"], \
    # total_gross_income = session['Total_income']["Total_gross_income"], \
    # total_taxable_income = session['Total_income']["Total_taxable_income"], \
    # total_subsidy_amount = session['Total_income']["Total_taxable_income"], \
    # total_transfer_amount = session['Total_income']["Total_taxable_income"], \
    # total_earned_income = session['Total_income']["Total_earned_income"])


@app.route('/questionnaire', methods=['POST', 'GET'])
def questionnaire():
    if request.method == 'GET':
        return render_template('questionnaire.html', model=session['Model'])

    elif request.method == 'POST':
        print(request.form)
        session['Questionnaire']=request.form
        print(request.form)
        session['Questionnaire_list']={"":""}
        session['Questionnaire_list']['Q8']=request.form.getlist('Q8')
        session['Questionnaire_list']['Q9']=request.form.getlist('Q9')
        session['Questionnaire_list']['Q10']=request.form.getlist('Q10')
        session['Questionnaire_list']['Q12']=request.form.getlist('Q12')
        session['Questionnaire_list']['Q13']=request.form.getlist('Q13')
        session['Questionnaire_list']['Q15']=request.form.getlist('Q15')
        session['Questionnaire_list']['Q16']=request.form.getlist('Q16')
        session['Questionnaire_list']['Q20']=request.form.getlist('Q20')
        session['Questionnaire_list']['Q22']=request.form.getlist('Q22')
        session['Questionnaire_list']['Q23']=request.form.getlist('Q23')
            # subject_dict['Questionnaire']=session['Questionnaire']
            # save_json(path_subject_file, path_subject_file)
            
        path_subject_file=os.path.join(paths.path_subjects_folder, f'{session["Subject"]}.json')
        subject_dict=tools.load_data(path_subject_file)
            # pathData=os.path.join(path_subjects_folder, f"{session['Subject']}_recovered.json")
        # questionnaireQuestions = list(request.form.keys())
        # questionnaireAnswers = list(request.form.values())
        # questionnaireDict = dict(zip(questionnaireQuestions, questionnaireAnswers))
            
        # questionnaireDict['Q6'] = request.form.getlist('Q6')
        # questionnaireDict['Q8'] = request.form.getlist('Q8')
        # questionnaireDict['Q9'] = request.form.getlist('Q9')
        # questionnaireDict['Q18'] = request.form.getlist('Q18')
        # questionnaireDict['Q20'] = request.form.getlist('Q20')
        # subject_dict = load_data(path_subject_file)
            # dummyDict['Questionnaire_answers']={}
        # subject_dict.update(questionnaireDict)
        subject_dict.update(session)
        tools.save_data(path_subject_file,subject_dict)        
        return redirect('/end')


@app.route('/end')
def end():
    return render_template('end.html')


@app.route('/clear', methods=['POST', 'GET'])
def clear():
    if request.method == "GET":
        return render_template('clear.html')
    elif request.method == "POST":
        session.clear()
       # return redirect('/')    
    return '''session cleared
    <br> 
    <a href="https://2023.socolab.online">https://2023.socolab.online</a>
    
    '''
@app.route('/change', methods=['POST', 'GET'])
def change_model():
    if request.method == "GET":
        return render_template('change.html', model=session['Model'])
    elif request.method == "POST":
        session['Model'] = next((model_name for model_name in settings.button_names if model_name in request.form), None)
       # return redirect('/')    
    return f'''Model changed to {session["Model"]}
        '''


@app.route('/activepart', methods=['POST', 'GET'])
def active_part():
    if request.method == "GET":
        session['Active_part']=1 if session['Active_part']==2 else 2
    return f'Round changed to {session["Active_part"]}' 
    #     return render_template('change.html', model=session['Model'])
    # elif request.method == "POST":
    #     session['Model'] = next((model_name for model_name in settings.button_names if model_name in request.form), None)
    #    # return redirect('/')    
    # return f'''Model changed to {session["Model"]}
    #     '''
@app.route('/settask', methods=['POST', 'GET'])
def task_switcher():
    if request.method=='GET':
        print(session)
        return render_template('set_task_id.html', \
        task_id=session['Task_id'], \
        task1=settings.task_ids[0], \
        task2=settings.task_ids[1], \
        task3=settings.task_ids[2] )
 
    elif request.method=='POST':
        session['Task_id'] = int(request.form['set_task'])-1
        return f'Current task id will be {session["Task_id"]+1}'
  
@app.route('/session')
def show_session():
    print(session)
    # print (type (session[f'Income{session["Active_part"]}']["Earned_income"]))
    return '''hey there'''


if __name__=="__main__":
    # app.config['ENV'] = "development"
    # socketio.run(app, debug=True, host="0.0.0.0")
    app.run(debug=True, host="0.0.0.0")



