import mysql
from mysql.connector import Error
from tkinter import *
from tkinter.ttk import Combobox
from functools import partial
import datetime


def no_free_beds_warning():
    window = Tk()
    window.geometry('400x200')
    window.title("WARNING")
    label = Label(window, text="There are no free beds in this department at the moment.\n"
                               "The patient can't stay.\n"
                               " `Is staying?` automatically assigned to 'No'.\n")
    label.grid(column=0, row=0)
    btn = Button(window, text="Ok", command=window.destroy)
    btn.grid(column=2, row=0)


def get_id(string):
    num = '0'
    for letter in string:
        if letter.isdigit():
            num += letter
        else:
            break
    num = num[1:]
    return int(num)


def success_message():
    window = Tk()
    window.geometry('250x250')
    window.title("Success")
    label = Label(window, text="Operation successful!\n")
    label.grid(column=0, row=0)
    btn = Button(window, text="Ok", command=window.destroy)
    btn.grid(column=2, row=0)


def error_in_data():
    foolproof = Tk()
    foolproof.geometry('250x50')
    foolproof.title("Error")
    fool_lbl = Label(foolproof, text="There's an error in your data!\n Please check your input and try again")
    fool_lbl.grid(column=0, row=0)
    btn = Button(foolproof, text="Ok", command=foolproof.destroy)
    btn.grid(column=2, row=0)


def get_departments(connection):
    try:
        query = """SELECT idDEPARTMENT, `Name of the department` FROM `DEPARTMENT`"""
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            departments = []
            records = cursor.fetchall()
            for val in records:
                departments.append((val[0], val[1]))
    except:
        error_in_data()
    return departments


def get_diagnoses(connection):
    try:
        query = """SELECT idDIAGNOSIS, `Diagnosis name` FROM `DIAGNOSIS`"""
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            diagnoses = []
            records = cursor.fetchall()
            for val in records:
                diagnoses.append((val[0], val[1]))
    except:
        error_in_data()
    return diagnoses


def get_docs(connection):
    try:
        query = """SELECT idDOCTOR, `Full name` FROM `DOCTOR`
        WHERE `Wants to leave` = 0 AND `Ended work` IS NULL"""
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            docs = []
            records = cursor.fetchall()
            for val in records:
                docs.append((val[0], val[1]))
    except:
        error_in_data()
    return docs


def get_patients(connection):
    try:
        query = """SELECT idPATIENT, `Full name` FROM `PATIENT`"""
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            patients = []
            records = cursor.fetchall()
            for val in records:
                patients.append((val[0], val[1]))
    except:
        error_in_data()
    return patients


def get_meds(connection, diag):
    meds = []
    try:
        with connection.cursor(buffered=True) as cursor:
            query_get_diag_id = f"""SELECT idDIAGNOSIS FROM `DIAGNOSIS`
                    WHERE `Diagnosis name` = '{diag}'"""
            cursor.execute(query_get_diag_id)
            ((diag_id,),) = cursor.fetchall()

            query_get_meds_id = f"""SELECT `idMEDICINE` FROM `MEDICINE-DIAGNOSIS`
                    WHERE `idDIAGNOSIS` = {diag_id}"""
            cursor.execute(query_get_meds_id)
            meds_ids = []
            records = cursor.fetchall()
            for val in records:
                print(f"val={val}")
                meds_ids.append(val[0])

            for med_id in meds_ids:
                query_get_med_name = f"""SELECT `Medicine name` FROM `MEDICINE`
                            WHERE `idMEDICINE` = {med_id}"""
                cursor.execute(query_get_med_name)
                ((med,),) = cursor.fetchall()
                meds.append(med)
    except:
        error_in_data()
    return meds


def get_procedures(connection, diag):
    try:
        with connection.cursor(buffered=True) as cursor:
            query_get_diag_id = f"""SELECT idDIAGNOSIS FROM `DIAGNOSIS`
                    WHERE `Diagnosis name` = '{diag}'"""
            cursor.execute(query_get_diag_id)
            ((diag_id,),) = cursor.fetchall()

            query_get_procedure_id = f"""SELECT `idPROCEDURE` FROM `PROCEDURE-DIAGNOSIS`
                    WHERE `idDIAGNOSIS` = {diag_id}"""
            cursor.execute(query_get_procedure_id)
            procedure_ids = []
            records = cursor.fetchall()
            for val in records:
                procedure_ids.append(val[0])

            procedures = []
            for procedure_id in procedure_ids:
                query_get_procedure_name = f"""SELECT `Name of the procedure` FROM `PROCEDURE`
                            WHERE `idPROCEDURE` = {procedure_id}"""
                cursor.execute(query_get_procedure_name)
                ((procedure,),) = cursor.fetchall()
                procedures.append(procedure)
    except:
        error_in_data()
    return procedures


def get_p_diagnoses(connection, p_name):
    try:
        query = f"""SELECT idDIAGNOSIS FROM `PATIENT-DIAGNOSIS`
        WHERE idPATIENT = {get_id(p_name)}
        """
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            id_diagnoses = []
            records = cursor.fetchall()
            for val in records:
                id_diagnoses.append(val)
            diagnoses = []
            for id_d in id_diagnoses:
                print(f"id_d = {id_d[0]}")
                query_get_names = f"""SELECT `Diagnosis name` FROM `DIAGNOSIS`
                WHERE idDIAGNOSIS = {id_d[0]}
                """
                cursor.execute(query_get_names)
                (di,) = cursor.fetchone()
                diagnoses.append(di)
            connection.commit()
    except:
        error_in_data()
    return diagnoses


