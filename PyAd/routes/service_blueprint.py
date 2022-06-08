import json
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify


ldap_bp = Blueprint('ldap_blueprint', __name__)


@ldap_bp.route('/load_list', methods=['POST', 'GET'])
def uploader():
    if request.method == "POST":
        key = request.form['key']
        if key:
            return render_template('load_list.html', key=key)
        else:
            return render_template('service.html', key=key)
    else:
        return render_template('load_list.html')


@ldap_bp.route('/check_list/<key>', methods=['POST', 'GET'])
def check_list(key):
    print(f"key={key}")
    if request.method == "POST":
        try:
            # ****
            if key in ["Add", "Del", "Mod", "ACTV"]:
                f = request.files['fileupload']
                ldap_server = request.form['server-name']
                if not f:
                    message = "Please select a file"
                    if not ldap_server:
                        message = "Please select a file,Please enter server dn name"
                if not ldap_server:
                    message = "Please enter server dn name"
                if not f or not ldap_server:
                    flash(message)
                    # return redirect(url_for('ldap_blueprint.uploader'))

                    return render_template('load_list.html', key=key)
                # check whether the specified path exists or not
                data_path = "./data"
                isExist = os.path.exists(data_path)
                if isExist:
                    if os.path.exists("./list_student.csv"):
                        os.remove("./list_student.csv")
                    print("The file has been deleted successfully")

                if not isExist:
                    os.makedirs(data_path)
                # save csv file and server url in csv and txt file
                f.save(f"./data/{f.filename}")
                old_name = f"./data/{f.filename}"
                new_name = f"./data/list_student.csv"
                if os.path.exists(f"./data/list_student.csv"):
                    os.remove("./data/list_student.csv")
                os.rename(old_name, new_name)
                with open("./data/server_dn.txt", "w") as text_file:
                    text_file.write(ldap_server)
                text_file.close()
                print("go to connect_ldap")
                if key == "Add":
                    return redirect(url_for('ldap_blueprint.add_students'))
                elif key == "Del":
                    return redirect(url_for('ldap_blueprint.delete_students'))
                elif key == "Mod":
                    return redirect(url_for('ldap_blueprint.modify_students'))
                elif key == "ACTV":
                    return redirect(url_for('ldap_blueprint.toggle_student_status'))
            elif key == "Inf":
                student_Id = request.form['student_Id']
                with open("./data/std_ID.txt", "w") as text_file:
                    text_file.write(student_Id)
                text_file.close()
                if not student_Id:
                    message = "Please enter student ID"
                    flash(message)
                    return render_template('load_list.html', key=key)
                else:
                    return redirect(url_for('ldap_blueprint.display_student_info'))

            elif key == "CRT":
                cohort_name = request.form['cohort_name']
                with open("./data/cohort.txt", "w") as text_file:
                    text_file.write(cohort_name)
                text_file.close()
                if not cohort_name:
                    message = "Please enter cohort name"
                    flash(message)
                    return render_template('load_list.html', key=key)
                else:
                    return redirect(url_for('ldap_blueprint.display_student_in_cohort'))

            else:
                flash("please select you action")
                # return redirect(url_for('ldap_blueprint.uploader'))
                return render_template('load_list.html')
        except Exception as e:
            flash("please go home page and try again")
            return e

        # *************
    # *************************************************
    if request.method == "GET":
        # return redirect(url_for('ldap_blueprint.uploader'))
        return render_template('load_list.html')


#









