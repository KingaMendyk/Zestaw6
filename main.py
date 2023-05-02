import smtplib
from email.mime.text import MIMEText
import MyLinkedList
import Student


def show(students):
    print(students)


def read_file(filepath):
    res = MyLinkedList.LinkedList()
    with open(filepath) as file_object:
        for line in file_object:
            line_list = line.rstrip().split(",")

            student = Student.Student(line_list[0], line_list[1], line_list[2])
            student.all_grade["project"] = int(line_list[3])
            student.all_grade["l_1"] = int(line_list[4])
            student.all_grade["l_2"] = int(line_list[5])
            student.all_grade["l_3"] = int(line_list[6])
            student.all_grade["h_1"] = int(line_list[7])
            student.all_grade["h_2"] = int(line_list[8])
            student.all_grade["h_3"] = int(line_list[9])
            student.all_grade["h_4"] = int(line_list[10])
            student.all_grade["h_5"] = int(line_list[11])
            student.all_grade["h_6"] = int(line_list[12])
            student.all_grade["h_7"] = int(line_list[13])
            student.all_grade["h_8"] = int(line_list[14])
            student.all_grade["h_9"] = int(line_list[15])
            student.all_grade["h_10"] = int(line_list[16])
            student.all_grade["grade"] = int(line_list[17])
            student.status = line_list[18]

            el = MyLinkedList.Element(student)
            res.append(el)

    return res


def save_to_file(filepath, content):
    with open(filepath, "w") as file_object:
        el = content.head
        while el is not None:
            student = el.data
            line = student.email + "," + student.name + "," + student.surname + ","
            for v in student.all_grade.values():
                line += str(v) + ","

            if student.status is None:
                line += "None\n"
            else:
                line += student.status + "\n"
            file_object.write(line)
            el = el.nextE


def mail_students(students):
    el = students.head
    while el is not None:
        student = el.data
        if student.status == "GRADED":
            send_mail("Grade", student.all_grade["grade"], "mymail@gmail.com", student.email, "mypassword")
            student.status = "MAILED_FINAL"
        el = el.nextE
    save_to_file("new_file.txt", students)


def send_mail(subject, body, sender, recipients, password):
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ",".join(recipients)
    smtp_server = smtplib.SMTP_SSL("smpt.gmail.com", 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, message.as_string())
    smtp_server.quit()


# 50 i mniej - 2
# 51 -60 pkt - 3
# 61 – 70 pkt – 3.5
# 71 – 80 pkt - 4
# 81 - 90 pkt – 4.5
# 91 - 100 pkt – 5

# 1 ocena za projekt – 40 pkt
# 3 oceny z list z zadaniami – 20 pkt każda
# Oceny z prac domowych.
# W zależności od średniej z prac domowych należy zastąpić
# najsłabsze oceny z list od 1 do 3.
# 60% - jedna lista (20pkt)
# 70% - dwie listy (40pkt)
# 80% - trzy listy (60 pkt)
# Ocenę końcową można wystawić tylko, kiedy wszystkie oceny
# cząstkowe są wystawione.
def grade_students(students):
    el = students.head
    while el is not None:
        if el.data.all_grade["grade"] == -1:
            grade(el.data)
        el = el.nextE
    save_to_file("new_file.txt", students)


def grade(student):
    if check_if_grading(student):
        homework_grade(student)
        allSum = 1
        grades = student.all_grade
        for g in grades.values():
            allSum += g

        if allSum <= 50:
            student.all_grade["grade"] = 2
        elif allSum <= 60:
            student.all_grade["grade"] = 3
        elif allSum <= 70:
            student.all_grade["grade"] = 3.5
        elif allSum <= 80:
            student.all_grade["grade"] = 4
        elif allSum <= 90:
            student.all_grade["grade"] = 4.5
        else:
            student.all_grade["grade"] = 5
        student.status = "GRADED"


def check_if_grading(student):
    res = True
    grades = student.all_grade
    i = 0

    for g in grades.values():
        if g == -1 and i != len(grades) - 1:
            res = False
        i += 1
    return res


def homework_grade(student):
    grades = student.all_grade
    hwsum = 0
    for i in range(1, 11):
        hwsum += grades["h_" + str(i)]
    average = hwsum / 10

    if 60 <= average < 70:
        student.all_grade[min_of_three(student)] = 20
    elif 70 <= average < 80:
        res1 = min_of_three(student)
        if res1 == "l_1":
            res2 = min_of_two(student, "l_2", "l_3")
        elif res1 == "l_2":
            res2 = min_of_two(student, "l_1", "l_3")
        else:
            res2 = min_of_two(student, "l_2", "l_1")

        student.all_grade[res1] = 20
        student.all_grade[res2] = 20
    elif average >= 80:
        student.all_grade["l_1"] = 20
        student.all_grade["l_2"] = 20
        student.all_grade["l_3"] = 20


def min_of_two(student, i1, i2):
    l1 = student.all_grade[i1]
    l2 = student.all_grade[i2]

    if l1 <= l2:
        res = i1
    else:
        res = i2
    return res


def min_of_three(student):
    l1 = student.all_grade["l_1"]
    l2 = student.all_grade["l_2"]
    l3 = student.all_grade["l_3"]
    if (l1 <= l2) and (l1 <= l3):
        res = "l_1"

    elif (l2 <= l1) and (l2 <= l3):
        res = "l_2"
    else:
        res = "l_3"
    return res


def add_student(students, email, name, surname):
    student = Student.Student(email, name, surname)
    el = MyLinkedList.Element(student)
    if students.get(el) is not None:
        print("Student already exists!")
        return

    students.append(el)
    save_to_file("new_file.txt", students)


def delete_student(students, email):
    student = Student.Student(email, "", "")
    el = MyLinkedList.Element(student)

    if students.get(el) is None:
        print("No such student")
        return

    students.delete(el)
    save_to_file("new_file.txt", students)


# 1.
linkedList = read_file("ocenystudenci")
print("\nStudents:")
show(linkedList)

# 2.
grade_students(linkedList)
print("\nStudents after grading:")
show(linkedList)

# 3.
print("\nAdding student:")
add_student(linkedList, "darbaj@gmail.com", "Darek", "Bajeczny")
show(linkedList)
print("\nDeleting student:")
delete_student(linkedList, "darbaj@gmail.com")
show(linkedList)

# 4.
print("\nSending emails:")
mail_students(linkedList)
show(linkedList)

# 5.
# Zrealizowane na końcu w odpowiednich funkcjach - add_student, delete_student,
# grade_students, mail_students