""" DOCTOR FUNCS """


def add_doc_clicked(conn, doc_info1, doc_info2, doc_info3, dep_box):
    try:
        doc_name = doc_info1.get()
        doc_birth = doc_info2.get()
        doc_position = doc_info3.get()
        doc_dep = dep_box.get()
        query = f"""INSERT INTO `DOCTOR`
        (`Full name`, `idDEPARTMENT`, `Date of birth`, `Position`, `Started work`)
        VALUES ('{doc_name}', {get_id(doc_dep)}, '{doc_birth}', '{doc_position}', '{datetime.date.today()}')
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
    except:
        error_in_data()
    else:
        success_message()


def add_doc_btn(connection):
    window = Tk()
    window.geometry('300x250')
    window.title("Doctor registration")

    doc_info1 = Entry(window, width=15)
    lbl1 = Label(window, text="Doctor's name")
    lbl1.grid(column=0, row=0)
    doc_info1.grid(column=1, row=0)

    doc_info2 = Entry(window, width=15)
    lbl2 = Label(window, text="Date of birth")
    lbl2.grid(column=0, row=1)
    doc_info2.grid(column=1, row=1)

    doc_info3 = Entry(window, width=15)
    lbl3 = Label(window, text="Position")
    lbl3.grid(column=0, row=2)
    doc_info3.grid(column=1, row=2)

    lbl3 = Label(window, text="Department")
    lbl3.grid(column=0, row=3)
    dep_box = Combobox(window)
    dep_box['values'] = get_departments(connection)
    dep_box.grid(column=1, row=3)
    add_doc_clicked_wo_arg = partial(add_doc_clicked, connection, doc_info1, doc_info2, doc_info3, dep_box)
    btn1 = Button(window, text='Add doctor into database', command=add_doc_clicked_wo_arg)
    btn1.grid(column=0, row=4)


def cant_fire_doctor():
    window = Tk()
    window.geometry('250x250')
    window.title("Success")
    label = Label(window, text="You can't fire this doctor because he has\n"
                               "patients to treat\n")
    label.grid(column=0, row=0)
    btn = Button(window, text="Ok", command=window.destroy)
    btn.grid(column=0, row=1)


def fire_doc_clicked(conn, doc):
    doc_id = get_id(doc.get())
    query_has_patients = f"""SELECT `idPATIENT` FROM `PATIENT-DIAGNOSIS`
    WHERE `idDOCTOR` = {doc_id}"""
    patients = []

    try:
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_has_patients)
            records = cursor.fetchall()
            conn.commit()
            for val in records:
                patients.append(val)
                print(val)
        if len(patients) == 0:
            query = f"""UPDATE `DOCTOR`
                SET `Ended work` = '{datetime.date.today()}',
                    `Wants to leave` = 1
                WHERE idDOCTOR = {doc_id}
                """
            with conn.cursor(buffered=True) as cursor:
                cursor.execute(query)
                conn.commit()
        else:
            query_wants_to_leave = f"""UPDATE `DOCTOR`
            SET `Wants to leave` = 1
            WHERE `idDOCTOR` = {doc_id}"""
            with conn.cursor(buffered=True) as cursor:
                cursor.execute(query_wants_to_leave)
                conn.commit()
            cant_fire_doctor()
    except:
        error_in_data()
    else:
        success_message()


def fire_doc_btn(conn):
    window = Tk()
    window.geometry('300x250')
    window.title("Firing doctor")
    doc_box = Combobox(window)
    doc_box['values'] = get_docs(conn)
    doc_box.grid(column=0, row=0)
    fire_doc_clicked_wo_arg = partial(fire_doc_clicked, conn, doc_box)
    btn1 = Button(window, text='Delete doctor from database', command=fire_doc_clicked_wo_arg)
    btn1.grid(column=0, row=1)


""" PATIENT FUNCS """


def free_beds(conn, p_diag):
    try:
        query_get_dep = f"""SELECT idDEPARTMENT FROM `DIAGNOSIS`
        WHERE idDIAGNOSIS = {get_id(p_diag)}
        """
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_dep)
            conn.commit()
            ((dep,),) = cursor.fetchall()
            print(f"dep={dep}")

        query = f"""SELECT `Number of beds` FROM `DEPARTMENT`
        WHERE idDEPARTMENT = {dep}
        """
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query)
            conn.commit()
            ((beds,),) = cursor.fetchall()
    except:
        error_in_data()
    else:
        success_message()
    if beds > 0:
        return True
    else:
        return False


def add_patient_btn_clicked(conn, p_info1, p_info2, p_info3, p_info4, p_info5, p_info6):
    p_name = p_info1.get()
    p_birth = p_info2.get()
    p_cond = p_info3.get()
    p_diag = p_info4.get()
    p_doc = p_info5.get()
    p_stay = p_info6.get()
    if p_stay == 'Yes' and not free_beds(conn, p_diag):
        no_free_beds_warning()
        p_stay = 'No'

    query_is_in_db =f"""SELECT IFNULL((SELECT `idPATIENT` FROM `PATIENT`
    WHERE `Full name` = '{p_name}' AND `Date of birth` = '{p_birth}'), 'null')"""
    with conn.cursor(buffered=True) as cursor:
        cursor.execute(query_is_in_db)
        ((p_in_db,),) = cursor.fetchall()
        conn.commit()

    if p_in_db == 'null':
        query_patient = f"""INSERT INTO `PATIENT`
        (`Full name`, `Date of birth`)
        VALUES ('{p_name}', '{p_birth}')
        """
        with conn.cursor() as cursor:
            cursor.execute(query_patient)
            conn.commit()
    query_get_patient_id = f"""SELECT idPATIENT FROM `PATIENT`
    WHERE `Full name` = '{p_name}'
    """
    with conn.cursor() as cursor:
        cursor.execute(query_get_patient_id)
        ((p_id,),) = cursor.fetchall()
        conn.commit()
    query_patient_doc = f"""INSERT INTO `PATIENT-DIAGNOSIS`
    (`idPATIENT`, `idDIAGNOSIS`, `Start of treatment`, `Is staying`, `idDOCTOR`, `Condition`)
    VALUES ({p_id}, {get_id(p_diag)}, '{datetime.date.today()}', '{p_stay}', {get_id(p_doc)}, '{p_cond}')
    """
    with conn.cursor() as cursor:
        cursor.execute(query_patient_doc)
        conn.commit()
    if p_stay == 'Yes':
        query_get_dep = f"""SELECT `idDEPARTMENT` FROM `DIAGNOSIS`
        WHERE `idDIAGNOSIS` = {get_id(p_diag)}"""
        with conn.cursor() as cursor:
            cursor.execute(query_get_dep)
            ((dep_id,),) = cursor.fetchall()
            conn.commit()
        query_change_beds = f"""UPDATE `DEPARTMENT`
        SET `Number of beds` = `Number of beds` - 1
        WHERE `idDEPARTMENT` = {dep_id}"""
        with conn.cursor() as cursor:
            cursor.execute(query_change_beds)
            conn.commit()



def add_patient_btn(connection):
    window = Tk()
    window.geometry('300x250')
    window.title("Patient registration")

    p_name = Entry(window, width=15)
    lbl1 = Label(window, text="Patient's name")
    lbl1.grid(column=0, row=0)
    p_name.grid(column=1, row=0)

    p_birthday = Entry(window, width=15)
    lbl2 = Label(window, text="Date of birth")
    lbl2.grid(column=0, row=1)
    p_birthday.grid(column=1, row=1)

    lbl3 = Label(window, text="Patient's condition")
    lbl3.grid(column=0, row=2)
    p_condition = Combobox(window)
    p_condition["values"] = ["Sick", "Healthy", "Dead", "Dead due to other reasons"]
    p_condition.grid(column=1, row=2)

    lbl3 = Label(window, text="Is staying?")
    lbl3.grid(column=0, row=3)
    p_staying = Combobox(window)
    p_staying["values"] = ["Yes", "No"]
    p_staying.grid(column=1, row=3)

    lbl4 = Label(window, text="Diagnosis")
    lbl4.grid(column=0, row=4)
    p_diag = Combobox(window)
    p_diag['values'] = get_diagnoses(connection)
    p_diag.grid(column=1, row=4)

    lbl5 = Label(window, text="Doctor")
    lbl5.grid(column=0, row=5)
    p_doc = Combobox(window)
    p_doc['values'] = get_docs(connection)
    p_doc.grid(column=1, row=5)

    add_patient_btn_clicked_wo_arg = partial(add_patient_btn_clicked, connection, p_name, p_birthday,
                                             p_condition, p_diag, p_doc, p_staying)
    btn1 = Button(window, text='Add patient into database', command=add_patient_btn_clicked_wo_arg)
    btn1.grid(column=0, row=6)


def change_meds_btn_clicked(conn, p_box, diag_box, meds_box):
    p_name = p_box.get()
    med = meds_box.get()
    diag = diag_box.get()

    try:
        query_get_med_id = f"""SELECT idMEDICINE FROM `MEDICINE`
        WHERE `Medicine name` = '{med}'"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_med_id)
            ((med_id,),) = cursor.fetchall()
        query_get_diag_id = f"""SELECT idDIAGNOSIS FROM `DIAGNOSIS`
            WHERE `Diagnosis name` = '{diag}'"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_diag_id)
            ((diag_id,),) = cursor.fetchall()

        query_get_dose = f"""SELECT `Dosage` FROM `MEDICINE-DIAGNOSIS`
        WHERE `idMEDICINE` = {med_id} AND `idDIAGNOSIS` = {diag_id}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_dose)
            ((dose,),) = cursor.fetchall()

        query_get_max_dose = f"""SELECT `Max dosage` FROM `MEDICINE`
        WHERE `Medicine name` = '{med}'"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_max_dose)
            ((max_dose,),) = cursor.fetchall()

        query_get_total_dose = f"""SELECT COUNT(*) FROM `PATIENT-MEDICINE`
        WHERE `idPATIENT` = {get_id(p_name)} AND `idMEDICINE` = {med_id}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_total_dose)
            ((total_dose,),) = cursor.fetchall()
            if total_dose > 0:
                query_get_total_dose = f"""SELECT `Total dose` FROM `PATIENT-MEDICINE`
                    WHERE `idPATIENT` = {get_id(p_name)} AND `idMEDICINE` = {med_id}"""
                cursor.execute(query_get_total_dose)
                ((total_dose,),) = cursor.fetchall()
            else:
                total_dose = 0

        total_dose += dose
        if total_dose > max_dose:
            total_dose = max_dose

        query_count = f"""SELECT COUNT(*) FROM `PATIENT-MEDICINE` WHERE `idPATIENT` = {get_id(p_name)} AND `idMEDICINE` = {med_id}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_count)
            ((exists,),) = cursor.fetchall()

        if exists > 0:
            query = f"""UPDATE `PATIENT-MEDICINE`
            SET `Total dose` = {total_dose}
            WHERE `idPATIENT` = {get_id(p_name)} AND `idMEDICINE` = {med_id}"""
        else:
            query = f"""INSERT INTO `PATIENT-MEDICINE` (idPATIENT, idMEDICINE, `Total dose`)
            VALUES ({get_id(p_name)}, {med_id}, {total_dose})
            """
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query)
            conn.commit()

        query_date_change = f"""UPDATE `PATIENT`
        SET `Treatment changed` = '{datetime.date.today()}'
        WHERE `idPATIENT` = {get_id(p_name)}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_date_change)
            conn.commit()
    except:
        error_in_data()
    else:
        success_message()


