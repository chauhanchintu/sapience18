import sqlite3
from flask import Flask, request, jsonify, render_template,redirect,url_for,send_from_directory
import datetime
import os
import random
import string
# from xlrd import open_workbook
# import xlwt 

from xlwt import Workbook
import datetime
import xlsxwriter 
import sqlite3
from num2words import num2words

from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from flask import Flask, request, render_template, send_file








bill_api = Flask(__name__)



conn_bill = sqlite3.connect('bill.db', check_same_thread=False)

conn_bill.execute('''CREATE TABLE IF NOT EXISTS aimDB
        (id INTEGER NOT NULL PRIMARY KEY,
        Datetime timestamp,
        From_Date TEXT,
        To_Date TEXT,
        Name TEXT,
        Current_Unit TEXT,
        Last_Unit TEXT,
        Unit TEXT,
        Rent TEXT,
        Total_Amt TEXT,
        Elec_Bill TEXT,
        ApplicationNo TEXT,
        document_path TEXT
        );''')
conn_bill.commit()




def random_char(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

def randomString(stringLength=6):
    otp=""
    for i in range(6):
        otp+=str(random.randint(1,9))
    return otp



@bill_api.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@bill_api.route('/home',methods=['GET','POST'])
def home():
    return render_template('index.html')

@bill_api.route('/insertdata',methods=['GET','POST'])
def insertdata():
    if request.method == "POST":
        From_Date=request.form['From_Date']
        current_time = datetime.datetime.now()
        b=str(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        To_Date=b[0:10]
        c=str(datetime.datetime.now())
        c=c[0:19]
        a=request.form['Name']
        Name=str(a.upper())
        Current_Unit=request.form['Current_Unit']
        Last_Unit=request.form['Last_Unit']
        Unit=request.form['Unit']
        Rent=request.form['Rent']
        Rent=int(Rent)
        Unit=int(Unit)
        Current_Unit=int(Current_Unit)
        Last_Unit=int(Last_Unit)
        Elec_Bill=Current_Unit-Last_Unit
        Total_Bill=Elec_Bill*Unit
        Total_Bill=int(Total_Bill)
        Total_Amt=Total_Bill+Rent
        Total_Amt=int(Total_Amt)
        ApplicationNo=randomString()
        # Check if a file was uploaded
        if 'document' in request.files:
            document = request.files['document']

            # Allow all file types
            def allowed_file(filename):
                return True

            if document:
                # Save the uploaded file to a specific directory
                upload_folder = 'static/BILL_Admin'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                document.save(os.path.join(upload_folder, document.filename))
                # You can also store the file path in your database if needed
                document_path = os.path.join(upload_folder, document.filename)
            else:
                # If no document is uploaded, set document_path to NULL or an empty string
                document_path = None
            conn_bill.execute("INSERT INTO aimDB(Datetime,From_Date,To_Date,Name,Current_Unit,Last_Unit,Unit,Rent,Total_Amt,Elec_Bill,ApplicationNo,document_path) values(?,?,?,?,?,?,?,?,?,?,?,?)" ,(c,From_Date,To_Date,Name,Current_Unit,Last_Unit,Unit,Rent,Total_Amt,Elec_Bill,ApplicationNo,document_path))
            conn_bill.commit()

        try:
            a=conn_bill.execute('SELECT * FROM aimDB ORDER BY ID DESC').fetchall()
            Address='Noida - 201301, Uttar Pradesh, India'
            Address=Address.upper()
            Landlord='Binesh Bhati'
            Landlord=Landlord.upper()
            To_DateCur1=To_Date[0:4]
            To_DateCur2=To_Date[5:7]
            To_DateCur3=To_Date[8:10]
            NumWords=num2words(Total_Amt)

            Rent=str(Rent)
            Unit=str(Unit)
            Current_Unit=str(Current_Unit)
            Last_Unit=str(Last_Unit)
            Total_Amt=str(Total_Amt)
            Total_Amt1=str(Total_Amt)
            ApplicationNo=ApplicationNo
            ApplicationNo='ReceiptNo. - '+ApplicationNo
            NumWords=str(NumWords).upper()
            Balance=str('0')
            Advance=str('0')

            import calendar

            

            # Extract year and month as integers
            From_Date_year = int(From_Date[:4])
            From_Date_month = int(From_Date[5:7])

            b_year = int(b[:4])
            b_month = int(b[5:7])

            # Get month names
            month_name1 = calendar.month_name[From_Date_month]
            month_name2 = calendar.month_name[b_month]

            month_name1=str(month_name1)
            month_name2=str(month_name2)
            From_Date_year=str(From_Date_year)
            b_year=str(b_year)
            # print(month_name1, month_name2, From_Date_year, b_year)



            mergedObject = PdfFileMerger()
    
            for i in range(1):
                print(i)
                packet = io.BytesIO()
                # create a new PDF with Reportlab
                can = canvas.Canvas(packet, pagesize=letter)
                can.setFontSize(10) 

            
                if i==0:
                    try: 
                        can.drawString(180,250,Name)
                        can.drawString(185,228,Address)
                        can.drawString(170,275,Landlord)
                        can.drawString(532,276,To_DateCur1)
                        can.drawString(500,276,To_DateCur2)
                        can.drawString(465,276,To_DateCur3)
                        can.drawString(152,157,Rent)
                        can.drawString(281,157,month_name1)
                        can.drawString(332,157,From_Date_year)
                        can.drawString(422,157,month_name2)
                        can.drawString(475,157,b_year)
                        can.drawString(140,135,Total_Amt)
                        can.drawString(95,101,Total_Amt1)
                        can.drawString(450,75,ApplicationNo)
                        can.drawString(152,182,NumWords)
                        can.drawString(320,135,Balance)
                        can.drawString(450,135,Advance)
                    
                    
                        can.save()

                            # move to the beginning of the StringIO buffer
                        packet.seek(0)
                        new_pdf = PdfFileReader(packet)
                            #read your existing PDF
                        existing_pdf = PdfFileReader(open("Rent-Receipt-Format.pdf", "rb"))
                        output = PdfFileWriter()
                            # add the "watermark" (which is the new pdf) on the existing page
                        page = existing_pdf.getPage(i)
                        page.mergePage(new_pdf.getPage(0))
                        output.addPage(page)
                            # finally, write "output" to a real file
                        outputStream = open("destination"+str(i)+".pdf", "wb")
                        output.write(outputStream)
                        outputStream.close()
                            

                        mergedObject.append(PdfFileReader("destination"+str(i)+".pdf", "rb"), import_outline=False)
                        # After generating the PDF
                        slic=ApplicationNo[0:1]+ApplicationNo[2:3]+ApplicationNo[5:6]+ApplicationNo[6:7]+ApplicationNo[7:10]
                        ApplicationNo=slic+'_'+ApplicationNo[13:19]
                        pdf_filename = f"{Name}_{ApplicationNo}.pdf"
                        path = os.path.join('static/pdf/', pdf_filename)
                        mergedObject.write(path)
                        
                         
                        return redirect(url_for("payment"))
                    except Exception as e:
                        print("google-chrome",e)
                        pass
                return redirect(url_for("download_file", filename=pdf_filename))
            
            
        except:
            return redirect(url_for("index"))


@bill_api.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('static/pdf', filename, as_attachment=True)



@bill_api.route('/payment',methods=['GET','POST'])
def payment():
    try:
        a=conn_bill.execute('SELECT * FROM aimDB ORDER BY ID DESC').fetchall()

        Total_Amt=a[0][9]
        Bill=int(a[0][10])
        unit=int(a[0][7])
        Elec_Bill=int(unit*Bill)
        name=a[0][4]  
        last_unit=a[0][6]
        curr_unit=a[0][5]
        receiptno=a[0][11]  
        total_amt = Total_Amt  # Replace with the actual variable that holds the total amount
        electricity_bill = str(Elec_Bill)
        return render_template('payment.html', total_amt=total_amt,electricity_bill=electricity_bill,name=name,curr_unit=curr_unit,last_unit=last_unit,receiptno=receiptno)
    except:
        pass



@bill_api.route('/download_receipt/pdf', methods=['GET'])
def download_receipt():
    data = request.args
    receipt_number = data.get('receipt_number')
    # print("jjjjjjjjjjjjjjjjjjj",receipt_number)

    conn_bill = sqlite3.connect('bill.db',check_same_thread=False)



    a=conn_bill.execute('SELECT * FROM aimDB where ApplicationNo = "'+receipt_number+'"').fetchall()
    To_Date=a[0][3]
    From_Date=a[0][2]
    Rent=a[0][8]
    Unit=a[0][7]
    Current_Unit=a[0][5]
    Last_Unit=a[0][6]
    # Elec_Bill=a[0][10]
    Total_Amt=a[0][9]
    Name=a[0][4]
    ApplicationNo=receipt_number
    b=str(a[0][1])
    

    # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",a)
    try:
        Address='Noida - 201301, Uttar Pradesh, India'
        Address=Address.upper()
        Landlord='Binesh Bhati'
        Landlord=Landlord.upper()
        To_DateCur1=To_Date[0:4]
        To_DateCur2=To_Date[5:7]
        To_DateCur3=To_Date[8:10]
        NumWords=num2words(Total_Amt)

        Rent=str(Rent)
        Unit=str(Unit)
        Current_Unit=str(Current_Unit)
        Last_Unit=str(Last_Unit)
        Total_Amt=str(Total_Amt)
        Total_Amt1=str(Total_Amt)
        Name=str(Name)
        ApplicationNo=ApplicationNo
        ApplicationNo='ReceiptNo. - '+ApplicationNo
        NumWords=str(NumWords).upper()
        Balance=str('0')
        Advance=str('0')

        import calendar

        

        # Extract year and month as integers
        From_Date_year = int(From_Date[:4])
        From_Date_month = int(From_Date[5:7])

        b_year = int(b[:4])
        b_month = int(b[5:7])

        # Get month names
        month_name1 = calendar.month_name[From_Date_month]
        month_name2 = calendar.month_name[b_month]

        month_name1=str(month_name1)
        month_name2=str(month_name2)
        From_Date_year=str(From_Date_year)
        b_year=str(b_year)
        # print(month_name1, month_name2, From_Date_year, b_year)



        mergedObject = PdfFileMerger()

        for i in range(1):
            print(i)
            packet = io.BytesIO()
            # create a new PDF with Reportlab
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFontSize(10) 

        
            if i==0:
                try: 
                    can.drawString(180,250,Name)
                    can.drawString(185,228,Address)
                    can.drawString(170,275,Landlord)
                    can.drawString(532,276,To_DateCur1)
                    can.drawString(500,276,To_DateCur2)
                    can.drawString(465,276,To_DateCur3)
                    can.drawString(152,157,Rent)
                    can.drawString(281,157,month_name1)
                    can.drawString(332,157,From_Date_year)
                    can.drawString(422,157,month_name2)
                    can.drawString(475,157,b_year)
                    can.drawString(140,135,Total_Amt)
                    can.drawString(95,101,Total_Amt1)
                    can.drawString(450,75,ApplicationNo)
                    can.drawString(152,182,NumWords)
                    can.drawString(320,135,Balance)
                    can.drawString(450,135,Advance)
                
                
                    can.save()

                        # move to the beginning of the StringIO buffer
                    packet.seek(0)
                    new_pdf = PdfFileReader(packet)
                        #read your existing PDF
                    existing_pdf = PdfFileReader(open("Rent-Receipt-Format.pdf", "rb"))
                    output = PdfFileWriter()
                        # add the "watermark" (which is the new pdf) on the existing page
                    page = existing_pdf.getPage(i)
                    page.mergePage(new_pdf.getPage(0))
                    output.addPage(page)
                        # finally, write "output" to a real file
                    outputStream = open("destination"+str(i)+".pdf", "wb")
                    output.write(outputStream)
                    outputStream.close()
                        

                    mergedObject.append(PdfFileReader("destination"+str(i)+".pdf", "rb"), import_outline=False)
                    # After generating the PDF
                    slic=ApplicationNo[0:1]+ApplicationNo[2:3]+ApplicationNo[5:6]+ApplicationNo[6:7]+ApplicationNo[7:10]
                    ApplicationNo=slic+'_'+ApplicationNo[13:19]
                    pdf_filename = f"{Name}_{ApplicationNo}.pdf"
                    path = os.path.join('static/pdf/AppNo', pdf_filename)
                    mergedObject.write(path)
                    download_url = f"/static/pdf/AppNo/{pdf_filename}"  # Adjust the path as needed
                    

                except:
                    pass

            return jsonify({"download_url": download_url})
            
        pass
    except:
        pass







@bill_api.route('/bill/admin', methods=['GET','POST'])
def login():
    if request.method == 'GET':
            return render_template('login_bill.html')

    elif request.method == 'POST':
        if request.form["password"]=="bill2ws":
            try:
                conn = sqlite3.connect('bill.db')
                cursor = conn.cursor()

                # Execute an SQL query to retrieve data from your database
                cursor.execute("SELECT * FROM aimDB ORDER BY ID DESC")
                data = cursor.fetchall()

                # Close the database connection
                conn.close()

                return render_template('admin.html', data=data)
            except:
                pass
                # print(e,'exception')
    


        else:
            return render_template('login_bill.html',error="Invalid Login/password")
        



@bill_api.route('/bill/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    try:
        conn = sqlite3.connect('bill.db')
        cursor = conn.cursor()

        # Execute an SQL query to delete the entry
        cursor.execute("DELETE FROM aimDB WHERE ID=?", (id,))
        conn.commit()

        # Close the database connection
        conn.close()
        
        # Return a JSON response indicating success
        return jsonify({"status": "success"})
    
    except:
        # print(e, 'exception')
        return jsonify({"status": "error"})

    


@bill_api.route('/logout')
def logout():
    return redirect(url_for("login"))




@bill_api.route('/billgenerate')
def billgenerate():
    return redirect(url_for("index"))









@bill_api.route('/bill/admin/downloadexcel', methods=['GET'])
def download_page():
    company='bill'
    a=conn_bill.execute('SELECT * FROM aimDB').fetchall()
    data=[]
    for i in a:
        From_Date=i[2]
        To_Date=i[3]
        Name=i[4]
        Current_Unit=i[5]
        Last_Unit=i[6]
        Unit=i[7]
        Rent=i[8]
        Elec_Bill=i[9]
        Total_Bill=i[10]
        ApplicationNo=i[11]

        #print(Unit)


        data.append({'From_Date':From_Date,'To_Date':To_Date,
                    'Name':Name,'Current_Unit':Current_Unit,'Last_Unit':Last_Unit,
                    'Unit':Unit,'Rent':Rent,'Elec_Bill':Elec_Bill,
                    'Total_Bill':Total_Bill,'ApplicationNo':ApplicationNo})
        
    wb = Workbook()
    chk=(os.path.isdir("static/BILL_Admin_Excel/"+str(company)))
    #print(chk)
    if chk==False:
        try:
            os.mkdir("static/BILL_Admin_Excel")
        except:
            pass
        try:
            os.mkdir("static/BILL_Admin_Excel/"+str(company))
        except:
            pass

    temp_name='_'+random_char(5)
    workbook = xlsxwriter.Workbook('static/BILL_Admin_Excel/'+company+'/bill'+temp_name+'.xlsx') 
    worksheet = workbook.add_worksheet() 

    worksheet.write(0, 0, 'From_Date') 
    worksheet.write(0, 1, 'To_Date') 
    worksheet.write(0, 2, 'Name')
    worksheet.write(0, 3, 'Current_Unit') 
    worksheet.write(0, 4, 'Last_Unit') 
    worksheet.write(0, 5, 'Unit')
    worksheet.write(0, 6, 'Rent')
    worksheet.write(0, 7, 'Elec_Bill')
    worksheet.write(0, 8, 'Total_Bill')
    worksheet.write(0, 9, 'ApplicationNo')   


    count=1

    for k in data:
        worksheet.write(count, 0, k['From_Date'])
        worksheet.write(count, 1, k['To_Date'])
        worksheet.write(count, 2, k['Name'])
        worksheet.write(count, 3, k['Current_Unit'])
        worksheet.write(count, 4, k['Last_Unit'])
        worksheet.write(count, 5, k['Unit'])
        worksheet.write(count, 6, k['Rent'])
        worksheet.write(count, 7, k['Elec_Bill'])
        worksheet.write(count, 8, k['Total_Bill'])
        worksheet.write(count, 9, k['ApplicationNo'])

        count=count+1

    workbook.close()

    return jsonify({'filename':'/static/BILL_Admin_Excel/'+company+'/bill'+temp_name+'.xlsx'})
    






























if (__name__ == "__main__"):
    # http = WSGIServer(('0.0.0.0',7000), bill)
    # http.serve_forever()
    bill_api.run(host='0.0.0.0',port=5000)