def change_meds_btn(conn, p_box, diag_box):
    p_diag = diag_box.get()
    window = Tk()
    window.geometry('300x250')
    window.title("Patient's treatment")

    lbl1 = Label(window, text="Meds")
    lbl1.grid(column=0, row=0)
    meds = Combobox(window)
    meds["values"] = get_meds(conn, p_diag)
    meds.grid(column=1, row=0)

    change_meds_btn_clicked_wo_arg = partial(change_meds_btn_clicked, conn, p_box, diag_box, meds)
    btn1 = Button(window, text='Change meds', command=change_meds_btn_clicked_wo_arg)
    btn1.grid(column=0, row=1)


def change_procedures_btn_clicked(conn, p_box, diag_box, procedures_box):
    p_name = p_box.get()
    procedure = procedures_box.get()
    procedure_id = get_id(procedure)
    diag = diag_box.get()

    try:
        query_get_diag_id = f"""SELECT idDIAGNOSIS FROM `DIAGNOSIS`
                WHERE `Diagnosis name` = '{diag}'"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_diag_id)
            ((diag_id,),) = cursor.fetchall()

        query_get_dose = f"""SELECT `How many a day` FROM `PROCEDURE-DIAGNOSIS`
            WHERE `idPROCEDURE` = {procedure_id} AND `idDIAGNOSIS` = {diag_id}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_dose)
            ((dose,),) = cursor.fetchall()

        query_get_total_amount = f"""SELECT COUNT(*) FROM `PATIENT-PROCEDURE`
            WHERE `idPATIENT` = {get_id(p_name)} AND `idPROCEDURE` = {procedure_id}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_get_total_amount)
            ((total_dose,),) = cursor.fetchall()
            if total_dose > 0:
                query_get_total_amount = f"""SELECT `How many a day` FROM `PATIENT-PROCEDURE`
                        WHERE `idPATIENT` = {get_id(p_name)} AND `idPROCEDURE` = {procedure_id}"""
                cursor.execute(query_get_total_amount)
                ((total_dose,),) = cursor.fetchall()
            else:
                total_dose = 0

        total_dose += dose
        query_count = f"""SELECT COUNT(*) FROM `PATIENT-PROCEDURE` WHERE `idPATIENT` = {get_id(p_name)} AND `idPROCEDURE` = {procedure_id}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_count)
            ((exists,),) = cursor.fetchall()

        if exists > 0:
            query = f"""UPDATE `PATIENT-PROCEDURE`
                SET `How many a day` = {total_dose}
                WHERE `idPATIENT` = {get_id(p_name)} AND `idPROCEDURE` = {procedure_id}"""
        else:
            query = f"""INSERT INTO `PATIENT-PROCEDURE` (idPATIENT, idPROCEDURE, `How many a day`)
                VALUES ({get_id(p_name)}, {procedure_id}, {total_dose})
                """
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query)
            conn.commit()

        query_date_change = f"""UPDATE `PATIENT`
            SET `Treatment changed` = '{datetime.date.today()}'
            WHERE `idPATIENT` = {get_id(p_name)}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_date_change)
            conn.commit()
    except:
        error_in_data()
    else:
        success_message()


def change_procedures_btn(conn, p_box, diag_box):
    window = Tk()
    window.geometry('300x250')
    window.title("Patient's treatment")

    lbl1 = Label(window, text="Procedures")
    lbl1.grid(column=0, row=0)
    procedures = Combobox(window)
    procedures["values"] = get_procedures(conn, diag_box.get())
    procedures.grid(column=1, row=0)

    change_procedures_btn_clicked_wo_arg = partial(change_procedures_btn_clicked, conn, p_box, diag_box, procedures)
    btn1 = Button(window, text='Change procedures', command=change_procedures_btn_clicked_wo_arg)
    btn1.grid(column=0, row=1)


def treatment_changed_today():
    window = Tk()
    window.geometry('250x250')
    window.title("Error")
    label = Label(window, text="Treatment have been already changed today.\n"
                               "Wait till tomorrow to change it.\n")
    label.grid(column=0, row=0)
    btn = Button(window, text="Ok", command=window.destroy)
    btn.grid(column=0, row=1)


def change_treats_btn_p_chosen(conn, p_box):
    try:
        query_check_treatment_change =f"""SELECT `Treatment changed` FROM `PATIENT`
        WHERE idPATIENT = {get_id(p_box.get())}"""
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_check_treatment_change)
            ((date,),) = cursor.fetchall()
    except:
        error_in_data()
        return
    if str(date) == str(datetime.date.today()):
        treatment_changed_today()
    else:
        window = Tk()
        window.geometry('300x250')
        window.title("Patient's treatment")

        lbl1 = Label(window, text=f'Patient: {p_box.get()}')
        lbl1.grid(column=0, row=0)

        lbl2 = Label(window, text='Diagnoses')
        lbl2.grid(column=0, row=1)
        diag_box = Combobox(window)
        diag_box["values"] = get_p_diagnoses(conn, p_box.get())
        diag_box.grid(column=1, row=1)

        change_meds_btn_wo_arg = partial(change_meds_btn, conn, p_box, diag_box)
        btn1 = Button(window, text='Change meds', command=change_meds_btn_wo_arg)
        btn1.grid(column=0, row=2)

        change_procedures_btn_wo_arg = partial(change_procedures_btn, conn, p_box, diag_box)
        btn1 = Button(window, text='Change procedures', command=change_procedures_btn_wo_arg)
        btn1.grid(column=0, row=3)


def change_treatment_btn(conn):
    window = Tk()
    window.geometry('500x250')
    window.title("Treatment")

    lbl0 = Label(window, text="Choose patient to change his treatment.\n"
                 "Note that if the dosage of medicine have already been changed\n"
                 "today, you won't be able to change it.")
    lbl0.grid(column=0, row=0)
    lbl1 = Label(window, text="Patient")
    lbl1.grid(column=0, row=1)
    p_box = Combobox(window)
    p_box["values"] = get_patients(conn)
    p_box.grid(column=1, row=1)

    change_treats_btn_p_chosen_wo_arg = partial(change_treats_btn_p_chosen, conn, p_box)
    btn1 = Button(window, text='Change treatment', command=change_treats_btn_p_chosen_wo_arg)
    btn1.grid(column=1, row=2)


def change_condition_btn_clicked(conn, p_name, p_cond, p_diag):
    p_cond = p_cond.get()
    p_name = p_name.get()
    p_diag = p_diag.get()

    try:
        with conn.cursor(buffered=True) as cursor:
            query_get_diag_id = f"""SELECT idDIAGNOSIS FROM `DIAGNOSIS`
                    WHERE `Diagnosis name` = '{p_diag}'"""
            cursor.execute(query_get_diag_id)
            ((diag_id,),) = cursor.fetchall()

        query = f"""UPDATE `PATIENT-DIAGNOSIS`
        SET `Condition` = '{p_cond}',
        `Condition changed` = '{datetime.date.today()}'
        WHERE idPATIENT = {get_id(p_name)} AND idDIAGNOSIS = {diag_id} AND `End of treatment` IS NULL
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

        if p_cond == 'Healthy' or p_cond == 'Dead':
            query_get_staying = f"""SELECT `Is staying` FROM `PATIENT-DIAGNOSIS`
            WHERE `idPATIENT` = {get_id(p_name)} AND idDIAGNOSIS = {diag_id} AND `End of treatment` IS NULL
            """
            with conn.cursor() as cursor:
                cursor.execute(query_get_staying)
                ((p_stay,),) = cursor.fetchall()
                conn.commit()

            query_discharge = f"""UPDATE `PATIENT-DIAGNOSIS`
            SET `End of treatment` = '{datetime.date.today()}',
                `Is staying` = 'No'
            WHERE `idPATIENT` = {get_id(p_name)} AND idDIAGNOSIS = {diag_id} AND `End of treatment` IS NULL
            """
            with conn.cursor() as cursor:
                cursor.execute(query_discharge)
                conn.commit()

            if p_stay == 'Yes':
                query_get_id_dep = f"""SELECT idDEPARTMENT FROM `DIAGNOSIS`
                            WHERE `Diagnosis name` = '{p_diag}'
                            """
                with conn.cursor() as cursor:
                    cursor.execute(query_get_id_dep)
                    ((p_dep,),) = cursor.fetchall()
                    conn.commit()

                query_dep = f"""UPDATE `DEPARTMENT`
                SET `Number of beds` = `Number of beds` + 1
                WHERE idDEPARTMENT = {p_dep}
                """
                with conn.cursor() as cursor:
                    cursor.execute(query_dep)
                    conn.commit()

        if p_cond == 'Dead':
            query_set_dead = f"""UPDATE `PATIENT-DIAGNOSIS`
            SET `Condition` = 'Dead due to other reasons',
                `End of treatment` = '{datetime.date.today()}'
            WHERE idPATIENT = '{get_id(p_name)}' AND NOT `Condition` = 'Dead' AND `End of treatment` IS NULL
            """
            with conn.cursor() as cursor:
                cursor.execute(query_set_dead)
                conn.commit()
    except:
        error_in_data()
    else:
        success_message()


def change_condition_btn_p_chosen(conn, p_name_box):
    window = Tk()
    window.geometry('300x250')
    window.title("Patient condition")

    lbl1 = Label(window, text="Diagnosis and condition")
    lbl1.grid(column=0, row=0)

    p_name = p_name_box.get()
    lbl2 = Label(window, text="Patient's diagnosis")
    lbl2.grid(column=0, row=1)
    p_diagnoses = Combobox(window)
    p_diagnoses["values"] = get_p_diagnoses(conn, p_name)
    p_diagnoses.grid(column=1, row=1)

    lbl3 = Label(window, text="Patient's condition")
    lbl3.grid(column=0, row=2)
    p_condition = Combobox(window)
    p_condition["values"] = ["Sick", "Healthy", "Dead", "Dead due to other reasons"]
    p_condition.grid(column=1, row=2)

    change_condition_btn_clicked_wo_arg = partial(change_condition_btn_clicked, conn,
                                                  p_name_box, p_condition, p_diagnoses)
    btn1 = Button(window, text='Change condition', command=change_condition_btn_clicked_wo_arg)
    btn1.grid(column=0, row=4)


def change_condition_btn(conn):
    window = Tk()
    window.geometry('300x250')
    window.title("Choose patient to change his condition")

    lbl1 = Label(window, text="Patient")
    lbl1.grid(column=0, row=0)
    p_box = Combobox(window)
    p_box["values"] = get_patients(conn)
    p_box.grid(column=1, row=0)

    change_condition_btn_p_chosen_wo_arg = partial(change_condition_btn_p_chosen, conn, p_box)
    btn1 = Button(window, text='Change condition', command=change_condition_btn_p_chosen_wo_arg)
    btn1.grid(column=0, row=4)


def change_dep_btn_clicked(conn, p_name, prev_dep, new_dep_box):
    new_dep = new_dep_box.get()

    try:
        query_new_dep_id = f"""SELECT idDEPARTMENT FROM `DEPARTMENT`
        WHERE `Name of the department` = '{new_dep}'"""
        with conn.cursor() as cursor:
            cursor.execute(query_new_dep_id)
            ((new_dep_id,),) = cursor.fetchall()
            conn.commit()

        query_check_free_beds = f"""SELECT `Number of beds` FROM `DEPARTMENT`
        WHERE `Name of the department` = '{new_dep}'"""
        with conn.cursor() as cursor:
            cursor.execute(query_check_free_beds)
            ((beds,),) = cursor.fetchall()
            conn.commit()
        if beds <= 0:
            no_free_beds_warning()
            return

        query_diags = f"""SELECT `idDIAGNOSIS` FROM `PATIENT-DIAGNOSIS`
            WHERE idPATIENT = '{get_id(p_name)}'"""
        with conn.cursor() as cursor:
            cursor.execute(query_diags)
            records = cursor.fetchall()
            diags_id = []
            for val in records:
                diags_id.append(val[0])
            conn.commit()

        for diag in diags_id:
            query = f"""SELECT idDEPARTMENT FROM `DIAGNOSIS`
            WHERE idDIAGNOSIS = {diag}"""
            with conn.cursor() as cursor:
                cursor.execute(query)
                ((dep,),) = cursor.fetchall()
                conn.commit()
            if int(dep) == int(new_dep_id):
                query = f"""UPDATE `PATIENT-DIAGNOSIS`
                SET `Is staying` = 'Yes'
                WHERE idDIAGNOSIS = {diag} AND idPATIENT = {get_id(p_name)} AND `End of treatment` IS NULL"""
                break

        query_dep1 = f"""UPDATE `DEPARTMENT`
                            SET `Number of beds` = `Number of beds` + 1
                            WHERE idDEPARTMENT = {prev_dep}
                            """
        with conn.cursor() as cursor:
            cursor.execute(query_dep1)
            conn.commit()

        query_dep2 = f"""UPDATE `DEPARTMENT`
                                SET `Number of beds` = `Number of beds` - 1
                                WHERE `Name of the department` = '{new_dep}'
                                """
        with conn.cursor() as cursor:
            cursor.execute(query_dep2)
            conn.commit()
    except:
        error_in_data()
    else:
        success_message()


def change_dep_btn_p_chosen(conn, p_box):
    p_name = p_box.get()

    try:
        query_find_diag = f"""SELECT `idDIAGNOSIS` FROM `PATIENT-DIAGNOSIS`
        WHERE idPATIENT = {get_id(p_name)}"""
        with conn.cursor() as cursor:
            cursor.execute(query_find_diag)
            deps_id = []
            records = cursor.fetchall()
            for val in records:
                print(val)
                query = f"""SELECT idDEPARTMENT FROM `DIAGNOSIS`
                WHERE `idDIAGNOSIS` = {val[0]}"""
                cursor.execute(query)
                ((dep_id,),) = cursor.fetchall()
                deps_id.append(dep_id)
            conn.commit()
            deps = []
            for dep_id in deps_id:
                query = f"""SELECT `Name of the department` FROM `DEPARTMENT`
                            WHERE `idDEPARTMENT` = {dep_id}"""
                cursor.execute(query)
                ((dep,),) = cursor.fetchall()
                deps.append(dep)

        window = Tk()
        window.geometry('400x400')
        window.title("Choose department")

        lbl = Label(window, text="Choose department to move patient to")
        lbl.grid(column=0, row=0)

        deps_combo = Combobox(window)
        deps_combo["values"] = deps
        deps_combo.grid(column=1, row=0)

        change_dep_btn_clicked_wo_arg = partial(change_dep_btn_clicked, conn, p_name, dep_id, deps_combo)
        btn = Button(window, text="Change department", command=change_dep_btn_clicked_wo_arg)
        btn.grid(column=1, row=1)

        query_dep = f"""UPDATE `DEPARTMENT`
                        SET `Number of beds` = `Number of beds` - 1
                        WHERE idDEPARTMENT = {dep_id}
                        """
        with conn.cursor() as cursor:
            cursor.execute(query_dep)
            conn.commit()
    except:
        error_in_data()
    else:
        success_message()


def change_dep_btn(conn):
    window = Tk()
    window.geometry('300x250')
    window.title("Choose patient to change his department")

    lbl1 = Label(window, text="Patient")
    lbl1.grid(column=0, row=0)
    p_box = Combobox(window)
    p_box["values"] = get_patients(conn)
    p_box.grid(column=1, row=0)

    change_dep_btn_p_chosen_wo_arg = partial(change_dep_btn_p_chosen, conn, p_box)
    btn1 = Button(window, text='Change department', command=change_dep_btn_p_chosen_wo_arg)
    btn1.grid(column=0, row=4)


""" REPORTS FUNCS """


def docs_whose_patients_die(conn):
    query = f"""SELECT idDOCTOR FROM `PATIENT-DIAGNOSIS`
    WHERE `Condition` = 'Dead'"""
    filename = "docs_whose_patients_die_" + str(datetime.date.today()) + ".csv"
    with open(filename, 'a') as file:
        file.write(f"Full name;idDEPARTMENT;Date of birth;Position;\n")

    try:
        with conn.cursor() as cursor:
            docs = []
            cursor.execute(query)
            records = cursor.fetchall()
            for val in records:
                docs.append(val[0])

        docs = list(set(docs))
        with conn.cursor() as cursor:
            for doc in docs:
                query = f"""SELECT `Full name`, idDEPARTMENT, `Date of birth`, `Position` FROM `DOCTOR`
                WHERE idDOCTOR = {doc}"""
                cursor.execute(query)
                record = cursor.fetchall()
                with open(filename, 'a') as file:
                    file.write(f"{record[0][0]};{record[0][1]};{record[0][2]};{record[0][3]};\n")
    except:
        error_in_data()
    else:
        success_message()


def best_doctors(conn):
    filename = f"best_doctors_{str(datetime.date.today())}.csv"
    with open(filename, 'a') as file:
        file.write(f"Doctor name;Deaths;\n")

    docs_query = f"""SELECT idDOCTOR FROM `DOCTOR` WHERE `Ended work` IS NULL"""
    try:
        with conn.cursor() as cursor:
            docs_id = {}
            cursor.execute(docs_query)
            records = cursor.fetchall()
            for val in records:
                docs_id[val[0]] = 0

            for doc in docs_id.keys():
                query_get_dead = f"""SELECT COUNT(*) FROM `PATIENT-DIAGNOSIS`
                WHERE idDOCTOR = {doc} AND `Condition` = 'Dead'"""
                cursor.execute(query_get_dead)
                ((val,),) = cursor.fetchall()
                docs_id[doc] = int(val)

            sorted_docs = {k: v for k, v in sorted(docs_id.items(), key=lambda item: item[1])}
            for key in sorted_docs.keys():
                query = f"""SELECT `Full name` FROM `DOCTOR`
                WHERE idDOCTOR = {key}"""
                cursor.execute(query)
                ((name,),) = cursor.fetchall()
                with open(filename, 'a') as file:
                    file.write(f"{name};{sorted_docs[key]};\n")
    except:
        error_in_data()
    else:
        success_message()


def diagnosis_frequency(conn, start_date, end_date):
    start_date = start_date.get()
    end_date = end_date.get()
    filename = f"diagnoses_frequency_from_{str(start_date)}_to_{str(end_date)}.csv"
    with open(filename, 'a') as file:
        file.write(f"Diagnosis;Frequency;\n")

    digs_tuple = get_diagnoses(conn)
    diags = {}
    for tuple in digs_tuple:
        diags[tuple[0]] = tuple[1]
    try:
        with conn.cursor() as cursor:
            for diag in diags.keys():
                query = f"""SELECT COUNT(*) FROM `PATIENT-DIAGNOSIS`
                WHERE idDIAGNOSIS = {diag} AND `Start of treatment` BETWEEN '{start_date}' AND '{end_date}'"""
                cursor.execute(query)
                ((freq,),) = cursor.fetchall()
                with open(filename, 'a') as file:
                    file.write(f"{diags[diag]};{freq};\n")
    except:
        error_in_data()
    else:
        success_message()


def d_frequency(conn):
    window = Tk()
    window.geometry('300x250')
    start_date = Entry(window, width=15)
    lbl1 = Label(window, text="Start date")
    lbl1.grid(column=0, row=0)
    start_date.grid(column=1, row=0)

    end_date = Entry(window, width=15)
    lbl2 = Label(window, text="End date")
    lbl2.grid(column=0, row=1)
    end_date.grid(column=1, row=1)

    diagnosis_frequency_wo_arg = partial(diagnosis_frequency, conn, start_date, end_date)
    btn = Button(window, text="Get report", command=diagnosis_frequency_wo_arg)
    btn.grid(column=0, row=2)


def hospital_history_report_all_time(conn):
    filename = f"hospital_history_report_alltime.csv"
    with open(filename, 'a') as file:
        file.write(f"Patient name; Diagnosis; Start of treatment; End of treatment; "
                   f"Is staying; Doctor name; Condition;\n")
    query = f"""SELECT idPATIENT, idDIAGNOSIS, `Start of treatment`, `End of treatment`, 
    `Is staying`, idDOCTOR, `Condition` FROM `PATIENT-DIAGNOSIS`"""

    query_get_patients = f"""SELECT idPATIENT, `Full name` FROM `PATIENT`"""
    query_get_diagnoses = f"""SELECT idDIAGNOSIS, `Diagnosis name` from `DIAGNOSIS`"""
    query_get_docs = f"""SELECT idDOCTOR, `Full name` FROM `DOCTOR`"""
    try:
        with conn.cursor() as cursor:
            patients = {}
            cursor.execute(query_get_patients)
            records = cursor.fetchall()
            for val in records:
                patients[val[0]] = val[1]

            diagnoses = {}
            cursor.execute(query_get_diagnoses)
            records = cursor.fetchall()
            for val in records:
                diagnoses[val[0]] = val[1]

            doctors = {}
            cursor.execute(query_get_docs)
            records = cursor.fetchall()
            for val in records:
                doctors[val[0]] = val[1]

            cursor.execute(query)
            records = cursor.fetchall()
            for val in records:
                with open(filename,'a') as file:
                    file.write(f"{patients[val[0]]}; {diagnoses[val[1]]}; {val[2]}; {val[3]};"
                               f"{val[4]}; {doctors[val[5]]}; {val[6]}\n")
    except:
        error_in_data()
    else:
        success_message()


def hospital_history_report_one_year(conn):
    filename = f"hospital_history_report_one_year.csv"
    with open(filename, 'a') as file:
        file.write(f"Patient name; Diagnosis; Start of treatment; End of treatment; "
                   f"Is staying; Doctor name; Condition;\n")

    query = f"""SELECT idPATIENT, idDIAGNOSIS, `Start of treatment`, `End of treatment`, 
        `Is staying`, idDOCTOR, `Condition` FROM `PATIENT-DIAGNOSIS`
    WHERE `Start of treatment` >= {datetime.date.today() - datetime.timedelta(days=365)}
    OR `End of treatment` >= {datetime.date.today() - datetime.timedelta(days=365)}"""

    query_get_patients = f"""SELECT idPATIENT, `Full name` FROM `PATIENT`"""
    query_get_diagnoses = f"""SELECT idDIAGNOSIS, `Diagnosis name` from `DIAGNOSIS`"""
    query_get_docs = f"""SELECT idDOCTOR, `Full name` FROM `DOCTOR`"""
    try:
        with conn.cursor() as cursor:
            patients = {}
            cursor.execute(query_get_patients)
            records = cursor.fetchall()
            for val in records:
                patients[val[0]] = val[1]

            diagnoses = {}
            cursor.execute(query_get_diagnoses)
            records = cursor.fetchall()
            for val in records:
                diagnoses[val[0]] = val[1]

            doctors = {}
            cursor.execute(query_get_docs)
            records = cursor.fetchall()
            for val in records:
                doctors[val[0]] = val[1]

            cursor.execute(query)
            records = cursor.fetchall()
            for val in records:
                with open(filename, 'a') as file:
                    file.write(f"{patients[val[0]]}; {diagnoses[val[1]]}; {val[2]}; {val[3]};"
                               f"{val[4]}; {doctors[val[5]]}; {val[6]}\n")
    except:
        error_in_data()
    else:
        success_message()


def hospital_history(conn):
    window = Tk()
    window.geometry('300x250')
    window.title("Hospital database")

    hospital_history_report_all_time_wo_arg = partial(hospital_history_report_all_time, conn)
    btn1 = Button(window, text="All time", command=hospital_history_report_all_time_wo_arg)
    btn1.grid(column=0, row=0)

    hospital_history_report_one_year_wo_arg = partial(hospital_history_report_one_year, conn)
    btn2 = Button(window, text="One year", command=hospital_history_report_one_year_wo_arg)
    btn2.grid(column=0, row=1)


def gui_reports(connection):
    window = Tk()
    window.geometry('300x250')
    window.title("Hospital database")
    lbl1 = Label(window, text="Choose report to save")
    lbl1.grid(column=0, row=0)

    docs_whose_patients_die_wo_arg = partial(docs_whose_patients_die, connection)
    btn1 = Button(window, text="Doctors whose patients die", command=docs_whose_patients_die_wo_arg)
    btn1.grid(column=0, row=1)

    d_frequency_wo_arg = partial(d_frequency, connection)
    btn2 = Button(window, text="Diagnosis frequency", command=d_frequency_wo_arg)
    btn2.grid(column=0, row=2)

    best_doctors_wo_arg = partial(best_doctors, conn)
    btn3 = Button(window, text="Best doctors", command=best_doctors_wo_arg)
    btn3.grid(column=0, row=3)

    hospital_history_wo_arg = partial(hospital_history, conn)
    btn3 = Button(window, text="Hospital history", command=hospital_history_wo_arg)
    btn3.grid(column=0, row=4)


""" MAIN INTERFACE """


def gui(connection):
    window = Tk()
    window.geometry('300x250')
    window.title("Hospital database")
    lbl1 = Label(window, text="Welcome to hospital database.", font=("Montserrat", 15))
    lbl1.grid(column=0, row=0)

    add_doc_btn_wo_arg = partial(add_doc_btn, connection)
    btn1 = Button(window, text="Register new doctor", command=add_doc_btn_wo_arg)
    btn1.grid(column=0, row=1)

    fire_doc_btn_wo_arg = partial(fire_doc_btn, connection)
    btn2 = Button(window, text="Fire doctor", command=fire_doc_btn_wo_arg)
    btn2.grid(column=0, row=2)

    add_patient_btn_wo_arg = partial(add_patient_btn, connection)
    btn3 = Button(window, text="Register new patient", command=add_patient_btn_wo_arg)
    btn3.grid(column=0, row=3)

    change_treatment_btn_wo_arg = partial(change_treatment_btn, connection)
    btn4 = Button(window, text="Change patient's treatment", command=change_treatment_btn_wo_arg)
    btn4.grid(column=0, row=4)

    change_condition_btn_wo_arg = partial(change_condition_btn, connection)
    btn6 = Button(window, text="Change patient's condition", command=change_condition_btn_wo_arg)
    btn6.grid(column=0, row=5)

    change_dep_btn_wo_arg = partial(change_dep_btn, connection)
    btn7 = Button(window, text="Change patient's department", command=change_dep_btn_wo_arg)
    btn7.grid(column=0, row=6)

    gui_reports_wo_arg = partial(gui_reports, connection)
    btn8 = Button(window, text="Get report", command=gui_reports_wo_arg)
    btn8.grid(column=0, row=7)

    window.mainloop()


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


conn = create_connection("127.0.0.1", "root", "26081202", "hospital")
gui(conn)